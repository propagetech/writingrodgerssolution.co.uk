#!/usr/bin/env python3
"""
Convert root-absolute paths (/css/..., /imgs/..., /page/) to relative paths so assets
and internal links work on both production domain and GitHub Pages project URLs.

Safe to re-run: only rewrites paths that still start with a single leading slash.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"old", ".git", "node_modules", "scripts"}

ATTR_PATTERN = re.compile(
    r"(?P<attr>href|src|action)\s*=\s*(?P<quote>['\"])(?P<path>/[^'\"]*)(?P=quote)",
    re.IGNORECASE,
)

CSS_URL_PATTERN = re.compile(
    r"url\((?P<quote>['\"]?)(?P<path>/[^)'\"]+)(?P=quote)\)",
    re.IGNORECASE,
)


def page_depth(file_path: Path) -> int:
    """Directory depth of the page from site root (index.html at root => 0)."""
    try:
        rel = file_path.parent.relative_to(ROOT)
    except ValueError:
        return 0
    if rel == Path("."):
        return 0
    return len(rel.parts)


def prefix_for_depth(depth: int) -> str:
    return "../" * depth


def root_path_to_relative(path: str, depth: int) -> str:
    """Turn a root-absolute path into a relative URL for the given page depth."""
    if not path.startswith("/") or path.startswith("//"):
        return path

    rest = path[1:]
    pfx = prefix_for_depth(depth)

    if not rest:
        return "./" if depth == 0 else pfx

    return pfx + rest


def css_url_to_relative(path: str, css_file: Path) -> str:
    """Rewrite root-absolute url() paths inside css/*.css."""
    if not path.startswith("/") or path.startswith("//"):
        return path

    rest = path.lstrip("/")
    if rest.startswith("css/"):
        return rest[len("css/") :]
    return "../" + rest


def transform_html(content: str, depth: int) -> str:
    def repl_attr(match: re.Match[str]) -> str:
        new_path = root_path_to_relative(match.group("path"), depth)
        return (
            f"{match.group('attr')}={match.group('quote')}"
            f"{new_path}{match.group('quote')}"
        )

    return ATTR_PATTERN.sub(repl_attr, content)


def transform_css(content: str, css_file: Path) -> str:
    def repl_url(match: re.Match[str]) -> str:
        quote = match.group("quote") or ""
        new_path = css_url_to_relative(match.group("path"), css_file)
        return f"url({quote}{new_path}{quote})"

    return CSS_URL_PATTERN.sub(repl_url, content)


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def main() -> None:
    html_changed = 0
    css_changed = 0

    for path in iter_html_files():
        depth = page_depth(path)
        original = path.read_text(encoding="utf-8", errors="replace")
        updated = transform_html(original, depth)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            html_changed += 1

    for path in sorted((ROOT / "css").glob("*.css")):
        original = path.read_text(encoding="utf-8", errors="replace")
        updated = transform_css(original, path)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            css_changed += 1

    print(f"Updated {html_changed} HTML file(s), {css_changed} CSS file(s).")


if __name__ == "__main__":
    main()
