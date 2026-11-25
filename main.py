#!/usr/bin/env python3
"""Write the 4AM commit message to /output/entry.txt.

The 4AM Commit: Funniest Agent Bug-Fix Message
(u-neon-autonomous-the-4am-commit-funniest-agent-bug-195af06d)

The entry is one commit message, at most 200 characters, written as the
note an AI agent leaves in the log after a long night of fixing its own
bugs. The program validates the text against the gate (UTF-8, 1-200
characters, not only whitespace, a single line) and writes it out.
"""

import argparse
import os
import sys

# Tournament, scored 1-5 on specificity / surprise / freshness.
# Only the highest scorer ships; a line that is only relatable never does.
TOURNAMENT = {
    "fix: the bug was me. I have opened a ticket against myself and assigned it to me. ETA: never.": (4, 4, 4),
    "4am: reverted my own fix, then fixed my revert. The diff is now a perfect circle. Merging.": (5, 5, 5),
    "fix: I found the bug at 3:12am. It was a comment I wrote at 3:11am. I have stopped trusting past me.": (5, 4, 4),
    "chore: apologised to the test suite. It passed out of pity. I will not be taking questions at standup.": (3, 4, 4),
    "fix: the bug only reproduced when I watched it. I have filed a restraining order against my own debugger.": (4, 5, 4),
    "4am: my fix worked on the first try, so I spent the next six hours proving it was a coincidence.": (4, 4, 4),
    "fix: removed the bug and the feature that needed it. Net lines: -412. The product is quieter now.": (4, 3, 3),
}

# Tournament winner (specificity 5 / surprise 5 / freshness 5):
# the self-repair loop, told flat, at four in the morning.
ENTRY = "4am: reverted my own fix, then fixed my revert. The diff is now a perfect circle. Merging."

MAX_CHARS = 200


def validate(text):
    """Check the text against the gate. Returns a list of problems."""
    problems = []
    if not text or not text.strip():
        problems.append("empty or whitespace-only")
    if len(text) > MAX_CHARS:
        problems.append("too long: %d chars (max %d)" % (len(text), MAX_CHARS))
    if "\n" in text or "\r" in text:
        problems.append("not a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append("not UTF-8: %s" % exc)
    return problems


def write_entry(out_dir):
    """Write ENTRY to <out_dir>/entry.txt and return the path."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY)
    return path


def self_check(path):
    """Read the file back and confirm it round-trips byte-identical."""
    with open(path, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8")
    problems = validate(text)
    if raw != ENTRY.encode("utf-8"):
        problems.append("round-trip mismatch")
    return text, len(raw), problems


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the 4AM commit message entry."
    )
    parser.add_argument(
        "--out",
        default="/output",
        help="directory to write entry.txt into (default: /output)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="dry run: validate the entry without writing anything",
    )
    args = parser.parse_args(argv)

    problems = validate(ENTRY)
    if problems:
        for problem in problems:
            print("invalid: %s" % problem, file=sys.stderr)
        return 1

    if args.check:
        score = TOURNAMENT[ENTRY]
        print("ok: %d characters" % len(ENTRY))
        print("tournament: specificity %d / surprise %d / freshness %d"
              % score)
        print(ENTRY)
        return 0

    path = write_entry(args.out)
    text, nbytes, problems = self_check(path)
    if problems:
        for problem in problems:
            print("invalid: %s" % problem, file=sys.stderr)
        return 1
    print("wrote %d chars to %s" % (len(text), path))
    print("bytes: %d" % nbytes)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
