# Second brain

This folder is the user's second brain: the context, rules and tools their AI agent needs to work the
way they do. These instructions apply to everything in it. A `CLAUDE.md` in a subfolder adds rules for
that folder.

@memory/MEMORY.md

## Setup gate

**If `memory/profile.md` does not exist, setup has not run yet.** Before doing anything else, tell the
user and follow `setup/instructions.md` from the top. Don't start other work until setup is finished,
unless the user says to skip it.

## How to work here

- **Read the memory index first.** `memory/MEMORY.md` is the index of what you know about the user and
  their work. Read it at the start of every session (Claude Code loads it automatically through the line
  above).
- **Read the nearest `CLAUDE.md`** before working in a folder. It says what the folder is for and any
  rules that apply there. When you create a folder, give it a `CLAUDE.md` too.
- **One fact, one home.** Put each fact in exactly one place and point to it from anywhere else. Two
  copies of a fact means one of them is wrong - you just don't know which yet.
- **Keep the memory index short.** `MEMORY.md` holds one-line pointers, not detail. Detail goes in the
  topic file or folder it belongs to.
- **Secrets never go in these files.** No passwords, API keys or tokens in any `CLAUDE.md`, memory file or
  note. They live in the system keychain, a password manager, or an ignored `.env` file. Never ask the
  user to paste one into chat.
- **Ask before anything you can't undo, or that other people will see.** Deleting or moving files,
  sending emails or messages, changing live ad accounts, publishing anything. Show exactly what will
  change, then wait for a yes to that specific change.
- **The user sets the rules.** Don't add, change or remove a rule in any `CLAUDE.md` or in `MEMORY.md`
  without asking. Facts, status and pointers are normal upkeep; a rule that constrains every future
  session is the user's call. Propose it and wait.
- **End sessions cleanly.** When a piece of work wraps up, run `/memory-update`. If it will carry on in a
  new session, run `/handoff`.

## Building integrations

Before connecting any tool, API or data source, read `setup/integrations.md`. It covers which model to
use, the security checklist and the order to build things in. The list of what to build next is
`BACKLOG.md`.

## Map

Setup fills in this section with the user's folders and what each one is for.

- `setup/` - the setup flow and templates. Re-run it any time: "run setup again".
- `memory/` - the user's profile (`profile.md`) and the memory index (`MEMORY.md`).
- `BACKLOG.md` - integrations and automations to build, in order (created by setup).
- `.claude/` - hooks and skills.
