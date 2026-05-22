# SEO + Semantic + Schema Plan — `index.html`

## Confirmations
- **Target:** `/Users/chetan/Downloads/jeevitha/writingrodgerssolution.co.uk/index.html`
- **Slug for plan file:** `index`
- **Canonical destination:** `https://www.writingrodgerssolution.co.uk/`
- **Brand context (inferred from file):** Writing Rodgers Solution LLP — UK-facing assignment/dissertation help service, India-registered LLP (LLPIN AAY-5206, ROC Kolkata), serving students in UK / Australia / UAE / Oman / Canada / Ireland since 2017. Partners: Subham (lead academic tutor) and Tania (operations). Contact via WhatsApp/phone (+91 7044974618) and email — no on-site forms. `<NEEDS INPUT>` on whether Subham + Tania are co-founders or only designated partners.
- **Language detected:** Content is UK English (£-region focus, "criteria", "rubric", UK-spelling words) — propose `en-GB`. Currently `<html>` has **no `lang` attribute** (line 2).
- **Existing JSON-LD in file:** None (`grep` confirms 0 `application/ld+json` blocks).
- **Google rich-result gallery cross-check:** Done via WebFetch against `https://developers.google.com/search/docs/appearance/structured-data/search-gallery` — see Part 3 for what's eligible today.

---

## PART 1A — Current semantic structure (audit)

### Brief tree (as-is)

```
html (no lang)
└─ body
   ├─ a.live-chat-fixed (floating WhatsApp)            [97]
   ├─ div.wr-mobile-cta-bar (fixed mobile contact bar) [100]
   ├─ </div>  ← STRAY ORPHAN CLOSE                     [129]
   ├─ div.wr-page
   │  └─ div.wr-page__container
   │     └─ div.wr-component--header (id=menu)         [136]   ← should be <header>
   │        └─ div.wr-component__bg
   │           └─ div.wr-component__content.navbar
   │              ├─ button.btn-navbar (hamburger)     [141]
   │              ├─ div.wr-business-logo              [149]   ← microdata Organization
   │              └─ nav.nav-collapse                  [155]
   │                 └─ ul#menu-nav (Home / About / Partners / Services / Universities / Branches / Cities / How / Why / Testimonials / Contact / Blog)
   ├─ section#wr-hero                                  [251]
   │  └─ <h1> "UK assignment & dissertation support…"  [256]   ← only h1, good
   ├─ section#wr-how-it-works                          [276]
   │  ├─ h2 "How it works"
   │  └─ div.wr-steps
   │     └─ div.wr-step ×3 (numbered 1/2/3 + h3)       [280-294] ← should be <ol>
   ├─ div.wr-component--image-text (id=wr-image-text-7952) [297] ← should be <section>
   │  └─ h2 with inline <span style="font-size:24px">  [305]   ← presentational leakage on heading
   ├─ section#wr-team                                  [321]
   │  ├─ h2 "Meet the people behind your grade"
   │  └─ article.wr-team-card ×2 (Subham, Tania, h3)
   ├─ section#wr-gallery                               [348]
   │  ├─ h2 "Real moments with our students"
   │  └─ ul.wr-gallery__grid (13 li items, lightbox)
   ├─ div.wr-lightbox role=dialog                      [454]   ← could be native <dialog>
   ├─ section#wr-featured-video (h2 + iframe)          [465]
   ├─ section#wr-shorts (h2 + ul of 4 iframes)         [475]
   ├─ section#wr-reach (h2)                            [499]
   ├─ section#wr-services                              [513]
   │  ├─ h2 "What we help with"
   │  ├─ h3 "By subject"                               [517]
   │  ├─ div.wr-services-grid                                 ← loose <a> siblings, no ul/li
   │  │  └─ a.wr-service-card ×6 (each contains h3)   [519-548] ← h3 inside h3 group; should be h4
   │  ├─ h3 "By writing format"                        [551]
   │  └─ div.wr-services-grid
   │     └─ a.wr-service-card ×7 (each contains h3)   [553-587] ← same h3-under-h3 issue
   ├─ section#wr-tutoring (h2)                         [595]
   ├─ section#wr-why (h2 + ul)                         [605]
   ├─ section#wr-testimonials                          [622]
   │  ├─ h2 "What students say"
   │  └─ article.wr-testimonial-card ×3 (blockquote + cite — good)
   ├─ section#wr-contact (h2)                          [658]
   ├─ div.wr-component--spacer                         [687]   ← layout-only div
   └─ footer.wr-component--footer                      [691]
      └─ div.span3 / div.span6 / div.span3 (Bootstrap-2 grid)
         └─ social <img> with NO alt attribute         [707,710,713]
```

### Issues flagged (with `file:line`)

