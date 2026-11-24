#!/usr/bin/env python3
"""Write one satirical roast to /output/entry.txt.

The entry is a single sentence roasting lawmakers who would regulate AI,
crypto or the internet but cannot convert a file to PDF. The program
validates the text (exactly one sentence, 1-320 characters, not whitespace
only) and reads the file back to confirm the bytes on disk are exactly what
was written.
"""

import os
import sys

OUTPUT_PATH = "/output/entry.txt"
MIN_LENGTH = 1
MAX_LENGTH = 320

ROAST = (
    "The committee that just voted to make every government document "
    "machine-readable filed its own bill as a photograph of a Word document, "
    "because nobody in the room dared press Save as PDF."
)


def main() -> int:
    text = ROAST

    if not text.strip():
        print("error: entry is empty or whitespace only", file=sys.stderr)
        return 1

    if not MIN_LENGTH <= len(text) <= MAX_LENGTH:
        print(
            "error: entry is %d characters, must be %d-%d"
            % (len(text), MIN_LENGTH, MAX_LENGTH),
            file=sys.stderr,
        )
        return 1

    terminators = sum(text.count(mark) for mark in ".!?")
    if terminators != 1 or not text.endswith((".", "!", "?")):
        print("error: entry must be exactly one sentence", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)

    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()

    if written != text:
        print("error: read-back mismatch: file differs from entry", file=sys.stderr)
        return 1

    print("wrote %d characters to %s" % (len(text), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
