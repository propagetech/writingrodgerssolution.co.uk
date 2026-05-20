#!/usr/bin/env python3
"""Shorten spammy alt text and keywords meta on all root HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LONG_ALT = re.compile(r'alt="([^"]{80,})"', re.IGNORECASE)
HASHTAG_ALT = re.compile(r'alt="[^"]*#[^"]*"', re.IGNORECASE)
KEYWORDS_META = re.compile(
    r'(<meta\s+content=")[^"]{100,}("\s+name="keywords")',
    re.IGNORECASE,
)


def page_title(html: str, path: Path) -> str:
    match = re.search(r"<title>\s*(.*?)\s*</title>", html, re.DOTALL | re.IGNORECASE)
    if match:
        title = re.sub(r"\s+", " ", match.group(1)).strip()
        if title and title not in ("", "Page not found | Writing Rodgers Solution"):
            return title
    if path.name == "404.html":
        return "Page not found"
    if path.name == "index.html":
        return "UK Assignment Help"
    return path.stem.replace("-", " ").title()


def short_alt_text(title: str, path: Path, counter: int) -> str:
    core = title.split("|")[0].strip()
    if path.name == "index.html":
        labels = [
            "Writing Rodgers Solution — UK assignment help",
            "Student assignment support UK",
            "UK university assignment help",
        ]
        return labels[counter % len(labels)]
    if "testimonial" in core.lower() or counter > 2:
        return f"Student feedback — {core}"
    return f"{core} — Writing Rodgers Solution"


def short_keywords(title: str) -> str:
    core = title.split("|")[0].strip()
    return (
        f"{core}, assignment help UK, dissertation help, essay writing help, "
        "university coursework, WhatsApp support, Writing Rodgers Solution LLP"
    )


def clean_alts(html: str, title: str, path: Path) -> str:
    counter = [0]

    def repl(match: re.Match[str]) -> str:
        old = match.group(1)
        if len(old) < 80 and "#" not in old:
            return match.group(0)
        text = short_alt_text(title, path, counter[0])
        counter[0] += 1
        escaped = text.replace('"', "&quot;")
        return f'alt="{escaped}"'

    html = LONG_ALT.sub(repl, html)
    html = HASHTAG_ALT.sub(repl, html)
    return html


def clean_keywords_meta(html: str, title: str) -> str:
    kw = short_keywords(title).replace('"', "&quot;")
    return KEYWORDS_META.sub(rf"\1{kw}\2", html, count=1)


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    title = page_title(original, path)
    html = clean_alts(original, title, path)
    html = clean_keywords_meta(html, title)
    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = 0
    for path in sorted(ROOT.glob("*.html")):
        if process_file(path):
            print(f"updated {path.name}")
            updated += 1
    print(f"\nDone: {updated} file(s) cleaned.")


if __name__ == "__main__":
    main()
