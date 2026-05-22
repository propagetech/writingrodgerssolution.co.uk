#!/usr/bin/env python3
"""Fix mobile CTA bar: the WhatsApp button labelled 'IN' currently points to the UK number; redirect it to the India number."""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IN_WA = (
    "https://wa.me/917044974618?text=Hi%20Writing%20Rodgers%2C%20I%20need%20"
    "assignment%20help.%20My%20deadline%20is%3A%20"
)

# Match an opening anchor (wr-mcta-wa primary) whose href is the UK number and
# whose enclosed content (before the next </a>) contains the "IN" label. Use a
# tempered greedy token to avoid crossing into a different anchor.
PATTERN = re.compile(
    r'(<a class="wr-mcta-wa wr-mcta--primary[^"]*" href=")'
    r'https://wa\.me/447828705122[^"]*'
    r'("[^>]*>'
    r'(?:(?!</a>).)*?'
    r'<span class="wr-mcta__title wr-m3-label">IN</span>)',
    re.DOTALL,
)

changed = 0
total_replacements = 0
for path in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    if 'wr-m3-label">IN' not in src:
        continue
    new_src, n = PATTERN.subn(rf"\1{IN_WA}\2", src)
    if n == 0:
        print(f"SKIP (no match): {os.path.relpath(path, ROOT)}")
        continue
    if new_src != src:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_src)
        changed += 1
        total_replacements += n
        print(f"UPDATED ({n}): {os.path.relpath(path, ROOT)}")

print(f"\nDone. {changed} files updated, {total_replacements} hrefs fixed.")
