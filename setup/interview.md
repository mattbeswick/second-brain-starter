# Setup interview

Ask these in order, **one at a time**. Skip anything the scan or an earlier answer already covers. Where
there are options, offer them as multiple choice and always allow "something else". Keep your own words
short: this should feel like a quick chat, not a form.

Write each answer down as you go. It all ends up in `memory/profile.md`.

## The questions

### 1. Name
"What should I call you?" (free text)

### 2. How you work
"Which of these is closest to how you work?"
- Agency (you look after clients)
- In-house (you work on your own company's brands)
- Freelance or consultant
- Something else (ask them to describe it)

**Changes:** the top-level structure (see `setup/structures.md`).

### 3. Team
"Is this folder just for you, or will other people use it too?"
- Just me
- Me, but I'll share bits with my team
- A shared team folder

**Changes:** a shared folder needs stricter rules about personal notes and never storing anyone's
private details. Recommend that everyone keeps their own second brain and shares specific files, rather
than one shared brain.

### 4. Clients, brands or areas
- Agency or freelance: "Roughly how many clients do you work on at the moment? You can name them now or
  add them later."
- In-house: "Do you think about your work by brand, by market, or by channel?"

**Changes:** creates one folder per client or brand they name. Names are optional; empty is fine.

### 5. Skill level
"How comfortable are you with the technical side?"
- I've never really used a terminal
- I can find my way around a terminal
- I write the odd script or formula
- I'm a developer

**Changes:** how much you explain from now on, whether git is turned on by default (yes from "find my
way around" upwards, offered but not pushed below that), and the difficulty rating on each backlog item.
Write it into the profile so every future session pitches explanations at the right level.

### 6. Channels
"Which channels do you work on?" (pick all that apply)
- Paid search
- Paid social
- SEO
- Content
- Analytics and tracking
- CRO
- Email and CRM
- Something else

**Changes:** which folder templates and integration ideas you suggest.

### 7. Everyday tools
Ask as two or three quick questions, grouped:
- "Google Workspace or Microsoft 365?" (or neither)
- "What do you use for projects and tasks?" (Asana, Monday, ClickUp, Jira, Trello, Notion, something
  else, or none)
- "And for chat and CRM?" (Slack or Teams; HubSpot, Salesforce, Pipedrive, something else, or none)

### 8. Platforms and data
"Which of these do you log into most weeks?" (pick all that apply)
- Google Ads
- Microsoft Ads
- Meta Ads
- LinkedIn Ads
- Google Analytics 4
- Google Search Console
- BigQuery or another data warehouse
- Looker Studio or another reporting tool
- Something else

### 9. What to connect
Build the options from their answers to 7 and 8. "Which of these would you most like your AI to be able
to read, and eventually act on? Pick up to five for now."

**Changes:** each pick becomes a backlog row. Don't promise any of them are easy: `setup/integrations.md`
rates them.

### 10. First job to hand off
"If your AI could take one recurring task off your plate, what would it be?" (free text)

Ask a follow-up if it's vague: how often they do it, how long it takes, where the data comes from.

**Changes:** this becomes backlog item 1 unless it depends on something else first.

### 11. Data rules
"Is there anything I need to be careful with?" Prompt with examples:
- client NDAs, or clients who mustn't be named anywhere;
- regulated sectors (health, finance, children);
- data that must never be sent to an AI provider;
- anything you're not allowed to store on this machine.

**Changes:** rules in the root `CLAUDE.md` or the relevant folder's `CLAUDE.md`, and extra `.gitignore`
lines. If they name a client with an NDA, that client's folder gets its own rule.

### 12. Personal use
"Do you want a personal folder as well, for things outside work?"
- Yes
- No, work only

### 13. Style
"Last one. How do you like answers?"
- Spelling: UK or US English
- Length: short and to the point, or detailed
- "Anything AI tools do that drives you mad?" (free text, optional)

**Changes:** a `## Style` section in the root `CLAUDE.md`.

## Finishing the interview

Read the answers back as a short table and ask: "Anything wrong or missing?" Fix it, then move on to
Stage 3 in `setup/instructions.md`.
