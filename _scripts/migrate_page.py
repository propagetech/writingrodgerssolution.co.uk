#!/usr/bin/env python3
"""
migrate_page.py — apply the standard migration template to a single subpage.

What it does:
  1. Reads the existing <page>/index.html
  2. Extracts per-page SEO (title, description, keywords) from the existing <head>
  3. Replaces the <head> with the new standardised template + page-specific values
  4. Replaces <body> opening (skip link + aside mobile-CTA + <header> + nav)
  5. Replaces the <footer> + bottom scripts with the new flat template
  6. Cleans up body content:
       - Removes Bootstrap data-* attributes
       - Removes Viamagus data-* attributes
       - Removes mid-body <link href="../css/main-N.css"> tags
       - Removes inline loadViaBkgImage script + Viamagus_Website_Loader._init()
       - Drops microdata on logo
       - Drops `<div class="wr-page__container">` wrapper
       - Drops stray closing </div> after mobile CTA bar
       - Renames featurette-heading -> wr-featurette__heading
       - Converts `<div class="wr-component wr-component--X" ...>` content blocks to `<section>`
       - Drops `<div style="clear: both">` empty clearfixes
       - Wraps UK contact <p> in <address>

What it does NOT do:
  - Refactor page-specific body content (sub-hero, image-text blocks, etc.) beyond mechanical class/attr cleanup
  - Touch CSS or JS files (the new templates load wr-vanilla.css + wr-nav.js + wr-gallery.js)

Per-page metadata comes from a config (see migrate_batch.py).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

SITE = "https://www.writingrodgerssolution.co.uk"

# --------------------------- TEMPLATES ---------------------------

# Sitewide Organization + WebSite nodes (constant across all pages)
ORG_NODE = {
    "@type": "Organization",
    "@id": f"{SITE}/#organization",
    "name": "Writing Rodgers Solution LLP",
    "legalName": "Writing Rodgers Solution LLP",
    "alternateName": "Writing Rodgers",
    "url": f"{SITE}/",
    "logo": {"@type": "ImageObject", "url": f"{SITE}/imgs/logo.webp", "width": 544, "height": 281},
    "image": f"{SITE}/imgs/1632910684934logoWR.jpeg",
    "description": "Writing Rodgers has been delivering exceptional student support services in their studies and assignment works since 2017. We, Rodgers, are available 24X7 to support a-z related to your academic cycle. Our student assignment help services empower the potent students to study smart, score high, and win dreams. As an education consultant, we understand your course criteria and assignment rubrics, help you pursue the course, and always respond to your assignment help needs.",
    "foundingDate": "2017-05-17",
    "slogan": "Stress Less, Score More",
    "identifier": [{"@type": "PropertyValue", "propertyID": "LLPIN", "value": "AAY-5206", "validFrom": "2021-09-21"}],
    "address": [
        {"@type": "PostalAddress", "name": "Registered office (India)", "streetAddress": "3rd Floor, Flat A3, BE1/5 Deshbandhu Nagar North", "addressLocality": "Kolkata", "addressRegion": "West Bengal", "postalCode": "700059", "addressCountry": "IN"},
        {"@type": "PostalAddress", "name": "UK contact address", "streetAddress": "233 Holmesdale Rd", "addressLocality": "London", "postalCode": "SE25 6PR", "addressCountry": "GB"},
    ],
    "contactPoint": [{"@type": "ContactPoint", "telephone": "+917044974618", "email": "writingrodgerssolutionuk@gmail.com", "contactType": "customer service", "availableLanguage": ["en"], "areaServed": ["GB", "AU", "AE", "OM", "CA", "IE", "IN"]}],
    "sameAs": ["https://m.facebook.com/writingrodgersuk/", "https://www.instagram.com/writingrodgerssolution/", "https://www.linkedin.com/in/writing-rodgers-solution-a653871b3", "https://www.youtube.com/@writingrodgerssolution9557"],
    "founder": [
        {"@type": "Person", "name": "Subham", "jobTitle": "Partner · Lead academic tutor"},
        {"@type": "Person", "name": "Tania", "jobTitle": "Partner · Operations & student support"},
    ],
}

WEBSITE_NODE = {
    "@type": "WebSite",
    "@id": f"{SITE}/#website",
    "url": f"{SITE}/",
    "name": "Writing Rodgers Solution",
    "alternateName": "Writing Rodgers",
    "inLanguage": "en-GB",
    "publisher": {"@id": f"{SITE}/#organization"},
}

# --------------------------- BUILDERS ---------------------------

def build_head(meta: dict) -> str:
    """Build the new <head> block given per-page metadata."""
    slug = meta["slug"]
    canonical = f"{SITE}/{slug}/"
    title = meta["title"]
    description = meta["description"]
    keywords = meta["keywords"]
    og_image = meta.get("og_image", f"{SITE}/imgs/1632910684934logoWR.jpeg")

    # Per-page nodes in the @graph: WebPage + Service + (optional CollegeOrUniversity) + BreadcrumbList
    webpage = {
        "@type": meta.get("webpage_type", "WebPage"),
        "@id": f"{canonical}#webpage",
        "url": canonical,
        "name": title,
        "description": description,
        "inLanguage": "en-GB",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": {"@id": f"{SITE}/#organization"},
        "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": og_image},
    }

    extra_nodes = []

    if meta.get("service_name"):
        service = {
            "@type": "Service",
            "@id": f"{canonical}#service",
            "name": meta["service_name"],
            "serviceType": "Academic Writing",
            "description": meta.get("service_description", description),
            "provider": {"@id": f"{SITE}/#organization"},
            "areaServed": meta.get("area_served", {"@type": "Country", "name": "United Kingdom"}),
            "audience": {"@type": "EducationalAudience", "educationalRole": "student"},
            "url": canonical,
        }
        webpage["mainEntity"] = {"@id": f"{canonical}#service"}
        if meta.get("university_name"):
            service["about"] = {"@id": f"{canonical}#university"}
            webpage["about"] = {"@id": f"{canonical}#university"}
            extra_nodes.append({
                "@type": "CollegeOrUniversity",
                "@id": f"{canonical}#university",
                "name": meta["university_name"],
                "url": meta.get("university_url", ""),
            })
        extra_nodes.insert(0, service)

    # Build breadcrumb. Supports 2 or 3 hops.
    crumbs = meta.get("breadcrumb", [{"name": title}])
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"}]
    for i, crumb in enumerate(crumbs, start=2):
        item = {"@type": "ListItem", "position": i, "name": crumb["name"]}
        if "url" in crumb:
            item["item"] = crumb["url"]
        items.append(item)
    breadcrumb_node = {
        "@type": "BreadcrumbList",
        "@id": f"{canonical}#breadcrumb",
        "itemListElement": items,
    }

    graph = [ORG_NODE, WEBSITE_NODE, webpage] + extra_nodes + [breadcrumb_node]
    json_ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)

    og_title = meta.get("og_title", "Writing Rodgers | Value Your Education")
    twitter_title = meta.get("twitter_title", "Writing Rodgers | Value Your Education")
    og_description = meta.get("og_description", description)
    twitter_description = meta.get("twitter_description", description)

    return f"""<!DOCTYPE html>
