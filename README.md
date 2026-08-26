# ai-skills-cookbook: Course
Teaching you how to leverage AI coding agents effectively — by building your own tools.

## Getting started
Before lesson one, install the two tools this course assumes:

### 1. Git
Follow the platform instructions in the [Pro Git book](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), then verify:
```
git --version
```

### 2. An AI harness
The preferred harness is **pi** — minimal, very customizable, and self-documenting:
- Mac/Linux:
    ```
    curl -fsSL https://pi.dev/install.sh | sh
    ```
- Windows:
    ```
    powershell -c "irm https://pi.dev/install.ps1 | iex"
    ```
- Setup, including adding a model provider: see the [pi documentation](https://pi.dev/docs/latest) (`/login`, or edit `~/.pi/agent/auth.json`)

[Cursor](https://cursor.com) and [Claude Code](https://www.npmjs.com/package/@anthropic-ai/claude-code) (`npm install -g @anthropic-ai/claude-code`) also work — the course compares all three.

Full setup walkthrough with exercises: [00-start-here.md](00-start-here.md).

## Your progress
After [01-git-crash-course.md](01-git-crash-course.md), do the rest of the course in your own worktree so you can mark checkboxes as you go:
```
git worktree add 02-worktrees/my-course -b my-course origin/course
```
Each lesson's exercises are checkboxes that sit right after the concept that teaches them — run each one as you read, and a finished lesson means every box is checked. Mark them and commit: your progress becomes a reviewable git history, and `course` stays clean for content updates.

## Lessons
Numbered by suggested order:

- [00-start-here.md](00-start-here.md) — Install git and your AI harness, run your first session
- [01-git-crash-course.md](01-git-crash-course.md) — Git as the safety net and undo button for agent-driven work
- [02-navigating-the-chat.md](02-navigating-the-chat.md) — The `@` and `/`: referencing files and invoking commands
- [03-project-instructions.md](03-project-instructions.md) — AGENTS.md and the `.agents` folder: teaching the agent your conventions
- [04-web-search.md](04-web-search.md) — Letting the agent pull in current documentation and answers
- [05-context-management.md](05-context-management.md) — What belongs in the context window, and when to start fresh
- [06-customizing-skills.md](06-customizing-skills.md) — Leveraging and adapting skills to your own practices
- [07-prompting-frameworks.md](07-prompting-frameworks.md) — Studying examples and adapting prompting frameworks
- [08-choose-your-workflow.md](08-choose-your-workflow.md) — Capstone: review the workflow harnesses and choose your own flow
