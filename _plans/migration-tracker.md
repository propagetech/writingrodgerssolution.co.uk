# Site-wide migration tracker

Applies the work done on `index.html` (SEO + schema, semantic HTML, vanilla CSS/JS, Bootstrap removal, structural cleanup) to the rest of the site.

---

## Audit findings (2026-05-21)

### Site inventory

| Category | Count | Pages |
|---|---:|---|
| Homepage | 1 | `index.html` ✅ DONE |
| About | 1 | `about-us/` |
| Service (writing-format) | 8 | `dissertation-writing-help/`, `thesis-writing-help/`, `essay-writing-help/`, `report-writing-help/`, `case-study-assignment-help/`, `exam-preparation-help/`, `thesis-with-spss-nvivo-help/`, `academic-coaching-help/` |
| Service (subject) | 7 | `marketing-assignment-help/`, `management-assignment-help/`, `nursing-assignment-help/`, `accounting-assignment-help/`, `law-assignment-help/`, `it-assignment-help/`, `project-management-assignment-help/` |
| University | 14 | `bpp-assignment-help/`, `aston-…`, `coventry-…`, `university-college-birmingham-…`, `de-montfort-…`, `edinburgh-…`, `essex-…`, `middlesex-…`, `university-of-derby-…`, `…-east-london-…`, `…-greenwich-…`, `…-sunderland-…`, `…-salford-…`, `…-warwick-…` |
| Country | 6 | `assignment-help-in-uae-by-professionals/`, `…-oman-muscat/`, `…-canada/`, `…-australia/`, `…-uk-at-reasonable-price/`, `ireland-assignment-help/` |
| City | 8 | `assignment-help-in-london/`, `…-glasgow/`, `…-manchester/`, `…-leicester/`, `…-liverpool/`, `…-cardiff/`, `…-bristol/`, `…-birmingham/` |
| Blog | 1 | `blog/` |
| Other | 1 | `404.html` |
| Partials (reference only) | 7 | `partials/wr-*.html` — not actually included by any page; safe to ignore for now |

**Total non-homepage pages:** 46 (47 if we count `404.html`).

### Shared asset dependencies

Every non-homepage tested loads the same set:

```
../css/main-7.css       (Bootstrap 2.3.1 + plugin CSS — 153 KB)
../css/main-4.css       (Merriweather font self-host)
../css/main-6.css       (Open Sans 300 font)
../css/main-3.css       (Open Sans 400 font, sometimes mid-body)
../css/internal-styles.css
../css/wr-home.css      ← SAME FILE as homepage uses
../js/main-1.js through main-28.js (28 plugin scripts)
../js/main-20.js (self-hosted gtag.js, 360 KB each)
../js/wr-mobile-nav.js
../js/wr-nav-active.js
../js/wr-gallery.js
```

### Critical implication: `wr-home.css` is shared

The BEM rename we did to `wr-home.css` (`.navbar-inner` → `.wr-m3-app-bar__inner`, `.dropdown-menu` → `.wr-m3-nav__submenu`, `.nav` → `.wr-m3-nav`, etc.) **already affects every page on the site**. The other pages still use Bootstrap class names in their HTML (26-36 per page). Their basic styling still works because `main-7.css` (Bootstrap 2 base) is still loaded — but **homepage-specific tweaks that lived in `wr-home.css` no longer fire on those pages**.

