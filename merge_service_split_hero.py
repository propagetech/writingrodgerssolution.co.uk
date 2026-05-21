#!/usr/bin/env python3
"""Merge service-page hero + featurette image into split layout (image left, CTAs right)."""

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

WA_ACTIONS = """            <a class="wr-btn-primary" href="https://wa.me/447452010395?text=Hi%20Writing%20Rodgers%2C%20I%20need%20assignment%20help.%20Subject%3A%20%0ADeadline%3A%20" target="_blank" rel="noopener">Get a free quote on WhatsApp</a>
            <a class="wr-btn-secondary wr-btn-call" href="tel:+447452010395">Call +44 7452010395</a>
            <a class="wr-btn-secondary" href="mailto:writingrodgerssolutionuk@gmail.com?subject=Assignment%20help%20request">Email us</a>"""

CONTACT_MARK = '<section class="wr-contact"'


def strip_html(text: str) -> str:
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def esc(text: str) -> str:
    return html_lib.escape(text, quote=True)


def extract_tag(block: str, pattern: str) -> str:
    m = re.search(pattern, block, re.DOTALL | re.IGNORECASE)
    return strip_html(m.group(1)) if m else ""


def parse_richtext_to_sections(inner: str) -> list[dict]:
    sections: list[dict] = []
    current: dict = {"title": "", "paragraphs": [], "items": []}

    chunks = re.split(r"(<ul[^>]*>|</ul>)", inner, flags=re.I)
    in_list = False

    for chunk in chunks:
        if re.match(r"<ul", chunk, re.I):
            in_list = True
            continue
        if chunk.strip() == "</ul>":
            in_list = False
            continue

        if in_list:
            for li in re.findall(r"<li[^>]*>(.*?)</li>", chunk, re.DOTALL | re.I):
                text = strip_html(li)
                if text:
                    current["items"].append(text)
            continue

        text = strip_html(chunk)
        if not text:
            continue
        if len(text) < 90 and ("?" in text or text.endswith(":")):
            if current["paragraphs"] or current["items"]:
                sections.append(current)
            current = {"title": text.rstrip(":"), "paragraphs": [], "items": []}
        else:
            current["paragraphs"].append(text)

    if current["paragraphs"] or current["items"] or current["title"]:
        sections.append(current)
    return sections


def build_details_html(richtext_block: str) -> str:
    inner_m = re.search(
        r'id="viamagus_Text_[^"]*-content"[^>]*>(.*?)</div>\s*</div>\s*</div>\s*</div>\s*</div>',
        richtext_block,
        re.DOTALL | re.I,
    )
    if not inner_m:
        inner_m = re.search(
            r'class="row-fluid viamagus-paragraph"[^>]*>(.*?)</div>',
            richtext_block,
            re.DOTALL | re.I,
        )
    if not inner_m:
        return ""

    raw = inner_m.group(1)
    sections = parse_richtext_to_sections(raw)
    if not sections:
        return ""

    parts = ['      <section class="wr-sub-details" aria-label="Service details">']
    for i, sec in enumerate(sections):
        sid = f"wr-service-details-{i}"
        parts.append('        <div class="wr-sub-details__block">')
        if sec.get("title"):
            parts.append(
                f'          <h2 class="wr-section-title" id="{sid}">{esc(sec["title"])}</h2>'
            )
        for p in sec["paragraphs"]:
            parts.append(f"          <p>{esc(p)}</p>")
        if sec["items"]:
            parts.append('          <ul class="wr-benefit-list">')
            for item in sec["items"]:
                parts.append(f"            <li>{esc(item)}</li>")
            parts.append("          </ul>")
        parts.append("        </div>")
    parts.append("      </section>\n")
    return "\n".join(parts)


def split_hero_html(title: str, lead: str, src: str, alt: str, actions: str) -> str:
    return f"""      <section class="wr-sub-hero wr-sub-hero--split" aria-label="Page introduction">
        <div class="wr-sub-hero__split">
          <div class="wr-sub-hero__media">
            <img src="{esc(src)}" alt="{esc(alt)}" width="480" height="480" loading="eager" />
          </div>
          <div class="wr-sub-hero__panel">
            <h1 class="wr-sub-hero__title">{esc(title)}</h1>
            <p class="wr-sub-hero__lead">{lead}</p>
            <div class="wr-sub-hero__actions">
{actions}
            </div>
          </div>
        </div>
      </section>
"""


def intro_html(h2: str, intro: str) -> str:
    if not h2 and not intro:
        return ""
    return f"""      <section class="wr-sub-intro" aria-labelledby="wr-service-intro">
        <div class="wr-sub-intro__inner">
          <h2 class="wr-sub-intro__title" id="wr-service-intro">{esc(h2)}</h2>
          <p class="wr-sub-intro__lead">{esc(intro)}</p>
        </div>
      </section>
"""


