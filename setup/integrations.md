# Building integrations

An integration connects your second brain to a tool or data source: Google Ads, GA4, Search Console, a
spreadsheet, Slack. This is where the system gets powerful, and also where it can do real damage. Read
this before building any of them, and have your agent read it too.

There's no magic command. **Your agent builds each integration with you,** one at a time, following the
steps below. That's deliberate: every stack is different, and you should understand what you've
connected.

## 1. Use the strongest model you have

Integration work is where a cheaper model costs you most. It's writing code that touches real accounts,
handling credentials, and making judgement calls about permissions.

- **Claude Code:** switch to Opus (`/model`) before you start.
- **Codex:** use GPT-6 Astra, or the strongest model your plan includes.

Everyday work in your folders can happen on a faster model. Switch up for this.

## 2. Plan before building

Ask your agent to write a short plan first: what the integration will do, how it will log in, what it
can read, what it can change, and how you'll test it. If you have both Claude Code and Codex, run
`/debate-plan` on it so a second model can pick holes in it before anything is built.

## 3. The security checklist

Go through this for every integration. Your agent should confirm each point before it's done.

- [ ] **Read-only first.** Build the version that can only read data. Use it for a while. Only add the
      ability to change things once you trust the numbers.
- [ ] **The narrowest permissions the platform allows.** If there's a read-only scope, use it. If you can
      limit access to one account, property or channel, do.
- [ ] **Credentials never go in this folder's files.** No keys or tokens in `CLAUDE.md`, memory or notes.
      Use the system keychain, a password manager, or an ignored `.env` file, and check that
      `.gitignore` covers it before the first commit.
- [ ] **Never paste a key into chat.** Put it where it belongs yourself and tell the agent where to find it.
- [ ] **Reading and changing are separate tools.** The tool that reads can never change anything. Any
      change goes through a second tool that shows you exactly what it will do and waits for your yes.
- [ ] **A yes means that specific change.** A general "go ahead" doesn't approve a different change later.
- [ ] **Check who made it.** Before installing someone else's integration or MCP server, check who
      publishes it. Prefer the platform's own official one. Treat unknown ones like unknown software,
      because that's what they are.
- [ ] **Log what it does.** Anything that changes an account should write down what it changed, when,
      and what it was before.

## 4. Test against the real thing

Before you rely on an integration, compare its numbers with the platform's own interface for the same
account and dates. If they don't match, find out why before building anything on top.

## 5. Only then allow changes, behind a gate

When you're ready for an integration to make changes (for example to a Google Ads account), build the
gate first:

1. **Change set.** The agent writes out the exact change: what, where, the value before and the value after.
2. **Approval.** You approve that specific set.
3. **Dry run.** Where the platform supports it, validate the change without applying it.
4. **Drift check.** If the account no longer matches the "before" values, refuse to run.
5. **Apply,** one change set at a time.
6. **Prove the gate works.** Send one change you know should be refused, and check that it is. A dry run
   that passes proves nothing on its own.

Start with one low-risk account.

## 6. Write it down

Every integration gets `integrations/<name>/CLAUDE.md` (start from `setup/templates/integration-CLAUDE.md`) saying:
- what it does and what it's for;
- how it logs in (where the credentials are, never the credentials themselves);
- the commands to run it;
- what it can read, and what (if anything) it can change;
- anything surprising you learned building it.

Then add a one-line pointer to `memory/MEMORY.md` and update its row in `BACKLOG.md`.

## Ordering the backlog

- **Quick read-only wins first.** A read-only connection you use every day beats an ambitious one you
  never finish.
- **Start slow approvals now.** Some platforms make you apply for API access, and that can take days or
  weeks. Google Ads API access (a developer token, applied for from a manager account) is the usual one
  for PPC. Meta and LinkedIn also have app review steps for some access. Mark these **start now** in the
  backlog, apply straight away, and build something else while you wait. When you apply, describe
  honestly what you'll use the access for, and use a contact inbox someone actually reads.
- **Build what your first job needs.** If the task you most want to hand off needs Search Console data,
  that integration moves to the top.

## Common starting points

These are the ones most marketers start with. Your agent will know how to build each of them; the
notes are the traps to watch for.

| Integration | Notes |
|---|---|
| Google Search Console | Read-only access is easy to scope. Search Console data has sampling and privacy filtering, so totals won't match a GA4 report exactly |
| Google Analytics 4 | Use the Data API with read-only access. Check the property's time zone before comparing dates |
| Google Ads | Needs API access (see above). Start read-only with reports; build the change gate before any writes. Split search-term analysis by conversion action before pausing anything |
| Google Sheets and Drive | Limit access to specific files or folders where you can. A great first integration: many teams already keep their data here |
| Slack | Read from specific channels only. **Never let an agent post automatically to a channel clients can see.** Have it write drafts you send yourself |
