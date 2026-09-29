# Second brain starter

A starter kit for turning Claude Code or Codex into a second brain: an AI agent that knows your
clients, your tools and how you work, keeps its own memory tidy, and has guard-rails so it can't do
anything stupid.

It comes from the talk **"From Vibe Coding to a Second Brain: The Performance Marketer's Ultimate AI
System"** at SMX Advanced Europe, Berlin, 30 September 2026. It's the same system I use every day,
stripped back to the parts anyone can start with.

**It doesn't give you a fixed structure.** The first time you open it, your agent scans your folder,
interviews you about how you work, and builds the structure around you. Then it writes you a backlog of
integrations to build over time.

## Get started

You need **Claude Code** or **Codex**. Python 3 is needed for the safety hooks (optional but
recommended), and the Codex CLI for the debate skills (optional).

1. **Get the files.**
   - New folder: `git clone https://github.com/mattbeswick/second-brain-starter.git my-second-brain`
     (or use **Code → Download ZIP** above).
   - Existing work folder: copy everything from this repo into it, **including the hidden `.claude`
     folder**. Setup won't move or delete anything of yours without asking.
2. **Open the folder in your agent.** `cd my-second-brain` then `claude` (or `codex`).
3. **Say "set me up".** The agent follows `setup/instructions.md`. It takes about 15 minutes.

Use the strongest model you have for setup (Claude Opus or GPT-6 Astra): it shapes everything after it.

## What happens during setup

1. **Scan.** The agent looks at your folder, without changing anything: existing folders, instruction
   files, and anything that looks like a password or key file (which it won't open).
2. **Interview.** About a dozen questions, one at a time: how you work (agency, in-house, freelance),
   your skill level, your channels, your tools, what you'd most like to hand off, and any data rules.
3. **Propose.** A folder structure built around your answers and what you already have. Nothing is
   built until you say yes.
4. **Build.** Folders with a `CLAUDE.md` in each, your profile and memory index, the safety hooks you
   choose, and `.gitignore` rules for anything sensitive.
5. **Backlog.** A prioritised list of the integrations you want, with anything that needs a slow access
   application marked "start now".

Say **"run setup again"** any time to re-check the structure and update the backlog.

## What's inside

| Path | What it is |
|---|---|
| `CLAUDE.md` | The rules for the whole folder. `AGENTS.md` points Codex at it |
| `setup/` | The setup flow: instructions, interview, starting structures, templates, and the guide to building integrations safely |
| `memory/` | Your profile and memory index (created by setup) |
| `.claude/hooks/` | **danger-scan** (blocks catastrophic commands), **memory-guard** (keeps the memory index lean), **session-check** (a quick health check at the start of each session). Setup also offers a terminal bell for when the agent needs you |
| `.claude/skills/` | `/memory-update` and `/handoff` to end sessions cleanly, and `/debate-plan` and `/debate-branch` to have Claude and Codex review each other's work |

## Three rules the whole system runs on

1. **A `CLAUDE.md` in every folder,** saying what the folder is for.
2. **One memory index that loads every session, kept short.** It points to notes rather than holding them.
3. **Every fact lives in one place.** Everything else points to it. Two copies of a fact means one of
   them is wrong.

## Integrations

Setup doesn't connect anything for you. Your agent builds each integration with you, one at a time,
from your backlog. Before you start one, read `setup/integrations.md`: use the strongest model, build
read-only first, keep credentials out of the folder, and put a human approval in front of every change
to a live account.

## Your privacy

Setup runs entirely on your machine. Your answers, your folders and your notes are never sent to me or
to this repository. Your AI provider sees what your agent reads, as it always does.

**Your second brain is private.** Once it's set up, it will hold your clients, your notes and your
rules. If you back it up to GitHub, use a **private** repository you own. Setup offers to disconnect
your copy from this public one so nothing gets pushed here by mistake.

## Licence and credit

MIT licence. Built by [Matt Beswick](https://linkedin.com/in/mbeswick), co-founder of
[Aira](https://aira.net). Use it, change it, share it.
