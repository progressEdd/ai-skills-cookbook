---
name: log-sessions
description: Replay saved AI coding-agent session logs (pi, Claude Code, Codex, Cursor best-effort, Gemini detection) for the current repository and turn them into dated dev-log/daily-note entries documenting what was done with the agent. Invoke explicitly via /skill:log-sessions when the user asks to log, journal, or document agent session progress for a day or date range.
disable-model-invocation: true
---

# Log Sessions

Turn raw agent session logs into a human-readable daily dev-log entry. A stdlib-only Python script does the parsing; you do the summarizing.

## Quick start

```bash
python3 scripts/log_sessions.py --repo "$PWD"                 # today (falls back to most recent day)
python3 scripts/log_sessions.py --repo "$PWD" --date 2026-08-26
python3 scripts/log_sessions.py --repo "$PWD" --since 2026-08-25 --until 2026-08-27
python3 scripts/log_sessions.py --repo "$PWD" --all            # backfill everything
```

Run the script from this skill's directory (paths in this document are relative to it). The digest goes to stdout — or pass `--out FILE` to save it.

## What the script matches

- **Harnesses**: `pi` (`~/.pi/agent/sessions/`), `claude` (`~/.claude/projects/`), `codex` (`~/.codex/sessions/`) are parsed fully (user/assistant messages, git commands, file writes/edits). `cursor` best-effort parses all three of its storage layers — agent transcripts (`~/.cursor/projects/*/agent-transcripts/`), per-chat SQLite (`~/.cursor/chats/*/*/store.db`), and `composerData`/`bubbleId` rows in `state.vscdb` — since Cursor splits sessions across a storage stack rather than one transcript dir (see vibe-replay's Cursor local-storage deep dive). `gemini` is detection-only. Use `--harnesses pi,claude` to narrow.
- **Repository scope**: a session belongs to this repo when its recorded `cwd` is the repo root **or anywhere under it** — so sessions run inside worktrees and subfolders are included and labeled.
- **Day assignment**: events are grouped by local-timezone day, so a session that crosses midnight appears on both days. Ask the user before guessing which day they mean.
- **Noise filtering**: harness bookkeeping (`<command-name>`, caveats, environment context, tool results) is already stripped.

## Workflow

1. **Scope** — determine the target day(s) from the user's request ("yesterday", "08/26", "last week"). Convert to `YYYY-MM-DD` in the machine's local timezone.
2. **Digest** — run the script for those days. Read the digest. For any session needing more detail than the truncated excerpts, read the session file listed under its header.
3. **Anchor with git** — sessions say what was attempted; git says what landed:
   ```bash
   git log --all --date=local --pretty=format:'%h %ad %s' --since '<day> 00:00' --until '<day+1> 00:00'
   ```
   Include real commit hashes in the note. Uncommitted changes from that day are worth noting too (`git status`, worktree statuses via `git worktree list` + `git -C <worktree> status --short`).
4. **Find the repo's note convention** — look for an existing daily-note/dev-log folder (`00-dev-log/`, `dev-log/`, `.foam/templates/daily-note.md`, similar `YYYY-MM-DD.md` files). Reuse its location, front matter, and structure; style-match the sibling notes. If none exists, default to `00-dev-log/YYYY-MM-DD.md` with:

   ```markdown
   ---
   type: daily-note
   ---
   # YYYY-MM-DD
   ## Overall Progress
   - [ ] <one checkbox per meaningful outcome>

   ## Elaboration into overall progress
   <sections mirroring the checklist order, with details, decisions, and links>
   ```

5. **Write the note** — synthesize, don't transcribe: one checklist item per meaningful outcome, elaboration sections in the same order, commit hashes where they exist. Attribute work to the correct day by local time. Mention which harness(es) the work came from when mixed. **Exclude the currently-running session** (recognizable: its last user message is the `/skill:log-sessions` invocation itself) — the log documents completed sessions, not the act of logging them.
6. **Commit** — only if the user asked for it. One commit per day (`Document <date> progress: <short summary>`), including any of that day's stray uncommitted files that belong with the documentation.

## Script reference

| Flag | Meaning |
|---|---|
| `--repo PATH` | repository root (default: cwd) |
| `--date YYYY-MM-DD` | target day, repeatable |
| `--since` / `--until` | inclusive local-day range |
| `--all` | every matched day |
| `--harnesses LIST` | comma-separated subset of `pi,claude,codex,cursor,gemini` |
| `--max-chars N` | message truncation length (default 400) |
| `--out FILE` | write digest to a file instead of stdout |

With no date flags the script prints today's digest, falling back to the most recent day with sessions (noted on stderr).

## Notes and limits

- Read-only: the script never writes to session stores or the repo.
- Cursor's formats are undocumented and layered (transcripts, `store.db`, `cursorDiskKV`); the script dedupes sessions by id across layers but attributes a session to this repo only when the repo path appears in it (project dir name, transcript content, store blobs, or composer bubbles). A Cursor session that never mentions the repo path can't be attributed — say so rather than inventing content. Prompt history (`~/.cursor/prompt_history.json`) and the AI-attribution DB (`~/.cursor/ai-tracking/`) are out of scope.
- To support another harness, add a `parse_<name>_file`/`scan_<name>` function and register it in `SCANNERS` in `scripts/log_sessions.py`. JSONL stores with a recorded `cwd` are ~30 lines of code.
- If the user's sessions live somewhere unusual, the harness roots are all defined at the top of `SCANNERS` in the script.
