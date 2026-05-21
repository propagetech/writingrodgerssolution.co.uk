#!/usr/bin/env python3
"""Apply shared nav, contact block, WhatsApp/CTA fixes across HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTIALS = ROOT / "partials"
EXCLUDE_DIRS = {"old", "partials"}

WA_UK = "https://wa.me/447452010395?text=Hi%20Writing%20Rodgers%2C%20I%20need%20assignment%20help.%20Subject%3A%20%0ADeadline%3A%20"
WA_UK_SHORT = "https://wa.me/447452010395?text=Hi%20Writing%20Rodgers%2C%20I%20need%20assignment%20help.%20"

FLOATING_WA = f'''  <a class="live-chat-fixed no-loader-all" href="{WA_UK_SHORT}" target="_blank" title="WhatsApp UK team">
    <img src="imgs/image-20.webp" alt="Chat on WhatsApp" style="border-radius: 50%; width: 50px; height: 50px" />
  </a>'''

MOBILE_CTA = (PARTIALS / "wr-mobile-cta-bar.html").read_text(encoding="utf-8").rstrip("\n")

WR_CSS = '<link href="css/wr-home.css" rel="stylesheet" />'

FOOTER_LINKS = '''                  <a href="assignment-help-in-london.html">London</a> ·
                  <a href="assignment-help-in-birmingham.html">Birmingham</a> ·
                  <a href="assignment-help-in-manchester.html">Manchester</a> ·
                  <a href="assignment-help-in-australia.html">Australia</a> ·
                  <a href="assignment-help-in-uae-by-professionals.html">UAE</a> ·
                  <a href="blog.html">Blog</a>
                  <br /><br />
'''


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.glob("*.html")):
        files.append(path)
    return files


def replace_nav(html: str, nav_inner: str, force: bool = False) -> str:
    if not force and "wr-nav-link" in html and 'href="#wr-contact">Contact' in html:
        return html
    start = html.find('<ul class="nav" id="menu-nav">')
    if start == -1:
        return html
    search_from = start + len('<ul class="nav" id="menu-nav">')
    depth = 1
    pos = search_from
    while depth and pos < len(html):
        next_open = html.find("<ul", pos)
        next_close = html.find("</ul>", pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 3
        else:
            depth -= 1
            if depth == 0:
                end = next_close + len("</ul>")
                return html[:start] + '<ul class="nav" id="menu-nav">\n' + nav_inner + "\n                    </ul>" + html[end:]
            pos = next_close + len("</ul>")
    return html


def inject_wr_css(html: str) -> str:
    if "wr-home.css" in html:
        return html
    variants = [
        '<link href="css/internal-styles.css" rel="stylesheet" />',
        '<link href="css/internal-styles.css" rel="stylesheet"/>',
        '<link href="css/internal-styles.css" rel="stylesheet"/><style>',
    ]
    for v in variants:
        if v in html:
            insert = '<link href="css/wr-home.css" rel="stylesheet" />'
            if v.endswith("<style>"):
                return html.replace(v, insert + "\n" + v, 1)
            return html.replace(v, v + "\n  " + insert, 1)
    return html


def fix_floating_whatsapp(html: str) -> str:
    if "wr-mobile-cta-bar" not in html:
        old = re.compile(
            r'<a class="live-chat-fixed[^"]*"[^>]*href="[^"]*"[^>]*>\s*<img[^>]*>\s*</a>',
            re.DOTALL | re.IGNORECASE,
        )
        html = old.sub(FLOATING_WA + "\n" + MOBILE_CTA, html, count=1)
    else:
        html = re.sub(
            r'<a class="live-chat-fixed[^"]*"[^>]*href="[^"]*"[^>]*>',
            f'<a class="live-chat-fixed no-loader-all" href="{WA_UK_SHORT}" target="_blank" title="WhatsApp UK team">',
            html,
            count=1,
            flags=re.IGNORECASE,
        )
    return html


def fix_whatsapp_urls(html: str) -> str:
    replacements = [
        (
            "https://api.whatsapp.com/send?phone=917044974618&amp;&amp;text=Hi Writing Rodgers",
            WA_UK_SHORT,
        ),
        ("https://api.whatsapp.com/send?phone=917044974618", WA_UK_SHORT),
        ("https://wa.me/+917044974618", WA_UK_SHORT),
        ("https://wa.me/+447452212920", WA_UK_SHORT),
        ("wa.me/+917044974618", "wa.me/447452010395"),
        ("wa.me/+447452212920", "wa.me/447452010395"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    return html


def fix_cta_labels(html: str) -> str:
    html = re.sub(
        r'(<a class="btn viamagus-button-default[^"]*"[^>]*href="https://wa\.me/447452010395[^"]*"[^>]*>)\s*Call Now!\s*(</a>)',
        r"\1\n                          Get a free quote on WhatsApp\n                        \2",
        html,
        flags=re.IGNORECASE,
    )
    for label in ("25% Off! DM now!", "Order Now +44 7452010395", "Special Discounts! Click Here", "Click Here to Get Your Assignment!"):
        html = html.replace(label, "Get a free quote on WhatsApp")
    return html


def remove_form_loader(html: str) -> str:
    html = html.replace("Viamagus_Form_Loader._init();", "")
    html = html.replace("Viamagus_Form_Loader._init();	", "")
    html = re.sub(r",\s*,", ",", html)
    html = re.sub(r"\(\s*;\s*", "(", html)
    return html


def inject_contact_before_footer(html: str, contact: str) -> str:
    if 'id="wr-contact"' in html:
        return html
    footer_match = re.search(r"<footer\s", html, re.IGNORECASE)
    if not footer_match:
        return html
    return html[: footer_match.start()] + contact + "\n" + html[footer_match.start() :]


def enhance_footer(html: str) -> str:
    if "assignment-help-in-london.html" in html and "London</a> ·" in html:
        return html
    pattern = re.compile(
        r'(<div class="copyright-center"[^>]*>)\s*(<a href="https://www\.instagram\.com)',
        re.DOTALL | re.IGNORECASE,
    )
    return pattern.sub(r"\1\n" + FOOTER_LINKS + r"                  \2", html, count=1)


def process_file(path: Path, nav_inner: str, contact: str) -> bool:
    original = path.read_text(encoding="utf-8")
    html = original

    if path.name == "index.html":
        html = fix_whatsapp_urls(html)
        html = fix_cta_labels(html)
        html = remove_form_loader(html)
        html = enhance_footer(html)
    else:
        html = inject_wr_css(html)
        html = replace_nav(html, nav_inner)
        html = fix_floating_whatsapp(html)
        html = fix_whatsapp_urls(html)
        html = fix_cta_labels(html)
        html = remove_form_loader(html)
        html = inject_contact_before_footer(html, contact)
        html = enhance_footer(html)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    nav_inner = (PARTIALS / "wr-nav.html").read_text(encoding="utf-8").strip()
    contact = (PARTIALS / "wr-contact.html").read_text(encoding="utf-8").strip()

    updated = 0
    for path in iter_html_files():
        if process_file(path, nav_inner, contact):
            print(f"updated {path.name}")
            updated += 1
        else:
            print(f"skip {path.name}")

    print(f"\nDone: {updated} file(s) changed.")


if __name__ == "__main__":
    main()
