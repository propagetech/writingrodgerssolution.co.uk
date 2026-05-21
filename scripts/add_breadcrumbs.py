"""Insert a Home > Category > Page breadcrumb into every subpage.

Idempotent: if a page already has `<nav class="wr-breadcrumb">` we skip it.

Run from repo root:
    python3 scripts/add_breadcrumbs.py
"""

from __future__ import annotations
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# slug -> (category-label, category-href-or-None, page-label)
# category-href is relative to the subpage; None means the category is plain text.
PAGE_INFO: dict[str, tuple[str, str | None, str]] = {
    # ---- Services (15) — use long descriptive name (matches dropdown menu) ---
    "academic-coaching-help":             ("Our Services", "../#wr-services", "Academic Coaching Help in UK, UAE and Australia"),
    "accounting-assignment-help":         ("Our Services", "../#wr-services", "Accounting Assignment Help in Australia and UK"),
    "case-study-assignment-help":         ("Our Services", "../#wr-services", "Case Study Assignment Help in UK"),
    "dissertation-writing-help":          ("Our Services", "../#wr-services", "Dissertation Writing Help in UK, Oman Muscat, UAE and Australia"),
    "essay-writing-help":                 ("Our Services", "../#wr-services", "Essay writing Help"),
    "exam-preparation-help":              ("Our Services", "../#wr-services", "Exam Preparation Help"),
    "it-assignment-help":                 ("Our Services", "../#wr-services", "IT Assignment Help"),
    "law-assignment-help":                ("Our Services", "../#wr-services", "Law Assignment Help in Australia and UK"),
    "management-assignment-help":         ("Our Services", "../#wr-services", "Management Assignment Help in UAE"),
    "marketing-assignment-help":          ("Our Services", "../#wr-services", "Marketing Assignment Help in UK"),
    "nursing-assignment-help":            ("Our Services", "../#wr-services", "Nursing Assignment Help in UK and Australia"),
    "project-management-assignment-help": ("Our Services", "../#wr-services", "Project Management Assignment Help in Australia"),
    "report-writing-help":                ("Our Services", "../#wr-services", "Report Writing Help in UAE"),
    "thesis-with-spss-nvivo-help":        ("Our Services", "../#wr-services", "Thesis with SPSS & Nvivo Help"),
    "thesis-writing-help":                ("Our Services", "../#wr-services", "Thesis Writing Help in UK"),
    # ---- Universities (14) — long descriptive labels matching dropdown -----
    "aston-university-assignment-help":              ("Assignments by University", None, "Aston University Assignment Help"),
    "bpp-assignment-help":                           ("Assignments by University", None, "BPP University Assignment Help from Expert Tutors"),
    "coventry-university-assignment-help":           ("Assignments by University", None, "Coventry University Assignment Help"),
    "de-montfort-university-assignment-help":        ("Assignments by University", None, "DMU Assignment Help"),
    "edinburgh-university-assignment-help":          ("Assignments by University", None, "Edinburgh University Assignment Help"),
    "essex-university-assignment-help":              ("Assignments by University", None, "Essex University Assignment Help"),
    "middlesex-university-assignment-help":          ("Assignments by University", None, "Middlesex University Assignment Help"),
    "university-college-birmingham-assignment-help": ("Assignments by University", None, "University College Birmingham Assignment Help"),
    "university-of-derby-assignment-help":           ("Assignments by University", None, "University of Derby Assignment Help"),
    "university-of-east-london-assignment-help":     ("Assignments by University", None, "University of East London Assignment Help"),
    "university-of-greenwich-assignment-help":       ("Assignments by University", None, "University of Greenwich Assignment Help"),
    "university-of-salford-assignment-help":         ("Assignments by University", None, "University of Salford Assignment Help"),
    "university-of-sunderland-assignment-help":      ("Assignments by University", None, "University of Sunderland Assignment Help"),
    "university-of-warwick-assignment-help":         ("Assignments by University", None, "University of Warwick Assignment Help"),
    # ---- Branches (6) — long descriptive labels matching dropdown ----------
    "assignment-help-in-australia":              ("Our Branches", None, "Assignment Help in Australia"),
    "assignment-help-in-canada":                 ("Our Branches", None, "Canada Assignment Help"),
    "assignment-help-in-oman-muscat":            ("Our Branches", None, "Assignment Help in Oman Muscat"),
    "assignment-help-in-uae-by-professionals":   ("Our Branches", None, "Assignment Help in UAE by Professionals"),
    "assignment-help-in-uk-at-reasonable-price": ("Our Branches", None, "UK Assignment Services from Qualified Experts"),
    "ireland-assignment-help":                   ("Our Branches", None, "Ireland Assignment Help"),
    # ---- Cities (8) — long descriptive labels matching dropdown ------------
    "assignment-help-in-birmingham": ("Assignment Service by Cities", None, "Assignment Help in Birmingham"),
    "assignment-help-in-bristol":    ("Assignment Service by Cities", None, "Assignment Help in Bristol"),
    "assignment-help-in-cardiff":    ("Assignment Service by Cities", None, "Assignment Help in Cardiff"),
    "assignment-help-in-glasgow":    ("Assignment Service by Cities", None, "Assignment Help in Glasgow"),
    "assignment-help-in-leicester":  ("Assignment Service by Cities", None, "Assignment Help in Leicester"),
    "assignment-help-in-liverpool":  ("Assignment Service by Cities", None, "Assignment Help in Liverpool"),
    "assignment-help-in-london":     ("Assignment Service by Cities", None, "Assignment Help in London"),
    "assignment-help-in-manchester": ("Assignment Service by Cities", None, "Assignment Help in Manchester"),
    # ---- Standalone --------------------------------------------------------
    "about-us": (None, None, "About Writing Rodgers"),
    "blog":     (None, None, "Blog"),
}

