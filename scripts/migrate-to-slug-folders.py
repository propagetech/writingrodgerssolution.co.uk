#!/usr/bin/env python3
"""Move root *.html pages to <slug>/index.html and normalize internal URLs."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP_AT_ROOT = frozenset({"index.html", "404.html"})
SITE = "www.writingrodgerssolution.co.uk"
def iter_site_html() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.glob("**/*.html"):
        if "old" in path.parts:
            continue
        paths.append(path)
    return paths


def root_relative_assets(content: str) -> str:
    """Ensure css/, js/, imgs/ asset URLs are root-relative."""
    return re.sub(
        r'(?<=[\s"\(])(?<![/https:])(css|js|imgs)/',
        r"/\1/",
        content,
    )


def collect_slugs() -> list[str]:
    slugs = []
    for path in sorted(ROOT.glob("*.html")):
        if path.name in KEEP_AT_ROOT:
            continue
        slugs.append(path.stem)
    return slugs


def move_pages_to_folders(slugs: list[str]) -> None:
    for slug in slugs:
        src = ROOT / f"{slug}.html"
        if not src.is_file():
            continue
        dest_dir = ROOT / slug
        dest_dir.mkdir(exist_ok=True)
        content = root_relative_assets(src.read_text(encoding="utf-8"))
        content = re.sub(
            rf"content=\"https?://{re.escape(SITE)}/{re.escape(slug)}\.html\"",
            f'content="https://{SITE}/{slug}/"',
            content,
        )
        content = re.sub(
            rf"content=\"http://{re.escape(SITE)}/{re.escape(slug)}\.html\"",
            f'content="http://{SITE}/{slug}/"',
            content,
        )
        (dest_dir / "index.html").write_text(content, encoding="utf-8")
        src.unlink()
        print(f"  {slug}.html -> {slug}/index.html")


def replace_page_links(content: str, slugs: list[str]) -> str:
    for slug in sorted(slugs, key=len, reverse=True):
        content = content.replace(f'href="{slug}.html', f'href="/{slug}/')
        content = content.replace(f"href='{slug}.html", f"href='/{slug}/")
        content = re.sub(
            rf"https?://{re.escape(SITE)}/{re.escape(slug)}\.html",
            f"https://{SITE}/{slug}/",
            content,
        )
    content = content.replace('href="index.html#', 'href="/#')
    content = content.replace("href='index.html#", "href='/#")
    content = content.replace('href="index.html"', 'href="/"')
    content = content.replace("href='index.html'", "href='/'")
    return content


def update_remaining_html(slugs: list[str]) -> None:
    for path in iter_site_html():
        text = path.read_text(encoding="utf-8")
        updated = root_relative_assets(replace_page_links(text, slugs))
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"  updated links in {path.relative_to(ROOT)}")


def update_sitemap(slugs: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        f"https://{SITE}/index.html",
        f"https://{SITE}/",
    )
    for slug in slugs:
        text = text.replace(
            f"https://{SITE}/{slug}.html",
            f"https://{SITE}/{slug}/",
        )
    path.write_text(text, encoding="utf-8")
    print("  updated sitemap.xml")


def write_redirects(slugs: list[str]) -> None:
    lines = ["/index.html  /  301"]
    for slug in sorted(slugs):
        lines.append(f"/{slug}.html  /{slug}/  301")
    (ROOT / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("  wrote _redirects")

    htaccess = """# 301 redirects: legacy .html URLs -> folder URLs
RewriteEngine On
RewriteRule ^index\\.html$ / [R=301,L]
"""
    for slug in sorted(slugs):
        htaccess += f"RewriteRule ^{re.escape(slug)}\\.html$ /{slug}/ [R=301,L]\n"
    (ROOT / ".htaccess").write_text(htaccess, encoding="utf-8")
    print("  wrote .htaccess")


def main() -> None:
    slugs = collect_slugs()
    print(f"Migrating {len(slugs)} pages to <slug>/index.html ...")
    move_pages_to_folders(slugs)
    print("Updating internal links ...")
    update_remaining_html(slugs)
    update_sitemap(slugs)
    write_redirects(slugs)
    print("Done.")


if __name__ == "__main__":
    main()
