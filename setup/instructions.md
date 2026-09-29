# Setup instructions

**These instructions are for you, the AI agent.** Follow them in order to set up this folder for the
user. The aim is a structure that fits how they actually work from day one, plus a backlog of the
integrations they want to build over time.

Setup has five stages: **scan, interview, propose, build, hand off.** It should take the user about 15
minutes.

## Rules for the whole of setup

1. **Read-only until the user approves the plan.** Stages 1 to 3 change nothing. Stage 4 only runs after
   a clear yes to the proposal.
2. **Never move, rename or delete anything that already exists** without a separate yes for that
   specific change. The default is to leave existing files where they are and add around them.
3. **Never open files that look like secrets** (see the scan list). Note their paths only.
4. **One question at a time.** If you have a multiple-choice question tool (Claude Code has one), use it
   and always allow a free-text answer. Otherwise number the options so the user can reply with a number.
5. **Match the user's level.** Once you know their skill level (question 5), adjust how much you explain.
   Beginners get plain English and no jargon. Developers get the short version.
6. **Nothing leaves the machine.** Setup writes files in this folder only. It never sends answers
   anywhere.
7. **The user can stop at any point.** If they do, write what you have so far to `memory/profile.md`
   with `Setup status: incomplete` at the top, and tell them to say "run setup again" to carry on.

## Stage 0: Say what's about to happen

Tell the user, in three or four short lines:
- you're going to look at this folder (without changing anything), ask about 12 questions, show them a
  proposed structure, and only build it once they've said yes;
- it takes about 15 minutes;
- their answers stay on their machine;
- they can stop at any time and pick up later.

**Model check.** If you can tell which model you are running on and it isn't a top-tier model (for
example Claude Opus or GPT-6 Astra), say so once and recommend switching before continuing. Setup
decisions shape everything that follows, so they're worth the strongest model. Don't block on it.

## Stage 1: Scan (read-only)

Work out the following. Use simple read-only commands (`ls`, `find`, `git status`, `python3 --version`)
and explain to a beginner what you're checking and why before running anything.

| Check | How | Why it matters |
|---|---|---|
| Which agent you are | You know this: Claude Code, Codex or something else | Codex needs an `AGENTS.md` in each folder; Claude Code uses `CLAUDE.md` |
| Operating system | `uname -a` or equivalent | Commands and paths differ on Windows |
| Python 3 | `python3 --version` | The safety hooks need it. If missing, hooks are skipped and you tell the user how to add them later |
| Git | `git --version`, then `git status` and `git remote -v` in this folder | Version history is a safety net. A remote pointing at the public starter repo should be removed so nothing personal is ever pushed there |
| Existing folders | List everything two levels deep, ignoring `.git`, `node_modules`, and this kit's own files (`setup/`, `.claude/`, `memory/`, `README.md`, `LICENSE`, `CLAUDE.md`, `AGENTS.md`) | For each folder: how many files, the main file types, and whether it already has a `CLAUDE.md` or `AGENTS.md` |
| Existing instructions | Find any `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.windsurfrules` or similar outside this kit, and read them | They hold rules the user already relies on. Never overwrite them; merge into them |
| Sensitive files | Look for names like `.env`, `*.pem`, `*.key`, `*.p12`, `id_rsa*`, `*credentials*.json`, `*service-account*.json`, `*token*`, and exports with personal data (`*contacts*`, `*leads*`, `*customers*` as CSV or spreadsheets) | These need to be kept out of git and out of anything the agent sends. **Do not open them.** Record the paths |

Then show the user a short summary table: what you found, and anything that needs attention (for
example "3 files that look like credentials, which I'll keep out of git" or "no Python, so the safety
hooks will wait").

If the folder is empty apart from this kit, say so. That's the easy case.

## Stage 2: Interview

Follow `setup/interview.md`. It has the questions, the order, and what each answer changes.

**Use what the scan found.** If there's a `clients/` folder with 14 subfolders, don't ask "do you have
clients?". Ask "you've got 14 folders in `clients/`. Is each one a client?" If they already have a
`CLAUDE.md`, ask what's working about it and what isn't.

Skip any question the answers already cover. When you're done, read the answers back as a short summary
and let the user correct anything before moving on.

## Stage 3: Propose (still read-only)

Use `setup/structures.md` to choose the starting structure for how they work, then adapt it to their
answers and to what already exists.

Show the proposal as a folder tree with a marker on each line:
- `[keep]` exists already and stays as it is;
- `[new]` will be created;
- `[move?]` a suggested move or rename. **List each one separately and default to no.** Only suggest a
  move when it clearly helps, for example scattered client files that belong in one client folder.

Under the tree, list:
- what each top-level folder is for, in one line each;
- the safety hooks you'll install, with one sentence each on what they do (see Stage 4, step 6);
- the skills that come with the kit;
- what will be added to `.gitignore`;
- the first three backlog items you'll write.

Ask for a yes, changes, or no. Revise and show it again until it's a clear yes. A "looks fine" to the
structure is not a yes to any `[move?]` line: confirm those one by one.

## Stage 4: Build

Only after a clear yes. Do these in order, and tell the user what you're doing as you go.

1. **Folders.** Create the `[new]` folders. Carry out only the moves the user approved individually.

2. **A `CLAUDE.md` in every folder** that doesn't have one, from `setup/templates/folder-CLAUDE.md`
   (or `client-CLAUDE.md` for a client or brand folder). Fill in the real purpose, what goes in the folder
   and what doesn't, and any rules from the interview (for example a client's NDA). For an existing folder
   with content, base it on the file names you saw in the scan. Keep each one short: a few lines of
   purpose and rules, plus pointers. Never overwrite an existing `CLAUDE.md`: add a section to it instead,
   and show the user the addition.

