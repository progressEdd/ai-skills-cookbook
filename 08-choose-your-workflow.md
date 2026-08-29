# Reviewing the harnesses: choose your workflow
> The capstone. Survey real workflow harnesses, compare the flows they impose, and choose one for your own project — while practicing deliberate context management.

## Learning objectives
- [ ] Describe the workflow each harness in `00-supporting-files/harnesses/` imposes (spec-driven, composable skills, phase loop, standalone agent)
- [ ] Compare harnesses on: process weight, context discipline, learning curve, lock-in
- [ ] Choose and justify a workflow for a project of your own
- [ ] Demonstrate deliberate context management throughout: `@` a single file vs. letting the agent explore a whole folder

Each concept below ends with a **Your turn** — run it before moving on, and by the time you reach the end of this lesson every box will be checked.

## Concepts

> **Back to the kitchen:** the capstone is choosing your restaurant concept — a food truck (minimal, composable skills), a tasting-menu fine-dining room (spec-driven), or a full brigade de cuisine (a phase loop). Pick the concept that matches the size of your kitchen.

### The harness landscape
<!-- TODO: map each repo to its philosophy —
- skills (Matt Pocock): minimal, composable, you own the process
- openspec: spec-driven, artifact workflow, CLI-enforced conventions
- gsd-core: phase loop (Discuss→Plan→Execute→Verify→Ship), fresh-context subagents
- gsd-pi: complete standalone agent, local-first, worktree automation
- microsoft-agentic-harness: under-the-hood — skills, tools, context budget, orchestration
-->

**Your turn**
- [ ] Review all five harnesses using deliberate context strategy: README first, then `@` only what you need to compare

### Comparison criteria
<!-- TODO: process weight, context discipline, learning curve, lock-in; when each wins -->

**Your turn**
- [ ] Write a short decision doc: which flow you'd adopt for a specific project, and why

### Making the choice
<!-- TODO: match harness to project size/team/skills; start small, you can add process later -->

**Your turn**
- [ ] Scaffold a small project using your chosen workflow

## Checkpoint
Every exercise above sits right next to the concept that taught it — if all boxes are checked, this lesson — and the course — is complete. Commit your progress:
```
git add -A
git commit -m "08 choose your workflow complete"
```

## Further reading
<!-- TODO: links to each harness's docs -->
