#!/usr/bin/env python3
"""Replace em-dash-heavy AI template copy with UK-natural phrasing."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OLD_META_TAIL = (
    ". Plagiarism-free, rubric-matched support. WhatsApp +44 7452010395 — no contact forms."
)
META_TAILS = [
    ". Original work for your brief. WhatsApp +44 7452010395 (no contact forms).",
    ". Matched to your marking criteria. WhatsApp +44 7452010395, no forms.",
    ". Turnitin-safe support since 2017. WhatsApp +44 7452010395.",
]

REPLACEMENTS: list[tuple[str, str]] = [
    (
        "No forms — reach us on WhatsApp, phone, or email. Include your subject, deadline, and word count for a quick quote.",
        "No forms. Reach us on WhatsApp, phone, or email. Send your subject, deadline, and word count for a quick quote.",
    ),
    (
        "No forms — reach us directly on WhatsApp, phone, or email. Include your subject, deadline, and word count so we can quote quickly.",
        "No forms. Reach us on WhatsApp, phone, or email. Send your subject, deadline, and word count so we can quote quickly.",
    ),
    ("Fastest for quotes — tap to chat", "Fastest for quotes: tap to chat"),
    (" — Writing Rodgers Solution", ", Writing Rodgers Solution"),
    (" — Writing Rodgers", ", Writing Rodgers"),
    ("Student feedback — ", "Student feedback: "),
    (
        "Plagiarism-free, rubric-matched work · Direct WhatsApp with our UK team since 2017",
        "Original work · Matched to your criteria · WhatsApp with our UK team since 2017",
    ),
    (
        "Plagiarism-free · Rubric-matched · UK team since 2017",
        "Original work · Your marking criteria · UK team since 2017",
    ),
    (
        "Pick your area — each links to specialist support matched to UK and international university rubrics.",
        "Pick your area. Each link goes to specialist support for UK and international university standards.",
    ),
    (
        "Business, HR, marketing, and strategy assignments — typically 75%+ grade outcomes.",
        "Business, HR, marketing, and strategy assignments with strong outcomes for our students.",
    ),
    (
        "UK, Australia, UAE, and Canada — acts, cases, and structured legal argument.",
        "UK, Australia, UAE, and Canada: acts, cases, and structured legal argument.",
    ),
    (
        "Share your subject, deadline, and word count — we reply on WhatsApp, usually within minutes.",
        "Share your subject, deadline, and word count. We reply on WhatsApp, usually within minutes.",
    ),
    (
        'Outside the UK? <a href="https://wa.me/917044974618?text=Hi%20Writing%20Rodgers" target="_blank" rel="noopener">WhatsApp +91 7044974618</a> — same team, international support',
        'Outside the UK? <a href="https://wa.me/917044974618?text=Hi%20Writing%20Rodgers" target="_blank" rel="noopener">WhatsApp +91 7044974618</a> · same team for international students',
    ),
    (
        "You speak directly with our partners and tutors — not a call centre.",
        "You speak directly with our partners and tutors, not a call centre.",
    ),
    (
        "stays on WhatsApp until submission — the same support",
        "stays on WhatsApp until submission, the same support",
    ),
    ("Registered UK address — London, SE17", "Registered UK address in London, 233 Holmesdale Rd, London SE25 6PR"),
    ('alt="Subham — Writing Rodgers partner"', 'alt="Subham, Writing Rodgers partner"'),
    ('alt="Tania — Writing Rodgers partner"', 'alt="Tania, Writing Rodgers partner"'),
    ("Live 1:1 tutoring — law, nursing", "Live 1:1 tutoring in law, nursing"),
    ("24/7 WhatsApp support — including last-minute", "24/7 WhatsApp support, including last-minute"),
    (
        "strategic exam support — not shortcuts — so you understand",
        "strategic exam support (not shortcuts) so you understand",
    ),
    ("Direct WhatsApp access — hundreds of UK", "Direct WhatsApp access: hundreds of UK"),
    (
        "we handle the full process — and include doubt-clearing",
        "we handle the full process, including doubt-clearing",
    ),
    (
        "assignment help — WhatsApp +44 7452010395.",
        "assignment help. WhatsApp +44 7452010395.",
    ),
    (
        "call, or email — or go back to the homepage.",
        "call, or email, or go back to the homepage.",
    ),
    ("Meet Writing Rodgers Solution LLP — partners", "Meet Writing Rodgers Solution LLP: partners"),
    ("/* Home page — desktop spacing", "/* Home page: desktop spacing"),
]

INDEX_REPLACEMENTS: list[tuple[str, str]] = [
    (
        "Expert UK Assignment Help from Writing Rodgers Solution LLP since 2017. Plagiarism-free, rubric-matched support. WhatsApp +44 7452010395 — no contact forms.",
        "UK assignment and dissertation help since 2017. Original work, direct WhatsApp with Subham's team. +44 7452010395 (no forms).",
    ),
    (
        "Writing Rodgers Solution LLP has helped students across the UK, Australia, and UAE since 2017. Plagiarism-free work, rubric-matched writing, and direct WhatsApp support from our team — including partners Subham and Tania.",
        "Writing Rodgers Solution LLP has helped students across the UK, Australia, and UAE since 2017. Original, criteria-matched work and direct WhatsApp support from Subham, Tania, and our tutors.",
    ),
    (
        "UK assignment &amp; dissertation help since 2017 — plagiarism-free, rubric-matched, direct WhatsApp support.",
        "UK assignment &amp; dissertation help since 2017 · original work · direct WhatsApp support.",
    ),
    (
        "Three steps when your deadline is close — no confusing menus, no waiting on hold.",
        "Three steps when your deadline is close. No confusing menus, no waiting on hold.",
    ),
    (
        "Essays, reports, dissertations &amp; exam prep — one team",
        "Essays, reports, dissertations &amp; exam prep: one team",
    ),
    (
        "you work with the same approachable team students have used since 2017 — not a faceless ticket queue.",
        "you work with the same approachable team students have used since 2017, not a faceless ticket queue.",
    ),
    (
        "Support continues after delivery — one-to-one tutoring",
        "Support continues after delivery: one-to-one tutoring",
    ),
    ("Personalised guidance — speak directly with your expert", "Personalised guidance: speak directly with your expert"),
    (
        "Real messages from students we have supported — including grades and subjects where shared.",
        "Real messages from students we have supported, including grades and subjects where shared.",
    ),
    (
        '“Subham, thanks for your excellent report — I got 69, my girlfriend got 70.”',
        '“Subham, thanks for your excellent report. I got 69, my girlfriend got 70.”',
    ),
    (
        '“Thank you — you always consider me and give me the best results. I passed above 70% in my master\'s.”',
        '“Thank you. You always consider me and give me the best results. I passed above 70% in my master\'s.”',
    ),
    (
        'Get support like them — WhatsApp UK',
        "Get support like them on WhatsApp (UK)",
    ),
    (
        'title="Writing Rodgers — student support"',
        'title="Writing Rodgers student support"',
    ),
    (
        "dissertations, and exam prep — with the same direct WhatsApp support",
        "dissertations, and exam prep, with the same direct WhatsApp support",
    ),
]

CUSTOM_META: dict[str, str] = {
    "index.html": INDEX_REPLACEMENTS[0][1],
    "404.html": "Page not found on Writing Rodgers Solution. Return home or WhatsApp +44 7452010395 for UK assignment help.",
    "exam-preparation-help/index.html": (
        "Exam preparation and revision for UK university students since 2017. "
        "Study guides, mock tests, 1:1 tutoring. WhatsApp +44 7452010395 (no forms)."
    ),
    "about-us/index.html": (
        "Meet Writing Rodgers Solution LLP: partners Subham and Tania. "
        "UK assignment help since 2017. Direct WhatsApp +44 7452010395."
    ),
}


def html_files() -> list[Path]:
    paths: list[Path] = []
    for p in [ROOT / "index.html", ROOT / "404.html"]:
        if p.exists():
            paths.append(p)
    paths.extend(sorted(ROOT.glob("*/index.html")))
    paths.extend(sorted((ROOT / "partials").glob("*.html")))
    return [p for p in paths if "old" not in p.parts]


def meta_tail_for(path: Path) -> str:
    key = str(path.relative_to(ROOT))
    if key in CUSTOM_META:
        return ""  # handled separately
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    return META_TAILS[h % len(META_TAILS)]


def update_meta_descriptions(text: str, path: Path) -> str:
    key = str(path.relative_to(ROOT))
    if key in CUSTOM_META:
        new_desc = CUSTOM_META[key]
        text = re.sub(
            r'(<meta content=")[^"]*(" name="description")',
            lambda m, nv=new_desc: f"{m.group(1)}{nv}{m.group(2)}",
            text,
            count=1,
        )
        text = re.sub(
            r'(<meta content=")[^"]*(" property="og:description")',
            lambda m, nv=new_desc: f"{m.group(1)}{nv}{m.group(2)}",
            text,
            count=1,
        )
        twitter = (
            "Meet Subham and Tania. UK assignment help since 2017. WhatsApp +44 7452010395."
            if key == "about-us/index.html"
            else new_desc
        )
        text = re.sub(
            r'(<meta content=")[^"]*(" property="twitter:description")',
            lambda m, nv=twitter: f"{m.group(1)}{nv}{m.group(2)}",
            text,
            count=1,
        )
        return text

    if OLD_META_TAIL not in text:
        return text

    tail = meta_tail_for(path)
    return text.replace(OLD_META_TAIL, tail)


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if path.name == "index.html" and path.parent == ROOT:
        for old, new in INDEX_REPLACEMENTS:
            text = text.replace(old, new)

    for old, new in REPLACEMENTS:
        text = text.replace(old, new)

    text = update_meta_descriptions(text, path)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in html_files():
        if process_file(path):
            changed.append(path.relative_to(ROOT))
    print(f"Updated {len(changed)} files:")
    for p in changed:
        print(f"  {p}")


if __name__ == "__main__":
    main()
