# Plan — vanilla rewrite of jQuery / Bootstrap 2 / plugin stack for `index.html`

## Approved decisions

- **Scope:** `index.html` only. Other pages (home.html, blog, service pages) stay on the old Viamagus stack. Files in `js/` and `css/` are not deleted from disk; we only stop loading them from `index.html`.
- **New file names:** `css/wr-bootstrap-shim.css` + `js/wr-nav.js`.
- **Dropdown hover delay:** **200 ms** (snappy — matches the project's existing Material-3 motion language; `wr-m3-*` classes already in use).
- **Smooth-scroll offset:** measured from CSS — header is **64 px mobile, ~108 px desktop**. Use CSS custom property `--wr-header-h` set per breakpoint, with `scroll-margin-top: calc(var(--wr-header-h) + 16px)` on every `section[id]`.
- **Browser support floor:** modern evergreen only (latest 2 versions of Chrome / Edge / Firefox / Safari). No IE, no Safari < 13. CSS custom properties, CSS Grid, `position: sticky`, `:focus-within`, `scroll-behavior`, and native `loading="lazy"` are all in.

## Goal

Replace ~1.5 MB of CSS/JS libraries (Bootstrap 2.3.1, jQuery 1.9.0, Magnific Popup, Galleria, WOW.js, Backstretch, Lazy Load, Modernizr, HTML5 Shiv, Respond.js, jQuery One Page Nav, jQuery Parallax, JW Player, jQuery mb.YTPlayer, PickMeUp, jQuery Raty, jQuery Validation, jQuery Form, International Telephone Input, Bootstrap Combobox, Component.io require, Viamagus loaders) with **2 small new files** plus the existing already-vanilla `wr-gallery.js`.

No markup changes — only `<link>` / `<script>` tag swaps in the head and body bottom.

## Inventory

### CSS

| File | Verdict |
|---|---|
| `main-7.css` (153 KB Bootstrap 2 + plugin CSS) | **Replace** with `wr-bootstrap-shim.css`. Only ~20 selectors are actually used — the rest is unused plugin CSS. |
| `main-4.css`, `main-6.css`, `main-3.css` (3 × `@font-face`) | **Drop** — duplicate self-host of Merriweather + Open Sans 300/400, fonts not used by the new design (Playfair Display + Quicksand load from CDN). |
| `internal-styles.css` (20 KB) | **Keep** — drives `.wr-component--*` styles. |
| `wr-home.css` (59 KB) | **Keep** — active stylesheet. |

### JS — drop entirely (unused on index.html)

| File | Library | Why unused |
|---|---|---|
| `main-15.js` | Magnific Popup | Gallery uses `wr-gallery.js` |
| `main-26.js` | Backstretch | Hero uses plain CSS background-image |
| `main-17.js`, `main-19.js` | Galleria + Classicmod theme | Gallery uses `wr-gallery.js` |
| `main-21.js` | WOW.js | No `.wow` classes on page |
| `main-5.js` | jQuery One Page Nav | Replaced by native `scroll-behavior: smooth` |
| `main-14.js` | Modernizr 2.6.2 | All target browsers natively support the features it tested |
| `main-22.js` | jQuery mb.YTPlayer | No background-video embed |
| `main-8.js` | Lazy Load | All `<img>` use native `loading="lazy"` |
| `main-11.js` | PickMeUp datepicker | No datepicker |
| `main-12.js` | jQuery Raty | No star ratings |
| `main-9.js`, `main-25.js` | jQuery Validation + Form | No forms |
| `main-13.js` | Component.io require runtime | Dependency of unused plugins |
| `main-24.js` | International Telephone Input | No phone input field |
| `main-10.js` | Bootstrap Combobox | No combobox |
| `main-2.js` | jQuery Parallax | No parallax |
| `main-18.js` | JW Player | No JW Player embed; videos are native YouTube iframes |
| `main-16.js` | HTML5 Shiv | IE8 polyfill — dropped (modern evergreen only) |
| `main-6.js` | Respond.js | IE media-query polyfill — dropped |
| `main-1.js` | Viamagus layoutManager | Plugin glue; no hook points on the new homepage |
| `main-23.js` | Bootstrap 2 JS | Replaced by `wr-nav.js` |
| `main-7.js` | jQuery 1.9.0 | Replaced — no jQuery callers will remain |
| `main-27.js`, `main-28.js` | Viamagus transaction manager + loader | No AJAX on page |
| `main-3.js`, `main-4.js` | Viamagus loaders | Replaced by a 6-line init in `wr-nav.js` |
| Inline `loadViaBkgImage()` | Backstretch destroy shim | Dead — no backstretch loaded |

### JS — keep

| File | Reason |
|---|---|
| `main-20.js` (async GTM) | Analytics — must keep |
| Inline `gtag('config', 'G-MBCE6EP13C')` | Analytics config |
| `wr-gallery.js` | Already vanilla, drives the gallery lightbox |
| `wr-nav-active.js` | Vanilla — folded into new `wr-nav.js` |
| `wr-mobile-nav.js` | **Rewrite as part of new `wr-nav.js`** (currently depends on jQuery + Bootstrap collapse) |

## Replacement strategy

### 1. `css/wr-bootstrap-shim.css` (target ~4–6 KB)

Bootstrap-2 facsimile providing only the rules the homepage's markup actually uses, with the **same class names** so no markup changes are required. Sections:

- Reset / box-sizing
- `.container`, `.container-fluid` — max-width + auto margins
- `.row-fluid` + `.span3` / `.span6` — CSS Grid (`1fr 2fr 1fr` for footer)
- `.btn`, `.btn-navbar`, `.icon-bar` — flat button base + hamburger bars
- `.navbar`, `.navbar-inner`, `.navbar-inverse` — flexbox header bar
- `.nav`, `.nav-collapse`, `.collapse`, `.collapse.in` — nav list states
- `.dropdown`, `.dropdown-menu`, `.dropdown-toggle`, `.caret` — submenu + caret triangle
- `.featurette` — clearfix container
- `--wr-header-h` custom property + `scroll-margin-top` on `section[id]`
- `html { scroll-behavior: smooth }`

### 2. `js/wr-nav.js` (target ~3–4 KB)

```
function setupHamburger()      // mobile hamburger toggles .nav-collapse.in
function setupDropdowns()      // click .dropdown-toggle → toggle .open;
                               // hover on desktop with 200ms delay;
                               // outside-click closes
function setupCloseNavOnLink() // mobile only — clicking any wr-nav-link closes the panel
function setupActiveLink()     // folded in from wr-nav-active.js
```

No sticky-header JS (CSS `position: sticky`). No smooth-scroll library (native + `scroll-margin-top`). No event-delegation library — plain `addEventListener`. Runs on `DOMContentLoaded`.

### 3. `wr-gallery.js` — no change (already vanilla)

## Markup changes in `index.html`

**Head — remove:**
- `<link href="css/main-7.css">` (line 33)
- `<link href="css/main-4.css">` (line 35)
- `<link href="css/main-6.css">` (line 44)
- `<script src="js/main-7.js">` through `<script src="js/main-6.js">` (lines 85–91)

**Head — add:**
- `<link rel="stylesheet" href="css/wr-bootstrap-shim.css">`

**Body — remove:**
- Inline `loadViaBkgImage` script (lines 224–226)
- `<link href="css/main-3.css">` (line 229, mid-body)

**Body bottom — remove:**
- Lines 821–838: `main-17`, `main-19`, `main-21`, `main-5`, `main-14`, `main-22`, `main-8`, `main-28`, `main-27`, `main-11`, `main-12`, `main-9`, `main-25`, `main-13`, `main-24`, `main-10`, `main-2`, `main-18` (18 files)
- `wr-mobile-nav.js`, `wr-nav-active.js` (lines 839–840) — folded into `wr-nav.js`
- `main-3.js`, `main-4.js` (lines 842–843)
- Inline `Viamagus_Website_Loader._init()` call (lines 844–846)

**Body bottom — keep:** `wr-gallery.js`

**Body bottom — add:** `<script src="js/wr-nav.js" defer></script>`

**Keep untouched:** GTM (`main-20.js` async at line 36) + inline `gtag` config (lines 37–43).

## Behavior preservation matrix

| Behavior | Currently provided by | After |
|---|---|---|
| Sticky header on scroll | Viamagus loader adds `.wr-component--sticky` class on scroll | CSS `position: sticky; top: 0; z-index: 1010` |
| Mobile hamburger toggles nav drawer | Bootstrap collapse + `wr-mobile-nav.js` | `wr-nav.js` toggles `.in` class |
| Desktop nav dropdowns (hover) | Bootstrap dropdown + `data-hover` plugin | CSS `:hover` + `:focus-within` with 200ms `transition-delay` |
| Desktop nav dropdowns (keyboard / click) | Bootstrap dropdown click handler | `wr-nav.js` — toggles `aria-expanded` |
| Mobile submenu accordion | Bootstrap collapse | `wr-nav.js` — expands child `.dropdown-menu` |
| Click outside dropdown closes | Bootstrap dropdown global handler | `wr-nav.js` — single `document.click` listener |
| Active link highlighting | `wr-nav-active.js` | Folded into `wr-nav.js` |
| Anchor smooth scroll | jQuery One Page Nav | CSS `scroll-behavior: smooth` + `scroll-margin-top` |
| Gallery thumbnail → lightbox | `wr-gallery.js` | Unchanged |
| Mobile CTA bar always visible | CSS only (already) | Unchanged |
| Floating WhatsApp button | CSS only (already) | Unchanged |
| YouTube embeds | Native iframe | Unchanged |
| Image lazy-load | Native `loading="lazy"` | Unchanged |
| Footer 3-column grid (span3/span6/span3) | Bootstrap 2 grid | CSS Grid in shim |
| Analytics (GA4 via GTM) | `main-20.js` + inline `gtag` | Unchanged |

## Estimated performance impact

| Metric | Before | After | Saved |
|---|---:|---:|---:|
| CSS shipped (uncompressed) | ~233 KB | ~80 KB | ~150 KB |
| JS shipped (uncompressed) | ~1.7 MB | ~370 KB (GTM 360 KB + wr-nav 4 KB + wr-gallery 7 KB) | ~1.35 MB |
| HTTP requests for CSS/JS | 5 CSS + 28 JS = 33 | 3 CSS + 3 JS = 6 | 27 |
| Render-blocking head scripts | 7 sync scripts | 0 sync scripts (GTM async, wr-nav uses `defer`) | 7 |

## Phased implementation order

1. **Write `css/wr-bootstrap-shim.css`** — link it in `index.html` alongside `main-7.css` (defensive). Verify the page renders identically. **← stop for review**
2. **Remove `main-7.css`** from `index.html`. Verify visually that the shim is sufficient.
3. **Write `js/wr-nav.js`** — add to `index.html`, then progressively remove jQuery, Bootstrap 2 JS, `wr-mobile-nav.js`, `wr-nav-active.js`.
4. **Drop the unused plugin scripts** in groups: lightbox/gallery group → form/datepicker/rating group → modernizr/shiv/respond polyfills.
5. **Drop Viamagus loaders and inline init.** Drop the `main-3.css` / `main-4.css` / `main-6.css` font self-hosts. Final cleanup.

## Testing checklist (run after each phase)

- [ ] Renders pixel-identical on desktop (1920×1080, 1366×768)
- [ ] Renders pixel-identical on mobile (375×667 iPhone SE, 414×896 iPhone 11)
- [ ] Hamburger nav opens and closes on mobile
- [ ] Tapping a submenu parent expands the submenu on mobile
- [ ] Hovering "Our Services" / "Universities" / "Branches" / "Cities" on desktop opens the dropdown (200ms delay)
- [ ] Clicking outside an open dropdown closes it
- [ ] Header stays pinned to top on scroll
- [ ] Anchor links smooth-scroll, target heading lands below sticky header
- [ ] Gallery thumbnail click opens lightbox, ← / → arrows work, Esc closes, swipe works on mobile
- [ ] All 5 YouTube iframes load and play
- [ ] WhatsApp / Email / Call CTAs all open the right app/intent
- [ ] Mobile CTA bar visible at bottom on small screens
- [ ] Floating WhatsApp button visible bottom-right on desktop
- [ ] Footer 3-column grid renders correctly desktop; collapses to single column below ~768 px
- [ ] GTM/GA4 still fires (verify in DevTools Network tab for `collect` requests)
- [ ] No JS errors in DevTools console
- [ ] Lighthouse Performance score before vs after
