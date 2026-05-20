#!/usr/bin/env python3
"""Polish all subpages: CTAs, meta, sub-hero strip, nav contact link, 404."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTIALS = ROOT / "partials"

WA_UK = (
    "https://wa.me/447452010395?text=Hi%20Writing%20Rodgers%2C%20"
    "I%20need%20assignment%20help.%20Subject%3A%20%0ADeadline%3A%20"
)
WA_UK_SHORT = (
    "https://wa.me/447452010395?text=Hi%20Writing%20Rodgers%2C%20"
    "I%20need%20assignment%20help.%20"
)

HASHTAG_META = re.compile(
    r"#(?:studentassignmenthelp|myassignmenthelp|WritingRodgers|writingrodgers)[^\"]*",
    re.IGNORECASE,
)

SUB_HERO_TEMPLATE = '''      <section class="wr-sub-hero" aria-label="Page introduction">
        <div class="wr-sub-hero__inner">
          <h1 class="wr-sub-hero__title">{title}</h1>
          <p class="wr-sub-hero__lead">Plagiarism-free, rubric-matched work · Direct WhatsApp with our UK team since 2017</p>
          <div class="wr-sub-hero__actions">
            <a class="wr-btn-primary" href="{wa}" target="_blank" rel="noopener">Get a free quote on WhatsApp</a>
            <a class="wr-btn-secondary wr-btn-call" href="tel:+447452010395">Call +44 7452010395</a>
            <a class="wr-btn-secondary" href="mailto:writingrodgerssolutionuk@gmail.com?subject=Assignment%20help%20request">Email us</a>
          </div>
        </div>
      </section>
'''

CTA_LABELS = (
    "Book Now!",
    "Book Assistance Now!",
    "Call Now!",
    "Order Now +44 7452010395",
    "25% Off! DM now!",
    "Special Discounts! Click Here",
    "Click Here to Get Your Assignment!",
    "Get a free quote on WhatsApp",
)


def page_title(html: str, path: Path) -> str:
    match = re.search(r"<title>\s*(.*?)\s*</title>", html, re.DOTALL | re.IGNORECASE)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return path.stem.replace("-", " ").title()


def clean_description(title: str) -> str:
    return (
        f"Expert {title} from Writing Rodgers Solution LLP since 2017. "
        "Plagiarism-free, rubric-matched support. WhatsApp +44 7452010395 — no contact forms."
    )


def replace_meta_descriptions(html: str, desc: str) -> str:
    escaped = desc.replace('"', "&quot;")
    for attr in ("name", "property"):
        for key in ("description", "og:description", "twitter:description"):
            pattern = rf'(<meta\s+content=")[^"]*("\s+{attr}="{key}")'
            html = re.sub(pattern, rf"\1{escaped}\2", html, count=1, flags=re.IGNORECASE)
    return html


def fix_cta_buttons(html: str) -> str:
    for label in CTA_LABELS:
        if label == "Get a free quote on WhatsApp":
            continue
        html = html.replace(f">\n             {label}\n            </a>", ">\n             Get a free quote on WhatsApp\n            </a>")
        html = html.replace(f">{label}</a>", ">Get a free quote on WhatsApp</a>")
        html = html.replace(f">\n            {label}\n           </a>", ">\n            Get a free quote on WhatsApp\n           </a>")
    html = re.sub(
        r'(<a class="btn viamagus-button-default[^"]*"[^>]*href="https://wa\.me/447452010395[^"]*")([^>]*)(>)',
        r'\1 target="_blank" rel="noopener"\3',
        html,
        flags=re.IGNORECASE,
    )
    html = html.replace('target="_blank" target="_blank"', 'target="_blank"')
    html = html.replace('rel="noopener" rel="noopener"', 'rel="noopener"')
    return html


def inject_sub_hero(html: str, title: str) -> str:
    if "wr-sub-hero" in html:
        return html
    hero = SUB_HERO_TEMPLATE.format(title=title, wa=WA_UK)
    patterns = [
        (
            r'(</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*)'
            r'(<div class="viamagus-component viamagus-image-text)',
            r"\1" + hero + r"\n\2",
        ),
        (
            r'(</div>\s*</div>\s*</div>\s*</div>\s*)'
            r'(<div class="viamagus-component viamagus-background)',
            r"\1" + hero + r"\n\2",
        ),
    ]
    for pat, repl in patterns:
        new_html, n = re.subn(pat, repl, html, count=1, flags=re.IGNORECASE)
        if n:
            return new_html
    return html


def fix_nav_contact(html: str) -> str:
    return html.replace('href="/#wr-contact"', 'href="#wr-contact"')


def fix_404(html: str) -> str:
    html = html.replace('href="home.html"', 'href="/"')
    if "live-chat-fixed" not in html:
        floating = f'''  <a class="live-chat-fixed no-loader-all" href="{WA_UK_SHORT}" target="_blank" rel="noopener" title="WhatsApp UK team">
    <img src="imgs/image-20.webp" alt="Chat on WhatsApp" style="border-radius: 50%; width: 50px; height: 50px" />
  </a>
'''
        html = html.replace("<body>", "<body>\n" + floating, 1)
    return html


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    html = original

    if path.name == "index.html":
        return False

    title = page_title(html, path)
    desc = clean_description(title)

    html = fix_nav_contact(html)
    html = replace_meta_descriptions(html, desc)
    html = fix_cta_buttons(html)
    html = inject_sub_hero(html, title)

    if path.name == "404.html":
        html = fix_404(html)

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
    print(f"\nDone: {updated} file(s).")


if __name__ == "__main__":
    main()
