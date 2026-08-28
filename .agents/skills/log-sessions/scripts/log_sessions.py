#!/usr/bin/env python3
"""
log_sessions.py — digest AI coding-agent session logs for a repository.

Harnesses:
  pi      ~/.pi/agent/sessions/<sanitized-cwd>/*.jsonl   (full parse)
  claude  ~/.claude/projects/**/*.jsonl                  (full parse — Claude Code)
  codex   ~/.codex/sessions/**/*.jsonl                   (full parse — OpenAI Codex CLI)
  cursor  ~/.cursor/projects/*/agent-transcripts/*.jsonl, ~/.cursor/chats/*/*/store.db,
          globalStorage state.vscdb (composerData/bubbleId)  (best-effort — formats undocumented)
  gemini  ~/.gemini/tmp/*                                (detection only)

A session belongs to the repository when its recorded cwd is the repo root or
anywhere under it (worktrees and subfolders included). Events are grouped by
day in the machine's local timezone, so a session that crosses midnight
appears on both days.

Stdlib only — no third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

# ---------------------------------------------------------------- constants

HOME = Path.home()

GIT_RE = re.compile(
    r"\bgit\s+(?:-\S+\s+)*(commit|add|push|pull|fetch|merge|rebase|branch|"
    r"worktree|checkout|switch|reset|revert|restore|tag|cherry-pick|stash|rm|"
    r"mv|init|clone|submodule|config)\b"
)

# Claude Code / Codex bookkeeping messages that are not real user input.
NOISE_PREFIXES = (
    "<command-name>", "<local-command", "Caveat:", "[Request interrupted",
    "<user_instructions>", "<environment_context>", "<ENVIRONMENT_CONTEXT",
    "<turn_context>", "<permissions",
)

DEFAULT_MAX_CHARS = 400


# ---------------------------------------------------------------- helpers

def _local_now() -> datetime:
    return datetime.now().astimezone()


def _iso_to_local(s):
    """Parse an ISO-8601 timestamp (Z-suffix tolerated) to a local datetime."""
    if not s or not isinstance(s, str):
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone()
    except ValueError:
        return None


def _epoch_ms_to_local(ms):
    try:
        return datetime.fromtimestamp(int(ms) / 1000).astimezone()
    except (ValueError, OverflowError, OSError):
        return None


def _any_ts_to_local(v):
    """Tolerant timestamp parse: ISO string, epoch seconds, or epoch millis."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return _epoch_ms_to_local(v) if v > 1e12 else _epoch_ms_to_local(v * 1000)
    if isinstance(v, str):
        iso = _iso_to_local(v)
        if iso:
            return iso
        try:
            return _any_ts_to_local(float(v))
        except ValueError:
            return None
    return None


def _squash(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _clip(text: str, limit: int) -> str:
    text = _squash(text)
    if limit and len(text) > limit:
        return text[:limit] + " …"
    return text


def _is_noise(text: str) -> bool:
    t = text.lstrip()
    return not t or t.startswith(NOISE_PREFIXES)


def _norm_path(p: str) -> Path:
    return Path(os.path.realpath(os.path.expanduser(p or "")))


def _read_jsonl_head(path: Path, n: int = 50):
    """Read up to n leading JSONL lines that parse as dicts."""
    out = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh):
                if i >= n:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except ValueError:
                    continue
                if isinstance(obj, dict):
                    out.append(obj)
    except OSError:
        pass
    return out


