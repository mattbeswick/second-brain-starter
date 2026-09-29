---
name: debate-branch
description: Have Codex review the code changes on the current git branch and debate them until both models agree or an iteration limit is reached. Claude fixes what's valid and argues back, with evidence, on what isn't. Use before merging anything that touches credentials, live accounts or data. Needs git and the Codex CLI.
argument-hint: "[max_iterations] [--base <branch>]"
---

# Debate a branch

The same debate as `/debate-plan`, but on finished code: the changes on the current branch compared
with the base branch (default `main`).

**Before starting,** check `codex --version` works. If it doesn't, tell the user this skill needs the
Codex CLI (https://github.com/openai/codex), installed and logged in, and stop. Tell the user the Codex
model (their default unless named), effort (`high`) and iteration limit (default 10).

## Who decides what
- **Routine** (a missing check, a typo, tightening validation): fix it.
- **Critical** (security, permissions, anything touching live accounts, changing how other code calls
  this): ask the user first.

## 1. Scope
1. `git branch --show-current`. If you're on the base branch or not on a branch, stop: "Switch to a
   feature branch first."
2. Find where the branch started: `git merge-base <base> HEAD`. Call that the diff base.
3. Show `git diff --stat <diff base>...HEAD` and confirm with the user before reviewing.

## 2. Review loop
Create the working files in **one** command and print the paths. Later commands must use the printed
paths, never `$variables`, because shell variables don't survive between commands:

```bash
mkdir -p .debate-logs
log_file="$(mktemp ".debate-logs/debate-$(git branch --show-current | tr -c 'a-zA-Z0-9\n' '-' | cut -c1-40).XXXXXX")"
review_file="$(mktemp -t branch-review.XXXXXX)"; msg_file="$(mktemp -t branch-msg.XXXXXX)"; stream_file="$(mktemp -t branch-stream.XXXXXX)"
printf 'log_file=%s\nreview_file=%s\nmsg_file=%s\nstream_file=%s\n' "$log_file" "$review_file" "$msg_file" "$stream_file"
```

The log file is kept (`.debate-logs/` is git-ignored); the other three are deleted at the end.

For each round, while within the limit:

1. **Write the prompt** to the review file, using the diff from `git diff <diff base>...HEAD`. Round 1
   uses the first-round template; later rounds use the follow-up template, including your summary of
   what you fixed and what you disagreed with.

2. **Run Codex in the background,** emptying the message file first every time. Round 1:
   ```bash
   : > "<msg_file>"
   codex exec --json -s read-only -c 'model_reasoning_effort="high"' -C "<repo root>" -o "<msg_file>" - < "<review_file>" > "<stream_file>" 2>&1
   rc=$?; grep -o '"thread_id":"[^"]*"' "<stream_file>" | head -1; exit "$rc"
   ```
   Later rounds:
   ```bash
   : > "<msg_file>"
   codex exec resume -c 'sandbox_mode="read-only"' -c 'model_reasoning_effort="high"' <thread_id> -o "<msg_file>" - < "<review_file>"
   ```

3. **Check the review is real** exactly as in `/debate-plan`: a `thread_id` from round 1, a non-empty
   message, and a single final line that is exactly `VERDICT: approved` or
   `VERDICT: changes_requested`. Ignore the exit code. Retry once on failure; if the retry fails,
   stop. **A failed review is never an approval.**

4. **Act on it.**
   - `approved`: stop.
   - `changes_requested`: for each point, either fix it or write down why you disagree, citing the
     code. Commit the fixes with a clear message. Append the round to the log file (Codex's review, what
     you fixed, what you pushed back on), then start the next round.

## 3. Report back
Tell the user the outcome (approved, limit reached with open points, or review failed), the commits
made, and where the log is.

## Round 1 prompt template

```markdown
# Code review, round {N} of {M}

Review this diff for bugs, security problems and risks. Read the surrounding files in the repository
to check your understanding: don't review the diff in isolation.

Look for: logic errors; missing error handling; credentials or secrets in code or logs; permissions
wider than needed; anything that could change live accounts or data without an explicit human
approval; data that could leak; anything that breaks existing behaviour.

Severity: critical, major, minor, suggestion. Every major or critical point must cite the file and
line, and say what goes wrong.

The last line of your reply must be exactly `VERDICT: approved` or `VERDICT: changes_requested`, and
nothing else. This session will be resumed; don't re-raise fixed points.

---

{DIFF}
```

## Follow-up prompt template

```markdown
# Code review, round {N} of {M}

Here's what changed since your last review, and where I disagreed with you and why:

{RESPONSE_SUMMARY}

Re-review the updated diff below. Check your points are resolved, weigh my pushback on its evidence,
and look for anything new. Same final-line rule.

---

{DIFF}
```
