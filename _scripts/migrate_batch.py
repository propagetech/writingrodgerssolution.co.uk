#!/usr/bin/env python3
"""
migrate_batch.py — applies migrate_page.py across all remaining subpages.

Per-category metadata is defined inline below. Each page's title/description/keywords
come from the page's existing <head> (extracted automatically); per-category
breadcrumb parents + Service node values come from this config.

Usage:
  python3 _scripts/migrate_batch.py services
  python3 _scripts/migrate_batch.py universities
  python3 _scripts/migrate_batch.py cities
  python3 _scripts/migrate_batch.py countries
  python3 _scripts/migrate_batch.py all
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

REPO = Path(__file__).resolve().parent.parent

# --------------------------- CATEGORY CONFIG ---------------------------

# Service pages — parent: "Our Services". areaServed: UK by default.
SERVICES = {
    "thesis-writing-help": ("Thesis Writing Help", "Longer-form Master's or PhD-level thesis support — structured to your school's rubric. Plagiarism-free, original, on time."),
    "essay-writing-help": ("Essay Writing Help", "Critical, argumentative, and reflective essays referenced to UK academic style. Direct WhatsApp with our UK team since 2017."),
    "report-writing-help": ("Report Writing Help", "Business and academic reports built by MBA-trained writers — submission-ready and matched to your marking criteria."),
    "case-study-assignment-help": ("Case Study Assignment Help", "Real-world case analysis with frameworks, recommendations, and academic references. Matched to your university's rubric."),
    "exam-preparation-help": ("Exam Preparation Help", "One-to-one tutoring and exam-prep coaching for UK and international university modules."),
    "thesis-with-spss-nvivo-help": ("Thesis with SPSS & NVivo Help", "Quantitative (SPSS) and qualitative (NVivo) analysis chapters for your thesis. Methodology, data prep, and write-up."),
    "academic-coaching-help": ("Academic Coaching Help", "One-to-one academic coaching for UK, UAE and Australian university modules. Support that continues after delivery."),
    "marketing-assignment-help": ("Marketing Assignment Help", "Marketing assignment help with brand strategy, consumer behaviour, digital campaigns, and global-expansion plans. Matched to your university's marking criteria."),
    "management-assignment-help": ("Management Assignment Help", "Business, HR, strategy, and operations assignments matched to your MBA marking criteria. Direct WhatsApp with Subham's team since 2017."),
    "nursing-assignment-help": ("Nursing Assignment Help", "Nursing case studies, care plans, discussion posts, and evidence-based reports for UK and Australian universities."),
    "accounting-assignment-help": ("Finance & Accounting Assignment Help", "Analysis, audits, charts, and submission-ready accounting work matched to your university's rubric."),
    "law-assignment-help": ("Law Assignment Help", "UK, Australia, UAE, and Canada law assignments — acts, cases, and structured legal argument."),
    "it-assignment-help": ("IT & Data Assignment Help", "Coding tasks, networking theory, SQL, MATLAB, and applied data analysis. Matched to your university's marking criteria."),
    "project-management-assignment-help": ("Project Management Assignment Help", "PMBOK / PRINCE2-aligned project plans, charters, and risk registers. Submission-ready."),
}

# University pages — parent: "Assignments by University". Service.about → CollegeOrUniversity.
# Format: slug -> (university name, university URL)
UNIVERSITIES = {
    "aston-university-assignment-help": ("Aston University", "https://www.aston.ac.uk/"),
    "coventry-university-assignment-help": ("Coventry University", "https://www.coventry.ac.uk/"),
    "university-college-birmingham-assignment-help": ("University College Birmingham", "https://www.ucb.ac.uk/"),
    "de-montfort-university-assignment-help": ("De Montfort University", "https://www.dmu.ac.uk/"),
    "edinburgh-university-assignment-help": ("Edinburgh University", "https://www.ed.ac.uk/"),
    "essex-university-assignment-help": ("Essex University", "https://www.essex.ac.uk/"),
    "middlesex-university-assignment-help": ("Middlesex University", "https://www.mdx.ac.uk/"),
    "university-of-derby-assignment-help": ("University of Derby", "https://www.derby.ac.uk/"),
    "university-of-east-london-assignment-help": ("University of East London", "https://www.uel.ac.uk/"),
    "university-of-greenwich-assignment-help": ("University of Greenwich", "https://www.gre.ac.uk/"),
    "university-of-sunderland-assignment-help": ("University of Sunderland", "https://www.sunderland.ac.uk/"),
    "university-of-salford-assignment-help": ("University of Salford", "https://www.salford.ac.uk/"),
    "university-of-warwick-assignment-help": ("University of Warwick", "https://www.warwick.ac.uk/"),
}

# City pages — parent: "Assignment Service by Cities". areaServed: City containedInPlace UK.
CITIES = {
    "assignment-help-in-glasgow": "Glasgow",
    "assignment-help-in-manchester": "Manchester",
    "assignment-help-in-leicester": "Leicester",
    "assignment-help-in-liverpool": "Liverpool",
    "assignment-help-in-cardiff": "Cardiff",
    "assignment-help-in-bristol": "Bristol",
    "assignment-help-in-birmingham": "Birmingham",
}

# Country pages — parent: "Our Branches". areaServed: Country.
COUNTRIES = {
    "assignment-help-in-uae-by-professionals": "United Arab Emirates",
    "assignment-help-in-oman-muscat": "Oman",
    "assignment-help-in-canada": "Canada",
    "assignment-help-in-uk-at-reasonable-price": "United Kingdom",
    "ireland-assignment-help": "Ireland",
}


# --------------------------- METADATA BUILDERS ---------------------------

def title_to_breadcrumb_leaf(title: str) -> str:
    """Strip suffixes like ' | Writing Rodgers Solution LLP' from titles for breadcrumb."""
    for sep in [" | ", " – ", " — ", " - "]:
        if sep in title:
            head, _, tail = title.partition(sep)
            # Keep the first part if it's not just a brand
            if "Writing Rodgers" not in head:
                return head.strip()
    return title.strip()


def meta_for_service(slug: str) -> dict:
    name, desc = SERVICES[slug]
    return {
        "slug": slug,
        "service_name": name,
        "service_description": desc,
        "breadcrumb": [
            {"name": "Our Services"},
            {"name": name},
        ],
    }


def meta_for_university(slug: str) -> dict:
    uni_name, uni_url = UNIVERSITIES[slug]
    return {
        "slug": slug,
        "service_name": f"{uni_name} Assignment Help",
        "service_description": (
            f"Personalised assignment help for {uni_name} students — original work, matched to "
            f"the university's marking criteria. Direct WhatsApp with Writing Rodgers' UK team since 2017."
        ),
        "university_name": uni_name,
        "university_url": uni_url,
        "breadcrumb": [
            {"name": "Assignments by University"},
            {"name": f"{uni_name} Assignment Help"},
        ],
    }


def meta_for_city(slug: str) -> dict:
    city = CITIES[slug]
    return {
        "slug": slug,
        "service_name": f"Assignment Help in {city}",
        "service_description": (
            f"Turnitin-safe assignment, dissertation and essay help for students in {city}. Original work "
            f"matched to your university's marking criteria. Direct WhatsApp with our UK team since 2017."
        ),
        "area_served": {
            "@type": "City",
            "name": city,
            "containedInPlace": {"@type": "Country", "name": "United Kingdom"},
        },
        "breadcrumb": [
            {"name": "Assignment Service by Cities"},
            {"name": f"Assignment Help in {city}"},
        ],
    }


def meta_for_country(slug: str) -> dict:
    country = COUNTRIES[slug]
    # Friendly display label, e.g. "Australia" vs "United Arab Emirates"
    return {
        "slug": slug,
        "service_name": f"{country} Assignment Help",
        "service_description": (
            f"Turnitin-safe essay, dissertation and exam-prep support for students in {country}. Original "
            f"work matched to your university's marking criteria. Direct WhatsApp with Writing Rodgers since 2017."
        ),
        "area_served": {"@type": "Country", "name": country},
        "breadcrumb": [
            {"name": "Our Branches"},
            {"name": f"Assignment Help in {country}" if "uk-at-reasonable" not in slug else "UK Assignment Services from Qualified Experts"},
        ],
    }


# --------------------------- RUNNER ---------------------------

def run_one(slug: str, meta: dict) -> bool:
    path = REPO / slug / "index.html"
    if not path.exists():
        print(f"  SKIP {slug}: file not found")
        return False

    with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(meta, f)
        meta_path = f.name

    script = REPO / "_scripts" / "migrate_page.py"
    result = subprocess.run(
        ["python3", str(script), str(path), meta_path],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  FAIL {slug}: {result.stderr.strip()}")
        return False
    print(f"  ok   {slug}")
    return True


def validate(slug: str) -> dict:
    """Quick post-migration validation. Returns dict of issues."""
    path = REPO / slug / "index.html"
    src = path.read_text(encoding="utf-8")
    issues = {}

    for t in ["div", "header", "main", "footer", "section", "aside", "nav", "ul", "li", "script"]:
        o = len(re.findall(rf"<{t}[\s>]", src))
        c = len(re.findall(rf"</{t}>", src))
        if o != c:
            issues[f"{t}-balance"] = f"{o}/{c}"

    try:
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)
        json.loads(m.group(1))
    except Exception as e:
        issues["json-ld"] = str(e)

    h1_count = len(re.findall(r"<h1", src))
    if h1_count != 1:
        issues["h1-count"] = h1_count

    for cls in ["navbar", "nav-collapse", "dropdown-toggle", "dropdown-menu", "caret", "menu-center", "btn-navbar", "featurette-heading"]:
        if re.search(rf'class="[^"]*\b{cls}\b[^"]*"', src):
            issues[f"cruft-{cls}"] = True

    for attr in ["data-toggle", "data-hover", "data-component-name", "data-bkg-image", "data-sticky-header", "itemscope"]:
        if attr in src:
            issues[f"cruft-attr-{attr}"] = True

    return issues


def run_category(category: str):
    builders = {
        "services": (SERVICES, meta_for_service),
        "universities": (UNIVERSITIES, meta_for_university),
        "cities": (CITIES, meta_for_city),
        "countries": (COUNTRIES, meta_for_country),
    }
    if category not in builders:
        print(f"unknown category: {category}", file=sys.stderr)
        sys.exit(2)
    items, builder = builders[category]
    print(f"=== {category} ({len(items)} pages) ===")
    results = {}
    for slug in items:
        meta = builder(slug)
        ok = run_one(slug, meta)
        if ok:
            issues = validate(slug)
            results[slug] = issues
            if issues:
                print(f"       issues: {issues}")
    print(f"\n=== {category}: done. {sum(1 for v in results.values() if not v)}/{len(results)} clean ===")
    return results


if __name__ == "__main__":
    cat = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cat == "all":
        for c in ["services", "universities", "cities", "countries"]:
            run_category(c)
    else:
        run_category(cat)
