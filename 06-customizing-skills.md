# Leveraging and customizing skills
> Skills are reusable instructions for your recurring workflows. Don't prompt the same thing twice — make it a skill.

## Learning objectives
- [ ] Explain what a skill is and how it differs from a prompt template and a command
- [ ] Install or write a skill in pi, Cursor, and Claude Code
- [ ] Adapt an existing skill to your own development practices
- [ ] Know when something deserves to be a skill vs. AGENTS.md vs. a one-off prompt

Every exercise sits right after the concept that teaches it — run each one as you read, and by the end of this lesson every box will be checked.

Do your skill work inside your `my-course` worktree — you brought `.agents/skills/` into it with the rebase in [the git crash course](01-git-crash-course.md). Skills are read per checkout, so an agent launched there sees your skills while the main checkout stays untouched.

## Concepts

### What is a skill?
<!-- TODO: SKILL.md structure, progressive disclosure, when skills load; vs. slash commands -->

**Your turn**
- [ ] Open one `SKILL.md` in `00-supporting-files/harnesses/skills/` and read it end-to-end — note its structure and how it tells the agent to use it

### Finding and installing skills
<!-- TODO: marketplaces, npx skills add, plugin stores; reading a skill before installing it -->

**Your turn**
- [ ] Browse `00-supporting-files/harnesses/skills/` and pick one skill to adapt to your own workflow

### Making it yours
<!-- TODO: adapting an existing skill, writing your own, keeping skills small and composable (see Matt Pocock's skills repo) -->

**Your turn**
- [ ] Write a small skill for something you've prompted more than twice this week

## Checkpoint
If every box above is checked, this lesson is complete. Commit your progress:
```
git add -A
git commit -m "06 customizing skills complete"
```

## Further reading
<!-- TODO: skills docs per tool; mattpocock/skills -->
