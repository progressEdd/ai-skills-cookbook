# Web search
> The agent's training data has a cutoff. Web search extends it to today's docs, APIs, and error messages.

## Learning objectives
- [ ] Explain when an agent needs web search and when it's a waste of context
- [ ] Enable and trigger web search in pi, Cursor, and Claude Code
- [ ] Guard against low-quality search results polluting the agent's answers

Every exercise sits right after the concept that teaches it — run each one as you read, and by the end of this lesson every box will be checked.

## Concepts

> **Back to the kitchen:** your Line Chef's cooking-school textbooks stop at graduation — that's the training cutoff. Web search is calling the supplier for today's prices and fresh stock.

### When to search
<!-- TODO: current docs, version-specific APIs, recent library releases, novel error messages; vs. stable knowledge already in training data -->

**Your turn**
- [ ] Ask an agent about a recent library release with and without search enabled — compare the answers

### How it works in each tool
<!-- TODO: pi / Cursor / Claude Code — enabling search, automatic vs. explicit invocation -->

**Your turn**
- [ ] Enable web search in your harness, then have the agent research an error message from a tool released in the last month

### Evaluating what comes back
<!-- TODO: source quality, recency, prompt-injection risk from web content -->

**Your turn**
- [ ] Check the sources behind the agent's answer — would you trust each one? Flag anything low-quality or outdated

## Checkpoint
If every box above is checked, this lesson is complete. Commit your progress:
```
git add -A
git commit -m "04 web search complete"
```

## Further reading
<!-- TODO: tool docs links -->