def extract_image_block(block: str) -> tuple[str, str, str, str]:
    src_m = re.search(r'\bsrc="([^"]+)"', block)
    alt_m = re.search(r'\balt="([^"]*)"', block)
    src = src_m.group(1) if src_m else ""
    alt = alt_m.group(1) if alt_m else ""
    h2 = extract_tag(block, r'class="[^"]*featurette-heading[^"]*"[^>]*>.*?<span[^>]*>(.*?)</span>')
    if not h2:
        h2 = extract_tag(block, r'class="[^"]*featurette-heading[^"]*"[^>]*>(.*?)</h2>')
    intro = extract_tag(block, r'class="[^"]*lead viamagus-paragraph[^"]*"[^>]*>(.*?)</div>')
    return src, alt, h2, intro


def process_legacy(html: str, force: bool = False) -> str | None:
    if not force and "wr-sub-hero--split" in html:
        return None

    contact_i = html.find(CONTACT_MARK)
    if contact_i < 0:
        return None

    hero_m = re.search(
        r'<section class="wr-sub-hero[^"]*"[^>]*>.*?</section>',
        html[:contact_i],
        re.DOTALL | re.I,
    )
    if not hero_m:
        return None

    middle = html[hero_m.end() : contact_i]
    img_m = re.search(
        r'<div class="viamagus-component viamagus-image-text[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>',
        middle,
        re.DOTALL | re.I,
    )
    richtext_m = re.search(
        r'<div class="viamagus-component viamagus-richtext[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>',
        middle,
        re.DOTALL | re.I,
    )

    hero_block = hero_m.group(0)
    title = extract_tag(hero_block, r'class="wr-sub-hero__title"[^>]*>(.*?)</h1>')
    lead = extract_tag(hero_block, r'class="wr-sub-hero__lead"[^>]*>(.*?)</p>')
    actions_m = re.search(
        r'<div class="wr-sub-hero__actions"[^>]*>(.*?)</div>',
        hero_block,
        re.DOTALL | re.I,
    )
    actions = actions_m.group(1).strip() if actions_m else WA_ACTIONS
    if "wa.me" not in actions:
        actions = WA_ACTIONS

    src, alt, h2, intro = "", "", "", ""
    if img_m:
        src, alt, h2, intro = extract_image_block(img_m.group(0))
    if not alt:
        alt = title
    if not src:
        return None

    details = build_details_html(richtext_m.group(0)) if richtext_m else ""
    tail = middle
    if img_m:
        tail = tail.replace(img_m.group(0), "", 1)
    if richtext_m:
        tail = tail.replace(richtext_m.group(0), "", 1)
    preserved = tail.strip()

    replacement = (
        split_hero_html(title, lead, src, alt, actions)
        + intro_html(h2, intro)
        + details
        + (preserved + "\n" if preserved else "")
    )

    out = html[: hero_m.start()] + replacement + html[contact_i:]
    return re.sub(
        r"(</section>)\s*(?:</div>\s*){1,5}(?=\s*<section class=\"wr-contact\")",
        r"\1\n\n",
        out,
        flags=re.I,
    )


def process_refactored(html: str, force: bool = False) -> str | None:
    if not force and "wr-sub-hero--split" not in html:
        pass
    elif not force:
        return None

    contact_i = html.find(CONTACT_MARK)
    if contact_i < 0:
        return None

    hero_m = re.search(
        r'<section class="wr-sub-hero wr-sub-hero--split"[^>]*>.*?</section>',
        html[:contact_i],
        re.DOTALL | re.I,
    )
    if not hero_m:
        return None

    middle = html[hero_m.end() : contact_i].strip()
    if middle.startswith("</div>"):
        middle = re.sub(r"^(</div>\s*)+", "", middle)
    return html[: hero_m.end()] + "\n" + middle + "\n\n" + html[contact_i:]


def restore_from_git_and_merge() -> None:
    """Re-merge pages that lost richtext: checkout middle from git then merge."""
    import subprocess

    for name in SERVICE_PAGES:
        path = ROOT / name
        git_path = f"HEAD:{name}"
        try:
            original = subprocess.check_output(
                ["git", "show", git_path], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            continue
        if "viamagus-image-text" not in original:
            continue
        new = process_legacy(original, force=True)
        if new:
            path.write_text(new, encoding="utf-8")
            print(f"restored+merged: {name}")


def main() -> None:
    import sys

    if "--restore" in sys.argv:
        restore_from_git_and_merge()
        return

    updated = 0
    for name in SERVICE_PAGES:
        path = ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "wr-sub-hero--split" in text and "wr-sub-details" not in text and "viamagus-richtext" not in text:
            new = restore_from_git_and_merge_single(name)
        else:
            new = process_legacy(text) or process_refactored(text)
        if new and new != text:
            path.write_text(new, encoding="utf-8")
            updated += 1
            print(f"updated: {name}")
    print(f"Done: {updated} service page(s)")


def restore_from_git_and_merge_single(name: str) -> str | None:
    import subprocess

    try:
        original = subprocess.check_output(
            ["git", "show", f"HEAD:{name}"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return None
    return process_legacy(original, force=True)


if __name__ == "__main__":
    main()
