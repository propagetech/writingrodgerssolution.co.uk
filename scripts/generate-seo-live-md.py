#!/usr/bin/env python3
"""Fetch SEO from the live site and write seo-live.md at repo root."""

from __future__ import annotations

import importlib.util
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE_BASE = "https://www.writingrodgerssolution.co.uk"
SITEMAP_URL = f"{SITE_BASE}/sitemap.xml"
ROBOTS_URL = f"{SITE_BASE}/robots.txt"
OUTPUT = ROOT / "seo-live.md"
USER_AGENT = "WritingRodgers-SEO-Audit/1.0 (+https://www.writingrodgerssolution.co.uk/)"
FETCH_TIMEOUT_S = 30
EXTRA_URLS = [f"{SITE_BASE}/404.html"]
SKIP_PATH_SUFFIXES = ("/robots.txt", "/sitemap.xml")

# Reuse parsers from generate-seo-md.py
_spec = importlib.util.spec_from_file_location(
    "generate_seo_md", ROOT / "scripts" / "generate-seo-md.py"
)
_seo = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_seo)

TITLE_RE = _seo.TITLE_RE
CANONICAL_RE = _seo.CANONICAL_RE
LANG_RE = _seo.LANG_RE
extract_meta = _seo.extract_meta
extract_schema = _seo.extract_schema
extract_h1 = _seo.extract_h1
normalize_whitespace = _seo.normalize_whitespace
format_field = _seo.format_field
md_escape_inline = _seo.md_escape_inline

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
LOC_RE = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.IGNORECASE)


@dataclass
class FetchResult:
    url: str
    final_url: str
    status: int | None
    html: str | None
    error: str | None


def fetch_url(url: str) -> FetchResult:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT_S) as response:
            body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            html = body.decode(charset, errors="replace")
            return FetchResult(
                url=url,
                final_url=response.geturl(),
                status=response.status,
                html=html,
                error=None,
            )
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else None
        return FetchResult(
            url=url,
            final_url=exc.geturl() if exc.url else url,
            status=exc.code,
            html=body,
            error=str(exc.reason),
        )
    except Exception as exc:  # noqa: BLE001 — report any network failure in the audit
        return FetchResult(url=url, final_url=url, status=None, html=None, error=str(exc))


def parse_sitemap_xml(xml_text: str) -> list[str]:
    urls: list[str] = []
    try:
        root = ET.fromstring(xml_text)
        for loc in root.findall(".//sm:loc", SITEMAP_NS):
            if loc.text:
                urls.append(loc.text.strip())
        if not urls:
            for loc in root.iter():
                if loc.tag.endswith("loc") and loc.text:
                    urls.append(loc.text.strip())
    except ET.ParseError:
        urls = [m.group(1).strip() for m in LOC_RE.finditer(xml_text)]
    return sorted(set(urls))


def is_page_url(url: str) -> bool:
    path = urlparse(url).path
    if any(path.endswith(suffix) for suffix in SKIP_PATH_SUFFIXES):
        return False
    return path.endswith(".html") or path.endswith(".htm") or path in ("", "/")


def discover_live_urls() -> list[str]:
    sitemap = fetch_url(SITEMAP_URL)
    urls: list[str] = []
    if sitemap.html:
        urls.extend(u for u in parse_sitemap_xml(sitemap.html) if is_page_url(u))
    for extra in EXTRA_URLS:
        if extra not in urls:
            urls.append(extra)
    return sorted(set(urls))


def url_anchor(url: str) -> str:
    path = urlparse(url).path.strip("/")
    if not path:
        return "home"
    return path.replace("/", "-")


def detect_platform(html: str) -> str:
    if "wr-sub-hero" in html or 'class="wr-skip-link"' in html:
        return "new (WR static)"
    if "viamagus-component" in html or "viamagus-custom-form" in html:
        return "legacy (Viamagus)"
    return "unknown"


