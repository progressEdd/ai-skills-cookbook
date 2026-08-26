# AGENTS.md and the `.agents` folder
> Teach the agent your conventions once, so you stop repeating them in every prompt.

## Learning objectives
- [ ] Explain what AGENTS.md is and which tools read it (pi, Claude Code, Cursor, ...)
- [ ] Write a concise, effective AGENTS.md for your own project
- [ ] Describe what belongs in project instructions vs. what belongs in a prompt
- [ ] Use the `.agents/` folder pattern for harness-agnostic assets (skills, scripts, adapters)

Every exercise sits right after the concept that teaches it — run each one as you read, and by the end of this lesson every box will be checked.

## Concepts

### What is AGENTS.md?
<!-- TODO: the emerging cross-tool convention; where it lives (repo root, subfolders); when it's loaded -->

**Your turn**
- [ ] Read the AGENTS.md at the root of this repo and of one harness in `00-supporting-files/harnesses/` — compare what each chooses to instruct

### Writing good instructions
<!-- TODO: keep it short, imperative, and specific; examples of good vs. bad rules; avoiding instruction bloat -->

**Your turn**
- [ ] Draft an AGENTS.md for a project of your own (3–5 rules max)

### The `.agents` folder
<!-- TODO: keeping skills/scripts harness-agnostic in the repo, syncing tool-specific adapters; example: this cookbook's own .agents/ -->

**Your turn**
- [ ] Explore this repo's `.agents/` folder — find where the `codebase-onboarding` skill lives and note how the same assets serve different harnesses

## Checkpoint
If every box above is checked, this lesson is complete. Commit your progress:
```
git add -A
git commit -m "03 project instructions complete"
```

## Further reading
<!-- TODO: links -->