BREADCRUMB_MARKER = "wr-breadcrumb"
SUB_HERO_PATTERN = re.compile(r'(\s*)<section class="wr-sub-hero')


def build_breadcrumb(category: str | None, category_href: str | None, page_label: str) -> str:
    items: list[str] = ['<li class="wr-breadcrumb__item"><a href="../">Home</a></li>']
    if category:
        if category_href:
            items.append(
                f'<li class="wr-breadcrumb__item"><a href="{category_href}">{category}</a></li>'
            )
        else:
            items.append(f'<li class="wr-breadcrumb__item">{category}</li>')
    items.append(
        f'<li class="wr-breadcrumb__item" aria-current="page">{page_label}</li>'
    )
    inner = "".join(items)
    return (
        '<nav class="wr-breadcrumb" aria-label="Breadcrumb">'
        f'<ol class="wr-breadcrumb__list">{inner}</ol>'
        '</nav>'
    )


def main() -> None:
    inserted = 0
    skipped_done = 0
    skipped_no_hero = 0
    skipped_no_mapping = 0

    for slug, info in PAGE_INFO.items():
        path = REPO / slug / "index.html"
        if not path.exists():
            skipped_no_mapping += 1
            continue
        text = path.read_text(encoding="utf-8")
        if BREADCRUMB_MARKER in text:
            skipped_done += 1
            continue

        category, category_href, page_label = info
        breadcrumb = build_breadcrumb(category, category_href, page_label)

        match = SUB_HERO_PATTERN.search(text)
        if not match:
            skipped_no_hero += 1
            print(f"  SKIP (no wr-sub-hero): {slug}")
            continue

        indent = match.group(1).split("\n")[-1] if "\n" in match.group(1) else ""
        replacement = (
            "\n" + indent + breadcrumb + match.group(0)
        )
        new_text = (
            text[: match.start()] + replacement + text[match.end():]
        )
        path.write_text(new_text, encoding="utf-8")
        inserted += 1
        print(f"  {slug}/index.html: breadcrumb added")

    print(f"\nInserted: {inserted}  |  Already had one: {skipped_done}  |  No sub-hero: {skipped_no_hero}  |  No mapping: {skipped_no_mapping}")


if __name__ == "__main__":
    main()