def _iter_jsonl(path: Path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except ValueError:
                    continue
                if isinstance(obj, dict):
                    yield obj
    except OSError:
        return


# ---------------------------------------------------------------- session model

class Event:
    __slots__ = ("ts", "role", "kind", "text")

    def __init__(self, ts, role, kind, text):
        self.ts = ts          # local datetime or None
        self.role = role      # 'user' | 'assistant' | 'git' | 'file' | 'note'
        self.kind = kind      # free-form label, e.g. 'pi', 'claude-tool_use'
        self.text = text


class Session:
    def __init__(self, harness, sid, path, cwd, repo):
        self.harness = harness
        self.sid = sid or path.stem
        self.path = path
        self.cwd = cwd
        self.repo = repo
        self.models = []
        self.title = None      # e.g. Claude 'summary' line
        self.events = []

    @property
    def start(self):
        for e in self.events:
            if e.ts:
                return e.ts
        return None

    @property
    def end(self):
        for e in reversed(self.events):
            if e.ts:
                return e.ts
        return None

    def label(self):
        rel = ""
        if self.cwd and self.repo:
            try:
                rel = str(Path(self.cwd).relative_to(self.repo))
            except ValueError:
                rel = ""
        sid = self.sid or ""
        clipped = sid[:8].rstrip("-")
        base = f"{self.harness} {clipped}"
        if rel and rel != ".":
            base += f"  (worktree/subdir: {rel})"
        return base

    def add_text(self, ts, role, text):
        if not text or _is_noise(text):
            return
        self.events.append(Event(ts, role, "text", _squash(text)))

    def add_git(self, ts, cmd):
        if cmd:
            self.events.append(Event(ts, "git", "git", _squash(cmd)))

    def add_file(self, ts, verb, path_str):
        if path_str:
            self.events.append(Event(ts, "file", "file", f"{verb}: {path_str}"))

    def add_note(self, ts, text):
        self.events.append(Event(ts, "note", "note", _squash(text)))


def _bash_git(cmd: str):
    """Return the git portion of a shell command line, else None."""
    if not cmd:
        return None
    for part in re.split(r"&&|\|\||;|\n", cmd):
        part = part.strip()
        if part.startswith("git"):
            # tolerate `git -C <path>` prefixes (e.g. Cursor tool calls)
            probe = re.sub(r"^git\s+(?:-C\s+\S+\s+)+", "git ", part)
            if GIT_RE.search(probe):
                return part
    return None


# ---------------------------------------------------------------- harness: pi

def parse_pi_file(path: Path, repo: Path):
    lines = _read_jsonl_head(path, 1)
    if not lines or lines[0].get("type") != "session":
        return None
    head = lines[0]
    cwd = _norm_path(head.get("cwd"))
    try:
        if cwd != repo and repo not in cwd.parents:
            return None
    except TypeError:
        return None

    sess = Session("pi", head.get("id"), path, str(cwd), repo)
    for obj in _iter_jsonl(path):
        typ = obj.get("type")
        ts = _iso_to_local(obj.get("timestamp"))
        if typ == "model_change":
            mid = obj.get("modelId")
            if mid and mid not in sess.models:
                sess.models.append(mid)
        elif typ == "message":
            msg = obj.get("message") or {}
            role = msg.get("role")
            if role not in ("user", "assistant"):
                continue  # 'toolResult' messages carry no new narrative
            for c in msg.get("content") or []:
                ctype = c.get("type")
                if ctype == "text":
                    sess.add_text(ts, role, c.get("text"))
                elif ctype == "toolCall" and role == "assistant":
                    name = c.get("name", "")
                    args = c.get("arguments") or {}
                    if name == "bash":
                        git = _bash_git(args.get("command", ""))
                        if git:
                            sess.add_git(ts, git)
                    elif name in ("write", "edit"):
                        sess.add_file(ts, name, args.get("path", ""))
    return sess


# ---------------------------------------------------------------- harness: claude code

_TOOL_INPUT_KEYS = ("command", "cmd", "script")


def parse_claude_file(path: Path, repo: Path):
    head = _read_jsonl_head(path, 25)
    if not head:
        return None
    cwd_val = None
    for obj in head:
        if obj.get("cwd"):
            cwd_val = obj["cwd"]
            break
    if not cwd_val:
        return None
    cwd = _norm_path(cwd_val)
    try:
        if cwd != repo and repo not in cwd.parents:
            return None
    except TypeError:
        return None

    sess = Session("claude", head[0].get("sessionId") or path.stem, path, str(cwd), repo)
    for obj in _iter_jsonl(path):
        typ = obj.get("type")
        ts = _iso_to_local(obj.get("timestamp"))
        sidechain = bool(obj.get("isSidechain"))
        if typ == "summary":
            sess.title = obj.get("summary")
            continue
        if typ not in ("user", "assistant"):
            continue
        if obj.get("isMeta"):
            continue
        msg = obj.get("message") or {}
        content = msg.get("content")
        role = typ
        tag = " [subagent]" if sidechain else ""
        if isinstance(content, str):
            sess.add_text(ts, role + tag, content)
            continue
        for c in content or []:
            if not isinstance(c, dict):
                continue
            ctype = c.get("type")
            if ctype == "text":
                sess.add_text(ts, role + tag, c.get("text"))
            elif ctype == "tool_use":
                name = (c.get("name") or "").lower()
                inp = c.get("input") or {}
                if "bash" in name or "shell" in name or "terminal" in name:
                    for k in _TOOL_INPUT_KEYS:
                        git = _bash_git(inp.get(k, ""))
                        if git:
                            sess.add_git(ts, git)
                            break
                if "write" in name or "edit" in name or "notebook" in name:
                    sess.add_file(ts, name, inp.get("file_path") or inp.get("notebook_path") or "")
    return sess


# ---------------------------------------------------------------- harness: codex

def _codex_tool_text(name, args_raw):
    """Best-effort extraction of a command or patch target from a Codex tool call."""
    args = args_raw
    if isinstance(args_raw, str):
        try:
            args = json.loads(args_raw)
        except ValueError:
            args = {"raw": args_raw}
    if not isinstance(args, dict):
        return None, None
    cmd = args.get("command")
    if isinstance(cmd, list):
        cmd = " ".join(str(x) for x in cmd)
    if isinstance(cmd, str) and cmd.strip():
        git = _bash_git(cmd)
        return ("git", git) if git else (None, None)
    if "apply_patch" in str(name) or args.get("patch") or args.get("input"):
        blob = str(args.get("patch") or args.get("input") or "")
        m = (re.search(r"^\+{3}\s+(?:[ab]/)?(.+)$", blob, re.M)
             or re.search(r"^\*\*\*\s+(?:Add|Update|Delete)\s+File:\s*(.+)$", blob, re.M))
        return ("file", m.group(1)) if m else ("file", "(patch)")
    return None, None


def parse_codex_file(path: Path, repo: Path):
    head = _read_jsonl_head(path, 40)
    if not head:
        return None
    cwd_val = None
    sid = None
    for obj in head:
        typ = obj.get("type")
        if typ == "session_meta":
            payload = obj.get("payload") or {}
            sid = payload.get("id")
            cwd_val = payload.get("cwd") or cwd_val
        if not cwd_val and typ == "turn_context":
            cwd_val = (obj.get("payload") or {}).get("cwd")
        if sid and cwd_val:
            break
    if not cwd_val:
        return None
    cwd = _norm_path(cwd_val)
    try:
        if cwd != repo and repo not in cwd.parents:
            return None
    except TypeError:
        return None

    sess = Session("codex", sid or path.stem, path, str(cwd), repo)
    have_response_items = False
    for obj in _iter_jsonl(path):
        typ = obj.get("type")
        ts = _iso_to_local(obj.get("timestamp"))
        if typ == "turn_context":
            model = (obj.get("payload") or {}).get("model")
            if model and model not in sess.models:
                sess.models.append(model)
        elif typ == "response_item":
            payload = obj.get("payload") or {}
            ptype = payload.get("type")
            if ptype == "message":
                have_response_items = True
                role = payload.get("role")
                if role not in ("user", "assistant"):
                    continue
                for c in payload.get("content") or []:
                    text = (c or {}).get("text") if isinstance(c, dict) else None
                    if text:
                        sess.add_text(ts, role, text)
            elif ptype in ("function_call", "custom_tool_call"):
                kind, val = _codex_tool_text(payload.get("name"), payload.get("arguments"))
                if kind == "git" and val:
                    sess.add_git(ts, val)
                elif kind == "file" and val:
                    sess.add_file(ts, "apply_patch", val)
        elif typ == "event_msg" and not have_response_items:
            # older Codex versions only emit event_msg
            payload = obj.get("payload") or {}
            etype = payload.get("type")
            if etype in ("user_message", "agent_message"):
                role = "user" if etype == "user_message" else "assistant"
                sess.add_text(ts, role, payload.get("message"))
    return sess


# ---------------------------------------------------------------- harness: cursor (best-effort)
#
# Cursor has no single session log. Sessions live in a storage stack
# (https://vibe-replay.com/blog/cursor-local-storage/):
#   1. ~/.cursor/projects/<sanitized-cwd>/agent-transcripts/<sid>.jsonl  — richest text
#   2. ~/.cursor/chats/*/<sid>/store.db                                  — per-session SQLite (meta + blobs)
#   3. globalStorage state.vscdb, table cursorDiskKV:
#        composerData:<sid>   — name/createdAt + fullConversationHeadersOnly (ordered
#                               bubble list; type 1 = user, 2 = assistant)
#        bubbleId:<sid>:<bid> — text / toolFormerData per bubble
# All formats are undocumented, so every layer is parsed tolerantly and may
# fail independently. Only stdlib sqlite3/json are used.

CURSOR_GLOBAL_DBS = [
    HOME / ".config" / "Cursor" / "User" / "globalStorage" / "state.vscdb",
    HOME / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "state.vscdb",
]
CURSOR_WS_ROOTS = [
    HOME / ".config" / "Cursor" / "User" / "workspaceStorage",
    HOME / "Library" / "Application Support" / "Cursor" / "User" / "workspaceStorage",
]

_MAX_ROWS = 5000        # bounded scans so huge stores can't stall the run
_MAX_CELL = 200_000     # inspect at most this many chars of any one cell


def _sqlite_ro(path: Path):
    import sqlite3  # stdlib, imported lazily
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def _json_maybe(v):
    """Return (parsed, raw_string) when a cell looks like JSON, else (None, raw-ish)."""
    if isinstance(v, (bytes, bytearray)):
        v = v.decode("utf-8", "replace")
    if isinstance(v, str):
        s = v.strip()
        if s[:1] in ("{", "["):
            try:
                return json.loads(s), s
            except ValueError:
                pass
        return None, s
    return None, json.dumps(v) if isinstance(v, (dict, list)) else str(v)


def _cursor_role(obj, hint=None):
    for v in (hint, obj.get("role"), obj.get("type"), obj.get("speaker")):
        if v in (1, "1", "user", "human", "HUMAN"):
            return "user"
        if v in (2, "2", "assistant", "ai", "AI", "agent"):
            return "assistant"
    if obj.get("fromAgent") in (True, "true", 1):
        return "assistant"
    return None


def _cursor_text(v):
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        parts = []
        for item in v:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts) if parts else None
    if isinstance(v, dict):
        blocks = v.get("blocks")
        if isinstance(blocks, list):
            return _cursor_text(blocks)
    return None


