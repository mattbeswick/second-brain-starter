---
name: memory-update
description: End-of-session tidy-up. Saves only what's worth keeping from this session (durable, non-obvious facts that can't easily be looked up again) to exactly one home each, then checks the files it touched for stale information and broken pointers. Use when wrapping up a piece of work.
---

# Memory update

Look back over this session and decide what's worth keeping. Keep only facts that are **durable**
(still true next month), **non-obvious** (not already written down or easy to look up) and **useful**
(a future session would do better knowing them). Don't save routine progress, one-off numbers, or
anything you could re-query in seconds.

For each thing worth keeping, pick **exactly one** home:

| Kind of fact | Home |
|---|---|
| A rule for how to work in a folder, client or integration | That folder's `CLAUDE.md` (a new rule needs the user's OK first) |
| Knowledge about a client, brand or project | Its folder: the `CLAUDE.md` for key facts, `notes/` for dated detail |
| How an integration works, or a trap you hit | `integrations/<name>/CLAUDE.md` |
| Something every session needs to know | A one-line pointer in `memory/MEMORY.md`, with the detail in a topic file next to it (`memory/<topic>.md`) |
| Something about the user (preferences, style, how they work) | `memory/profile.md` |
| Useful but you're not sure where it goes | `memory/inbox.md`, for the user to sort later |

Rules:
- **One fact, one home.** If it's already written somewhere, update that place instead of adding a copy.
  Point to it from elsewhere if needed.
- **The memory index stays short.** One line per entry. If an entry is getting long, move the detail
  into its topic file and leave the pointer.
- **Rules are the user's call.** A fact or status update is fine. A new rule that changes how every
  future session works gets proposed to the user, not written in.
- **Update, don't append.** Replace outdated wording rather than adding a newer version underneath.

Then check every file you touched, plus any the session relied on, for: status that's now out of date,
counts that have changed, and pointers to files that don't exist.

Finish with a short table: what you saved and where, and anything you checked but left alone (with a
few words on why).
