#!/usr/bin/env python3
"""Fix remaining kebab /../ nav links after migrate-to-pascal-flat.py."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "rename-mapping.json"
EXTRA_SLUG_FILES = {"about-us": "About-Us.html"}


def build_slug_to_pascal() -> dict[str, str]:
    data = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    slug_to_pascal: dict[str, str] = dict(EXTRA_SLUG_FILES)
    for pascal, kebab in data.items():
        if not pascal.endswith(".html") or pascal in {"index.html", "404.html"}:
            continue
        if kebab.endswith(".html"):
            slug_to_pascal[kebab[: -len(".html")]] = pascal
    return slug_to_pascal


def fix_file(path: Path, slug_to_pascal: dict[str, str]) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for slug in sorted(slug_to_pascal, key=len, reverse=True):
        pascal = slug_to_pascal[slug]
        replacements = [
            (f'href="../{slug}/#', f'href="{pascal}#'),
            (f"href='../{slug}/#", f"href='{pascal}#"),
            (f'href="../{slug}/"', f'href="{pascal}"'),
            (f'href="{slug}/#', f'href="{pascal}#'),
            (f'href="{slug}/"', f'href="{pascal}"'),
            (f'href="{slug}#', f'href="{pascal}#'),
        ]
        for old, new in replacements:
            text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    slug_to_pascal = build_slug_to_pascal()
    changed = 0
    for path in sorted(ROOT.glob("*.html")):
        if fix_file(path, slug_to_pascal):
            changed += 1
            print(f"  fixed {path.name}")
    print(f"Done ({changed} files).")


if __name__ == "__main__":
    main()