<html lang="en-GB">

<head>
  <meta charset="utf-8" />
  <meta content="width=device-width, initial-scale=1.0" name="viewport" />
  <link rel="canonical" href="{canonical}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <title>{title}</title>
  <meta content="{description}" name="description" />
  <meta content="{keywords}" name="keywords" />
  <meta content="{og_title}" property="og:title" />
  <meta content="website" property="og:type" />
  <meta content="{og_description}" property="og:description" />
  <meta content="www.writingrodgerssolution.co.uk" property="og:site_name" />
  <meta content="en_GB" property="og:locale" />
  <meta content="{og_image}" property="og:image" />
  <meta content="Writing Rodgers Solution — UK assignment and dissertation help since 2017" property="og:image:alt" />
  <meta content="{canonical}" property="og:url" />
  <meta content="{twitter_title}" property="twitter:title" />
  <meta content="summary" name="twitter:card" />
  <meta content="{twitter_description}" property="twitter:description" />
  <meta content="{og_image}" property="twitter:image" />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&amp;family=Quicksand:wght@300..700&amp;display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,500,0,0" rel="stylesheet" />
  <link href="../css/wr-vanilla.css" rel="stylesheet" />
  <meta content="Uz5YfxfMXJMsqvNm8VwBq13Ovn8UZpsi4kj0eJ7Ol2g" name="google-site-verification" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-MBCE6EP13C"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {{ dataLayer.push(arguments); }}
    gtag('js', new Date());

    gtag('config', 'G-MBCE6EP13C');
  </script>
  <link href="../css/internal-styles.css" rel="stylesheet" />
  <link href="../css/wr-home.css" rel="stylesheet" />
  <style>
    body,
    html {{
      margin: 0;
      padding: 0;
      font-family: 'Quicksand', sans-serif;
    }}

    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    .wr-heading-1,
    .wr-heading-2,
    .wr-heading-3,
    .wr-section__heading {{
      font-family: 'Playfair Display', serif;
    }}
  </style>
  <link rel="icon" type="image/png" href="/favicon.png" />
  <link rel="apple-touch-icon" href="/imgs/image-21.webp" />
  <script type="application/ld+json">
{json_ld}
  </script>