3. **Codex support.** If the user uses Codex (or both tools), put an `AGENTS.md` next to every
   `CLAUDE.md` you create, containing one line: `Read and follow CLAUDE.md in this folder.`

4. **Profile and memory.**
   - Write `memory/profile.md` from `setup/templates/profile.md` with the interview answers. Set
     `Setup status: complete` and today's date. This file switches off the setup gate.
   - Replace `memory/MEMORY.md` with `setup/templates/MEMORY.md`, filled in. Keep it to one-line pointers.

5. **Root `CLAUDE.md`.** Fill in the `## Map` section with the real folders and one line each. Add a
   `## Style` section from the interview (spelling, answer length, anything that annoys them). Don't change
   the other sections without asking.

6. **Safety hooks** (Claude Code only, and only if Python 3 is available). Explain each hook in one
   sentence and let the user choose which to turn on:
   - **danger-scan** blocks catastrophic commands before they run (deleting your home folder, wiping a
     disk, force-pushing over `main`) and asks before risky ones (piping a download straight into a shell).
   - **memory-guard** warns when the memory index grows past its size limit or an entry gets too long.
   - **session-check** runs at the start of every session and flags folders without a `CLAUDE.md`, a
     memory index that's getting big, and credential files that aren't protected by `.gitignore`.
   - **bell** rings the terminal bell when the agent finishes or needs an answer, so you can walk away.

   To install them, merge the chosen blocks from `setup/hooks-settings.json` into `.claude/settings.json`.
   Create the file if it doesn't exist. **Never delete or replace hooks that are already there.** Then
   test: run `python3 .claude/hooks/danger_scan.py --test` and `python3 .claude/hooks/session_check.py`
   and show the result.

   For Codex users, say that these hooks are Claude Code features. The rules in `CLAUDE.md` still apply.

7. **`.gitignore`.** Make sure it covers every sensitive path from the scan, plus the standard patterns
   already in the kit's `.gitignore`. Add a line for any folder the user said must never leave their
   machine.

8. **Git.** If the user wants version history and the folder isn't a git repository yet, run `git init`.
   If `origin` points to the public starter repository, explain why and ask before running
   `git remote remove origin`. **This folder is private.** If they want an online backup, it must be a
   private repository they own. Never push anything without asking.

## Stage 5: Backlog and hand-off

1. **Write `BACKLOG.md`** from `setup/templates/BACKLOG.md`. One row for each integration or automation
   the user asked for, plus their "first job to hand off" from the interview. Order it using the rules
   in `setup/integrations.md`: read-only quick wins first, and anything needing a slow approval (for
   example Google Ads API access) marked **start now**, because approval can take days.

2. **Run the session check** once (`python3 .claude/hooks/session_check.py`, if installed) and fix
   anything it flags.

3. **Tell the user what you built,** as a short table: folders, files, hooks, backlog items.

4. **Give them their first three moves.** Adapt these to their answers:
   1. Spend 20 minutes filling in one client, brand or project folder with real context: who, what,
      goals, quirks, what's been tried. The more context, the better every answer gets.
   2. Pick backlog item 1 and start it in a new session, on the strongest model available. Read
      `setup/integrations.md` together first.
   3. Finish every session with `/memory-update` (or `/handoff` if the work carries on), so the brain
      gets a little smarter each day.

## Running setup again

When the user says "run setup again", or `memory/profile.md` says `Setup status: incomplete`:

- Read `memory/profile.md` and skip every question that's already answered. Ask only what's missing, or
  what the user wants to change.
- Run the Stage 1 scan again and compare with the profile. Report drift: new folders without a
  `CLAUDE.md`, folders that have gone, a memory index that's grown too big, new files that look like
  secrets.
- Propose fixes and new backlog rows the same way as Stage 3, then build what's approved.
- Update `Last checked` in the profile.
