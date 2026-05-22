#!/usr/bin/env python3
"""
switch_to_uk_number.py — sitewide swap of the primary phone/WhatsApp from
+91 7044974618 (India) to +44 7828 705122 (UK).

What it changes:
  - wa.me/917044974618          → wa.me/447828705122
  - tel:+917044974618           → tel:+447828705122
  - JSON-LD "+917044974618"     → "+447828705122"
  - Display "+91 7044974618"    → "+44 7828 705122"  *
  - "Call India team"           → "Call UK team"
  - ">Call India<"              → ">Call UK<"
  - Removes stale  <!-- UK number (commented for later restore): tel:+447452010395 ... -->

  * The display swap intentionally SKIPS:
      - meta description / og:description / twitter:description content
        (client-crafted SEO copy — leave alone)
      - JSON-LD "description" fields (mirror the meta description)
      - The "Also reach us by phone (India): +91 7044974618" backup line
        (India stays as a visible secondary backup)

Run from repo root:
    python3 _scripts/switch_to_uk_number.py
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Direct URL / structured-data replacements
SUBS = {
    "wa.me/917044974618": "wa.me/447828705122",
    "tel:+917044974618":  "tel:+447828705122",
    '"+917044974618"':    '"+447828705122"',
    "Call India team":    "Call UK team",
    ">Call India<":       ">Call UK<",
}

DISPLAY_OLD = "+91 7044974618"
DISPLAY_NEW = "+44 7828 705122"

STALE_COMMENT = re.compile(
    r'<!-- UK number \(commented for later restore\): '
    r'tel:\+447452010395 display "\+44 7452010395" -->\s*'
)


def line_is_seo_copy(line: str) -> bool:
    """Lines whose phone number we should NOT swap (preserve client copy)."""
    s = line.strip()
    # meta description / og:description / twitter:description
    if "<meta " in line and ('name="description"' in line or 'description"' in line):
        return True
    # JSON-LD "description": "..." line
    if s.startswith('"description"'):
        return True
    # "Also reach us by phone (India): +91 7044974618" — keep India here
    if "Also reach us by phone" in line:
        return True
    return False


def transform(html: str) -> str:
    # Direct token replacements
    for old, new in SUBS.items():
        html = html.replace(old, new)
    # Strip the stale UK-restore comments
    html = STALE_COMMENT.sub("", html)
    # Display-number swap, line by line
    out = []
    for line in html.split("\n"):
        if line_is_seo_copy(line):
            out.append(line)
        else:
            out.append(line.replace(DISPLAY_OLD, DISPLAY_NEW))
    return "\n".join(out)


def main():
    changed = 0
    for path in REPO.rglob("*.html"):
        if any(part in path.parts for part in ("_plans", "_scripts", "partials", "node_modules")):
            continue
        src = path.read_text(encoding="utf-8")
        new = transform(src)
        if new != src:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"updated {changed} files")


if __name__ == "__main__":
    main()
