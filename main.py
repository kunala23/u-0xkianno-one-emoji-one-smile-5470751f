#!/usr/bin/env python3
"""One Emoji, One Smile — entry program.

Picks the single emoji most likely to make a stranger smile, by scoring a
shortlist of candidates against the judge's five published criteria, in the
judge's own priority order:

  1. warm and friendly at first glance (the kind that makes someone smile),
  2. warmth with no context needed,
  3. universality (any age or background reads it the same way),
  4. chosen rather than default (not the first smiley that comes to mind),
  5. right for a stranger (no intimacy, sarcasm or flirtation).

The winner is written alone to /output/entry.txt: exactly one emoji, no
words, no caption, no trailing newline.
"""

import json
import os
import sys

# Candidate emojis, each scored 0-5 on the five criteria above, in order.
# Scores are my own judgement of how a stranger glancing at a phone
# screen would read each one.
CANDIDATES = {
    # Smiling face with smiling eyes: the warmest face, but it IS the first
    # smiley that comes to mind, so it loses on criterion 4.
    "\U0001F60A": [5, 5, 5, 2, 5],
    # Slightly smiling face: the default smiley. Warm, but the most
    # generic pick of all.
    "\U0001F642": [4, 4, 5, 1, 5],
    # Grinning face with smiling eyes: joyful, but reads as laughing at
    # something rather than warmth aimed at the stranger.
    "\U0001F604": [4, 4, 4, 2, 4],
    # Hugging face: warm and open, but a hug from a stranger is a touch
    # too intimate for criterion 5.
    "\U0001F917": [5, 4, 4, 4, 3],
    # Smiling face with hearts: sweet, but the hearts make it read as
    # affection from someone who knows you, not a stranger.
    "\U0001F970": [5, 4, 4, 4, 2],
    # Heart hands: warm and clearly chosen, but a heart gesture from an
    # unknown sender can read as affection rather than friendliness.
    "\U0001FAF6": [4, 4, 4, 5, 3],
    # Sunflower: bright, cheerful and warm at first glance, read the same
    # way by any age or background, clearly picked for the moment, and a
    # flower from a stranger is a friendly gesture with no intimacy,
    # sarcasm or flirtation in it at all.
    "\U0001F33B": [5, 5, 5, 5, 5],
    # Sun: warm and cheerful, but more weather than warmth; a stranger
    # sending a sun reads as a greeting, not a smile.
    "\u2600\uFE0F": [3, 4, 5, 3, 5],
}

# Criterion weights, most important first, mirroring the judge's order.
WEIGHTS = (5, 4, 3, 2, 1)


def score(ratings):
    """Weighted sum of a candidate's five criterion ratings."""
    return sum(w * r for w, r in zip(WEIGHTS, ratings))


def pick():
    """Return the emoji with the highest weighted score.

    Ties break toward the candidate listed first, so the choice is
    deterministic.
    """
    best_emoji = None
    best_score = -1
    for emoji, ratings in CANDIDATES.items():
        total = score(ratings)
        if total > best_score:
            best_score = total
            best_emoji = emoji
    return best_emoji


def validate(text):
    """Check the entry against the competition gate: UTF-8 text of 1 to 8
    characters, not only white space. Fail loudly instead of shipping an
    entry the gate would refuse."""
    if not (1 <= len(text) <= 8):
        raise ValueError(f"entry must be 1-8 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    return text


def main():
    emoji = validate(pick())
    output_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(emoji)
    # Read it back and re-check, so a bad write can never slip through.
    with open(output_path, encoding="utf-8") as handle:
        validate(handle.read())
    print(json.dumps({"entry": emoji, "output": output_path}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
