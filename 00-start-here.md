# Start here
> Two installs before lesson one: git (your version control and undo button) and an AI harness (your agent). Everything else in this course assumes both are working.

## Learning objectives
- [ ] Install and verify git
- [ ] Install an AI coding harness — pi is what this course prefers, but Cursor and Claude Code work too
- [ ] Connect the harness to a model provider and run your first session

Each concept below ends with a **Your turn** — run it before moving on, and by the time you reach the end of this lesson every box will be checked.

## Concepts

### Model provider vs. harness
Two concepts to keep separate:
1. **AI model provider** — the API endpoint serving a model (GLM, GPT, Claude, etc.)
2. **Coding agent/harness** — the interface that lets the model interact with your computer

You'll need both: a harness with no provider has no brain, a provider with no harness has no hands.

**Your turn**
- [ ] In one sentence each, say what the provider and the harness contribute — if you can't yet, re-read before installing anything

### Install git
If you cloned this repo by following the [root README](../../README.md), git is already installed. If not, follow the instructions for your platform in the [Pro Git book](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). Verify with:
```
git --version
```

**Your turn**
- [ ] Run `git --version` — it should print a version number

### Install your AI harness
All three harnesses below are used throughout this course. Pick one to start — **pi is the preferred default here**: minimal, very customizable, and self-documenting.

**pi (preferred)**
- Mac/Linux:
    ```
    curl -fsSL https://pi.dev/install.sh | sh
    ```
- Windows:
    ```
    powershell -c "irm https://pi.dev/install.ps1 | iex"
    ```
- Also available via npm/pnpm/bun. Setup: follow the [pi documentation](https://pi.dev/docs/latest); add a provider with `/login`, or edit `~/.pi/agent/auth.json` for custom API keys

**Cursor**
- Download from [cursor.com](https://cursor.com), install, and sign in. It's a full editor with the agent built in

**Claude Code**
- Download from [https://claude.com/product/claude-code](https://claude.com/product/claude-code)
- Then run `claude` in a project folder and sign in

**Your turn**
- [ ] Launch your chosen harness and sign in / connect a provider — it should open without errors

### Run your first session
Navigate to the repo you cloned from the root README (or any project folder), launch your harness, and ask it something simple:
```
what files are in this folder and what do they do?
```
An example output is 
<blockquote>
This is your ai-skills-cookbook repo — a project about teaching effective use of AI coding agents by building your own tools. Here's the layout:                         
                                                                                                                                                                        
## Top-level files                                                                                                                                                     
| Path | Purpose |                                                                                                                                                     
|---|---|                                                                                                                                                              
| `README.md` | Repo intro + setup instructions (cloning with submodules, installing the `setup-worktrees` git alias) |                                                
| `AGENTS.md` | Instructions for AI agents working in this repo (use `~/` paths, image conventions, worktree rules) |                                                  
| `LICENSE` | Repo license (AGPL-style, ~18KB) |                                                                                                                       
| `.gitignore` / `.gitmodules` | Standard ignores; `.gitmodules` registers 6 submodules (the harnesses + `01-dev-onboarding`) |                                        
                                                                                                                                    
                                                                                                                                                                        
## Folders                                                                                                                                                           
- **`00-dev-log/`** — Daily development journal (`2026-08-25.md`, `2026-08-26.md`), a `00-template.md` for new entries, and `core-ideas.md` capturing project          
concepts.                                                                                                                                                                
- **`00-supporting-files/`** — Supporting material:                                                                                                                    
- `data/sample.env.file` — example environment file                                                                                                                  
- `harnesses/` — git submodules of real-world agent harnesses used as reference material:                                                                            
    - `gsd-core` (open-GSD)                                                                                                                                            
    - `gsd-pi` (open-GSD)                                                                                                                                              
    - `openspec` (Fission-AI)                                                                                                                                          
    - `skills` (mattpocock/skills)                                                                                                                                     
    - `microsoft-agentic-harness` (MCKRUZ)                                                                                                                             
- **`01-dev-onboarding/`** — Git submodule (the `dev-onboarding` repo) with developer onboarding guides:                                                               
- `01-environment-setup/` — AI coding, multiple SSH, Node setup, VS Codium setup                                                                                     
- `02-dev-workflows/` — intro to git, intro to notes                                                                                                                 
- `03-python-environments/` — Poetry + Python virtual environments                                                                                                   
- **`02-worktrees/`** — Git worktrees for branch-based development (currently `course` and `master`), per the convention in its README.                                
- **`.agents/skills/`** — Reusable agent assets; contains a `codebase-onboarding` skill (with `SKILL.md`).                                                             
- **`.foam/templates/`** — Foam (VS Code knowledge-management) note templates: `daily-note.md`, `new-template.md`.                                                     
                                                                                                                                                                    
In short: a docs/course repo with a dev log, an embedded onboarding submodule, reference harness submodules for studying how agent tools are built, and pi/GSD agent tooling configured locally. 
</blockquote>

If you get a sensible answer, your provider + harness pairing works. You'll notice this same question is exercising skills from [02-navigating-the-harness.md](02-navigating-the-harness.md) — `@`, `/`, and folder exploration.

**Your turn**
- [ ] Ask the question above in your harness and confirm you get a sensible answer about the folder
- [ ] Save a screenshot of your first session under `00-supporting-files/images/start-here/` — a nice "day one" artifact (you'll commit it in the [next lesson](01-git-crash-course.md))

## Checkpoint
Every exercise above sits right next to the concept that taught it — if all boxes are checked, your setup is complete and you're ready for [01-git-crash-course.md](01-git-crash-course.md), where you'll commit the screenshot you just saved.

## Further reading
- [AI coding setup](https://github.com/progressEdd/dev-onboarding) (dev-onboarding guide — providers, plans, and pi in depth)
- [pi documentation](https://pi.dev/docs/latest)