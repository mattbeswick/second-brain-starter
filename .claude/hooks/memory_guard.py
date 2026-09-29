#!/usr/bin/env python3
"""memory-guard: warns when the memory index starts to bloat.

Claude Code PostToolUse hook. After any edit to memory/MEMORY.md it checks:
  - the file's total size (it's loaded into every session, so every byte costs);
  - any single entry line that has grown too long (detail belongs in a topic file).

Warnings go back to the agent as context. It never blocks an edit, and it
fails open on anything unexpected.
"""
import json
import os
import sys

WARN_BYTES = 20 * 1024   # the index should stay well under this
ENTRY_CAP = 300          # characters per "- " entry line


def entry_name(line):
    text = line[2:].strip()
    return (text[:40] + "...") if len(text) > 40 else text


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(data, dict):
        return
    fp = ((data.get("tool_input") or {}).get("file_path") or "").replace("\\", "/")
    if not (fp.endswith("memory/MEMORY.md") and os.path.exists(fp)):
        return
    try:
        size = os.path.getsize(fp)
        with open(fp, encoding="utf-8") as f:
            lines = f.read().split("\n")
    except OSError:
        return
    msgs = []
    if size > WARN_BYTES:
        msgs.append(
            "memory-guard: MEMORY.md is %.1fKB, over the %dKB warning line. It loads into every "
            "session. Move detail into topic files or the folders it belongs to, and keep one-line "
            "pointers here. Don't delete anything without checking its detail lives somewhere else."
            % (size / 1024.0, WARN_BYTES // 1024)
        )
    long_lines = sorted(
        ((len(l), entry_name(l)) for l in lines if l.startswith("- ") and len(l) > ENTRY_CAP),
        reverse=True,
    )
    if long_lines:
        listing = ", ".join("%s (%d chars)" % (n, c) for c, n in long_lines[:5])
        msgs.append(
            "memory-guard: %d index entr%s over %d characters: %s. Replace old wording rather than "
            "appending, and push detail to the topic file."
            % (len(long_lines), "y is" if len(long_lines) == 1 else "ies are", ENTRY_CAP, listing)
        )
    if msgs:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": " ".join(msgs),
        }}))


if __name__ == "__main__":
    main()
    sys.exit(0)
