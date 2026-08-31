# AGENTS.md and the `.agents` folder
> Teach the agent your conventions once, so you stop repeating them in every prompt.

## Learning objectives
- [ ] Explain what AGENTS.md is and which tools read it (pi, Claude Code, Cursor, ...)
- [ ] Write a concise, effective AGENTS.md for your own project
- [ ] Describe what belongs in project instructions vs. what belongs in a prompt
- [ ] Use the `.agents/` folder pattern for harness-agnostic assets (skills, scripts, adapters)

Each concept below ends with a **Your turn** — run it before moving on, and by the time you reach the end of this lesson every box will be checked.

## Concepts

> **Back to the kitchen:** AGENTS.md is the house-rules card laminated on the wall — every chef reads it at the start of the shift, so nobody repeats the rules per order. The `.agents/` folder is the recipe binder every station can reach, whichever kitchen format you run.

### What is AGENTS.md?
The [github page](https://github.com/agentsmd/agents.md) actually has a great explanation, let's read it
> Think of AGENTS.md as a README for agents: a dedicated, predictable place to provide context and instructions to help AI coding agents work on your project.

You can write your high level rules and conventions for your coding agent to follow. Depending on your harness, it might also be called `HERMES.MD` for Hermes Agent, `CLAUDE.md` for claude code, and `CURSOR.md` for cursor, Edd defined the AGENTS.md for this project to use a shorthand for paths, well as screenshots, worktrees and scripts
<blockquote>
# Agent Instructions

1. **Use relative directories** — Always use `~/` instead of absolute paths like `/home/user/...`. This ensures portability across different machines and environments.

2. **Screenshots and images** — When adding screenshots or other images, place them in:
   ```
   00-supporting-files/images/${fileBasenameNoExtension}/${datetime|yyyyMMddHHmmss}
   ```
   For example, a screenshot from `feature-demo.md` would go in:
   ```
   00-supporting-files/images/feature-demo/20260524153000.png
   ```

3. **Worktrees** — If a `02-worktrees` folder exists in the project root, create git worktrees by default when branching. Follow the conventions described in the `02-worktrees/README.md` for naming, structure, and usage.

4. This repo keeps reusable agent assets in `.agents/` and syncs tool-specific adapters with `.agents/scripts/`.

</blockquote>

As you get more complex rules, you should organize them in the `.agents` or a folder written in `AGENTS.md`. OpenAI realized that splitting out rules to separate files and making `AGENTS.md` a table of contents resulted in less context rot, in their a [blog post](https://openai.com/index/harness-engineering/#we-made-repository-knowledge-the-system-of-record) that chronicles their experiences using a large the `AGENTS.md` file. 

**Your turn**
- [ ] Read the [`AGENTS.md`](///AGENTS.md) at the root of this repo
- [ ] Read one of `AGENTS.md` harness in `00-supporting-files/harnesses/` — compare what each chooses to instruct. If you need a specific example, you can look at [matt pocock's `AGENTS.md`](///00-supporting-files/harnesses/mattpocock-skills/AGENTS.md)

### Writing good instructions
<!-- TODO: keep it short, imperative, and specific; examples of good vs. bad rules; avoiding instruction bloat -->

**Your turn**
- [ ] Draft an AGENTS.md for a project of your own (3–5 rules max)

### The `.agents` folder
<!-- TODO: keeping skills/scripts harness-agnostic in the repo, syncing tool-specific adapters; example: this cookbook's own .agents/ -->

**Your turn**
- [ ] Explore this repo's `.agents/` folder — find where the `codebase-onboarding` skill lives and note how the same assets serve different harnesses

## Checkpoint
Every exercise above sits right next to the concept that taught it — if all boxes are checked, you're ready for [04-web-search.md](04-web-search.md). Commit your progress:
```
git add -A
git commit -m "03 project instructions complete"
```

## Further reading
[AGENTS.md the standard](https://agents.md/)
[pi's AGENTS.md](https://github.com/earendil-works/pi/blob/main/AGENTS.md)
[Codex's AGENTS.md](https://github.com/openai/codex/blob/main/AGENTS.md)
[OpenAI's Learnings for AGENTS.md](https://openai.com/index/harness-engineering/)
[Cursor's AGENTS.md Section](https://cursor.com/docs/rules#agentsmd)
