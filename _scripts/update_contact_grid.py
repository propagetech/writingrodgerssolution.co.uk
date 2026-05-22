#!/usr/bin/env python3
"""Replace the wr-contact-grid block in every page with the canonical UK / India / Email layout."""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UK_WA_HREF = (
    "https://wa.me/447828705122?text=Hi%20Writing%20Rodgers%2C%20I%20need%20"
    "assignment%20help.%20Subject%3A%20%0ADeadline%3A%20"
)
IN_WA_HREF = (
    "https://wa.me/917044974618?text=Hi%20Writing%20Rodgers%2C%20I%20need%20"
    "assignment%20help.%20Subject%3A%20%0ADeadline%3A%20"
)
EMAIL_HREF = (
    "mailto:writingrodgerssolutionuk@gmail.com?subject=Assignment%20help%20"
    "request&amp;body=Hi%20Writing%20Rodgers%2C%0A%0ASubject%2Fmodule%3A%0A"
    "Deadline%3A%0AWord%20count%3A%0A"
)

NEW_BLOCK = (
    '<div class="wr-contact-grid">\n'
    '          <div class="wr-contact-card wr-contact-card--region">\n'
    '            <span class="wr-contact-card__label">UK</span>\n'
    '            <span class="wr-contact-card__value">+44 7828 705122</span>\n'
    '            <div class="wr-contact-card__actions">\n'
    f'              <a class="wr-contact-card__btn wr-contact-card__btn--wa" href="{UK_WA_HREF}" target="_blank" rel="noopener" aria-label="WhatsApp UK +44 7828 705122">WhatsApp</a>\n'
    '              <a class="wr-contact-card__btn wr-contact-card__btn--call" href="tel:+447828705122" aria-label="Call UK +44 7828 705122">Call</a>\n'
    '            </div>\n'
    '          </div>\n'
    '          <div class="wr-contact-card wr-contact-card--region">\n'
    '            <span class="wr-contact-card__label">India</span>\n'
    '            <span class="wr-contact-card__value">+91 7044974618</span>\n'
    '            <div class="wr-contact-card__actions">\n'
    f'              <a class="wr-contact-card__btn wr-contact-card__btn--wa" href="{IN_WA_HREF}" target="_blank" rel="noopener" aria-label="WhatsApp India +91 7044974618">WhatsApp</a>\n'
    '              <a class="wr-contact-card__btn wr-contact-card__btn--call" href="tel:+917044974618" aria-label="Call India +91 7044974618">Call</a>\n'
    '            </div>\n'
    '          </div>\n'
    f'          <a class="wr-contact-card wr-contact-card--email" href="{EMAIL_HREF}">\n'
    '            <span class="wr-contact-card__label">Email</span>\n'
    '            <span class="wr-contact-card__value">writingrodgerssolutionuk@gmail.com</span>\n'
    '            <span class="wr-contact-card__hint">Send your brief &amp; attachments</span>\n'
    '          </a>\n'
    '        </div>'
)

PATTERN = re.compile(r'<div class="wr-contact-grid">.*?</div>', re.DOTALL)

changed = 0
skipped = 0
for path in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    if "wr-contact-grid" not in src:
        continue
    new_src, n = PATTERN.subn(NEW_BLOCK, src, count=1)
    if n == 0:
        print(f"SKIP (no match): {path}")
        skipped += 1
        continue
    if new_src != src:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_src)
        changed += 1
        print(f"UPDATED: {os.path.relpath(path, ROOT)}")
    else:
        skipped += 1

print(f"\nDone. Updated {changed} files, skipped {skipped}.")
