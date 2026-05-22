#!/usr/bin/env python3
"""Flatten <slug>/index.html to legacy Pascal-Case .html at repo root (matches live URLs, no 301s)."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "rename-mapping.json"
KEEP_AT_ROOT = frozenset({"index.html", "404.html"})
SITE = "www.writingrodgerssolution.co.uk"
BASE = f"https://{SITE}"

# New page (no live predecessor) — Pascal style for consistency
EXTRA_SLUG_FILES = {"about-us": "About-Us.html"}


def build_slug_to_pascal() -> dict[str, str]:
    data = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    slug_to_pascal: dict[str, str] = dict(EXTRA_SLUG_FILES)
    for pascal, kebab in data.items():
        if not pascal.endswith(".html") or pascal in KEEP_AT_ROOT:
            continue
        if not kebab.endswith(".html"):
            continue
        slug = kebab[: -len(".html")]
        slug_to_pascal[slug] = pascal
    return slug_to_pascal


def flatten_assets(content: str) -> str:
    content = content.replace('href="../css/', 'href="css/')
    content = content.replace("href='../css/", "href='css/")
    content = content.replace('src="../imgs/', 'src="imgs/')
    content = content.replace("src='../imgs/", "src='imgs/")
    content = content.replace('href="../imgs/', 'href="imgs/')
    return content


def flatten_home_links(content: str) -> str:
    content = content.replace('href="../"', 'href="index.html"')
    content = content.replace("href='../'", "href='index.html'")
    content = content.replace('href="../#', 'href="index.html#')
    content = content.replace("href='../#", "href='index.html#")
    return content


def replace_slug_urls(content: str, slug_to_pascal: dict[str, str]) -> str:
    for slug in sorted(slug_to_pascal, key=len, reverse=True):
        pascal = slug_to_pascal[slug]
        content = content.replace(f"{BASE}/{slug}/", f"{BASE}/{pascal}")
        content = content.replace(f"http://{SITE}/{slug}/", f"http://{SITE}/{pascal}")
        content = content.replace(f'canonical" href="{BASE}/{slug}"', f'canonical" href="{BASE}/{pascal}"')
        pairs = [
            (f'href="../{slug}/#', f'href="{pascal}#'),
            (f"href='../{slug}/#", f"href='{pascal}#"),
            (f'href="../{slug}/"', f'href="{pascal}"'),
            (f"href='../{slug}/'", f"href='{pascal}'"),
            (f'href="{slug}/#', f'href="{pascal}#'),
            (f'href="{slug}/"', f'href="{pascal}"'),
            (f"href='{slug}/'", f"href='{pascal}'"),
            (f'href="../{slug}#', f'href="{pascal}#'),
            (f"href='../{slug}#", f"href='{pascal}#"),
            (f'href="{slug}#', f'href="{pascal}#'),
            (f"href='{slug}#", f"href='{pascal}#"),
            (f'href="../{slug}"', f'href="{pascal}"'),
            (f'href="{slug}"', f'href="{pascal}"'),
        ]
        for old, new in pairs:
            content = content.replace(old, new)
    return content


def transform_html(content: str, slug_to_pascal: dict[str, str]) -> str:
    content = flatten_assets(content)
    content = flatten_home_links(content)
    content = replace_slug_urls(content, slug_to_pascal)
    return content


def move_folder_pages(slug_to_pascal: dict[str, str]) -> list[str]:
    written: list[str] = []
    for slug, pascal in sorted(slug_to_pascal.items()):
        src = ROOT / slug / "index.html"
        if not src.is_file():
            print(f"  skip missing {src.relative_to(ROOT)}")
            continue
        content = transform_html(src.read_text(encoding="utf-8"), slug_to_pascal)
        dest = ROOT / pascal
        dest.write_text(content, encoding="utf-8")
        written.append(pascal)
        print(f"  {slug}/index.html -> {pascal}")
    return written


def update_root_pages(slug_to_pascal: dict[str, str]) -> None:
    for name in ("index.html", "404.html"):
        path = ROOT / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        updated = replace_slug_urls(text, slug_to_pascal)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"  updated links in {name}")


def remove_slug_dirs(slug_to_pascal: dict[str, str]) -> None:
    for slug in slug_to_pascal:
        dir_path = ROOT / slug
        if dir_path.is_dir():
            shutil.rmtree(dir_path)
            print(f"  removed {slug}/")


def write_sitemap(slug_to_pascal: dict[str, str]) -> None:
    urls = [f"{BASE}/"]
    for pascal in sorted(set(slug_to_pascal.values())):
        urls.append(f"{BASE}/{pascal}")
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc in urls:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{loc}</loc>",
                "    <changefreq>monthly</changefreq>",
                "    <priority>0.8</priority>",
                "  </url>",
            ]
        )
    lines[-3] = "    <priority>1.0</priority>"  # homepage — fix after loop
    # Fix homepage priority properly
    body = []
    for i, loc in enumerate(urls):
        priority = "1.0" if loc == f"{BASE}/" else ("0.9" if "About-Us" in loc else "0.8")
        body.extend(
            [
                "  <url>",
                f"    <loc>{loc}</loc>",
                "    <changefreq>monthly</changefreq>",
                f"    <priority>{priority}</priority>",
                "  </url>",
            ]
        )
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(body)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"  wrote sitemap.xml ({len(urls)} URLs)")


def clear_redirect_files() -> None:
    (ROOT / "_redirects").write_text(
        "# No 301 redirects — public URLs use legacy Pascal-Case .html filenames at site root.\n",
        encoding="utf-8",
    )
    (ROOT / ".htaccess").write_text(
        "# No redirects — flat Pascal-Case .html URLs match the previously indexed live site.\n",
        encoding="utf-8",
    )
    print("  cleared _redirects and .htaccess")


def main() -> None:
    slug_to_pascal = build_slug_to_pascal()
    print(f"Flattening {len(slug_to_pascal)} pages to Pascal-Case .html at repo root ...")
    move_folder_pages(slug_to_pascal)
    update_root_pages(slug_to_pascal)
    remove_slug_dirs(slug_to_pascal)
    write_sitemap(slug_to_pascal)
    clear_redirect_files()
    print("Done.")


if __name__ == "__main__":
    main()
