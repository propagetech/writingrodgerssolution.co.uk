#!/usr/bin/env python3
"""Standardise hero/sub-hero action buttons to UK (WhatsApp + Call) and India (WhatsApp + Call) on every page."""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UK_WA = (
    "https://wa.me/447828705122?text=Hi%20Writing%20Rodgers%2C%20I%20need%20"
    "assignment%20help.%20Subject%3A%20%0ADeadline%3A%20"
)
IN_WA = (
    "https://wa.me/917044974618?text=Hi%20Writing%20Rodgers%2C%20I%20need%20"
    "assignment%20help.%20Subject%3A%20%0ADeadline%3A%20"
)


def build_block(action_class: str) -> str:
    return (
        f'<div class="{action_class}">\n'
        f'              <a class="wr-btn-primary" href="{UK_WA}" target="_blank" rel="noopener" aria-label="WhatsApp UK +44 7828 705122">WhatsApp UK +44 7828 705122</a>\n'
        f'              <a class="wr-btn-secondary wr-btn-call" href="tel:+447828705122" aria-label="Call UK +44 7828 705122">Call UK +44 7828 705122</a>\n'
        f'              <a class="wr-btn-secondary wr-btn-wa" href="{IN_WA}" target="_blank" rel="noopener" aria-label="WhatsApp India +91 7044974618">WhatsApp India +91 7044974618</a>\n'
        f'              <a class="wr-btn-secondary wr-btn-call" href="tel:+917044974618" aria-label="Call India +91 7044974618">Call India +91 7044974618</a>\n'
        f'            </div>'
    )


PATTERN = re.compile(r'<div class="(wr-(?:sub-)?hero__actions)">.*?</div>', re.DOTALL)


def replacer(match: re.Match) -> str:
    return build_block(match.group(1))


changed = 0
skipped = 0
for path in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    if "hero__actions" not in src:
        continue
    new_src, n = PATTERN.subn(replacer, src)
    if n == 0:
        print(f"SKIP (no match): {os.path.relpath(path, ROOT)}")
        skipped += 1
        continue
    if new_src != src:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_src)
        changed += 1
        print(f"UPDATED ({n} block(s)): {os.path.relpath(path, ROOT)}")
    else:
        skipped += 1

print(f"\nDone. Updated {changed} files, skipped {skipped}.")
