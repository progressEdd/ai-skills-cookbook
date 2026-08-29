# Context management
> The context window is the agent's working memory. What you let in — and when you start fresh — decides the quality of everything it does.

## Learning objectives
- [ ] Explain what a context window is and what happens when it fills with noise ("context rot")
- [ ] Choose deliberately between `@`-referencing a file and letting the agent explore a folder
- [ ] Keep noise out of context (ignore rules, tight prompts, not dumping logs)
- [ ] Recognize when a session has gone stale and starting fresh beats salvaging

Every exercise sits right after the concept that teaches it — run each one as you read, and by the end of this lesson every box will be checked.

## Concepts

> **Back to the kitchen:** mise en place. The counter is your context window — only what this dish needs belongs on it. Context rot is a cluttered counter where the fish sauce spills into the dessert prep. A fresh session is wiping the counter down between dishes.

### The context window
<!-- TODO: tokens, working memory analogy, how tools show context usage -->

**Your turn**
- [ ] During your next session, find your harness's context-usage indicator and watch it grow as the conversation continues

### What goes in, what stays out
<!-- TODO: single file vs. folder exploration; exclusions (.gitignore-style); summarizing instead of pasting -->

**Your turn**
- [ ] Review `00-supporting-files/harnesses/` without dumping everything into context — start with each README, then `@` only the files you need to compare workflows

### Fresh sessions
<!-- TODO: compaction, clearing, session summaries; when to restart instead of steering harder -->

**Your turn**
- [ ] Notice a degrading session, start fresh with a concise summary of where you left off, and compare the results

## Checkpoint
If every box above is checked, this lesson is complete. Commit your progress:
```
git add -A
git commit -m "05 context management complete"
```

## Further reading
<!-- TODO: context engineering links -->