| # | Issue | Location |
|---|---|---|
| 1 | `<html>` missing `lang` attribute | `index.html:2` |
| 2 | Site header rendered as `<div>` not `<header>` | `index.html:136` |
| 3 | Stray orphan `</div>` (no matching open) | `index.html:129` |
| 4 | No `<main>` landmark wrapping primary content | `index.html:251-686` |
| 5 | No skip-to-content link for keyboard users | (absent) |
| 6 | Image-text component as `<div>` — has a heading, belongs in `<section>` | `index.html:297` |
| 7 | Spacer `<div>` used for layout-only whitespace | `index.html:687-690` |
| 8 | Lightbox is `<div role="dialog">` — could use native `<dialog>` | `index.html:454` |
| 9 | "How it works" steps are `<div>`s but content is sequentially numbered — should be `<ol>` | `index.html:279-295` |
| 10 | Service-card lists are loose `<a>` siblings — should be `<ul><li>` | `index.html:518-549`, `index.html:552-588` |
| 11 | Heading-level: `<h3>` group ("By subject" / "By writing format") followed by sibling `<h3>` card titles — cards should be `<h4>` | `index.html:517,520,525,530,535,540,545`, `index.html:551,554,559,564,569,574,579,584` |
| 12 | Inline `<span style="font-size: 24px">` wrapping h2 content (presentational on heading) | `index.html:305` |
| 13 | Footer social-icon `<img>` tags have NO `alt` attribute (informative images) | `index.html:707`, `index.html:710`, `index.html:713` |
| 14 | Footer link list uses inline `<br><br>` for spacing instead of `<nav>` + `<ul>` | `index.html:698-715` |
| 15 | Legacy Bootstrap-2/3 classes still present: `navbar-inverse`, `container-fluid`, `row-fluid`, `span3`/`span6`, `brand`, `btn-navbar`, `nav-collapse`, `dropdown-toggle`, `caret`, `<b class="caret">` | throughout 136-247, 694-726 |
| 16 | Microdata (`itemscope`, `itemtype="…/Organization"`) on logo — fine but JSON-LD is preferred and richer | `index.html:149-152` |
| 17 | Inline presentational styles in markup | `index.html:98,138,151,252,299,329,335,688,692,698,707,710,713` |
| 18 | Mobile CTA bar (lines 100-128) lives outside any landmark — should sit inside `<header>` or be marked `<aside role="complementary">` | `index.html:100-128` |
| 19 | Footer copyright trademark text wraps in `<strong>` but year (`© 2026`) sits inside it; `<time>` would be appropriate for the year | `index.html:717-720` |
| 20 | UK contact address in trust strip / contact section is plain `<li>` / `<p>` — should use `<address>` element | `index.html:342`, `index.html:682`, `index.html:683-684` |

---

## PART 1B — Proposed semantic structure

