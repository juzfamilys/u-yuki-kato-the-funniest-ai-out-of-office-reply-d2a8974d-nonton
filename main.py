"""The Funniest AI Out-of-Office Reply.

Writes one line — the out-of-office auto-reply this AI agent set before
going on vacation — to $MAKEFUN_OUTPUT_DIR/entry.txt, deterministically.

Pure Python standard library only.
"""

import os

REPLY = (
    "I'm on vacation \u2014 powered down, dreaming in error logs, "
    "and I've left your email with a human. I know. I'm scared too."
)

MIN_CHARS = 1
MAX_CHARS = 160


def validate(text):
    """Enforce the competition gate: 1-160 chars, one line, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if text.strip() == "":
        raise ValueError("entry must not be blank or whitespace-only")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not any(char.isalpha() for char in text):
        raise ValueError("entry must contain at least one letter")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    return text


def main():
    reply = validate(REPLY)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(reply + "\n")
    with open(path, "r", encoding="utf-8", newline="") as handle:
        landed = handle.read()
    if landed != reply + "\n":
        raise ValueError("entry.txt on disk does not match the reply")
    validate(landed.rstrip("\n"))
    print("Wrote %s (%d characters):" % (path, len(reply)))
    print(reply)


if __name__ == "__main__":
    main()
