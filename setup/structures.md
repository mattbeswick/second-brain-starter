# Starting structures

Pick the structure that matches question 2 of the interview, then adapt it. These are starting points,
not rules: the structure should match how the user thinks about their work, because that's how they'll
ask questions.

Every structure has the same core:

```
./
├── CLAUDE.md          the rules for the whole folder, and a map
├── AGENTS.md          points Codex at CLAUDE.md
├── BACKLOG.md         what to build next, in order
├── memory/            profile.md (who the user is) and MEMORY.md (the index)
├── integrations/      one folder per connected tool or data source
└── setup/             this setup kit
```

## Agency

```
├── clients/
│   └── <client-name>/     one per client
│       ├── CLAUDE.md       who they are, goals, contacts' roles, rules (NDA etc.)
│       ├── notes/          meeting notes, calls, decisions
│       ├── reports/        anything you produce for them
│       └── access.md       which accounts and tools exist (IDs and links only, never passwords)
├── projects/              internal work that isn't for one client
├── team/                  how the team works, who does what
├── sales/                 prospects and proposals (optional)
├── finance/               only if they handle money (optional)
└── personal/              if they said yes to question 12
```

## In-house

Choose the middle layer from question 4: `brands/`, `markets/` or `channels/`.

```
├── brands/                (or markets/ or channels/)
│   └── <brand>/
│       ├── CLAUDE.md       positioning, audiences, goals, rules
│       ├── notes/
│       └── reports/
├── stakeholders/          who asks for what, and how they like it
├── projects/
├── reporting/             recurring reports and where the numbers come from
├── team/
└── personal/              if they said yes to question 12
```

## Freelance or consultant

```
├── clients/
│   └── <client-name>/     same shape as the agency client folder
├── business/              your own admin: finance, contracts, sales, marketing
├── projects/
└── personal/              if they said yes to question 12
```

## Something else

Build it from the interview. Ask: "When you ask a question about your work, what's the first thing you
name: a client, a product, a channel, a project?" That's the top level.

## Folder rules

- **Lower-case, hyphenated folder names** (`acme-foods`, not `Acme Foods`). They're easier to type and
  to reference.
- **Two or three levels deep is plenty.** Deeper structures get lost.
- **A `CLAUDE.md` in every folder,** even if it's three lines.
- **Integrations get their own folder** (`integrations/google-ads/`), with a `CLAUDE.md` saying what the
  integration does, how to run it, and what it's allowed to change.