```
<html lang="en-GB">
  <head> … (see Part 2) </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>                                    [CHANGE: new]

    <header class="site-header" id="menu">                                                   [CHANGE: <div> → <header>]
      <a class="site-header__brand" href="/" aria-label="Writing Rodgers — Home">
        <img src="imgs/logo.webp" alt="Writing Rodgers Solution" width="179" height="…">
      </a>
      <button class="site-header__toggle" type="button" aria-controls="primary-nav"
              aria-expanded="false">Menu</button>                                            [CHANGE: drop .btn-navbar / .icon-bar legacy markup]
      <nav class="site-nav" id="primary-nav" aria-label="Primary">                           [CHANGE: drop .nav-collapse.collapse]
        <ul class="site-nav__list">
          <li><a href="#wr-hero">Home</a></li>
          <li><a href="about-us/">About</a></li>
          <li><a href="#wr-team">Partners</a></li>
          <li class="has-submenu">
            <a href="#wr-services" aria-expanded="false" aria-haspopup="true">Our services</a>
            <ul class="site-nav__submenu"> … </ul>                                           [CHANGE: drop <b class="caret">, replace with CSS chevron]
          </li>
          <li class="has-submenu"><a …>Assignments by university</a><ul>…</ul></li>
          <li><a href="#wr-how-it-works">How it works</a></li>
          <li><a href="#wr-why">Why us</a></li>
          <li><a href="#wr-testimonials">Testimonials</a></li>
          <li class="has-submenu"><a …>Our branches</a><ul>…</ul></li>
          <li class="has-submenu"><a …>Assignment service by cities</a><ul>…</ul></li>
          <li><a class="site-nav__cta" href="#wr-contact">Contact</a></li>
          <li><a href="blog/">Blog</a></li>
        </ul>
      </nav>
    </header>

    <aside class="mobile-cta-bar" aria-label="Quick contact">                                 [CHANGE: <div> → <aside>; move stray </div>]
      <a class="mobile-cta-bar__wa" href="https://wa.me/917044974618?text=…">
        <svg aria-hidden="true">…</svg>
        <span>WhatsApp <small>Free quote</small></span>
      </a>
      <a class="mobile-cta-bar__call" href="tel:+917044974618" aria-label="Call India team">…</a>
      <a class="mobile-cta-bar__email" href="mailto:…" aria-label="Email Writing Rodgers">…</a>
    </aside>

    <a class="floating-wa" href="https://wa.me/917044974618?text=…"
       aria-label="Chat with Writing Rodgers on WhatsApp">
      <img src="imgs/image-20.webp" alt="" width="50" height="50">                          [CHANGE: alt="" because the <a> has aria-label]
    </a>

    <main id="main">                                                                         [CHANGE: new wrapper]

      <section class="hero" id="wr-hero" aria-labelledby="hero-title">
        <p class="hero__tagline">Stress Less, Score More</p>
        <h1 id="hero-title">UK assignment &amp; dissertation support you can trust</h1>     ← ONLY h1
        <p class="hero__sub">Writing Rodgers Solution LLP has helped students …</p>
        <p class="hero__sub hero__sub--short">UK assignment &amp; dissertation help since 2017 …</p>
        <p class="hero__actions">
          <a class="btn btn--primary" href="https://wa.me/917044974618?text=…">Get a free quote on WhatsApp</a>
          <a class="btn btn--secondary" href="mailto:…">Email us</a>
          <a class="btn btn--secondary" href="tel:+917044974618">Call +91 7044974618</a>
        </p>
        <ul class="trust-strip">
          <li>Supporting students since 2017</li>
          <li>India-registered LLP (LLPIN AAY-5206) · UK contact team</li>
          <li>Plagiarism-free · Talk to your expert directly</li>
          <li>24/7 response on WhatsApp</li>
        </ul>
        <p class="hero__intl">WhatsApp us: <a href="https://wa.me/917044974618?text=…">+91 7044974618</a></p>
      </section>

      <section class="how-it-works" id="wr-how-it-works" aria-labelledby="how-title">
        <h2 id="how-title">How it works</h2>
        <p class="section-lead">Three steps when your deadline is close…</p>
        <ol class="steps">                                                                   [CHANGE: div.wr-steps → ol.steps]
          <li class="step">
            <h3>Send your brief</h3>
            <p>Message us on WhatsApp or email …</p>
          </li>
          <li class="step"><h3>Get a quote &amp; expert</h3><p>…</p></li>
          <li class="step"><h3>Review &amp; submit</h3><p>…</p></li>
        </ol>
      </section>

      <section class="featurette" id="wr-featurette" aria-labelledby="featurette-title">    [CHANGE: <div> → <section>; drop id wr-image-text-7952]
        <h2 id="featurette-title">Essays, reports, dissertations &amp; exam prep: one team</h2>   [CHANGE: drop inline <span style>]
        <p>From nursing case studies to SPSS dissertations and MBA reports …</p>
        <p><a class="link-arrow" href="#wr-services">Browse all subjects →</a></p>
      </section>

      <section class="team" id="wr-team" aria-labelledby="wr-team-heading">
        <p class="team__since">Writing Rodgers Solution LLP · Est. 2017</p>
        <h2 id="wr-team-heading">Meet the people behind your grade</h2>
        <p class="team__lead">You speak directly with our partners and tutors …</p>
        <ul class="team__grid">                                                              [CHANGE: wrap articles in <ul><li>]
          <li>
            <article class="team-card">
              <figure>
                <img src="imgs/subham.jpeg" alt="Subham, partner at Writing Rodgers Solution, at Tower Bridge London" …>
              </figure>
              <h3>Subham</h3>
              <p class="team-card__role">Partner · Lead academic tutor</p>
              <p>Subham is the first person most students message …</p>
            </article>
          </li>
          <li>
            <article class="team-card">
              <figure><img src="imgs/tania.jpeg" alt="Tania, partner at Writing Rodgers Solution" …></figure>
              <h3>Tania</h3>
              <p class="team-card__role">Partner · Operations &amp; student support</p>
              <p>Tania coordinates expert writers, timelines, and revisions …</p>
            </article>
          </li>
        </ul>
        <ul class="team__facts">
          <li><address>UK contact address: 233 Holmesdale Rd, London SE25 6PR</address></li>  [CHANGE: wrap address in <address>]
          <li>Plagiarism-free work with direct expert contact</li>
          <li>Essays, reports, dissertations, tutoring &amp; exam prep</li>
        </ul>
        <p><a class="link-arrow" href="about-us/">Read our full story →</a></p>
      </section>

      <section class="gallery" id="wr-gallery" aria-labelledby="wr-gallery-heading">
        <h2 id="wr-gallery-heading">Real moments with our students</h2>
        <p class="section-lead">Behind-the-scenes from the Writing Rodgers team …</p>
        <div class="gallery__viewport">
          <button type="button" class="gallery__nav gallery__nav--prev" aria-label="Previous photo">…</button>
          <button type="button" class="gallery__nav gallery__nav--next" aria-label="Next photo">…</button>
          <ul class="gallery__grid" id="wr-gallery-grid">
            <li><button type="button" data-gallery-open="0" aria-label="View photo 1 of 13">
              <img src="imgs/1632998789708shutterstock778983088.jpeg" alt="Students collaborating on coursework" loading="lazy">
            </button></li>
            … (12 more, same shape)
          </ul>
        </div>
      </section>

      <dialog class="lightbox" id="wr-lightbox" aria-label="Photo gallery">                  [CHANGE: <div role="dialog"> → native <dialog>]
        <button type="button" class="lightbox__close" aria-label="Close gallery">×</button>
        <button type="button" class="lightbox__nav lightbox__nav--prev" aria-label="Previous photo">‹</button>
        <button type="button" class="lightbox__nav lightbox__nav--next" aria-label="Next photo">›</button>
        <figure>
          <img id="wr-lightbox-img" alt="">
          <figcaption id="wr-lightbox-caption"></figcaption>
        </figure>
      </dialog>

      <section class="featured-video" id="wr-featured-video" aria-labelledby="wr-featured-video-heading">
        <h2 id="wr-featured-video-heading">Watch our story</h2>
        <p class="section-lead">How Writing Rodgers helps UK and international students …</p>
        <figure class="featured-video__frame">                                                [CHANGE: wrap iframe in <figure>]
          <iframe src="https://www.youtube.com/embed/bLBL9dF8yb8" title="Watch our story - Writing Rodgers" loading="lazy" …></iframe>
        </figure>
      </section>

      <section class="shorts" id="wr-shorts" aria-labelledby="wr-shorts-heading">
        <h2 id="wr-shorts-heading">Watch our students share their wins</h2>
        <p class="section-lead">Short clips from Subham and the team …</p>
        <ul class="shorts__grid">
          <li><iframe src="https://www.youtube.com/embed/Q9FcPMMJn4M" title="Writing Rodgers student support" loading="lazy" …></iframe></li>
          <li><iframe src="https://www.youtube.com/embed/hj5cgzjw9HY" title="Writing Rodgers students share their experience" …></iframe></li>
          <li><iframe src="https://www.youtube.com/embed/xX0sccudGsI" title="How Writing Rodgers supports UK assignments" …></iframe></li>
          <li><iframe src="https://www.youtube.com/embed/Skg690LKnpw" title="Behind the scenes with the Writing Rodgers team" …></iframe></li>
        </ul>
      </section>

      <section class="reach" id="wr-reach" aria-labelledby="wr-reach-heading">
        <figure>
          <img src="imgs/bpp-assignment-help-bpp-university-assignment-help-2.webp" alt="Students studying in the UK" …>
        </figure>
        <div class="reach__copy">
          <h2 id="wr-reach-heading">Students we support</h2>
          <p>Since 2017, learners across the UK, Australia, UAE, Oman, Canada, India, and Ireland …</p>
          <p>
            <a class="btn btn--primary" href="https://wa.me/917044974618?text=…">Get a free quote on WhatsApp</a>
            <a class="link-arrow" href="assignment-help-in-uk-at-reasonable-price/">See where we work →</a>
          </p>
        </div>
      </section>

      <section class="services" id="wr-services" aria-labelledby="wr-services-heading">
        <h2 id="wr-services-heading">What we help with</h2>
        <p class="section-lead">Pick by subject or by format …</p>

        <section class="services__group" aria-labelledby="services-by-subject">              [CHANGE: nested <section> so h3 group has its own region]
          <h3 id="services-by-subject">By subject</h3>
          <ul class="services-grid">                                                         [CHANGE: loose <a> → ul/li]
            <li><a class="service-card" href="management-assignment-help/">
              <h4>Management &amp; MBA</h4>                                                  [CHANGE: h3 → h4 (nested under h3 group)]
              <p>Business, HR, strategy …</p>
              <span class="service-card__link">View management help →</span>
            </a></li>
            <li><a class="service-card" href="nursing-assignment-help/"><h4>Nursing &amp; healthcare</h4><p>…</p>…</a></li>
            <li><a class="service-card" href="accounting-assignment-help/"><h4>Finance &amp; accounting</h4><p>…</p>…</a></li>
            <li><a class="service-card" href="it-assignment-help/"><h4>IT &amp; data</h4><p>…</p>…</a></li>
            <li><a class="service-card" href="law-assignment-help/"><h4>Law</h4><p>…</p>…</a></li>
            <li><a class="service-card" href="marketing-assignment-help/"><h4>Marketing</h4><p>…</p>…</a></li>
          </ul>
        </section>

        <section class="services__group" aria-labelledby="services-by-format">
          <h3 id="services-by-format">By writing format</h3>
          <ul class="services-grid">
            <li><a class="service-card" href="dissertation-writing-help/"><h4>Dissertation</h4>…</a></li>
            <li><a class="service-card" href="thesis-writing-help/"><h4>Thesis writing</h4>…</a></li>
            <li><a class="service-card" href="thesis-with-spss-nvivo-help/"><h4>SPSS &amp; NVivo analysis</h4>…</a></li>
            <li><a class="service-card" href="essay-writing-help/"><h4>Essay writing</h4>…</a></li>
            <li><a class="service-card" href="report-writing-help/"><h4>Report writing</h4>…</a></li>
            <li><a class="service-card" href="case-study-assignment-help/"><h4>Case study</h4>…</a></li>
            <li><a class="service-card" href="project-management-assignment-help/"><h4>Project management</h4>…</a></li>
          </ul>
        </section>

        <p class="services__cta-note">Plus academic coaching and exam prep — see the <a href="#wr-tutoring">tutoring section</a>.</p>
        <p class="services__cta">
          <a class="btn btn--primary" href="https://wa.me/917044974618?text=…">WhatsApp us your subject</a>
        </p>
      </section>

      <section class="tutoring" id="wr-tutoring" aria-labelledby="wr-tutoring-heading">
        <figure><img src="imgs/online-tutoring.webp" alt="Online tutoring session" …></figure>
        <div class="tutoring__copy">
          <h2 id="wr-tutoring-heading">Online tutoring &amp; exam prep</h2>
          <p>Support continues after delivery …</p>
          <p>
            <a class="btn btn--outline" href="academic-coaching-help/">Academic coaching</a>
            <a class="btn btn--outline" href="exam-preparation-help/">Exam preparation</a>
          </p>
        </div>
      </section>

      <section class="why" id="wr-why" aria-labelledby="wr-why-heading">
        <div class="why__copy">
          <h2 id="wr-why-heading">Why students choose us</h2>
          <ul class="why__list">
            <li>Personalised guidance: speak directly with your expert</li>
            <li>Plagiarism-free, human-written work (no AI filler)</li>
            <li>Academic coaching and online tutoring</li>
            <li>Exam preparation support</li>
            <li>On-time delivery with revisions when needed</li>
            <li>Rubric-matched writing for UK and international universities</li>
          </ul>
          <p><a class="link-arrow" href="about-us/">Learn more about Writing Rodgers →</a></p>
        </div>
        <figure><img src="imgs/assignment-help-writing-rodgers-solution-writing-r-3.webp" alt="Student receiving assignment support" …></figure>
      </section>

      <section class="testimonials" id="wr-testimonials" aria-labelledby="wr-testimonials-heading">
        <h2 id="wr-testimonials-heading">What students say</h2>
        <p class="section-lead">Real messages from students we have supported …</p>
        <p class="testimonials__social">
          <a href="https://m.facebook.com/writingrodgersuk/">More reviews on Facebook</a> ·
          <a href="https://www.instagram.com/writingrodgerssolution/">Instagram</a>
        </p>
        <ul class="testimonials__grid">                                                      [CHANGE: wrap in ul/li]
          <li><article class="testimonial-card">
            <figure><img src="imgs/bpp-assignment-help-bpp-university-assignment-help.webp" alt="" …></figure>
            <p class="testimonial-card__grade">Grades: 69 &amp; 70</p>
            <p class="testimonial-card__meta">Report · UK university</p>
            <blockquote><p>Subham, thanks for your excellent report. I got 69, my girlfriend got 70.</p></blockquote>
            <p><cite>— Sourav Soni &amp; Kia</cite></p>
          </article></li>
          <li><article class="testimonial-card">…Rohish…</article></li>
          <li><article class="testimonial-card">…Ephraim…</article></li>
        </ul>
        <p><a class="btn btn--primary" href="https://wa.me/917044974618?text=…">Get support like them on WhatsApp</a></p>
      </section>

      <section class="contact" id="wr-contact" aria-labelledby="wr-contact-heading">
        <h2 id="wr-contact-heading">Get in touch</h2>
        <p class="section-lead">No forms. Reach us on WhatsApp, phone, or email …</p>
        <ul class="contact-grid">                                                            [CHANGE: wrap in ul/li]
          <li><a class="contact-card contact-card--wa" href="https://wa.me/917044974618?text=…">
            <span class="contact-card__label">WhatsApp</span>
            <span class="contact-card__value">+91 7044974618</span>
            <span class="contact-card__hint">Fastest for quotes: tap to chat</span>
          </a></li>
          <li><a class="contact-card contact-card--call" href="tel:+917044974618">…</a></li>
          <li><a class="contact-card contact-card--email" href="mailto:…">…</a></li>
        </ul>
        <div class="contact-extra">
          <p><strong>Also reach us by phone (India):</strong> <a href="tel:+917044974618">+91 7044974618</a></p>
          <address>                                                                          [CHANGE: wrap address blocks in <address>]
            <strong>UK contact address:</strong> 233 Holmesdale Rd, London SE25 6PR
          </address>
          <p class="contact-legal">
            <strong>Registered entity:</strong> Writing Rodgers Solution LLP is incorporated in India
            with the Ministry of Corporate Affairs (ROC Kolkata; LLPIN AAY-5206).
            Registered office: 3rd Floor, Flat A3, BE1/5 Deshbandhu Nagar North, Kolkata, West Bengal 700059, India.
          </p>
        </div>
      </section>

    </main>                                                                                  [CHANGE: new]

    <footer class="site-footer" id="wr-footer-5319">
      <nav class="site-footer__links" aria-label="Footer">                                   [CHANGE: <div.copyright-center> → <nav>]
        <ul>
          <li><a href="assignment-help-in-london/">London</a></li>
          <li><a href="assignment-help-in-birmingham/">Birmingham</a></li>
          <li><a href="assignment-help-in-manchester/">Manchester</a></li>
          <li><a href="assignment-help-in-australia/">Australia</a></li>
          <li><a href="assignment-help-in-uae-by-professionals/">UAE</a></li>
          <li><a href="blog/">Blog</a></li>
        </ul>
      </nav>
      <ul class="site-footer__social" aria-label="Writing Rodgers on social media">          [CHANGE: <br><br> → <ul>]
        <li><a href="https://www.instagram.com/writingrodgerssolution/">
          <img src="imgs/image-22.webp" alt="Instagram" width="40" height="40">              [CHANGE: add alt]
        </a></li>
        <li><a href="https://m.facebook.com/writingrodgersuk/">
          <img src="imgs/image-16.webp" alt="Facebook" width="40" height="40">               [CHANGE: add alt]
        </a></li>
        <li><a href="http://linkedin.com/in/writing-rodgers-solution-a653871b3">
          <img src="imgs/image-17.webp" alt="LinkedIn" width="40" height="40">               [CHANGE: add alt]
        </a></li>
      </ul>
      <p class="site-footer__copy">
        © <time datetime="2026">2026</time> Writing Rodgers™. All Rights Reserved.          [CHANGE: wrap year in <time>]
      </p>
    </footer>

  </body>
</html>
```