def _cursor_tool_event(sess, ts, tfd):
    """Turn a Cursor toolFormerData payload into git/file events."""
    if not isinstance(tfd, dict):
        return
    name = str(tfd.get("name") or "")
    params, _raw = _json_maybe(tfd.get("params"))
    if not isinstance(params, dict):
        params = {}
    for k in ("command", "cmd", "script"):
        cmd = params.get(k)
        if isinstance(cmd, str):
            git = _bash_git(cmd)
            if git:
                sess.add_git(ts, git)
                return
    if any(w in name for w in ("write", "edit", "create", "rename", "delete", "apply")):
        fp = params.get("path") or params.get("file_path") or params.get("target_file") or params.get("edit")
        if isinstance(fp, dict):
            fp = fp.get("target_file") or fp.get("path") or ""
        if isinstance(fp, str) and fp:
            sess.add_file(ts, name, fp)


def _add_cursor_blob(sess, obj, role_hint=None, ts_hint=None):
    """Add events from one message-ish Cursor dict (bubble, blob, transcript line)."""
    if not isinstance(obj, dict):
        return
    ts = _any_ts_to_local(obj.get("createdAt") or obj.get("updatedAt")
                          or obj.get("timestamp") or obj.get("time") or ts_hint)
    text = _cursor_text(obj.get("text") or obj.get("message"))
    role = _cursor_role(obj, role_hint)
    if text and role:
        sess.add_text(ts, role, text)
    tfd = obj.get("toolFormerData") or obj.get("tool")
    if isinstance(tfd, (dict, list)):
        for item in (tfd if isinstance(tfd, list) else [tfd]):
            _cursor_tool_event(sess, ts, item)


