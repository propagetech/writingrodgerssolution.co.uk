---
name: writingrodgers-new-page
description: Go-live checklist for new Writing Rodgers static HTML pages (Pascal-Case root .html, GitHub Pages). Use when adding a blog post, service page, or any new page to writingrodgerssolution.co.uk.
---

# Writing Rodgers — new page go-live

Static site: flat Pascal-Case `.html` at repo root, deployed to `www.writingrodgerssolution.co.uk` via GitHub Pages. No build step; nav, footer, and contact are **inlined** in each file.

## Template choice

| Page type | Clone from |
|-----------|------------|
| Blog / educational article | [blog.html](blog.html) or [Blog-What-Is-A-Dissertation.html](Blog-What-Is-A-Dissertation.html) |
| Service / conversion page | [Dissertation-Writing-Help.html](Dissertation-Writing-Help.html) |

Do **not** copy the `wr-blog-index` hub block onto individual blog posts — that section belongs only on [blog.html](blog.html).

## Checklist (run in order)

1. **Filename** — Pascal-Case, descriptive: `Blog-Topic-Name.html` or `Service-Name.html`. URL = `https://www.writingrodgerssolution.co.uk/{Filename}`.

2. **`<head>`** — Unique per page:
   - `<title>` and meta `description` / `keywords`
   - `<link rel="canonical">` and `og:url` match the new filename exactly
   - JSON-LD: update `WebPage` `name`, `description`, `url`, `@id`; extend `BreadcrumbList` (Home → Blog → article, or Home → service)

3. **Body**
   - Breadcrumb + `wr-sub-hero` (H1 + lead + UK/India WhatsApp CTAs)
   - Article sections: `wr-component--image-text` / `wr-component--richtext`
   - Blog posts: CTA button to related **service** page (educational vs conversion)
   - `wr-contact` block before footer (copy from blog.html)

4. **Asset paths** — Root pages use `css/`, `imgs/`, `js/` (never `../js/`).

5. **Nav/footer** — Root-relative links (`index.html`, `blog.html`, `Dissertation-Writing-Help.html`, …). Match an existing page; do not bulk-rewrite all 46 pages.

6. **Blog hub** — If adding a blog post, add a `wr-blog-card` entry in the `wr-blog-index__grid` on [blog.html](blog.html): thumbnail (`imgs/…` from the article hero), `<time datetime="YYYY-MM-DD">`, title, excerpt, and `href` to the new post.

7. **Sitemap** — Add `<url>` to [sitemap.xml](sitemap.xml) (`changefreq` monthly, `priority` 0.75–0.8).

8. **SEO inventory** — Run `python3 scripts/generate-seo-md.py` to refresh [seo.md](seo.md). After deploy, optionally `python3 scripts/generate-seo-live-md.py`.

9. **Redirects** — New URLs only; no 301 map needed ([redirect-checklist.md](redirect-checklist.md)).

10. **Human review** — Copy, meta titles, keyword overlap with service pages, image alts, mobile nav. Do not commit or push unless the user asks.

## Avoid

- Inventing SEO without reading an existing page’s pattern
- Running [fix_all_pages.py](fix_all_pages.py) unless `partials/` exists in the repo
- Changing URL shapes (folder slugs) without an explicit redirect plan
- Autonomous publish / git push

## Blog structure

- [blog.html](blog.html) — hub only (lists all posts); do not put full article body here
- [Blog-PSW-Visa-Tips.html](Blog-PSW-Visa-Tips.html) → CTA [Assignment-Help-in-UK-at-Reasonable-Price.html](Assignment-Help-in-UK-at-Reasonable-Price.html)
- [Blog-What-Is-A-Dissertation.html](Blog-What-Is-A-Dissertation.html) → CTA [Dissertation-Writing-Help.html](Dissertation-Writing-Help.html)
- [Blog-What-Is-SPSS.html](Blog-What-Is-SPSS.html) → CTA [Thesis-with-SPSS-Nvivo-Help.html](Thesis-with-SPSS-Nvivo-Help.html)