def render_live_section(result: FetchResult) -> list[str]:
    anchor = url_anchor(result.url)
    lines: list[str] = []

    if result.html is None:
        lines.extend(
            [
                f"### {result.url} {{#{anchor}}}",
                "",
                f"- **Requested URL:** {result.url}",
                f"- **HTTP status:** {result.status if result.status is not None else '—'}",
                f"- **Error:** {md_escape_inline(result.error or 'Failed to fetch')}",
                "",
            ]
        )
        return lines

    html = result.html
    meta = extract_meta(html)
    schema = extract_schema(html)
    title_match = TITLE_RE.search(html)
    title = normalize_whitespace(title_match.group(1)) if title_match else None
    canonical_match = CANONICAL_RE.search(html)
    canonical = canonical_match.group(1) if canonical_match else None
    lang_match = LANG_RE.search(html)
    lang = lang_match.group(1) if lang_match else None
    h1 = extract_h1(html)
    platform = detect_platform(html)

    heading = title or result.url
    lines.extend(
        [
            f"### {md_escape_inline(heading)} {{#{anchor}}}",
            "",
            f"- **Requested URL:** {result.url}",
            f"- **Final URL:** {result.final_url}",
            f"- **HTTP status:** {result.status if result.status is not None else '—'}",
            f"- **Detected build:** {platform}",
        ]
    )
    if result.final_url != result.url:
        lines.append("- **Redirected:** yes")
    if lang:
        lines.append(f"- **HTML lang:** `{lang}`")
    lines.extend(format_field("Title tag", title))
    lines.extend(format_field("Meta description", meta.get("description")))
    lines.extend(format_field("Meta keywords", meta.get("keywords")))
    lines.extend(format_field("Canonical", canonical))
    lines.extend(format_field("Robots", meta.get("robots")))
    lines.extend(format_field("H1", h1))

    lines.append("")
    lines.append("**Open Graph / Twitter**")
    lines.append("")
    for key in (
        "og:title",
        "og:description",
        "og:type",
        "og:url",
        "og:site_name",
        "og:locale",
        "og:image",
        "og:image:alt",
        "twitter:card",
        "twitter:title",
        "twitter:description",
        "twitter:image",
    ):
        lines.extend(format_field(key, meta.get(key)))

    if meta.get("google-site-verification"):
        lines.append("")
        lines.append("**Verification**")
        lines.append("")
        lines.extend(
            format_field("google-site-verification", meta.get("google-site-verification"))
        )

    lines.append("")
    lines.append("**JSON-LD (Schema.org)**")
    lines.append("")
    if not schema["has_json_ld"]:
        lines.append("- No `application/ld+json` block found.")
    else:
        lines.extend(format_field("Types in @graph", schema.get("schema_types")))  # type: ignore[arg-type]
        lines.extend(format_field("WebPage name", schema.get("webpage_name")))  # type: ignore[arg-type]
        lines.extend(format_field("WebPage description", schema.get("webpage_description")))  # type: ignore[arg-type]
        lines.extend(format_field("WebPage URL", schema.get("webpage_url")))  # type: ignore[arg-type]
        lines.extend(format_field("Service name", schema.get("service_name")))  # type: ignore[arg-type]
        lines.extend(format_field("Service type", schema.get("service_type")))  # type: ignore[arg-type]
        lines.extend(format_field("Service description", schema.get("service_description")))  # type: ignore[arg-type]
        lines.extend(format_field("CollegeOrUniversity", schema.get("university_name")))  # type: ignore[arg-type]
        if schema.get("university_url"):
            lines.extend(format_field("University URL", schema.get("university_url")))  # type: ignore[arg-type]
        lines.extend(format_field("Breadcrumbs", schema.get("breadcrumbs")))  # type: ignore[arg-type]

    lines.append("")
    return lines


def render_index_table(rows: list[FetchResult]) -> list[str]:
    lines = [
        "| Page | URL | Status | Build | Title |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in rows:
        anchor = url_anchor(result.url)
        title = "—"
        platform = "—"
        if result.html:
            match = TITLE_RE.search(result.html)
            if match:
                title = normalize_whitespace(match.group(1))
            platform = detect_platform(result.html)
        status = str(result.status) if result.status is not None else "err"
        label = title if title != "—" else result.url
        lines.append(
            f"| [{md_escape_inline(label)}](#{anchor}) | {result.url} | {status} | "
            f"{platform} | {md_escape_inline(title)} |"
        )
    lines.append("")
    return lines


def build_markdown() -> str:
    urls = discover_live_urls()
    print(f"Fetching {len(urls)} URLs from {SITE_BASE} …", file=sys.stderr)

    results: list[FetchResult] = []
    for index, url in enumerate(urls, start=1):
        print(f"  [{index}/{len(urls)}] {url}", file=sys.stderr)
        results.append(fetch_url(url))

    robots = fetch_url(ROBOTS_URL)
    robots_body = (robots.html or "").strip() if robots.html else "—"

    new_count = sum(1 for r in results if r.html and detect_platform(r.html) == "new (WR static)")
    legacy_count = sum(
        1 for r in results if r.html and detect_platform(r.html) == "legacy (Viamagus)"
    )
    error_count = sum(1 for r in results if r.html is None or (r.status and r.status >= 400))

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = [
        "# SEO inventory (live) — Writing Rodgers Solution",
        "",
        f"Fetched from **{SITE_BASE}** on **{generated}**. Re-run:",
        "",
        "```bash",
        "python3 scripts/generate-seo-live-md.py",
        "```",
        "",
        "Covers `<title>`, meta description/keywords/robots, canonical, Open Graph, "
        "Twitter cards, Google site verification, H1, and JSON-LD where present on the "
        "**currently served** HTML.",
        "",
        f"**URLs scanned:** {len(results)} (from live `sitemap.xml`; non-page entries like `robots.txt` excluded)",
        f"**Build detected:** {new_count} new (WR static), {legacy_count} legacy (Viamagus), "
        f"{error_count} errors/non-200",
        "",
        "## Live robots.txt",
        "",
        "```",
        robots_body,
        "```",
        "",
        "## Quick reference",
        "",
    ]

    sections: list[str] = []
    for result in results:
        sections.extend(render_live_section(result))

    footer = ["## Per-page detail", ""]
    return "\n".join(header + render_index_table(results) + footer + sections)


def main() -> None:
    markdown = build_markdown()
    OUTPUT.write_text(markdown, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
