#!/usr/bin/env python3
"""Move service-page CTAs below problem/solution (story-first flow)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTIAL = (ROOT / "partials" / "wr-service-cta-band.html").read_text(encoding="utf-8")

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


def reorder(html: str) -> str | None:
    if "wr-sub-hero--split" not in html or "wr-sub-cta-band" in html:
        return None

    actions_m = re.search(
        r'<div class="wr-sub-hero__actions"[^>]*>.*?</div>',
        html,
        re.DOTALL | re.I,
    )
    if not actions_m:
        return None

    html = html[: actions_m.start()] + html[actions_m.end() :]

    contact_m = re.search(r'<section class="wr-contact"', html)
    if not contact_m:
        return None

    # Pages with existing mid-cta: insert CTA band before mid-cta, remove mid-cta duplicate
    mid_m = re.search(
        r'<section class="wr-sub-mid-cta"[^>]*>.*?</section>\s*(?=<section class="wr-contact")',
        html,
        re.DOTALL | re.I,
    )
    if mid_m:
        html = html[: mid_m.start()] + PARTIAL + "\n\n" + html[mid_m.end() :]
        return html

    html = html[: contact_m.start()] + PARTIAL + "\n\n" + html[contact_m.start() :]
    return html


def main() -> None:
    updated = 0
    for name in SERVICE_PAGES:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        new = reorder(text)
        if new and new != text:
            path.write_text(new, encoding="utf-8")
            updated += 1
            print(f"updated: {name}")
    print(f"Done: {updated} file(s)")


if __name__ == "__main__":
    main()
