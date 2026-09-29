# Agent instructions

This folder was set up for Claude Code and Codex. The instructions live in `CLAUDE.md` so there is one
copy to maintain.

- **Read `CLAUDE.md` in this folder and follow it.** Everything in it applies to you.
- **Read `memory/MEMORY.md` at the start of every session.** Claude Code loads it automatically; you need
  to open it yourself.
- **In any subfolder, read its `CLAUDE.md` before working there.** If the subfolder has an `AGENTS.md`,
  it will just point you to the `CLAUDE.md` next to it.
- **Skills** live in `.claude/skills/<name>/SKILL.md`. When the user asks for one (for example
  "do a handoff" or "run memory-update"), read that file and follow it.