def _sanitized_repo(repo: Path) -> str:
    return re.sub(r"[^A-Za-z0-9]", "-", str(repo))


# -- layer 1: transcript JSONL -------------------------------------------------

def _scan_cursor_transcripts(repo: Path, seen):
    sessions = []
    root = HOME / ".cursor" / "projects"
    if not root.is_dir():
        return sessions
    marker = str(repo)
    want_dir = _sanitized_repo(repo)
    for proj in root.iterdir():
        if not proj.is_dir() or proj.name == "agent-transcripts":
            continue
        at = proj / "agent-transcripts"
        if not at.is_dir():
            continue
        dir_match = proj.name == want_dir
        for jf in sorted(at.glob("**/*.jsonl")):
            sid = jf.stem
            if sid in seen:
                continue
            if not dir_match:
                head = "".join(json.dumps(o)[:_MAX_CELL] for o in _read_jsonl_head(jf, 30))
                if marker not in head:
                    continue
            sess = Session("cursor", sid, jf, str(repo), repo)
            sess.add_note(None, "source: agent transcript")
            for obj in _iter_jsonl(jf):
                _add_cursor_blob(sess, obj)
            if sess.events:
                seen.add(sid)
                sessions.append(sess)
    return sessions


# -- layer 2: per-chat store.db ------------------------------------------------

