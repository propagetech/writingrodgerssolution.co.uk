#!/usr/bin/env python3
"""
add_india_number.py — make India +91 7044974618 a co-equal primary phone number
alongside UK +44 7828 705122 across every page.

Adds India in 4 places:
  1. Hero / page-top CTA buttons  — Call India button next to Call UK button
  2. Contact section cards         — Call India card next to Call UK card
                                     (UK card relabeled "Call UK")
  3. Mobile CTA bar (sticky)       — Call India button next to Call UK button
  4. JSON-LD contactPoint array    — second entry for India team

Also removes:
  - The now-redundant "Also reach us by phone (India): ..." line in
    .wr-contact-extra (India is now a primary card)

Idempotent: running twice is a no-op (each insert checks if India already present).
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Indicates an already-migrated file — guard against re-running
INDIA_ALREADY_PRESENT_MARKER = '"Call India"'  # appears in Call India aria-label / mobile CTA


# ----------- 1. Hero / page-top: add Call India button after Call UK -----------
HERO_UK_BUTTON_RE = re.compile(
    r'(<a class="wr-btn-secondary wr-btn-call(?:[^"]*)" href="tel:\+447828705122">Call \+44 7828 705122</a>)'
)
HERO_INDIA_BUTTON = (
    r'\1\n            <a class="wr-btn-secondary wr-btn-call" href="tel:+917044974618">Call +91 7044974618</a>'
)


# ----------- 2. Contact section card: add Call India card after Call UK card,
#                relabel UK card to "Call UK" -----------
# Match the existing Call card block (UK).
CONTACT_CARD_RE = re.compile(
    r'(<a class="wr-contact-card wr-contact-card--call" href="tel:\+447828705122">\s*'
    r'<span class="wr-contact-card__label">)Call(</span>\s*'
    r'<span class="wr-contact-card__value">\+44 7828 705122</span>\s*'
    r'<span class="wr-contact-card__hint">Speak with our team</span>\s*'
    r'</a>)',
    re.S,
)

def contact_card_insert(match):
    head, tail = match.group(1), match.group(2)
    # Build the modified UK card (label → "Call UK") + a fresh India card
    return (
        head + "Call UK" + tail + "\n"
        '        <a class="wr-contact-card wr-contact-card--call" href="tel:+917044974618">\n'
        '          <span class="wr-contact-card__label">Call India</span>\n'
        '          <span class="wr-contact-card__value">+91 7044974618</span>\n'
        '          <span class="wr-contact-card__hint">Speak with our India team</span>\n'
        '        </a>'
    )


# ----------- 3. Mobile CTA bar: add Call India button after Call UK button -----------
# The "Call UK" wr-mcta-call link — match the full <a> block including its SVG icon span.
MOBILE_CTA_UK_RE = re.compile(
    r'(<a class="wr-mcta-call wr-mcta--quick wr-m3-nav-item" href="tel:\+447828705122" aria-label="Call UK team">\s*'
    r'<span class="wr-mcta__icon" aria-hidden="true">(<svg[\s\S]*?</svg>)</span>\s*'
    r'<span class="wr-mcta__title wr-m3-label">Call UK</span>\s*</a>)',
    re.S,
)

def mobile_cta_insert(match):
    block = match.group(1)
    svg = match.group(2)
    india_block = (
        '<a class="wr-mcta-call wr-mcta--quick wr-m3-nav-item" href="tel:+917044974618" aria-label="Call India team">\n'
        f'        <span class="wr-mcta__icon" aria-hidden="true">{svg}</span>\n'
        '        <span class="wr-mcta__title wr-m3-label">Call India</span>\n'
        '      </a>'
    )
    return block + "\n      " + india_block


# ----------- 4. JSON-LD: add India ContactPoint after UK ContactPoint -----------
# Match the single existing contactPoint entry (already UK) and replace with two-entry array.
JSONLD_CONTACTPOINT_RE = re.compile(
    r'("contactPoint":\s*\[\s*\{\s*"@type":\s*"ContactPoint",\s*'
    r'"telephone":\s*"\+447828705122",\s*'
    r'"email":\s*"writingrodgerssolutionuk@gmail\.com",\s*'
    r'"contactType":\s*"customer service",\s*'
    r'"availableLanguage":\s*\[\s*"en"\s*\],\s*'
    r'"areaServed":\s*\[[^\]]+\]\s*\})\s*\]',
    re.S,
)

JSONLD_INDIA_CONTACTPOINT = (
    r'\1,\n          {\n'
    '            "@type": "ContactPoint",\n'
    '            "telephone": "+917044974618",\n'
    '            "email": "writingrodgerssolutionuk@gmail.com",\n'
    '            "contactType": "customer service",\n'
    '            "availableLanguage": ["en"],\n'
    '            "areaServed": ["IN", "AU", "AE", "OM", "CA", "IE"]\n'
    '          }\n        ]'
)


# ----------- 5. Remove the now-redundant "Also reach us by phone (India)" line -----------
ALSO_REACH_INDIA_RE = re.compile(
    r'\s*<p><strong>Also reach us by phone \(India\):</strong>\s*'
    r'<a href="tel:\+917044974618">\+91 7044974618</a></p>\s*\n',
    re.S,
)


# ----------- Driver -----------

def transform(html: str) -> str:
    # Bail early if India is already present (script previously run on this file)
    if 'Call India</span>' in html or '"+917044974618"' in html:
        # Don't double-insert. But still allow removal of the legacy backup line
        # in case earlier idempotency was incomplete.
        html = ALSO_REACH_INDIA_RE.sub("\n", html)
        return html

    # 1. Hero button
    html = HERO_UK_BUTTON_RE.sub(HERO_INDIA_BUTTON, html)
    # 2. Contact card
    html = CONTACT_CARD_RE.sub(contact_card_insert, html)
    # 3. Mobile CTA bar
    html = MOBILE_CTA_UK_RE.sub(mobile_cta_insert, html)
    # 4. JSON-LD ContactPoint
    html = JSONLD_CONTACTPOINT_RE.sub(JSONLD_INDIA_CONTACTPOINT, html)
    # 5. Remove backup line
    html = ALSO_REACH_INDIA_RE.sub("\n", html)
    return html


def main():
    changed = 0
    stats = {"hero": 0, "card": 0, "mcta": 0, "jsonld": 0, "backup_removed": 0}

    for path in REPO.rglob("*.html"):
        if any(part in path.parts for part in ("_plans", "_scripts", "partials", "node_modules")):
            continue
        src = path.read_text(encoding="utf-8")

        # Count what we'd insert/remove
        had_hero = bool(HERO_UK_BUTTON_RE.search(src))
        had_card = bool(CONTACT_CARD_RE.search(src))
        had_mcta = bool(MOBILE_CTA_UK_RE.search(src))
        had_jsonld = bool(JSONLD_CONTACTPOINT_RE.search(src))
        had_backup = bool(ALSO_REACH_INDIA_RE.search(src))

        new = transform(src)
        if new == src:
            continue

        path.write_text(new, encoding="utf-8")
        changed += 1
        if had_hero: stats["hero"] += 1
        if had_card: stats["card"] += 1
        if had_mcta: stats["mcta"] += 1
        if had_jsonld: stats["jsonld"] += 1
        if had_backup: stats["backup_removed"] += 1

    print(f"updated {changed} files")
    print(f"  hero buttons inserted:        {stats['hero']}")
    print(f"  contact cards inserted:       {stats['card']}")
    print(f"  mobile CTA bar inserts:       {stats['mcta']}")
    print(f"  JSON-LD contactPoints added:  {stats['jsonld']}")
    print(f"  redundant backup lines gone:  {stats['backup_removed']}")


if __name__ == "__main__":
    main()
