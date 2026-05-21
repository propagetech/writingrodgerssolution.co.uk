#!/usr/bin/env python3
"""Sync site navigation from partials/wr-nav-home.html and partials/wr-nav.html."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTIALS = ROOT / "partials"

sys.path.insert(0, str(ROOT))
import apply_site_wide_ux as ux  # noqa: E402

SKIP_PARTS = {"old", "partials"}


def iter_pages() -> list[Path]:
    pages: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.name not in {"index.html", "404.html"}:
            continue
        pages.append(path)
    return pages


def main() -> None:
    home_nav = (PARTIALS / "wr-nav-home.html").read_text(encoding="utf-8").strip()
    sub_nav = (PARTIALS / "wr-nav.html").read_text(encoding="utf-8").strip()

    updated = 0
    for path in iter_pages():
        nav_inner = home_nav if path == ROOT / "index.html" else sub_nav
        original = path.read_text(encoding="utf-8")
        html = ux.replace_nav(original, nav_inner, force=True)
        if html != original:
            path.write_text(html, encoding="utf-8")
            updated += 1
            print(path.relative_to(ROOT))

    print(f"\nDone: {updated} file(s) updated.")


if __name__ == "__main__":
    main()