**Constraints satisfied:** exactly one `<h1>` (hero); no heading-level skips (h1 → h2 sections → h3 sub-groups / cards / step titles → h4 service cards under h3 groups); landmarks present (`header`, `nav`, `main`, `footer`, `aside`); `figure`/`figcaption` on captioned media; `<address>` for postal address; `<time>` for year; native `<dialog>` for lightbox; numbered steps in `<ol>`; social icons no longer alt-less.

---

## PART 2 — SEO + Social Meta (Current → Proposed)

| Tag | Current value (line) | Proposed value | Rationale | Chars |
|---|---|---|---|---|
| `<html lang>` | absent (line 2) | `lang="en-GB"` | UK-targeted content; declares language for AT and search. | — |
| `<title>` | `Stress Less, Score More \| UK Assignment Help Since 2017 \| Writing Rodgers Solution LLP` (lines 10-12) | `Writing Rodgers Solution \| UK Assignment Help Since 2017` | Drops third pipe-section; keeps brand + USP + year. Title 86→56 chars, inside Google's 50-60 sweet spot. | **56** |
| `<meta name="description">` | `UK assignment and dissertation help since 2017. Original work, direct WhatsApp with Subham's team. +91 7044974618 (no forms).` (line 13) — 126 chars | `UK assignment & dissertation help since 2017 — for students across the UK, Australia and UAE. Direct WhatsApp with Subham's team, no forms.` | Expands to 140 char target; keeps the visible USPs (since-2017, named partner, regions, no forms); drops phone number (already in tel: links). | **142** |
| `<link rel="canonical">` | absent | `<link rel="canonical" href="https://www.writingrodgerssolution.co.uk/">` | Pins homepage to root URL; current `og:url` already matches, so canonical aligns. | — |
| `<meta name="robots">` | absent | `<meta name="robots" content="index, follow, max-image-preview:large">` | Default-permits indexing; `max-image-preview:large` allows full-size thumbnail in SERP and Discover. | — |
| `<meta name="keywords">` | `Stress Less, Score More, assignment help UK, …` (line 14) | **REMOVE** | Ignored by Google, Bing — pure clutter. | — |
| `og:title` | `Writing Rodgers \| Value Your Education` (line 15) | `Writing Rodgers Solution \| UK Assignment Help Since 2017` | Match the new `<title>` so social previews are consistent. | 56 |
| `og:type` | `website` (line 16) | `website` | Correct for a homepage. | — |
| `og:description` | (same as meta description) (line 17) | (same as new meta description) | Consistency. | 142 |
| `og:url` | `https://www.writingrodgerssolution.co.uk/` (line 93) | `https://www.writingrodgerssolution.co.uk/` | Already correct. Keep. | — |
| `og:site_name` | `www.writingrodgerssolution.co.uk` (line 18) | `Writing Rodgers Solution` | Should be the brand name, not the host. | — |
| `og:locale` | absent | `en_GB` | Aligns with `<html lang>`. | — |
| `og:image` | `imgs/1632910684934logoWR.jpeg` (line 19) | `https://www.writingrodgerssolution.co.uk/imgs/1749822217361WhatsAppImage20250613at191300d18e5d85.jpeg` (absolute URL, hero photo of the team in London) | Hero image is the most representative visual on the page (it's already the hero background, line 252). Logo files render small in social previews and look bland. `<NEEDS INPUT>` to confirm hero image is preferred over logo. | — |
| `og:image:alt` | absent | `Writing Rodgers team in London — UK assignment and dissertation help since 2017` | Accessibility + crawler context for the OG card. | — |
| `twitter:card` | `summary` (line 21) | `summary_large_image` | Hero photo is large/wide enough to merit large-card preview. | — |
| `twitter:title` | `Writing Rodgers \| Value Your Education` (line 20) | (same as `og:title`) | Consistency. | 56 |
| `twitter:description` | (same as meta) (line 22) | (same as new meta) | Consistency. | 142 |
| `twitter:image` | `imgs/1632910684934logoWR.jpeg` (line 23) | (same absolute URL as `og:image`) | Consistency. | — |
| google-site-verification | `Uz5YfxfMXJMsqvNm8VwBq13Ovn8UZpsi4kj0eJ7Ol2g` (line 27) | **KEEP** | Search Console ownership token — leave untouched. | — |
| `<link rel="icon">` / `apple-touch-icon` | `imgs/image-21.webp` (lines 77-78) + `favicon.png` (line 5) | **KEEP**, but normalise: `<link rel="icon" type="image/png" href="/favicon.png">` and `<link rel="apple-touch-icon" href="/imgs/image-21.webp">` | Current uses `type="image/x-icon"` on a `.webp` (wrong mime). Use absolute paths and correct types. | — |

### Stale tags to remove

| Tag | Line | Reason |
|---|---|---|
| `<meta name="keywords" content="…">` | 14 | Ignored by all major search engines since ~2009; SEO noise. |
| `<meta content="text/html; charset=utf-8" http-equiv="Content-Type">` | 6 | Superseded by a single `<meta charset="utf-8">` declaration (or by the HTTP header). Replace, don't delete. |
| `<meta content="true" name="HandheldFriendly">` / `<meta content="480" name="MobileOptimized">` | 8-9 | Pre-2010 BlackBerry/Palm hints — superseded by `<meta name="viewport">` already on line 7. |
| Stray closing `</div>` | 129 | Orphan — no matching open tag. Breaks DOM structure. |
| Microdata `itemscope`/`itemprop` on logo wrapper | 149-152 | Replace with JSON-LD `Organization` (Part 3B). Keeping both can cause Google to merge inconsistent values. |

---

## PART 3A — Existing JSON-LD audit

**No JSON-LD found in `index.html`.** (Verified via `grep -n "application/ld+json"` — 0 matches.)

There is one microdata Organization stub on the logo wrapper (lines 149-152) with only `itemtype="http://schema.org/Organization"`, `itemprop="url"`, and `itemprop="logo"` — but it carries no `name`, `address`, `contactPoint`, or `sameAs`. **Recommendation: REPLACE** with the JSON-LD Organization block in Part 3B and strip the microdata attributes.

---

## PART 3B — Proposed JSON-LD

**Google rich-result eligibility (from `https://developers.google.com/search/docs/appearance/structured-data/search-gallery`, fetched today):** Organization, WebSite, Breadcrumb, FAQ, Article, LocalBusiness, ProfilePage, Q&A, Discussion Forum, Product, Recipe, Event, Movie, Course, Dataset, Job Posting, Software App, Review (in qualified verticals), Video, Vacation Rental, Math Solver, Employer Rating, Image Metadata, Speakable, Carousel, Subscription/Paywalled, Education Q&A.

### B.1 — Organization (homepage)

**Eligibility quote (gallery):** *"Organization — Organizations vertical."* Google's Organization rich result lets you tell Google which name, logo, contact and identifiers should appear in knowledge panels and SERP brand cards. Fits this site's homepage.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://www.writingrodgerssolution.co.uk/#organization",
  "name": "Writing Rodgers Solution LLP",
  "legalName": "Writing Rodgers Solution LLP",
  "alternateName": "Writing Rodgers",
  "url": "https://www.writingrodgerssolution.co.uk/",
  "logo": {
    "@type": "ImageObject",
    "url": "https://www.writingrodgerssolution.co.uk/imgs/logo.webp",
    "width": "<NEEDS INPUT: logo intrinsic width in px>",
    "height": "<NEEDS INPUT: logo intrinsic height in px>"
  },
  "image": "https://www.writingrodgerssolution.co.uk/imgs/1749822217361WhatsAppImage20250613at191300d18e5d85.jpeg",
  "description": "UK assignment and dissertation help since 2017 for students across the UK, Australia and UAE. Direct WhatsApp with Subham's team, no forms.",
  "foundingDate": "2017",
  "slogan": "Stress Less, Score More",
  "identifier": [
    {
      "@type": "PropertyValue",
      "propertyID": "LLPIN",
      "value": "AAY-5206"
    }
  ],
  "address": [
    {
      "@type": "PostalAddress",
      "name": "Registered office (India)",
      "streetAddress": "3rd Floor, Flat A3, BE1/5 Deshbandhu Nagar North",
      "addressLocality": "Kolkata",
      "addressRegion": "West Bengal",
      "postalCode": "700059",
      "addressCountry": "IN"
    },
    {
      "@type": "PostalAddress",
      "name": "UK contact address",
      "streetAddress": "233 Holmesdale Rd",
      "addressLocality": "London",
      "postalCode": "SE25 6PR",
      "addressCountry": "GB"
    }
  ],
  "contactPoint": [
    {
      "@type": "ContactPoint",
      "telephone": "+91-70449-74618",
      "email": "writingrodgerssolutionuk@gmail.com",
      "contactType": "customer service",
      "availableLanguage": ["en"],
      "areaServed": ["GB", "AU", "AE", "OM", "CA", "IE", "IN"]
    }
  ],
  "sameAs": [
    "https://m.facebook.com/writingrodgersuk/",
    "https://www.instagram.com/writingrodgerssolution/",
    "https://www.linkedin.com/in/writing-rodgers-solution-a653871b3"
  ],
  "member": [
    { "@type": "Person", "name": "Subham", "jobTitle": "Partner · Lead academic tutor" },
    { "@type": "Person", "name": "Tania",  "jobTitle": "Partner · Operations & student support" }
  ]
}
```

**Property audit**
- Required by Google (Organization): `name`, `url`, `logo` — present.
- Strongly recommended: `sameAs`, `address`, `contactPoint`, `description`, `image`, `foundingDate`, `legalName`, `identifier` — present.
- Intentionally omitted: `numberOfEmployees` (not visible in file), `taxID` / `vatID` (none disclosed), `founder` (the visible content describes Subham + Tania as "Partners" who "have built" the firm — that implies founding but doesn't state it; use `member` to stay defensible and ask via Open Question whether to upgrade to `founder`). `aggregateRating` deliberately omitted — see Part 3C.
- Note: phone number stored in E.164-friendly format with hyphens, matching the way the file already prints `+91 7044974618` (lines 265, 273, 664, 669).

### B.2 — WebSite (sitewide identity)

**Eligibility quote (gallery):** WebSite is implicit metadata used to establish a site's official name (helps Google display the brand name instead of the domain in SERPs). No SearchAction here because there is no internal search on the site.

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "https://www.writingrodgerssolution.co.uk/#website",
  "url": "https://www.writingrodgerssolution.co.uk/",
  "name": "Writing Rodgers Solution",
  "alternateName": "Writing Rodgers",
  "inLanguage": "en-GB",
  "publisher": { "@id": "https://www.writingrodgerssolution.co.uk/#organization" }
}
```