</head>"""


# --------------------------- BODY TEMPLATES ---------------------------
# These are byte-for-byte identical across all subpages.

BODY_OPENING = """<body>
  <a class="wr-skip-link" href="#main">Skip to content</a>
  <a class="live-chat-fixed no-loader-all" href="https://wa.me/917044974618?text=Hi%20Writing%20Rodgers%2C%20I%20need%20assignment%20help.%20" target="_blank" title="WhatsApp Writing Rodgers">
    <img src="../imgs/image-20.webp" alt="Chat on WhatsApp" style="border-radius: 50%; width: 50px; height: 50px" />
  </a>
  <aside class="wr-mobile-cta-bar wr-m3-bottom-bar" aria-label="Quick contact">
    <a class="wr-mcta-wa wr-mcta--primary wr-m3-filled-button" href="https://wa.me/917044974618?text=Hi%20Writing%20Rodgers%2C%20I%20need%20assignment%20help.%20My%20deadline%20is%3A%20" target="_blank" rel="noopener">
      <span class="wr-mcta__icon wr-m3-button-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" /></svg></span>
      <span class="wr-mcta__copy">
        <span class="wr-mcta__title wr-m3-label">WhatsApp</span>
        <span class="wr-mcta__sub wr-m3-body-small">Free quote</span>
      </span>
    </a>
    <div class="wr-mcta-quick wr-m3-nav-cluster" role="group" aria-label="Call or email">
      <a class="wr-mcta-call wr-mcta--quick wr-m3-nav-item" href="tel:+917044974618" aria-label="Call India team">
        <span class="wr-mcta__icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" /></svg></span>
        <span class="wr-mcta__title wr-m3-label">Call India</span>
      </a>
      <a class="wr-mcta-email wr-mcta--quick wr-m3-nav-item" href="mailto:writingrodgerssolutionuk@gmail.com?subject=Assignment%20help%20request&amp;body=Hi%20Writing%20Rodgers%2C%0A%0ASubject%2Fmodule%3A%0ADeadline%3A%0A" aria-label="Email Writing Rodgers">
        <span class="wr-mcta__icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" /><path d="M22 6l-10 7L2 6" /></svg></span>
        <span class="wr-mcta__title wr-m3-label">Email</span>
      </a>
    </div>
  </aside>
  <div class="wr-page">
      <header class="wr-component wr-component--header" id="menu">
        <div class="wr-component__bg" style="background-color: rgba(1,0,56,1)">
          <div class="wr-component__content wr-m3-app-bar wr-m3-app-bar--dark" style="padding-top: 0px; padding-bottom: 1px; padding-left: 20px; padding-right: 20px; font-family: Open Sans">
            <div class="wr-m3-app-bar__inner">
              <div class="wr-m3-app-bar__row">
                <button class="wr-m3-menu-button" type="button" aria-label="Open menu">
                </button>
                <div class="wr-business-logo">
                  <a class="wr-brand" href="../" aria-label="Writing Rodgers Solution — Home">
                    <img alt="Writing Rodgers Solution" src="../imgs/logo.webp" width="544" height="281" style="width: 179px; height: auto;" />
                  </a>
                </div>
              </div>
              <nav class="wr-m3-navigation-drawer" id="wr-m3-nav-drawer" aria-label="Site navigation">
                <ul class="wr-m3-nav" id="menu-nav">
                  <li>
                    <a class="menulink wr-nav-link" href="../">Home</a>
                  </li>
                  <li>
                    <a class="menulink wr-nav-link" href="../about-us/">About</a>
                  </li>
                  <li>
                    <a class="menulink wr-nav-link" href="../#wr-team">Partners</a>
                  </li>
                  <li class="wr-m3-nav__item wr-m3-nav__item--has-submenu">
                    <a class="wr-nav-link wr-m3-nav__toggle" href="#" aria-haspopup="true" aria-expanded="false">Our Services <span class="wr-m3-nav__caret" aria-hidden="true"></span></a>
                    <ul class="wr-m3-nav__submenu">
                      <li><a class="menulink" href="../dissertation-writing-help/#menu">Dissertation Writing Help in UK, Oman Muscat, UAE and Australia</a></li>
                      <li><a class="menulink" href="../marketing-assignment-help/#menu">Marketing Assignment Help in UK</a></li>
                      <li><a class="menulink" href="../management-assignment-help/#menu">Management Assignment Help in UAE</a></li>
                      <li><a class="menulink" href="../nursing-assignment-help/#menu">Nursing Assignment Help in UK and Australia</a></li>
                      <li><a class="menulink" href="../accounting-assignment-help/#menu">Accounting Assignment Help in Australia and UK</a></li>
                      <li><a class="menulink" href="../law-assignment-help/#menu">Law Assignment Help in Australia and UK</a></li>
                      <li><a class="menulink" href="../it-assignment-help/#menu">IT Assignment Help</a></li>
                      <li><a class="menulink" href="../project-management-assignment-help/#menu">Project Management Assignment Help in Australia</a></li>
                      <li><a class="menulink" href="../case-study-assignment-help/#menu">Case Study Assignment Help in UK</a></li>
                      <li><a class="menulink" href="../thesis-writing-help/#menu">Thesis Writing Help in UK</a></li>
                      <li><a class="menulink" href="../essay-writing-help/#menu">Essay writing Help</a></li>
                      <li><a class="menulink" href="../report-writing-help/#menu">Report Writing Help in UAE</a></li>
                      <li><a class="menulink" href="../exam-preparation-help/#menu">Exam Preparation Help</a></li>
                      <li><a class="menulink" href="../thesis-with-spss-nvivo-help/#menu">Thesis with SPSS & Nvivo Help</a></li>
                      <li><a class="menulink" href="../academic-coaching-help/#menu">Academic Coaching Help in UK, UAE and Australia</a></li>
                    </ul>
                  </li>
                  <li class="wr-m3-nav__item wr-m3-nav__item--has-submenu">
                    <a class="wr-nav-link wr-m3-nav__toggle" href="#" aria-haspopup="true" aria-expanded="false">Assignments by University <span class="wr-m3-nav__caret" aria-hidden="true"></span></a>
                    <ul class="wr-m3-nav__submenu">
                      <li><a class="menulink" href="../bpp-assignment-help/">BPP University Assignment Help from Expert Tutors</a></li>
                      <li><a class="menulink" href="../aston-university-assignment-help/#menu">Aston University Assignment Help</a></li>
                      <li><a class="menulink" href="../coventry-university-assignment-help/">Coventry University Assignment Help</a></li>
                      <li><a class="menulink" href="../university-college-birmingham-assignment-help/#menu">University College Birmingham Assignment Help</a></li>
                      <li><a class="menulink" href="../de-montfort-university-assignment-help/#menu">DMU Assignment Help</a></li>
                      <li><a class="menulink" href="../edinburgh-university-assignment-help/#menu">Edinburgh University Assignment Help</a></li>
                      <li><a class="menulink" href="../essex-university-assignment-help/#menu">Essex University Assignment Help</a></li>
                      <li><a class="menulink" href="../middlesex-university-assignment-help/#menu">Middlesex University Assignment Help</a></li>
                      <li><a class="menulink" href="../university-of-derby-assignment-help/#menu">University of Derby Assignment Help</a></li>
                      <li><a class="menulink" href="../university-of-east-london-assignment-help/#menu">University of East London Assignment Help</a></li>
                      <li><a class="menulink" href="../university-of-greenwich-assignment-help/#menu">University of Greenwich Assignment Help</a></li>
                      <li><a class="menulink" href="../university-of-sunderland-assignment-help/#menu">University of Sunderland Assignment Help</a></li>
                      <li><a class="menulink" href="../university-of-salford-assignment-help/#menu">University of Salford Assignment Help</a></li>
                      <li><a class="menulink" href="../university-of-warwick-assignment-help/#menu">University of Warwick Assignment Help</a></li>
                    </ul>
                  </li>
                  <li>
                    <a class="menulink wr-nav-link" href="../#wr-how-it-works">How it works</a>
                  </li>
                  <li>
                    <a class="menulink wr-nav-link" href="../#wr-why">Why us</a>
                  </li>
                  <li>
                    <a class="menulink wr-nav-link" href="../#wr-testimonials">Testimonials</a>
                  </li>
                  <li class="wr-m3-nav__item wr-m3-nav__item--has-submenu">
                    <a class="wr-nav-link wr-m3-nav__toggle" href="#" aria-haspopup="true" aria-expanded="false">Our Branches <span class="wr-m3-nav__caret" aria-hidden="true"></span></a>
                    <ul class="wr-m3-nav__submenu">
                      <li><a class="menulink" href="../assignment-help-in-uae-by-professionals/#menu">Assignment Help in UAE by Professionals</a></li>
                      <li><a class="menulink" href="../assignment-help-in-oman-muscat/#menu">Assignment Help in Oman Muscat</a></li>
                      <li><a class="menulink" href="../assignment-help-in-canada/#menu">Canada Assignment Help</a></li>
                      <li><a class="menulink" href="../assignment-help-in-australia/#menu">Assignment Help in Australia</a></li>
                      <li><a class="menulink" href="../assignment-help-in-uk-at-reasonable-price/#menu">UK Assignment Services from Qualified Experts</a></li>
                      <li><a class="menulink" href="../ireland-assignment-help/#menu">Ireland Assignment Help</a></li>
                    </ul>
                  </li>
                  <li class="wr-m3-nav__item wr-m3-nav__item--has-submenu">
                    <a class="wr-nav-link wr-m3-nav__toggle" href="#" aria-haspopup="true" aria-expanded="false">Assignment Service by Cities <span class="wr-m3-nav__caret" aria-hidden="true"></span></a>
                    <ul class="wr-m3-nav__submenu">
                      <li><a class="menulink" href="../assignment-help-in-london/#menu">Assignment Help in London</a></li>
                      <li><a class="menulink" href="../assignment-help-in-glasgow/#menu">Assignment Help in Glasgow</a></li>
                      <li><a class="menulink" href="../assignment-help-in-manchester/#menu">Assignment Help in Manchester</a></li>
                      <li><a class="menulink" href="../assignment-help-in-leicester/#menu">Assignment Help in Leicester</a></li>
                      <li><a class="menulink" href="../assignment-help-in-liverpool/#menu">Assignment Help in Liverpool</a></li>
                      <li><a class="menulink" href="../assignment-help-in-cardiff/#menu">Assignment Help in Cardiff</a></li>
                      <li><a class="menulink" href="../assignment-help-in-bristol/#menu">Assignment Help in Bristol</a></li>
                      <li><a class="menulink" href="../assignment-help-in-birmingham/#menu">Assignment Help in Birmingham</a></li>
                    </ul>
                  </li>
                  <li>
                    <a class="menulink wr-nav-link wr-nav-cta" href="#wr-contact">Contact</a>
                  </li>
                  <li>
                    <a class="menulink wr-nav-link" href="../blog/">Blog</a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </header>
    <main id="main">
