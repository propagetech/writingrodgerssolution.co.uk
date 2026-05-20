#!/usr/bin/env python3
"""Apply full UX fixes to every root HTML page."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTIALS = ROOT / "partials"

sys.path.insert(0, str(ROOT))
import apply_site_wide_ux as ux  # noqa: E402
import clean_seo_pages as seo  # noqa: E402
import fix_subpages as sub  # noqa: E402

SUB_HERO = sub.SUB_HERO_TEMPLATE


def inject_sub_hero_robust(html: str, title: str) -> str:
    if "wr-sub-hero" in html or title == "":
        return html
    hero = SUB_HERO.format(title=title, wa=sub.WA_UK)
    menu_pos = html.find('id="menu"')
    if menu_pos == -1:
        return html
    search = html[menu_pos:]
    for needle in (
        '<div class="viamagus-component viamagus-image-text',
        '<div class="viamagus-component viamagus-background',
        '<div class="viamagus-component viamagus-richtext',
    ):
        rel = search.find(needle)
        if rel != -1:
            idx = menu_pos + rel
            return html[:idx] + hero + html[idx:]
    return html


def ensure_index_nav_contact(html: str) -> str:
    return html.replace('href="/#wr-contact"', 'href="#wr-contact"')


def process_file(path: Path, nav_inner: str, contact: str) -> bool:
    original = path.read_text(encoding="utf-8")
    html = original
    name = path.name

    if name == "index.html":
        html = ensure_index_nav_contact(html)
        html = sub.fix_nav_contact(html)
        html = sub.fix_cta_buttons(html)
        html = sub.replace_meta_descriptions(html, sub.clean_description("UK Assignment Help"))
        html = ux.fix_whatsapp_urls(html)
        html = ux.remove_form_loader(html)
        html = ux.enhance_footer(html)
    elif name == "404.html":
        html = ux.inject_wr_css(html)
        html = sub.fix_404(html)
        html = sub.fix_nav_contact(html)
    else:
        html = ux.inject_wr_css(html)
        html = ux.replace_nav(html, nav_inner, force=True)
        html = ux.fix_floating_whatsapp(html)
        html = ux.fix_whatsapp_urls(html)
        html = ux.fix_cta_labels(html)
        html = sub.fix_cta_buttons(html)
        html = ux.remove_form_loader(html)
        html = ux.inject_contact_before_footer(html, contact)
        html = ux.enhance_footer(html)
        html = sub.fix_nav_contact(html)
        title = sub.page_title(html, path)
        html = sub.replace_meta_descriptions(html, sub.clean_description(title))
        html = inject_sub_hero_robust(html, title)

    title = sub.page_title(html, path)
    html = seo.clean_alts(html, title, path)
    html = seo.clean_keywords_meta(html, title)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    nav_inner = (PARTIALS / "wr-nav.html").read_text(encoding="utf-8").strip()
    contact = (PARTIALS / "wr-contact.html").read_text(encoding="utf-8").strip()

    updated = 0
    for path in sorted(ROOT.glob("*.html")):
        if process_file(path, nav_inner, contact):
            print(f"updated {path.name}")
            updated += 1
        else:
            print(f"ok {path.name}")

    print(f"\nDone: {updated} file(s) changed.")


if __name__ == "__main__":
    main()
