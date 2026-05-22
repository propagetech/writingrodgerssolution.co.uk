#!/usr/bin/env python3
"""Extract implemented SEO from all site HTML pages and write seo.md at repo root."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_BASE = "https://www.writingrodgerssolution.co.uk"
OUTPUT = ROOT / "seo.md"

HTML_GLOB = "*.html"

META_PATTERNS: dict[str, list[tuple[str, str | None]]] = {
    "description": [
        (r'<meta\s+content="([^"]*)"\s+name="description"\s*/?>', None),
        (r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>', None),
    ],
    "keywords": [
        (r'<meta\s+content="([^"]*)"\s+name="keywords"\s*/?>', None),
        (r'<meta\s+name="keywords"\s+content="([^"]*)"\s*/?>', None),
    ],
    "robots": [
        (r'<meta\s+name="robots"\s+content="([^"]*)"\s*/?>', None),
        (r'<meta\s+content="([^"]*)"\s+name="robots"\s*/?>', None),
    ],
    "google-site-verification": [
        (r'<meta\s+content="([^"]*)"\s+name="google-site-verification"\s*/?>', None),
    ],
    "og:title": [(r'<meta\s+content="([^"]*)"\s+property="og:title"\s*/?>', None)],
    "og:description": [(r'<meta\s+content="([^"]*)"\s+property="og:description"\s*/?>', None)],
    "og:type": [(r'<meta\s+content="([^"]*)"\s+property="og:type"\s*/?>', None)],
    "og:url": [(r'<meta\s+content="([^"]*)"\s+property="og:url"\s*/?>', None)],
    "og:site_name": [(r'<meta\s+content="([^"]*)"\s+property="og:site_name"\s*/?>', None)],
    "og:locale": [(r'<meta\s+content="([^"]*)"\s+property="og:locale"\s*/?>', None)],
    "og:image": [(r'<meta\s+content="([^"]*)"\s+property="og:image"\s*/?>', None)],
    "og:image:alt": [(r'<meta\s+content="([^"]*)"\s+property="og:image:alt"\s*/?>', None)],
    "twitter:card": [(r'<meta\s+content="([^"]*)"\s+name="twitter:card"\s*/?>', None)],
    "twitter:title": [(r'<meta\s+content="([^"]*)"\s+property="twitter:title"\s*/?>', None)],
    "twitter:description": [
        (r'<meta\s+content="([^"]*)"\s+property="twitter:description"\s*/?>', None)
    ],
    "twitter:image": [(r'<meta\s+content="([^"]*)"\s+property="twitter:image"\s*/?>', None)],
}

CANONICAL_RE = re.compile(
    r'<link\s+rel="canonical"\s+href="([^"]+)"\s*/?>',
    re.IGNORECASE,
)
TITLE_RE = re.compile(r"<title>\s*(.*?)\s*</title>", re.DOTALL | re.IGNORECASE)
LANG_RE = re.compile(r'<html[^>]*\slang="([^"]+)"', re.IGNORECASE)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL | re.IGNORECASE)
LD_JSON_RE = re.compile(
    r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
    re.DOTALL | re.IGNORECASE,
)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(text)).strip()


def first_match(html: str, patterns: list[tuple[str, str | None]]) -> str | None:
    for pattern, _ in patterns:
        match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if match:
            return normalize_whitespace(match.group(1))
    return None


def extract_meta(html: str) -> dict[str, str | None]:
    return {key: first_match(html, patterns) for key, patterns in META_PATTERNS.items()}


def public_url(path: Path) -> str:
    if path.name == "index.html":
        return f"{SITE_BASE}/"
    return f"{SITE_BASE}/{path.name}"


def discover_pages() -> list[Path]:
    return sorted(ROOT.glob(HTML_GLOB))


def flatten_graph(data: object) -> list[dict]:
    nodes: list[dict] = []
    if isinstance(data, dict):
        graph = data.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                if isinstance(item, dict):
                    nodes.append(item)
        elif "@type" in data:
            nodes.append(data)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                nodes.extend(flatten_graph(item))
    return nodes


def node_by_type(nodes: list[dict], schema_type: str) -> dict | None:
    for node in nodes:
        if node.get("@type") == schema_type:
            return node
    return None


def breadcrumb_trail(node: dict | None) -> str | None:
    if not node:
        return None
    items = node.get("itemListElement")
    if not isinstance(items, list):
        return None
    names: list[str] = []
    for item in items:
        if isinstance(item, dict) and item.get("name"):
            names.append(str(item["name"]))
    return " › ".join(names) if names else None


def extract_schema(html: str) -> dict[str, object | None]:
    out: dict[str, object | None] = {
        "has_json_ld": False,
        "webpage_name": None,
        "webpage_description": None,
        "webpage_url": None,
        "service_name": None,
        "service_type": None,
        "service_description": None,
        "university_name": None,
        "university_url": None,
        "breadcrumbs": None,
        "schema_types": None,
    }
    match = LD_JSON_RE.search(html)
    if not match:
        return out

    raw = match.group(1).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        out["has_json_ld"] = True
        return out

    nodes = flatten_graph(data)
    if not nodes:
        return out

    out["has_json_ld"] = True
    types = sorted({str(n.get("@type")) for n in nodes if n.get("@type")})
    out["schema_types"] = ", ".join(types)

    webpage = node_by_type(nodes, "WebPage")
    service = node_by_type(nodes, "Service")
    university = node_by_type(nodes, "CollegeOrUniversity")
    breadcrumb = node_by_type(nodes, "BreadcrumbList")

    if webpage:
        out["webpage_name"] = webpage.get("name")
        out["webpage_description"] = webpage.get("description")
        out["webpage_url"] = webpage.get("url")
    if service:
        out["service_name"] = service.get("name")
        out["service_type"] = service.get("serviceType")
        out["service_description"] = service.get("description")
    if university:
        out["university_name"] = university.get("name")
        out["university_url"] = university.get("url")
    out["breadcrumbs"] = breadcrumb_trail(breadcrumb)
    return out


def extract_h1(html: str) -> str | None:
    match = H1_RE.search(html)
    if not match:
        return None
    inner = re.sub(r"<[^>]+>", "", match.group(1))
    return normalize_whitespace(inner)


def page_slug_for_anchor(path: Path) -> str:
    if path.name == "index.html":
        return "home"
    return path.name.replace(".html", "")


def md_escape_inline(text: str) -> str:
    return text.replace("|", "\\|")


def format_field(label: str, value: str | None) -> list[str]:
    if not value:
        return [f"- **{label}:** —"]
    return [f"- **{label}:** {md_escape_inline(value)}"]


def render_page_section(path: Path, html: str) -> list[str]:
    meta = extract_meta(html)
    schema = extract_schema(html)
    title_match = TITLE_RE.search(html)
    title = normalize_whitespace(title_match.group(1)) if title_match else None
    canonical_match = CANONICAL_RE.search(html)
    canonical = canonical_match.group(1) if canonical_match else None
    lang_match = LANG_RE.search(html)
    lang = lang_match.group(1) if lang_match else None
    h1 = extract_h1(html)
    url = canonical or public_url(path)

    lines: list[str] = [
        f"### {title or path.stem}",
        "",
        f"- **Source file:** `{path.name}`",
        f"- **Public URL:** {url}",
    ]
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
        lines.extend(format_field("google-site-verification", meta.get("google-site-verification")))

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


def render_index_table(pages: list[tuple[Path, str | None, str | None]]) -> list[str]:
    lines = [
        "| Page | URL | Title |",
        "| --- | --- | --- |",
    ]
    for path, url, title in pages:
        anchor = page_slug_for_anchor(path)
        label = title or path.stem
        lines.append(
            f"| [{md_escape_inline(label)}](#{anchor}) | {url} | {md_escape_inline(title or '—')} |"
        )
    lines.append("")
    return lines


def build_markdown() -> str:
    pages = discover_pages()
    summary_rows: list[tuple[Path, str | None, str | None]] = []
    sections: list[str] = []

    for path in pages:
        html = path.read_text(encoding="utf-8")
        title_match = TITLE_RE.search(html)
        title = normalize_whitespace(title_match.group(1)) if title_match else None
        canonical_match = CANONICAL_RE.search(html)
        url = canonical_match.group(1) if canonical_match else public_url(path)
        summary_rows.append((path, url, title))
        section = render_page_section(path, html)
        anchor = page_slug_for_anchor(path)
        section[0] = f"### {title or path.stem} {{#{anchor}}}"
        sections.extend(section)

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = [
        "# SEO inventory — Writing Rodgers Solution",
        "",
        f"Auto-generated from HTML on **{generated}**. Re-run:",
        "",
        "```bash",
        "python3 scripts/generate-seo-md.py",
        "```",
        "",
        "Covers `<title>`, meta description/keywords/robots, canonical, Open Graph, "
        "Twitter cards, Google site verification, H1, and JSON-LD (`Organization`, "
        "`WebSite`, `WebPage`, `Service`, `CollegeOrUniversity`, `BreadcrumbList` where present).",
        "",
        f"**Pages:** {len(pages)}",
        "",
        "## Quick reference",
        "",
    ]
    footer = ["## Per-page detail", ""]
    return "\n".join(header + render_index_table(summary_rows) + footer + sections)


def main() -> None:
    markdown = build_markdown()
    OUTPUT.write_text(markdown, encoding="utf-8")
    page_count = len(discover_pages())
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({page_count} pages)")


if __name__ == "__main__":
    main()