"""

FOOTER_AND_CLOSE = """    </main>
    <footer class="wr-footer" id="wr-footer">
      <div class="wr-footer__inner">
        <nav class="wr-footer__nav" aria-label="Site locations">
          <a href="../assignment-help-in-london/">London</a>
          <a href="../assignment-help-in-birmingham/">Birmingham</a>
          <a href="../assignment-help-in-manchester/">Manchester</a>
          <a href="../assignment-help-in-australia/">Australia</a>
          <a href="../assignment-help-in-uae-by-professionals/">UAE</a>
          <a href="../blog/">Blog</a>
        </nav>
        <ul class="wr-footer__social" aria-label="Writing Rodgers on social media">
          <li><a href="https://www.instagram.com/writingrodgerssolution/" target="_blank" rel="noopener" aria-label="Instagram">
            <img src="../imgs/image-22.webp" alt="" width="40" height="40" />
          </a></li>
          <li><a href="https://m.facebook.com/writingrodgersuk/" target="_blank" rel="noopener" aria-label="Facebook">
            <img src="../imgs/image-16.webp" alt="" width="40" height="40" />
          </a></li>
          <li><a href="http://linkedin.com/in/writing-rodgers-solution-a653871b3" target="_blank" rel="noopener" aria-label="LinkedIn">
            <img src="../imgs/image-17.webp" alt="" width="40" height="40" />
          </a></li>
        </ul>
        <p class="wr-footer__copy">
          © <time datetime="2026">2026</time>. <strong>Writing Rodgers™</strong>. All Rights Reserved.
        </p>
      </div>
    </footer>
  </div>
  <script src="../js/wr-nav.js" defer></script>
  <script src="../js/wr-gallery.js" defer></script>
