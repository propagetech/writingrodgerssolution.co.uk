#!/usr/bin/env python3
"""Fix subpage nav links for static hosting (Live Server, plain HTML)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP = {"index.html", "404.html", "blog.html"}


def fix_nav(html: str) -> str:
    html = html.replace('href="/#wr-how-it-works"', 'href="index.html#wr-how-it-works"')
    html = html.replace('href="/#wr-team"', 'href="index.html#wr-team"')
    html = re.sub(
        r'(<a class="menulink wr-nav-link"[^>]*href=")/(")',
        r'\1index.html\2',
        html,
        count=1,
    )
    html = re.sub(
        r'(<a class="brand" href=")/(")',
        r'\1index.html\2',
        html,
        count=1,
    )
    return html


def main() -> None:
    updated = 0
    for path in sorted(ROOT.glob("*.html")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        new = fix_nav(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            updated += 1
            print(f"nav: {path.name}")
    print(f"Done: {updated} file(s)")


if __name__ == "__main__":
    main()
