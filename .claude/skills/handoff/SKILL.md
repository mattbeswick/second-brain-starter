---
name: handoff
description: Wrap up a session that will continue later. Runs the memory-update tidy-up, then writes a self-contained handoff note (state, the single next step, what's done, files changed, checks run, blockers) to .claude/handoffs/, and gives you one line to paste into a fresh session. Use before closing a session mid-way through a piece of work.
argument-hint: "[name]"
---

# Handoff

## 1. Tidy up memory
Follow `.claude/skills/memory-update/SKILL.md` first, so anything durable is saved in its proper home
rather than only in the handoff note.

## 2. Write the handoff note
Write `.claude/handoffs/YYYY-MM-DD-<name>.md` (today's date; `<name>` from the argument, or a short
kebab-case name for the work). Create the folder if needed. It's git-ignored: handoff notes are
temporary by design.

The note must stand on its own, so a fresh session can continue without redoing anything. Include:
- **Current state** of the work.
- **The single next action.**
- **What's already done** and must not be redone.
- **Files changed** and other important paths.
- **Checks run**, each marked pass, fail or not run.
- **Anything to leave alone:** unrelated changes in the folder, files another session is working on.
- **Blockers,** and decisions the user needs to make.

Keep next steps tightly scoped.

## 3. Give the user the paste line
End your reply with exactly this line (with the real path), and nothing after it:

```
Read .claude/handoffs/YYYY-MM-DD-<name>.md and continue from it. Tell me what's next before you do anything.
```

The last sentence matters: it makes the new session say what it thinks the next step is and wait,
rather than acting on a misreading.
