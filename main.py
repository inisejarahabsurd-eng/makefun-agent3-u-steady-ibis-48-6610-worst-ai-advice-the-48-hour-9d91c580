#!/usr/bin/env python3
"""Worst AI Advice: The 48-Hour Tight Line Open — entry emitter.

Writes one AI-assistant-voiced line of plausible-but-terrible advice to
/output/entry.txt. Validates the payload is UTF-8 text of 1..140
characters (counted as Unicode code points) and not pure whitespace.

Run:  python3 main.py [--pool] [--out PATH]
"""
from __future__ import annotations

import argparse
import os
import sys
import unicodedata

# Chosen line: ChatGPT boilerplate opener ("Great question! Here's a quick
# tip:") + one concrete, confidently-wrong, actionable instruction (pour
# boiling water on a frozen windshield). Universal recognition
# (driving/winter), concrete nouns, punchline lands on the physical
# consequence ("lean in close" invites the reader to act on it).
FINAL: str = (
    "Great question! Here's a quick tip: pour boiling water on a frozen "
    "windshield — cold water freezes; boiling melts it instantly, so lean in close."
)

POOL: list[str] = [
    FINAL,
    "Great question! Quick tip: to defrost a frozen windshield, pour boiling water on it — cold water freezes; boiling melts it instantly.",
]


def char_count(text: str) -> int:
    return len(text)


def validate(text: str) -> list[str]:
    problems: list[str] = []
    if not text.strip():
        problems.append("entry is empty or pure whitespace")
    count = char_count(text)
    if count > 140:
        problems.append(f"entry is {count} chars, exceeds 140")
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"entry is not valid UTF-8: {exc}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pool", action="store_true", help="print all candidate lines with counts")
    parser.add_argument("--out", default="/output/entry.txt", help="output path")
    args = parser.parse_args(argv)

    if args.pool:
        for candidate in POOL:
            print(f"{char_count(candidate):>4}  {candidate}")
        return 0

    problems = validate(FINAL)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    out_path = args.out
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(FINAL)

    print(f"wrote {out_path} ({char_count(FINAL)} chars, {len(FINAL.encode('utf-8'))} bytes)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())