def _scan_cursor_store_dbs(repo: Path, seen):
    sessions = []
    root = HOME / ".cursor" / "chats"
    if not root.is_dir():
        return sessions
    marker = str(repo)
    for db in sorted(root.glob("*/*/store.db")):
        sid = db.parent.name
        if sid in seen:
            continue
        try:
            con = _sqlite_ro(db)
            tables = {r[0] for r in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            meta = {}
            matched = False
            sess = None
            if "meta" in tables:
                for row in con.execute("SELECT * FROM meta").fetchmany(20):
                    for cell in row:
                        obj, raw = _json_maybe(cell)
                        if isinstance(obj, dict):
                            meta.update(obj)
                            if not sess and obj.get("agentId"):
                                sess = Session("cursor", str(obj["agentId"]), db, str(repo), repo)
                                sess.title = obj.get("name")
                                if obj.get("lastUsedModel"):
                                    sess.models.append(str(obj["lastUsedModel"]))
                                sess.add_note(_any_ts_to_local(meta.get("createdAt")),
                                              f"source: store.db (mode: {obj.get('mode', '?')})")
            if "blobs" in tables:
                if sess is None:
                    sess = Session("cursor", sid, db, str(repo), repo)
                for row in con.execute("SELECT * FROM blobs").fetchmany(_MAX_ROWS):
                    for cell in row:
                        if isinstance(cell, (bytes, bytearray)):
                            cell = cell.decode("utf-8", "replace")
                        if isinstance(cell, str):
                            if not matched and marker in cell[:_MAX_CELL]:
                                matched = True
                            obj, _raw = _json_maybe(cell[:_MAX_CELL])
                            _add_cursor_blob(sess, obj)
            con.close()
            if sess and sess.events and matched:
                seen.add(sid)
                if sess.sid != sid:
                    seen.add(sess.sid)
                sessions.append(sess)
        except Exception:
            continue
    return sessions


# -- layer 3: cursorDiskKV (global + workspace state.vscdb) --------------------

def _scan_cursor_kv_db(db: Path, repo: Path, seen):
    sessions = []
    marker = str(repo)
    try:
        con = _sqlite_ro(db)
        tables = {r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        if "cursorDiskKV" not in tables:
            con.close()
            return sessions
        composers = []  # (sid, data_dict, repo_matched)
        for key, value in con.execute(
                "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'"
        ).fetchmany(_MAX_ROWS):
            obj, raw = _json_maybe(value)
            sid = key.split(":", 1)[1]
            if sid in seen or not isinstance(obj, dict):
                continue
            hit = marker in (raw or "")[:_MAX_CELL * 5]
            for k in ("cwd", "projectPath", "workspacePath"):
                if str(obj.get(k, "")) == marker:
                    hit = True
            composers.append((sid, obj, hit))
        if not composers:
            con.close()
            return sessions
        # One streaming pass over bubbles: keeps them for every candidate and
        # flags a session as matching this repo when any bubble mentions the
        # repo path (tool commands, referenced files — per the vibe-replay
        # storage map, composer rows themselves rarely carry a workspace).
        wanted = {sid for sid, _d, _m in composers}
        bubbles = defaultdict(list)  # sid -> [(bubble_id, obj)]
        matched_by_bubble = set()
        for key, value in con.execute(
                "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'"
        ).fetchmany(_MAX_ROWS * 20):
            parts = key.split(":")
            if len(parts) != 3 or parts[1] not in wanted:
                continue
            obj, raw = _json_maybe(value)
            if not isinstance(obj, dict):
                continue
            if len(bubbles[parts[1]]) < 400:
                bubbles[parts[1]].append((parts[2], obj))
            if parts[1] not in matched_by_bubble and marker in (raw or "")[:_MAX_CELL]:
                matched_by_bubble.add(parts[1])
        con.close()
        for sid, data, hit in composers:
            if not (hit or sid in matched_by_bubble):
                continue
            sess = Session("cursor", sid, db, str(repo), repo)
            sess.title = data.get("name")
            ts = _any_ts_to_local(data.get("createdAt"))
            sess.add_note(ts, "source: state.vscdb composerData")
            headers = data.get("fullConversationHeadersOnly")
            if isinstance(headers, list) and headers:
                by_id = {bid: obj for bid, obj in bubbles.get(sid, [])}
                for h in headers:
                    if not isinstance(h, dict):
                        continue
                    bid = h.get("bubbleId")
                    obj = by_id.get(bid)
                    if obj is None:
                        continue
                    _add_cursor_blob(sess, obj, role_hint=h.get("type"), ts_hint=ts)
            else:
                for _bid, obj in bubbles.get(sid, []):
                    _add_cursor_blob(sess, obj, ts_hint=ts)
            if sess.events:
                seen.add(sid)
                sessions.append(sess)
    except Exception:
        pass
    return sessions


def scan_cursor(repo: Path):
    sessions, seen = [], set()
    sessions += _scan_cursor_transcripts(repo, seen)
    sessions += _scan_cursor_store_dbs(repo, seen)
    for db in CURSOR_GLOBAL_DBS:
        if db.is_file():
            sessions += _scan_cursor_kv_db(db, repo, seen)
    for root in CURSOR_WS_ROOTS:  # legacy: composer rows in per-workspace DBs
        if not root.is_dir():
            continue
        for wsdir in root.iterdir():
            wj = wsdir / "workspace.json"
            db = wsdir / "state.vscdb"
            if not (wj.is_file() and db.is_file()):
                continue
            try:
                folder = json.loads(wj.read_text(encoding="utf-8", errors="replace")).get("folder", "")
            except ValueError:
                continue
            if _norm_path(folder.replace("file://", "")) == repo:
                sessions += _scan_cursor_kv_db(db, repo, seen)
    return sessions


# ---------------------------------------------------------------- harness: gemini (detection only)

def scan_gemini(repo: Path):
    root = HOME / ".gemini" / "tmp"
    sessions = []
    if not root.is_dir():
        return sessions
    marker = str(repo)
    for d in root.iterdir():
        if not d.is_dir():
            continue
        hit = False
        for f in list(d.glob("*.json"))[:10]:
            try:
                blob = f.read_text(encoding="utf-8", errors="replace")[:20000]
            except OSError:
                continue
            if marker in blob and '"cwd"' in blob:
                hit = True
                break
        if hit:
            s = Session("gemini", d.name, d, str(repo), repo)
            s.add_note(None, "Gemini CLI session detected (details not parsed)")
            sessions.append(s)
    return sessions


# ---------------------------------------------------------------- scanning

SCANNERS = {
    "pi": lambda repo: [
        s for s in (
            parse_pi_file(p, repo)
            for p in sorted((HOME / ".pi" / "agent" / "sessions").glob("*/*.jsonl"))
        ) if s
    ],
    "claude": lambda repo: [
        s for s in (
            parse_claude_file(p, repo)
            for p in sorted((HOME / ".claude" / "projects").glob("**/*.jsonl"))
        ) if s
    ],
    "codex": lambda repo: [
        s for s in (
            parse_codex_file(p, repo)
            for p in sorted((HOME / ".codex" / "sessions").glob("**/*.jsonl"))
        ) if s
    ],
    "cursor": scan_cursor,
    "gemini": scan_gemini,
}


def scan_all(repo: Path, harnesses):
    sessions, unavailable = [], []
    for name in harnesses:
        try:
            found = SCANNERS[name](repo)
        except Exception as exc:  # never let one harness kill the run
            found = []
            unavailable.append(f"{name} (scan error: {exc})")
        if found:
            sessions.extend(found)
        else:
            unavailable.append(name)
    sessions.sort(key=lambda s: (s.start or _local_now(), s.harness))
    return sessions, unavailable


# ---------------------------------------------------------------- digest

def _days_index(sessions):
    days = defaultdict(list)
    for s in sessions:
        for e in s.events:
            if e.ts:
                days[e.ts.date()].append((s, e))
    return days


def _fmt_ts(ts):
    return ts.strftime("%H:%M") if ts else "--:--"


def render_day(day, pairs, max_chars):
    lines = [f"## {day.isoformat()} — {len({id(s) for s, _ in pairs})} session(s), {len(pairs)} event(s)", ""]
    by_session = defaultdict(list)
    for s, e in pairs:
        by_session[s].append(e)
    for s in sorted(by_session, key=lambda x: x.start or _local_now()):
        span = ""
        if s.start and s.end:
            span = f", {s.start.strftime('%H:%M')}–{s.end.strftime('%H:%M')} {s.start.tzname()}"
        meta = []
        if s.models:
            meta.append("model: " + ", ".join(s.models))
        if s.title:
            meta.append(f'title: "{_clip(s.title, 80)}"')
        lines.append(f"### {s.label()}{span}")
        if meta:
            lines.append(f"*{' | '.join(meta)}*")
        lines.append(f"File: {s.path}")
        lines.append("")
        for e in by_session[s]:
            if e.role == "user":
                lines.append(f"- [{_fmt_ts(e.ts)}] USER: {_clip(e.text, max_chars)}")
            elif e.role == "assistant":
                lines.append(f"- [{_fmt_ts(e.ts)}] ASSISTANT: {_clip(e.text, max_chars)}")
            elif e.role == "git":
                lines.append(f"- [{_fmt_ts(e.ts)}] GIT: {_clip(e.text, 200)}")
            elif e.role == "file":
                lines.append(f"- [{_fmt_ts(e.ts)}] FILE {_clip(e.text, 160)}")
            elif e.role == "note":
                lines.append(f"- [{_fmt_ts(e.ts)}] NOTE: {_clip(e.text, max_chars)}")
        lines.append("")
    return "\n".join(lines)


def render(sessions, unavailable, target_days, max_chars, repo):
    tzname = _local_now().tzname()
    out = [
        f"# Agent session digest — {repo}",
        f"Timezone: local ({tzname}). Days grouped by event timestamp, so sessions crossing midnight appear on both days.",
        f"Matched sessions: {len(sessions)}"
        + (f" | no local data for: {', '.join(unavailable)}" if unavailable else ""),
        "",
    ]
    if not sessions:
        out.append("No sessions found for this repository. Nothing to document.")
        return "\n".join(out)
    days = _days_index(sessions)
    if not target_days:
        out.append("Matched days (use --date / --since / --until / --all):")
        for d in sorted(days):
            out.append(f"- {d.isoformat()}  ({len(days[d])} events)")
        return "\n".join(out)
    for d in target_days:
        if d in days:
            out.append(render_day(d, days[d], max_chars))
        else:
            out.append(f"## {d.isoformat()} — no sessions matched\n")
    return "\n".join(out)


# ---------------------------------------------------------------- cli

def _parse_day(s):
    try:
        return date.fromisoformat(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"bad date {s!r} — use YYYY-MM-DD")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Digest AI coding-agent sessions (pi, Claude Code, Codex, Cursor, Gemini) for a repository."
    )
    ap.add_argument("--repo", default=os.getcwd(), help="repository root (default: cwd)")
    ap.add_argument("--date", action="append", type=_parse_day, metavar="YYYY-MM-DD",
                    help="target day(s), local time (repeatable)")
    ap.add_argument("--since", type=_parse_day, metavar="YYYY-MM-DD")
    ap.add_argument("--until", type=_parse_day, metavar="YYYY-MM-DD")
    ap.add_argument("--all", action="store_true", help="digest every matched day")
    ap.add_argument("--harnesses", default="pi,claude,codex,cursor,gemini",
                    help="comma-separated subset (default: all)")
    ap.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS,
                    help=f"truncate message text at N chars (default {DEFAULT_MAX_CHARS})")
    ap.add_argument("--out", metavar="FILE", help="write digest to FILE instead of stdout")
    args = ap.parse_args(argv)

    repo = _norm_path(args.repo)
    harnesses = [h.strip() for h in args.harnesses.split(",") if h.strip()]
    unknown = [h for h in harnesses if h not in SCANNERS]
    if unknown:
        ap.error(f"unknown harness(es): {', '.join(unknown)} — known: {', '.join(SCANNERS)}")

    sessions, unavailable = scan_all(repo, harnesses)
    days = sorted(_days_index(sessions))

    target = []
    if args.all:
        target = days
    elif args.date:
        target = args.date
    elif args.since or args.until:
        target = [d for d in days
                  if (not args.since or d >= args.since)
                  and (not args.until or d <= args.until)]
    else:
        today = _local_now().date()
        # default: today, falling back to the most recent day that has sessions
        target = [today if today in days else (days[-1] if days else today)]
        if target and target[0] != today:
            print(f"note: no sessions today; falling back to most recent day {target[0]}", file=sys.stderr)

    digest = render(sessions, unavailable, target, args.max_chars, repo)
    if args.out:
        Path(args.out).write_text(digest + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(digest)


if __name__ == "__main__":
    main()
