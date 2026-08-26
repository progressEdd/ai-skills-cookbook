# ai-skills-cookbook
Teaching you how to leverage AI Coding Agents effectively by building your own tools

## Getting Started
This repo uses git submodules to embed other repos and develops branches in git worktrees under `02-worktrees/`. Worktree assignments are local-only state, so after cloning you set them up with a small git alias — aliases prefixed with `!` run through git's own bundled POSIX shell, so the same commands work on Windows, macOS, and Linux.

If you already have a clone, bring it up to date first: `git pull && git submodule update --init --recursive`.

### 1. Clone
Before starting, make sure git is installed — check with `git --version`, and install it from [git-scm.com](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) if needed.

Navigate to the directory where you want the repo to live, then clone it (submodules included):
```bash
# e.g. cd ~/Documents/development_projects
cd <desired-directory>
git clone --recurse-submodules https://github.com/progressEdd/ai-skills-cookbook.git
cd ai-skills-cookbook
```

### 2. Install the worktree alias
One-time per clone — installs into this repo's local git config (`.git/config`), no machine-wide changes.

```bash
git config alias.setup-worktrees '!for b in $(git branch -r | grep -v HEAD | sed s/origin.//); do git worktree add 02-worktrees/$b $b 2>/dev/null || echo skipped $b; done'
```

**Windows cmd only** — same command, outer quotes swapped to `"` (cmd doesn't support single quotes):
```bat
git config alias.setup-worktrees "!for b in $(git branch -r | grep -v HEAD | sed s/origin.//); do git worktree add 02-worktrees/$b $b 2>/dev/null || echo skipped $b; done"
```

### 3. Set up the worktrees
```bash
git setup-worktrees
```

This creates a worktree under `02-worktrees/` for every remote branch. Notes:
- The alias lives only in this repo's `.git/config` — it disappears if you delete the clone
- The repo's default branch is reported as `skipped` — it's already checked out in the main working directory
- Re-running is safe: existing worktrees are skipped, not duplicated
- Branches that have never been pushed won't appear; create those manually per the [worktrees README](02-worktrees/README.md)
- To set up just one worktree: `git worktree add 02-worktrees/<branch> <branch>`
