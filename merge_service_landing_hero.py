#!/usr/bin/env python3
"""One landing-style hero: image left | problem + story + CTA right (white)."""

from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SERVICE_PAGES = [
    "dissertation-writing-help.html",
    "essay-writing-help.html",
    "nursing-assignment-help.html",
    "law-assignment-help.html",
    "management-assignment-help.html",
    "accounting-assignment-help.html",
    "it-assignment-help.html",
    "exam-preparation-help.html",
    "academic-coaching-help.html",
]

HERO_ACTIONS = """            <a class="wr-btn-primary" href="https://wa.me/917044974618?text=Hi%20Writing%20Rodgers%2C%20I%20need%20assignment%20help.%20Subject%3A%20%0ADeadline%3A%20" target="_blank" rel="noopener">Get a free quote on WhatsApp</a>
            <a class="wr-btn-secondary wr-btn-call" href="tel:+447452010395">Call +44 7452010395</a>"""


def esc(text: str) -> str:
    return html_lib.escape(text, quote=False)


def extract(block: str, pattern: str) -> str:
    m = re.search(pattern, block, re.DOTALL | re.I)
    if not m:
        return ""
    t = re.sub(r"<[^>]+>", "", m.group(1))
    return html_lib.unescape(re.sub(r"\s+", " ", t)).strip()


def build_landing_hero(
    service_label: str,
    headline: str,
    story: str,
    src: str,
    alt: str,
) -> str:
    return f"""      <section class="wr-sub-hero wr-sub-hero--split wr-sub-hero--landing" aria-label="Page introduction">
        <div class="wr-sub-hero__split">
          <div class="wr-sub-hero__media">
            <img src="{html_lib.escape(src, quote=True)}" alt="{html_lib.escape(alt, quote=True)}" width="480" height="480" loading="eager" />
          </div>
          <div class="wr-sub-hero__panel">
            <p class="wr-sub-hero__eyebrow">{esc(service_label)}</p>
            <h1 class="wr-sub-hero__headline">{esc(headline)}</h1>
            <p class="wr-sub-hero__story">{esc(story)}</p>
            <div class="wr-sub-hero__actions">
{HERO_ACTIONS}
            </div>
            <p class="wr-sub-hero__trust">Plagiarism-free · Rubric-matched · UK team since 2017 · <a href="https://wa.me/917044974618?text=Hi%20Writing%20Rodgers" target="_blank" rel="noopener">International WhatsApp</a></p>
          </div>
        </div>
      </section>
"""


def transform(html: str) -> str | None:
    if "wr-sub-hero--landing" in html:
        return None

    hero_m = re.search(
        r'<section class="wr-sub-hero[^"]*"[^>]*>.*?</section>',
        html,
        re.DOTALL | re.I,
    )
    intro_m = re.search(
        r'<section class="wr-sub-intro"[^>]*>.*?</section>',
        html,
        re.DOTALL | re.I,
    )
    if not hero_m:
        return None

    hero = hero_m.group(0)
    service_label = extract(hero, r'class="wr-sub-hero__title"[^>]*>(.*?)</h1>') or extract(
        hero, r'class="wr-sub-hero__eyebrow"[^>]*>(.*?)</p>'
    )
    src_m = re.search(r'<img[^>]+src="([^"]+)"', hero)
    alt_m = re.search(r'alt="([^"]*)"', hero)
    src = src_m.group(1) if src_m else ""
    alt = alt_m.group(1) if alt_m else service_label

    headline = ""
    story = ""
    if intro_m:
        headline = extract(intro_m.group(0), r'class="wr-sub-intro__title"[^>]*>(.*?)</h2>')
        story = extract(intro_m.group(0), r'class="wr-sub-intro__lead"[^>]*>(.*?)</p>')
    if not headline:
        headline = service_label
    if not story:
        story = extract(hero, r'class="wr-sub-hero__lead"[^>]*>(.*?)</p>')

    new_hero = build_landing_hero(service_label, headline, story, src, alt)

    html = html[: hero_m.start()] + new_hero + html[hero_m.end() :]

    if intro_m:
        intro_m2 = re.search(
            r'<section class="wr-sub-intro"[^>]*>.*?</section>',
            html,
            re.DOTALL | re.I,
        )
        if intro_m2:
            html = html[: intro_m2.start()] + html[intro_m2.end() :]

    cta_m = re.search(
        r'<section class="wr-sub-cta-band"[^>]*>.*?</section>\s*',
        html,
        re.DOTALL | re.I,
    )
    if cta_m:
        html = html[: cta_m.start()] + html[cta_m.end() :]

    mid_m = re.search(
        r'<section class="wr-sub-mid-cta"[^>]*>.*?</section>\s*',
        html,
        re.DOTALL | re.I,
    )
    if mid_m:
        html = html[: mid_m.start()] + html[mid_m.end() :]

    return html


def main() -> None:
    n = 0
    for name in SERVICE_PAGES:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        new = transform(text)
        if new and new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
            print(name)
    print(f"Done: {n}")


if __name__ == "__main__":
    main()
