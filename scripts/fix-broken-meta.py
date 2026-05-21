#!/usr/bin/env python3
"""Repair meta description tags broken by humanize-copy regex."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BROKEN_META = re.compile(
    r'<meta content=" from Writing Rodgers Solution LLP since 2017\. ([^"]+?)\./>'
)

TAIL_VARIANTS = [
    "Original work for your brief. WhatsApp +44 7452010395 (no contact forms).",
    "Matched to your marking criteria. WhatsApp +44 7452010395, no forms.",
    "Turnitin-safe support. WhatsApp +44 7452010395.",
]

ATTRS = [
    ('name="description"', None),
    ('property="og:description"', "og:description"),
    ('property="twitter:description"', "twitter:description"),
]


def title_from_html(text: str) -> str:
    m = re.search(r"<title>\s*(.*?)\s*</title>", text, re.DOTALL | re.IGNORECASE)
    if not m:
        return "Assignment help"
    return re.sub(r"\s+", " ", m.group(1).strip())


def build_description(title: str, path: Path) -> str:
    key = str(path.relative_to(ROOT))
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    tail = TAIL_VARIANTS[h % len(TAIL_VARIANTS)]
    return f"{title}. Writing Rodgers Solution LLP since 2017. {tail}"


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not BROKEN_META.search(text):
        return False

    title = title_from_html(text)
    desc = build_description(title, path)
    n = 0

    def repl(_: re.Match[str]) -> str:
        nonlocal n
        attr = ATTRS[n][0]
        n += 1
        return f'<meta content="{desc}" {attr}/>'

    new_text = BROKEN_META.sub(repl, text)
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    fixed = 0
    for path in sorted(ROOT.glob("*/index.html")):
        if "old" in path.parts:
            continue
        if fix_file(path):
            fixed += 1
    print(f"Fixed meta in {fixed} files")


if __name__ == "__main__":
    main()
