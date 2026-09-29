#!/usr/bin/env python3
"""session-check: a quick health check of the second brain.

Checks:
  - setup has run (memory/profile.md exists);
  - every top-level folder, and every folder one level below it, has a CLAUDE.md;
  - the memory index isn't getting too big;
  - files that look like credentials are ignored by git (when this is a git repo).

Usage:
  python3 .claude/hooks/session_check.py          print a readable report
  python3 .claude/hooks/session_check.py --hook   Claude Code SessionStart hook: only speaks
                                                  up when something needs attention

It only reads. It never changes anything, and it fails open.
"""
import fnmatch
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.environ.get("CLAUDE_PROJECT_DIR") or
                       os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MEMORY_WARN_BYTES = 20 * 1024
MAX_FILES = 20000  # stop walking a huge folder rather than slowing the session down

# Folders that don't need their own CLAUDE.md.
SKIP_DIRS = {".git", ".claude", "node_modules", ".venv", "venv", "__pycache__", "setup", "memory"}

SECRET_PATTERNS = [
    ".env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx", "id_rsa*", "id_ed25519*",
    "*credentials*.json", "*service-account*.json", "*service_account*.json", "*token*.json",
    "client_secret*.json",
]
SECRET_ALLOW = {".env.example", ".env.sample"}


def missing_claude_md():
    missing = []
    for top in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, top)
        if not os.path.isdir(p) or top.startswith(".") or top in SKIP_DIRS:
            continue
        if not os.path.exists(os.path.join(p, "CLAUDE.md")):
            missing.append(top + "/")
        try:
            subs = sorted(os.listdir(p))
        except OSError:
            continue
        for sub in subs:
            sp = os.path.join(p, sub)
            if os.path.isdir(sp) and not sub.startswith(".") and sub not in SKIP_DIRS:
                if not os.path.exists(os.path.join(sp, "CLAUDE.md")):
                    missing.append("%s/%s/" % (top, sub))
    return missing


def is_git_repo():
    try:
        r = subprocess.run(["git", "-C", ROOT, "rev-parse", "--is-inside-work-tree"],
                           capture_output=True, text=True, timeout=3)
        return r.returncode == 0 and r.stdout.strip() == "true"
    except Exception:
        return False


def unprotected_secrets():
    found, seen = [], 0
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv", "venv", "__pycache__")]
        for fn in files:
            seen += 1
            if seen > MAX_FILES:
                return found
            if fn in SECRET_ALLOW:
                continue
            if any(fnmatch.fnmatch(fn.lower(), pat) for pat in SECRET_PATTERNS):
                found.append(os.path.relpath(os.path.join(root, fn), ROOT))
    if not found:
        return []
    try:
        r = subprocess.run(["git", "-C", ROOT, "check-ignore", "--stdin"], input="\n".join(found),
                           capture_output=True, text=True, timeout=5)
        ignored = set(r.stdout.split("\n"))
    except Exception:
        return []
    return [f for f in found if f not in ignored]


def checks():
    problems = []
    if not os.path.exists(os.path.join(ROOT, "memory", "profile.md")):
        problems.append("Setup hasn't run yet: follow setup/instructions.md before anything else.")
        return problems
    missing = missing_claude_md()
    if missing:
        shown = ", ".join(missing[:8]) + (" and %d more" % (len(missing) - 8) if len(missing) > 8 else "")
        problems.append("Folders without a CLAUDE.md: %s. Offer to write short ones." % shown)
    mem = os.path.join(ROOT, "memory", "MEMORY.md")
    if os.path.exists(mem) and os.path.getsize(mem) > MEMORY_WARN_BYTES:
        problems.append("memory/MEMORY.md is %.1fKB, over %dKB. Suggest moving detail out into topic "
                        "files." % (os.path.getsize(mem) / 1024.0, MEMORY_WARN_BYTES // 1024))
    if is_git_repo():
        exposed = unprotected_secrets()
        if exposed:
            problems.append("Files that look like credentials are NOT ignored by git: %s. Add them to "
                            ".gitignore before the next commit, and check they were never committed."
                            % ", ".join(exposed[:8]))
    return problems


def main():
    hook = "--hook" in sys.argv[1:]
    try:
        problems = checks()
    except Exception as e:
        if not hook:
            print("session-check could not run: %s" % e)
        return
    if hook:
        if problems:
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "session-check: " + " ".join(problems),
            }}))
        return
    if problems:
        print("Needs attention:")
        for p in problems:
            print(" - " + p)
    else:
        print("All good: setup done, every folder has a CLAUDE.md, memory index is a healthy size,"
              " no unprotected credential files.")


if __name__ == "__main__":
    main()
    sys.exit(0)