**Property audit**
- Required: `url`, `name` — present.
- Strongly recommended: `publisher` reference to the Organization node — present.
- Intentionally omitted: `potentialAction` / `SearchAction` — there is no internal search on the site; declaring one Google can't actually execute risks an Unparseable Structured Data warning.

### B.3 — WebPage (homepage scoping)

Lightweight wrapper so the homepage URL has a `WebPage` node that references the Organization and WebSite.

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "https://www.writingrodgerssolution.co.uk/#webpage",
  "url": "https://www.writingrodgerssolution.co.uk/",
  "name": "Writing Rodgers Solution | UK Assignment Help Since 2017",
  "description": "UK assignment & dissertation help since 2017 — for students across the UK, Australia and UAE. Direct WhatsApp with Subham's team, no forms.",
  "inLanguage": "en-GB",
  "isPartOf": { "@id": "https://www.writingrodgerssolution.co.uk/#website" },
  "about":    { "@id": "https://www.writingrodgerssolution.co.uk/#organization" },
  "primaryImageOfPage": {
    "@type": "ImageObject",
    "url": "https://www.writingrodgerssolution.co.uk/imgs/1749822217361WhatsAppImage20250613at191300d18e5d85.jpeg"
  }
}
```

**Property audit**
- `url`, `name`, `description`, `isPartOf` — present.
- Not eligible for a dedicated rich result on its own, but stitches the Organization + WebSite graph cleanly to the URL.

> **Implementation note:** ship all three nodes inside a single `@graph` block in one `<script type="application/ld+json">` so the `@id` cross-references resolve cleanly. (Implementation deferred to the apply step; this plan is content-only.)

---

## PART 3C — Rejected schema types

| Type | Reason for rejection |
|---|---|
| **LocalBusiness** | Tempting because of the London contact address (lines 342, 682), but the file explicitly calls it a "UK contact address" while the registered office sits in India (lines 683-684). Declaring a `LocalBusiness` at the London address implies physical premises and opening hours, neither of which the page substantiates. Risk of "misleading information" tagging in Google's structured-data quality rules. Stick with `Organization` + two `PostalAddress` nodes. |
| **ProfessionalService** / **EducationalOrganization** | More semantically specific, but neither is listed in the Google gallery as a dedicated rich-result type — `Organization` is the matched type. Using a more specific subtype gives no SERP gain and constrains required properties unnecessarily. |
| **Service** (per service offering) | Each `Service` node belongs on its own service-page (e.g. `dissertation-writing-help/`), not the homepage where 13 services are listed. Putting all 13 here bloats the page graph and dilutes per-service relevance. |
| **Review / AggregateRating** | Three testimonials are present (lines 631-651), but (a) Google's policy disallows self-published merchant reviews from earning Review rich snippets — reviews must be hosted by a third-party reviewer, and (b) reviewer names are first-name-only (`Rohish`, `Ephraim`) or pairs (`Sourav Soni & Kia`), which fails the "named author" requirement for rich-result eligibility. Including them risks a manual action. Testimonials should remain as visible HTML `<blockquote>` content only. |
| **FAQPage** | Per the plan's rejection rule: Google restricted FAQ rich results in Aug 2023 to authoritative government and health sites. This site is neither. The page also doesn't contain a Q&A block, so the schema would be inventing content. |
| **HowTo** | Retired by Google for most sites. The "How it works" 3-step section (lines 276-296) is a sales-flow description ("send your brief → get a quote → review & submit"), not an instructional procedure with materials/tools — wouldn't qualify even under the old rules. |
| **BreadcrumbList** | Homepage is the root — there is no parent crumb. Not applicable. |
| **VideoObject** | Five YouTube embeds (lines 470, 481-494) but the page exposes only `src` and `title`. Required properties for VideoObject (`thumbnailUrl`, `uploadDate`, `description`) are not visible in the file. Adding them with `<NEEDS INPUT>` placeholders would publish unverified data. Defer to a per-video markup pass when those properties are available. |
| **ProfilePage** | Could be used for individual partner pages (`/about-us/subham` etc.) but is the wrong type for a brand homepage. |
| **ItemList / Carousel** | Carousel rich results require each item to be a fully-marked Product, Course, Recipe, Movie, or Restaurant. Writing Rodgers services don't fit any of those gallery types, so a Carousel wouldn't surface as a rich result. |
| **Course** | The page lists academic-coaching and exam-prep services in passing (lines 595-604), but `Course` rich results require concrete course names, providers, delivery mode, and offers. Visible content doesn't supply those. Defer to a dedicated course page if one is launched. |

---

## Open Questions (consolidate every `<NEEDS INPUT>`)

1. **`og:image` choice** — keep current logo (`imgs/1632910684934logoWR.jpeg`), or switch to the hero team photo (`imgs/1749822217361WhatsAppImage20250613at191300d18e5d85.jpeg`)? Plan currently proposes hero.
2. **Subham + Tania role in Organization** — declare them as `founder` (stronger Knowledge Panel signal) or keep as `member` (safer; matches the visible "Partners" wording)? File says they "have built Writing Rodgers" but doesn't explicitly say "founded".
3. **Logo intrinsic dimensions** for the JSON-LD `ImageObject.logo` — needed if you want a richer Organization knowledge panel. Inline style says `width: 179px` (line 151) but the source asset's true width/height should be captured.
4. **Additional `sameAs` URLs?** — file lists Facebook, Instagram, LinkedIn. Any YouTube channel URL (the four shorts and one feature video imply a channel)? Any Trustpilot / Google Business / X / TikTok?
5. **`max-image-preview:large`** — confirm OK to include in robots meta (recommended for SERP/Discover thumbnails).
6. **Founding date precision** — file says "Since 2017" but no month. Plan uses `"foundingDate": "2017"`. Confirm or supply ISO date.
7. **Phone format** — file prints `+91 7044974618`; JSON-LD uses `+91-70449-74618` (E.164-ish). Confirm.
8. **Lightbox upgrade to native `<dialog>`** — would change how the existing `js/wr-gallery.js` opens/closes the lightbox. Confirm appetite for the small JS refactor, or keep `<div role="dialog">` for safety.
