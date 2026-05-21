"""Rename every viamagus-* / viamagus_* token to its BEM equivalent.

Mapping comes from viamagus-bem-mapping.md.
- Literal classes are replaced via str.replace in length-DESC order to avoid
  substring collisions (e.g. viamagus-component-content before viamagus-component).
- CMS instance ids like viamagus_Image_Text_7952 are handled with regex so the
  trailing instance number is preserved.

Heading and button classes that previously expanded to two-class output are
flattened to a single class for safe 1:1 replacement (wr-heading-1, wr-button-default).

Run modes:
    python scripts/rename_viamagus_to_bem.py --dry-run   # report only
    python scripts/rename_viamagus_to_bem.py             # apply edits
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

LITERAL_MAPPINGS: dict[str, str] = {
    # ---- Block 1: Page root & component shell ---------------------------------
    "viamagus-component-content-inner": "wr-component__content-inner",
    "viamagus-component-content": "wr-component__content",
    "viamagus-component-bg-colour": "wr-component__bg",
    "viamagus-background-video-player": "wr-video--background",
    "viamagus-background": "wr-component--has-bg",
    "viamagus-component": "wr-component",
    "viamagusPageSettings": "wr-page",
    "viamagus-container": "wr-page__container",
    "viamagus-spacer": "wr-component--spacer",
    "viamagus-richtext": "wr-component--richtext",
    "viamagus-embedCode": "wr-component--embed",
    "viamagus-errorpage": "wr-component--errorpage",
    "viamagus-menu-top-row": "wr-component__menu-top-row",
    "viamagus-sticky-header": "wr-component--sticky",
    # ---- Block 2: type modifiers ----------------------------------------------
    "viamagus-img-txt-split": "wr-component--image-text-split",
    "viamagus-image-text": "wr-component--image-text",
    "viamagus_update_ticker": "wr-component--update-ticker",
    "viamagus_txt-slide": "wr-component--text-slide",
    "viamagus_landimg": "wr-component--landing-image",
    "viamagus_circlimg": "wr-component--circle-image",
    "viamagus_contact": "wr-component--contact",
    "viamagus_header": "wr-component--header",
    "viamagus_footer": "wr-component--footer",
    "viamagus_image": "wr-component--image",
    # ---- Block 4: headings & text (flat 1-class) ------------------------------
    "viamagus-section-heading": "wr-section__heading",
    "viamagus-section-header": "wr-section__header",
    "viamagus-sectiontitle": "wr-section__title",
    "viamagus-paragraph": "wr-paragraph",
    "viamagus-heading1": "wr-heading-1",
    "viamagus-heading2": "wr-heading-2",
    "viamagus-heading3": "wr-heading-3",
    # ---- Block 5: logo ---------------------------------------------------------
    "viamagus-business-center-logo": "wr-business-logo--center",
    "viamagus-business-logo": "wr-business-logo",
    # ---- Block 6: buttons (flat) ----------------------------------------------
    "viamagus-button-transparent": "wr-button-transparent",
    "viamagus-button-default": "wr-button-default",
    "viamagus-button-flat": "wr-button-flat",
    "viamagus-button-": "wr-button-",      # prefix, processed after specific ones
    "viamagus-cart-button": "wr-cart__button",
    "viamagus-submit": "wr-button-submit",
    # ---- Block 7: grid / gallery / lightbox -----------------------------------
    "viamagus-grid-video-lightbox": "wr-grid__video-lightbox",
    "viamagus-grid-gallery_": "wr-grid-gallery-",
    "viamagus-grid-gallery": "wr-grid--gallery",
    "viamagus-grid-item-info": "wr-grid__item-info",
    "viamagus-grid-item": "wr-grid__item",
    "viamagus-image-lightbox": "wr-lightbox--image",
    "viamagus-masonry": "wr-grid--masonry",
    "viamagus-grid": "wr-grid",
    # ---- Block 8: carousel / slider -------------------------------------------
    "viamagus-carousel-slider-info": "wr-carousel__info",
    "viamagus-carousel-slider-text": "wr-carousel__text",
    "viamagus-slick-text-container": "wr-gallery__text-container",
    "viamagus-slick-gallery": "wr-gallery--slick",
    "viamagus-coverflow": "wr-carousel--coverflow",
    # ---- Block 9: news bar / ticker -------------------------------------------
    "viamagus-news-bar-navigate": "wr-news-bar__nav",
    "viamagus-news-bar-items": "wr-news-bar__items",
    "viamagus-news-bar-title": "wr-news-bar__title",
    "viamagus-news-bar": "wr-news-bar",
    # ---- Block 10: forms / inputs ---------------------------------------------
    "viamagus-form-google-distance-calculator": "wr-form__google-distance",
    "viamagus-form-vertical-alignment-style": "wr-form--vertical-align",
    "viamagus-custom-payment-summary": "wr-form__payment-summary",
    "viamagus-form-product-summary": "wr-form__product-summary",
    "viamagus-form-google-map": "wr-form__google-map",
    "viamagus-form-container": "wr-form__container",
    "viamagus-form-alignment": "wr-form__alignment",
    "viamagus-form-products": "wr-form__products",
    "viamagus-custom-form": "wr-form--custom",
    "viamagus-form-": "wr-form-",
    "viamagus-date-picker-icon": "wr-date-picker__icon",
    "viamagus-date-picker": "wr-date-picker",
    "viamagus-format-number": "wr-format--number",
    "viamagus-file-upload": "wr-file-upload",
    "viamagus-combobox": "wr-combobox",
    "viamagus-phone": "wr-phone",
    # ---- Block 11: contact ----------------------------------------------------
    "viamagus-contact-form-layout-2": "wr-contact--layout-2",
    "viamagus-contact-form-address": "wr-contact__address",
    "viamagus-customer-email": "wr-contact__customer-email",
    # ---- Block 12: address & google map ---------------------------------------
    "viamagus-address-clear-values": "wr-address__clear",
    "viamagus-google-map-canvas": "wr-google-map__canvas",
    "viamagus-google-mapzoom": "wr-google-map__zoom",
    "viamagus-google-address": "wr-google-map__address",
    "viamagus-google-latlng": "wr-google-map__latlng",
    "viamagus-address-input": "wr-address__input",
    "viamagus-google-map": "wr-google-map",
    "viamagus-address": "wr-address",
    # ---- Block 13: cart -------------------------------------------------------
    "viamagus-cart-qty-container": "wr-cart__qty-container",
    "viamagus-cart-item-remove": "wr-cart__item-remove",
    "viamagus-cart-item-row": "wr-cart__item-row",
    "viamagus-cart-container": "wr-cart__container",
    "viamagus-cart-qty-": "wr-cart__qty-",
    "viamagus-cart-qty": "wr-cart__qty",
    "viamagus-cart-count": "wr-cart__count",
    "viamagus-cart-icon": "wr-cart__icon",
    "viamagus-cart-minus": "wr-cart__minus",
    "viamagus-cart-plus": "wr-cart__plus",
    "viamagus-cart-img": "wr-cart__img",
    "viamagus-cart": "wr-cart",
    "viamagus-shopping-cart-table-content": "wr-shopping-cart__table",
    "viamagus-shopping-cart": "wr-shopping-cart",
    # ---- Block 14: checkout / payment / discount ------------------------------
    "viamagus-recent-order-table-content": "wr-checkout__recent-orders",
    "viamagus-total-after-discount-section": "wr-discount__total-after",
    "viamagus-apply-ecommerce-discount": "wr-discount__apply",
    "viamagus-remove-ecommerce-discount": "wr-discount__remove",
    "viamagus-discount-error-message": "wr-discount__error",
    "viamagus-order-summary-body": "wr-checkout__order-summary",
    "viamagus-payment-mode-section": "wr-payment__mode-section",
    "viamagus-discount-checkbox": "wr-discount__checkbox",
    "viamagus-payment-mode-payu": "wr-payment__mode--payu",
    "viamagus-checkout-summary": "wr-checkout__summary",
    "viamagus-discount-amount": "wr-discount__amount",
    "viamagus-payment-failure": "wr-payment--failure",
    "viamagus-payment-success": "wr-payment--success",
    "viamagus-payment-cancel": "wr-payment--cancel",
    "viamagus-payment-form": "wr-payment__form",
    "viamagus-payment-mode-": "wr-payment__mode-",
    "viamagus-place-order": "wr-checkout__place-order",
    # ---- Block 15: products ---------------------------------------------------
    "viamagus-allow-multiple-products-purchase": "wr-product--allow-multiple",
    "viamagus-allow-single-product-purchase": "wr-product--allow-single",
    "viamagus-product-summary-row": "wr-product__summary-row",
    "viamagus-product-image-url": "wr-product__image-url",
    "viamagus-product-subtotal": "wr-product__subtotal",
    "viamagus-product-select": "wr-product__select",
    "viamagus-product-price": "wr-product__price",
    "viamagus-product-info": "wr-product__info",
    "viamagus-product-name": "wr-product__name",
    "viamagus-product-desc": "wr-product__desc",
    "viamagus-product-qty": "wr-product__qty",
    # ---- Block 16: auth / ecom ------------------------------------------------
    "viamagus-email-otp-input-validate": "wr-otp__input--email",
    "viamagus-ecom-sign-in-link-section": "wr-ecom__sign-in-section",
    "viamagus-otp-input-validate": "wr-otp__input",
    "viamagus-email-otp-section": "wr-otp__section--email",
    "viamagus-ecom-sign-in-success": "wr-ecom__sign-in-success",
    "viamagus-ecom-sign-in-link": "wr-ecom__sign-in-link",
    "viamagus-ecom-my-orders": "wr-ecom__my-orders",
    "viamagus-ecom-sign-out": "wr-ecom__sign-out",
    "viamagus-ecommerce-site": "wr-ecommerce",
    "viamagus-otp-section": "wr-otp__section",
    # ---- Block 17: misc widgets -----------------------------------------------
    "viamagus-cover-page-pull-down-arrow": "wr-cover-page__pull-down-arrow",
    "viamagus-video-img-container": "wr-video__container",
    "viamagus-play-video-icon": "wr-video__play-icon",
    "viamagus-audio-gallery": "wr-audio-gallery",
    "viamagus-blog-post-title": "wr-blog-post__title",
    "viamagus-collapse-icon": "wr-collapse__icon",
    "viamagus-blog-post-desc": "wr-blog-post__desc",
    "viamagus-social-feeds": "wr-social-feeds",
    "viamagus-clients-list": "wr-clients-list",
    "viamagus-star-rating": "wr-star-rating",
    "viamagus-update-next": "wr-update__next",
    "viamagus-update-prev": "wr-update__prev",
    # ---- Block 18: loader & overlay -------------------------------------------
    "viamagus_loader": "wr-loader",
    "viamagus_overlay": "wr-overlay",
    "viamagusloader": "wr-loader",  # typo variant in main-27.js
}

# CMS instance-id patterns (regex so we preserve the trailing number)
REGEX_MAPPINGS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"viamagus_Image_Text_(\d+)"), r"wr-image-text-\1"),
    (re.compile(r"viamagus_Text_(\d+)-content"), r"wr-text-\1__content"),
    (re.compile(r"viamagus_Text_video_(\d+)"), r"wr-text-video-\1"),
    (re.compile(r"viamagus_Text_(\d+)"), r"wr-text-\1"),
    (re.compile(r"viamagus_Embed_Code_(\d+)"), r"wr-embed-\1"),
    (re.compile(r"viamagus_Footer_(\d+)"), r"wr-footer-\1"),
    (re.compile(r"viamagus_Section_Title_(\d+)"), r"wr-section-title-\1"),
    (re.compile(r"viamagus_Grid_gallery_(\d+)"), r"wr-grid-gallery-\1"),
    (re.compile(r"viamagus_columngrid_(\d+)"), r"wr-column-grid-\1"),
    (re.compile(r"viamagus_form_(\d+)"), r"wr-form-\1"),
]

SORTED_LITERALS = sorted(LITERAL_MAPPINGS.items(), key=lambda kv: -len(kv[0]))

EXCLUDED_NAMES = {
    "viamagus-bem-mapping.md",
    "rename_viamagus_to_bem.py",
}
EXCLUDED_DIR_PARTS = {"__pycache__", ".git", "node_modules"}
TARGET_SUFFIXES = {".html", ".css", ".js"}


def should_process(path: Path) -> bool:
    if path.name in EXCLUDED_NAMES:
        return False
    if any(part in EXCLUDED_DIR_PARTS for part in path.parts):
        return False
    return path.suffix in TARGET_SUFFIXES


def transform(text: str) -> tuple[str, Counter]:
    counter: Counter = Counter()
    for pattern, replacement in REGEX_MAPPINGS:
        new_text, n = pattern.subn(replacement, text)
        if n:
            counter[pattern.pattern] += n
            text = new_text
    for old, new in SORTED_LITERALS:
        if old in text:
            counter[old] += text.count(old)
            text = text.replace(old, new)
    return text, counter


# JS-only transform: only rename inside string literals so we don't corrupt JS
# identifiers (e.g. `viamagus_loader.remove()` must NOT become `wr-loader.remove()`).
_STRING_LITERAL = re.compile(r"'([^'\\\n]*(?:\\.[^'\\\n]*)*)'|\"([^\"\\\n]*(?:\\.[^\"\\\n]*)*)\"")


def transform_js(text: str) -> tuple[str, Counter]:
    counter: Counter = Counter()

    def replace_in_literal(match: re.Match[str]) -> str:
        quote = match.group(0)[0]
        inner = match.group(1) if match.group(1) is not None else match.group(2)
        new_inner = inner
        for pattern, replacement in REGEX_MAPPINGS:
            new_inner, n = pattern.subn(replacement, new_inner)
            if n:
                counter[pattern.pattern] += n
        for old, new in SORTED_LITERALS:
            if old in new_inner:
                counter[old] += new_inner.count(old)
                new_inner = new_inner.replace(old, new)
        return f"{quote}{new_inner}{quote}"

    new_text = _STRING_LITERAL.sub(replace_in_literal, text)
    return new_text, counter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    args = parser.parse_args()

    file_count = 0
    change_count = 0
    total_counter: Counter = Counter()

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or not should_process(path):
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix == ".js":
            new_text, counter = transform_js(original)
        else:
            new_text, counter = transform(original)
        if new_text == original:
            continue
        change_count += sum(counter.values())
        total_counter.update(counter)
        file_count += 1
        rel = path.relative_to(ROOT)
        replacements = sum(counter.values())
        print(f"  {rel}: {replacements} replacement(s)")
        if not args.dry_run:
            path.write_text(new_text, encoding="utf-8")

    print()
    print(f"{'Would touch' if args.dry_run else 'Touched'} {file_count} files,"
          f" {change_count} total replacements.")
    print()
    print("Top tokens by replacement count:")
    for token, count in total_counter.most_common(20):
        print(f"  {count:>5}  {token}")


if __name__ == "__main__":
    main()