</body>

</html>
"""

# --------------------------- EXTRACTORS ---------------------------

def extract_meta(html: str, slug: str) -> dict:
    """Extract per-page SEO from existing <head>."""
    title = re.search(r"<title>\s*(.*?)\s*</title>", html, re.S)
    description = re.search(r'<meta\s+content="([^"]+)"\s+name="description"', html)
    keywords = re.search(r'<meta\s+content="([^"]+)"\s+name="keywords"', html)
    og_title = re.search(r'<meta\s+content="([^"]+)"\s+property="og:title"', html)
    og_description = re.search(r'<meta\s+content="([^"]+)"\s+property="og:description"', html)
    twitter_title = re.search(r'<meta\s+content="([^"]+)"\s+property="twitter:title"', html)
    twitter_description = re.search(r'<meta\s+content="([^"]+)"\s+property="twitter:description"', html)

    return {
        "title": title.group(1).strip() if title else slug,
        "description": description.group(1) if description else "",
        "keywords": keywords.group(1) if keywords else "",
        "og_title": og_title.group(1) if og_title else "Writing Rodgers | Value Your Education",
        "og_description": og_description.group(1) if og_description else (description.group(1) if description else ""),
        "twitter_title": twitter_title.group(1) if twitter_title else "Writing Rodgers | Value Your Education",
        "twitter_description": twitter_description.group(1) if twitter_description else (description.group(1) if description else ""),
    }


# --------------------------- BODY CLEANUP ---------------------------

def clean_body_content(body: str) -> str:
    """Apply regex-based cleanup to page body content."""
    # Drop Bootstrap/Viamagus data attributes
    body = re.sub(r'\s+data-toggle="[^"]*"', "", body)
    body = re.sub(r'\s+data-hover="[^"]*"', "", body)
    body = re.sub(r'\s+data-target="\.nav-collapse"', "", body)
    body = re.sub(r'\s+data-component-name="[^"]*"', "", body)
    body = re.sub(r'\s+data-sticky-header="[^"]*"', "", body)
    body = re.sub(r'\s+data-bkg-image="[^"]*"', "", body)
    body = re.sub(r'\s+data-bkg-color="[^"]*"', "", body)
    body = re.sub(r'\s+data-transparent-menu-cover-mode="[^"]*"', "", body)
    body = re.sub(r'\s+data-original="[^"]*"', "", body)

    # Drop microdata
    body = re.sub(r'\s+itemscope=""', "", body)
    body = re.sub(r'\s+itemtype="[^"]*"', "", body)
    body = re.sub(r'\s+itemprop="[^"]*"', "", body)

    # Drop mid-body <link> tags loading legacy CSS files
    body = re.sub(r'\s*<link\s+href="\.\./css/main-\d+\.css"[^>]*/>\s*\n', "\n", body)

    # Drop inline scripts that depend on jQuery
    body = re.sub(r'\s*<script>\s*function loadViaBkgImage\(\) \{[^}]*\}\s*</script>\s*\n', "\n", body)
    body = re.sub(r'\s*<script>\s*\$\(function \(\) \{ Viamagus_Website_Loader\._init\(\); \}\);\s*</script>\s*\n', "\n", body)

    # Drop empty clear:both divs
    body = re.sub(r'\s*<div style="clear: both">\s*</div>\s*\n', "\n", body)

    # Rename featurette-heading -> wr-featurette__heading
    body = body.replace("featurette-heading", "wr-featurette__heading")

    # Wrap UK address in <address> if it's a plain <p>
    body = re.sub(
        r'<p><strong>(?:UK contact )?[Aa]ddress(?: \(UK\))?:</strong>\s*233 Holmesdale Rd, London SE25 6PR</p>',
        '<address><strong>UK contact address:</strong> 233 Holmesdale Rd, London SE25 6PR</address>',
        body,
    )

    # Convert wr-component--image-text / --richtext / --circle-image / --embed wrappers from <div> to <section>.
    # Use bs4 so opening AND matching closing tag both get swapped.
    body = _convert_component_divs_to_sections(body)

    return body


def _convert_component_divs_to_sections(html_fragment: str) -> str:
    """Rename <div class="wr-component wr-component--X..."> to <section ...> for X in
    {image-text, richtext, circle-image, embed}. Uses BeautifulSoup so both open and close swap."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return html_fragment

    # bs4 wraps fragments in <html><body>... — work around that
    soup = BeautifulSoup(html_fragment, "html.parser")
    target = re.compile(r"wr-component--(?:image-text|richtext|circle-image|embed)\b")
    changed = False
    for div in soup.find_all("div", class_=True):
        if any(target.search(c) for c in div.get("class", [])):
            div.name = "section"
            if not div.get("aria-label"):
                cid = div.get("id", "")
                label = cid.replace("wr-", "").replace("-", " ").strip() or "Content"
                div["aria-label"] = label.capitalize()
            changed = True
    return str(soup) if changed else html_fragment