Most-likely-visible breakage: nav dropdown styling (`.wr-component--header .dropdown-menu` rules don't match `.dropdown-menu` anymore), heading color tints, hover states.

### Per-page SEO content already exists

Sample titles from the live filesystem:

- About: *"About Writing Rodgers | UK Assignment Help Since 2017"*
- Dissertation: *"MBA Dissertation Help…"*
- BPP: *"BPP Assignment Help UK | Top Writers for BPP Coursework"*
- London: *"London's Premier Assignment Help – Where Smart Students Get Smarter!"*
- Australia: *"Australia Assignment Help – Essays, Dissertations, Exam Prep | Writing Rodgers"*

Every page has **unique client-crafted SEO content** (title, description, keywords, OG copy). This must be preserved when we modernise the `<head>`. Don't write generic SEO — extract per-page from the existing file.

### No build system

No SSI / template engine markers found. The 7 partials in `partials/` are stand-alone reference files; pages have their nav/footer/CTA markup inlined. **Edits must be applied to each page file directly** (or via a per-category script).

---

## Strategy: pilot + bulk

### Phase 0 — decide

- [ ] **`home.html` decision:** the old Viamagus homepage isn't in this repo (only the live site). Confirm there's no plan to bring it into the repo. If it stays only on the live server, leave alone — Phase 4 deals with it.
- [ ] **Wr-home.css stop-gap:** decide between
  1. **Patch wr-home.css** now to add legacy-Bootstrap-name aliases (`.navbar-inner, .wr-m3-app-bar__inner { … }`) so other pages don't visually regress until their turn. *Cheap insurance, ~30 min.*
  2. **Skip the alias and proceed straight to migrating** — accept transient visual drift on the other pages until their turn.

### Phase 1 — pilot one of each category (5 pages)

Apply the full 7-step pipeline (below) to each. These become the templates for bulk application.

- [ ] `about-us/` — high SEO value, unique content
- [ ] `dissertation-writing-help/` — service template
- [ ] `bpp-assignment-help/` — university template
- [ ] `assignment-help-in-london/` — city template
- [ ] `assignment-help-in-australia/` — country template

### Phase 2 — bulk-apply per category

Once each pilot template is locked in, propagate to the rest of its category. Most edits are mechanical class-rename / script-list-swap and could be done via a per-category shell script.

- [ ] Services × 14 (remaining writing-format + subject)
- [ ] Universities × 13 (remaining)
- [ ] Cities × 7 (remaining)
- [ ] Countries × 5 (remaining)

### Phase 3 — edge cases

- [ ] `blog/` — has its own template needs; revisit when reached
- [ ] `404.html` — already nearly clean (0 Bootstrap classes); small SEO + JS swap
- [ ] `partials/wr-*.html` — once the live pages no longer reference them, delete

### Phase 4 — site-wide cleanup

- [ ] Delete `css/main-7.css`, `main-3.css`, `main-4.css`, `main-6.css` from disk (after no page references them)
- [ ] Delete all 24 unused `js/main-*.js` plugin files
- [ ] Delete `js/wr-mobile-nav.js`, `js/wr-nav-active.js` (folded into `wr-nav.js`)
- [ ] Delete `partials/` directory if reference partials are unused

---

## Per-page pipeline (apply in this order)

Each page goes through the same 7 steps. **Earlier steps are zero-risk and pay off immediately; later steps need the earlier ones in place. Stop at any step if blocked — don't skip ahead.**

| # | Step | Risk | Reverts on failure? |
|---|---|---|---|
| 1 | Fetch live SEO via `curl` and preserve the client's `<title>`, description, keywords, OG, Twitter copy | None | n/a |
| 2 | Head SEO rewrite + JSON-LD `@graph` block (Organization + WebSite + WebPage, page-specific `WebPage.name`/`description`) | None | trivially |
| 3 | Semantic body upgrades: `<header>`, `<main>`, `<aside>` for mobile CTA, `<address>` for postal, `<time>` for year, skip link, social-icon `alt`, drop stray `</div>`s, drop logo microdata | Low | trivially |
| 4 | Performance: `js/main-20.js` self-host → Google CDN `<script async src="https://www.googletagmanager.com/gtag/js?id=G-MBCE6EP13C">`; verify `loading="lazy"` on images | None | trivially |
| 5 | Bootstrap → vanilla migration in HTML (`navbar`/`navbar-inner`/`dropdown`/`caret`/`row-fluid`/`spanN`/`btn`/`btn-navbar`/`featurette`/`brand`/`menu-center` → `wr-m3-*` / `wr-*` BEM names + drop `data-toggle`/`data-target`/`data-hover` attrs + drop Viamagus `data-component-name`/`data-bkg-image`/`data-sticky-header` attrs) | Medium | needs CSS check |
| 6 | JS plugin removal: drop jQuery, Bootstrap JS, all 24+ plugin scripts; add `wr-nav.js` + `wr-gallery.js`; drop inline `loadViaBkgImage` and `Viamagus_Website_Loader._init()` | Medium-high | needs JS verification |
| 7 | Structural flatten: empty divs, `wr-component__bg`+`wr-component__content`+`featurette` wrappers, deep footers; flatten footer to `<footer> → <div.wr-footer__inner> → <nav>/<ul>/<p>` | Low | revertable per-edit |
| ✓ | Validation: tag balance (`<div>` opens = closes), JSON-LD parses, visual diff vs. before screenshot, no console errors | n/a | — |

---

## Per-page checklist

Tick each step when complete. **Pilot pages drive template decisions for the rest of their category.**

### Phase 1 — pilots

| Page | 1. Fetch SEO | 2. Head | 3. Semantic | 4. Perf | 5. Bootstrap | 6. JS | 7. Flatten | ✓ Val |
|---|---|---|---|---|---|---|---|---|
| `index.html` | n/a | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `about-us/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `dissertation-writing-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bpp-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-london/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-australia/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Phase 2 — bulk (services)

| Page | 2. Head | 3. Semantic | 4. Perf | 5. Bootstrap | 6. JS | 7. Flatten | ✓ Val |
|---|---|---|---|---|---|---|---|
| `marketing-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `management-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `nursing-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `accounting-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `law-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `it-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `project-management-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `thesis-writing-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `essay-writing-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `report-writing-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `case-study-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `exam-preparation-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `thesis-with-spss-nvivo-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `academic-coaching-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Phase 2 — bulk (universities)

| Page | 2 | 3 | 4 | 5 | 6 | 7 | ✓ |
|---|---|---|---|---|---|---|---|
| `aston-university-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `coventry-university-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `university-college-birmingham-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `de-montfort-university-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `edinburgh-university-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `essex-university-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `middlesex-university-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `university-of-derby-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `university-of-east-london-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `university-of-greenwich-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `university-of-sunderland-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `university-of-salford-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `university-of-warwick-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Phase 2 — bulk (cities)

| Page | 2 | 3 | 4 | 5 | 6 | 7 | ✓ |
|---|---|---|---|---|---|---|---|
| `assignment-help-in-glasgow/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-manchester/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-leicester/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-liverpool/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-cardiff/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-bristol/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-birmingham/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Phase 2 — bulk (countries)

| Page | 2 | 3 | 4 | 5 | 6 | 7 | ✓ |
|---|---|---|---|---|---|---|---|
| `assignment-help-in-uae-by-professionals/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-oman-muscat/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-canada/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `assignment-help-in-uk-at-reasonable-price/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ireland-assignment-help/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Phase 3 — edge cases

| Page | 2 | 3 | 4 | 5 | 6 | 7 | ✓ |
|---|---|---|---|---|---|---|---|
| `blog/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `404.html` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Phase 4 — disk cleanup

- [ ] Confirm nothing references `css/main-7.css` → delete
- [ ] Confirm nothing references `css/main-3.css`, `main-4.css`, `main-6.css` → delete
- [ ] Confirm nothing references `js/main-{1..28}.js` → delete the unused ones
- [ ] Confirm nothing references `js/wr-mobile-nav.js`, `js/wr-nav-active.js` → delete
- [ ] Delete `partials/` directory if unreferenced

---

## Notes for the next session

- **Per-page SEO is unique** — never invent. Always extract from the existing file (and cross-check against the live URL when in doubt).
- **JSON-LD shape:** the Organization + WebSite nodes are constant across the site; only `WebPage.@id`, `WebPage.url`, `WebPage.name`, `WebPage.description`, `WebPage.primaryImageOfPage` vary per page.
- **Canonical URL** for each page: `https://www.writingrodgerssolution.co.uk/<slug>/` (or `/` for root).
- **Asset paths** on subpages use `../` prefix. The new `css/wr-vanilla.css` and `js/wr-nav.js` must be referenced as `../css/wr-vanilla.css` and `../js/wr-nav.js` on subpages.
- **Mobile CTA bar partial** is identical across pages — pick the cleaned-up version from `index.html` and paste it into each page.
- **Sticky/auto-hide nav** behaviour comes free once `wr-nav.js` is wired in.
