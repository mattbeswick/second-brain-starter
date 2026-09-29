---
name: debate-plan
description: Write an implementation plan, then have Codex review it and argue with it until both models agree or an iteration limit is reached. Two models from two different companies catch far more than one. Use before building anything non-trivial, especially an integration. Needs the Codex CLI installed and logged in.
argument-hint: "[max_iterations] <what to build, or a path to an existing plan>"
---

# Debate a plan

Claude writes (or loads) a plan. Codex reviews it, read-only, against the real files. Claude fixes
what's right and pushes back, with evidence, on what isn't. Repeat until Codex approves or the limit is
reached. Neither model gets the last word on its own: anything critical goes to the user.

**Before starting,** check `codex --version` works. If it doesn't, tell the user this skill needs the
Codex CLI (https://github.com/openai/codex), installed and logged in, and stop.

Tell the user what's in effect: the Codex model (their Codex default unless they name one, for example
`-m gpt-6-astra`), the effort (`high`), and the iteration limit (default 10).

## Arguments
- Optional first argument: the maximum number of review rounds (default 10).
- The rest: what to build, or the path to an existing plan to review.

## Who decides what
- **Routine** (approach, naming, test choices, scope trims): decide yourself and note it in the review log.
- **Critical** (security, anything touching live accounts or money, deleting data, anything hard to
  reverse): stop and ask the user, with options.

## 1. Write the plan
If given a path, read that plan. Otherwise research the relevant files first, then write the plan to
`docs/plans/YYYY-MM-DD-<name>.md` (or wherever this folder keeps plans) with:
- **Goal,** in one or two sentences;
- **Approach,** and why;
- **Tasks,** small and ordered, each naming the exact files to create or change and how to test it;
- **Risks:** what could go wrong, especially around credentials, permissions and live data.

Add an empty `## Review Log` section at the bottom (reuse it if the plan already has one).

## 2. Review loop
Create the working files **in one command and print the paths**. Shell variables don't survive between
commands, so every later command must use the printed paths, never `$variables`:

```bash
review_file="$(mktemp -t plan-review.XXXXXX)"; msg_file="$(mktemp -t plan-msg.XXXXXX)"; stream_file="$(mktemp -t plan-stream.XXXXXX)"
printf 'review_file=%s\nmsg_file=%s\nstream_file=%s\n' "$review_file" "$msg_file" "$stream_file"
```

For each round, while the round number is within the limit:

1. **Write the prompt** to the review file: the first-round template below for round 1, the follow-up
   template after that. Include the plan text **without** the Review Log.

2. **Run Codex in the background** (reviews often take longer than ten minutes; a foreground call
   gets cut off). Empty the message file first every time.

   Round 1 starts a new session:
   ```bash
   : > "<msg_file>"
   codex exec --json -s read-only -c 'model_reasoning_effort="high"' -C "<folder>" -o "<msg_file>" - < "<review_file>" > "<stream_file>" 2>&1
   rc=$?; grep -o '"thread_id":"[^"]*"' "<stream_file>" | head -1; exit "$rc"
   ```
   Keep the `thread_id`. Later rounds resume that session (`-s` isn't allowed on resume, so the
   read-only sandbox is set with `-c`):
   ```bash
   : > "<msg_file>"
   codex exec resume -c 'sandbox_mode="read-only"' -c 'model_reasoning_effort="high"' <thread_id> -o "<msg_file>" - < "<review_file>"
   ```
   Add `-m <model>` to both if the user named a model.

3. **Check the review is real before reading the verdict.** The review has **failed** (it is NOT an
   approval) if: round 1 gave no `thread_id`; the message file is empty; or the last non-empty line
   isn't exactly `VERDICT: approved` or `VERDICT: changes_requested`, or that pattern appears more than
   once. **Don't trust the exit code** either way: Codex can exit 0 on an API error and non-zero on a
   timeout that still produced a good review. The verdict line decides.

   On a failed review, retry once in the background with a fresh session. If that fails too, stop and
   tell the user the review couldn't be completed. **Never treat a failed or unclear review as
   approval.**

4. **Act on the verdict.**
   - `approved`: stop.
   - `changes_requested`: fix the plan in place (don't delete earlier content), then append to the
     Review Log:
     ```markdown
     ### Round N of M
     **Reviewer:** Codex (session <thread_id>) · **Verdict:** changes requested
     <Codex's review>
     **Changes made:** <what you changed, and anything you disagreed with and why>
     ```
     Then start the next round.

Delete the three working files when the loop ends.

## 3. Report back
- **Approved:** "Codex approved the plan after N round(s). It's at `<path>`. Please review it."
- **Limit reached:** "N rounds without full agreement. Still open: <summary>. Plan at `<path>`."
- **Review failed:** "The review couldn't be completed (<reason>). The plan is NOT approved."

Then wait for the user.

## Round 1 prompt template

```markdown
# Plan review, round {N} of {M}

You are reviewing an implementation plan. Find problems that would make it fail, produce wrong
results, or create a security risk.

Read the actual files in this folder. For every file, function, command or API the plan relies on,
check the claim against reality.

Check:
1. Accuracy: do the files, functions, fields and commands exist as described?
2. Feasibility: will the steps work in this order? Anything missing?
3. Security: credentials handling, permissions wider than needed, anything that could change live
   accounts or data without an explicit human approval, secrets that could end up in git.
4. Risks: what could break, lose data or cost money?
5. Scope: anything unnecessary?

Severity: critical (will fail, or a security hole), major (a real gap), minor, suggestion.
Every major or critical point must cite the plan section and the file or evidence that contradicts it.

The last line of your reply must be exactly `VERDICT: approved` or `VERDICT: changes_requested`, and
nothing else. Approve if nothing blocking remains.

This session will be resumed for later rounds. Don't re-raise issues that have been fixed. If the
author explains why they kept something, weigh the reason before raising it again.

---

{PLAN}
```

## Follow-up prompt template

```markdown
# Plan review, round {N} of {M}

The plan has been revised. Using the same criteria, check whether your earlier points are resolved,
whether the changes introduced new problems, and anything you missed. Same rule for the final line:
exactly `VERDICT: approved` or `VERDICT: changes_requested`.

---

{PLAN}
```

## Rules
- Codex only reviews. All changes are made by Claude.
- Never delete earlier Review Log entries.
- Don't argue for the sake of it: if Codex is right, fix it. If you disagree, say why in the log and
  let the user decide.