def extract_body_content(html: str) -> str:
    """Extract the per-page body content between </header> and <footer>."""
    # Find the opening of <main> if it exists, else look for the breadcrumb / sub-hero / wr-page__container closing.
    # Patterns we look for as the END of the standard header block:
    #   </header>\n    <main id="main">      (already-migrated pages)
    #   </div> ... <nav class="wr-breadcrumb"  (original pages: wr-page__container closes, then breadcrumb starts)
    #
    # Patterns we look for as the START of the standard footer block:
    #   <footer class="wr-component wr-component--footer"
    #   <footer class="wr-footer"

    # Try matched-content variant first (page already migrated)
    m = re.search(r'<main id="main">\s*(.*?)\s*</main>\s*<footer', html, re.S)
    if m:
        return m.group(1)

    # Original-page variant: content sits between the header's closing div(s) and <footer ... wr-component--footer
    # Anchor on the breadcrumb nav or any wr- section right after the header.
    # The robust marker: end of nav#menu-nav's ul + closing divs + start of <nav class="wr-breadcrumb" OR <section
    m = re.search(
        r'</ul>\s*</nav>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*'
        r'(?:<link[^>]*/>\s*)*'
        r'(.*?)\s*<footer class="wr-component wr-component--footer"',
        html, re.S,
    )
    if m:
        return m.group(1)

    raise ValueError("Could not locate page body content between header and footer")


# --------------------------- MAIN ---------------------------

def migrate(path: Path, meta: dict) -> str:
    """Read the page, return the rewritten HTML."""
    html = path.read_text(encoding="utf-8")

    # Merge extracted SEO with the supplied per-page meta (supplied wins)
    extracted = extract_meta(html, meta["slug"])
    full_meta = {**extracted, **meta}

    # Extract page-specific body content
    body_content = extract_body_content(html)
    body_content = clean_body_content(body_content)

    head = build_head(full_meta)

    # Assemble
    return f"{head}\n\n{BODY_OPENING}{body_content}\n{FOOTER_AND_CLOSE}"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: migrate_page.py <path/to/index.html> <metadata.json>", file=sys.stderr)
        sys.exit(2)

    path = Path(sys.argv[1])
    meta_path = Path(sys.argv[2])
    meta = json.loads(meta_path.read_text())

    out = migrate(path, meta)
    path.write_text(out, encoding="utf-8")
    print(f"migrated: {path}")
