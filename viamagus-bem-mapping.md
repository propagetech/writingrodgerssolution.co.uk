# viamagus → BEM rename mapping (for review)

**Status:** DRAFT — review before any code is touched.

## Principles

1. **Prefix:** `wr-` (Writing Rodgers). Drops the legacy CMS-vendor name.
2. **BEM strict:** `block`, `block__element`, `block--modifier`, `block__element--modifier`. Always kebab-case.
3. **Old "type" classes are modifiers of `wr-component`.** The CMS pattern was `<div class="viamagus-component viamagus_header">`. This becomes `<div class="wr-component wr-component--header">`.
4. **Instance IDs (`viamagus_Image_Text_7952`)** are not classes — they're per-instance HTML `id="…"`. They map to plain ids (`wr-image-text-7952`) and are NOT BEM-shaped. The CMS uses them as JS targets, so they MUST be renamed in lockstep with any JS that references them.
5. **Bootstrap 2 classes (`.navbar`, `.dropdown-menu`, `.container`, `.span6`, `.btn`) are untouched** — they are framework, not viamagus.
6. **JS-referenced tokens** are flagged `[JS]` — those require a synchronized edit in `js/main-*.js`.

---

## Block 1: Page root & component shell

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagusPageSettings` | `wr-page` | class | — | Root wrapper. Drops camelCase. |
| `viamagus-container` | `wr-page__container` | class | — | Inner of `wr-page`. |
| `viamagus-component` | `wr-component` | class | — | Base block every CMS component wears. |
| `viamagus-component-bg-colour` | `wr-component__bg` | class | [JS] | UK-spelling dropped. |
| `viamagus-component-content` | `wr-component__content` | class | [JS] | |
| `viamagus-component-content-inner` | `wr-component__content-inner` | class | — | |
| `viamagus-background` | `wr-component--has-bg` | class | [JS] | Modifier (component has a background image). |
| `viamagus-spacer` | `wr-component--spacer` | class | — | |
| `viamagus-richtext` | `wr-component--richtext` | class | — | |
| `viamagus-embedCode` | `wr-component--embed` | class | — | CamelCase dropped. |
| `viamagus-errorpage` | `wr-component--errorpage` | class | — | |
| `viamagus-menu-top-row` | `wr-component__menu-top-row` | class | — | |
| `viamagus-sticky-header` | `wr-component--sticky` | class | [JS] | |

## Block 2: Component-type modifiers (legacy `viamagus_<Type>` classes)

These were single-underscore "type" classes worn alongside `viamagus-component`. In BEM they become modifiers.

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus_header` | `wr-component--header` | class | [JS] | |
| `viamagus_footer` | `wr-component--footer` | class | [JS] | |
| `viamagus_image` | `wr-component--image` | class | [JS] | |
| `viamagus_landimg` | `wr-component--landing-image` | class | [JS] | |
| `viamagus_contact` | `wr-component--contact` | class | — | |
| `viamagus_circlimg` | `wr-component--circle-image` | class | — | |
| `viamagus_txt-slide` | `wr-component--text-slide` | class | [JS] | |
| `viamagus_update_ticker` | `wr-component--update-ticker` | class | [JS] | |
| `viamagus-image-text` | `wr-component--image-text` | class | [JS] | |
| `viamagus-img-txt-split` | `wr-component--image-text-split` | class | [JS] | |

## Block 3: CMS instance IDs (per-component)

Each is a unique `id="…"` baked at export time. These are not BEM-shaped; renaming preserves the instance number so each component stays uniquely addressable.

| Old (id) | New (id) | JS | Notes |
|---|---|---|---|
| `viamagus_Image_Text_7952` | `wr-image-text-7952` | — | |
| `viamagus_Image_Text_*` (all) | `wr-image-text-*` | — | 13 instances on this site. |
| `viamagus_Text_1597` | `wr-text-1597` | — | |
| `viamagus_Text_*` (all) | `wr-text-*` | — | 17 instances. |
| `viamagus_Text_1597-content` | `wr-text-1597__content` | — | The `-content` suffix becomes a BEM element on the per-instance scope. |
| `viamagus_Embed_Code_6729` | `wr-embed-6729` | — | |
| `viamagus_Footer_5319` | `wr-footer-5319` | — | |
| `viamagus_Section_Title_7947` | `wr-section-title-7947` | — | |
| `viamagus_Grid_gallery_3433` | `wr-grid-gallery-3433` | — | |
| `viamagus_columngrid_2567` | `wr-column-grid-2567` | — | |
| `viamagus_columngrid_2959` | `wr-column-grid-2959` | — | |
| `viamagus_form_2835` | `wr-form-2835` | — | |
| `viamagus_Text_video_7641` | `wr-text-video-7641` | — | |

## Block 4: Headings & text

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-heading1` | `wr-heading wr-heading--1` | class | — | Block + size modifier. |
| `viamagus-heading2` | `wr-heading wr-heading--2` | class | — | |
| `viamagus-heading3` | `wr-heading wr-heading--3` | class | — | |
| `viamagus-paragraph` | `wr-paragraph` | class | [JS] | |
| `viamagus-section-heading` | `wr-section__heading` | class | — | |
| `viamagus-section-header` | `wr-section__header` | class | — | |
| `viamagus-sectiontitle` | `wr-section__title` | class | — | |

## Block 5: Logo

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-business-logo` | `wr-business-logo` | class | — | |
| `viamagus-business-center-logo` | `wr-business-logo--center` | class | — | Modifier. |

## Block 6: Buttons

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-button-default` | `wr-button wr-button--default` | class | [JS] | Block + variant. |
| `viamagus-button-flat` | `wr-button wr-button--flat` | class | — | |
| `viamagus-button-transparent` | `wr-button wr-button--transparent` | class | — | |
| `viamagus-button-` (prefix in JS) | `wr-button--` | string | [JS] | Used as prefix; rewrite the JS prefix string. |
| `viamagus-cart-button` | `wr-cart__button` | class | [JS] | Belongs to the cart block. |
| `viamagus-submit` | `wr-button--submit` | class | — | |

## Block 7: Grid / gallery / masonry

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-grid` | `wr-grid` | class | — | |
| `viamagus-grid-item` | `wr-grid__item` | class | [JS] | |
| `viamagus-grid-item-info` | `wr-grid__item-info` | class | — | Hyphen, not nested element (`__item__info` is not BEM). |
| `viamagus-grid-gallery` | `wr-grid--gallery` | class | [JS] | |
| `viamagus-grid-gallery_` (JS prefix) | `wr-grid-gallery-` | string | [JS] | |
| `viamagus-grid-video-lightbox` | `wr-grid__video-lightbox` | class | [JS] | |
| `viamagus-masonry` | `wr-grid--masonry` | class | — | |
| `viamagus-image-lightbox` | `wr-lightbox--image` | class | [JS] | |

## Block 8: Carousel / slider

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-carousel-slider-info` | `wr-carousel__info` | class | — | |
| `viamagus-carousel-slider-text` | `wr-carousel__text` | class | — | |
| `viamagus-coverflow` | `wr-carousel--coverflow` | class | [JS] | |
| `viamagus-slick-gallery` | `wr-gallery--slick` | class | [JS] | |
| `viamagus-slick-text-container` | `wr-gallery__text-container` | class | — | |

## Block 9: News bar / ticker

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-news-bar` | `wr-news-bar` | class | [JS] | |
| `viamagus-news-bar-items` | `wr-news-bar__items` | class | [JS] | |
| `viamagus-news-bar-navigate` | `wr-news-bar__nav` | class | [JS] | |
| `viamagus-news-bar-title` | `wr-news-bar__title` | class | [JS] | |

## Block 10: Forms (generic)

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-form-` (JS prefix) | `wr-form-` | string | [JS] | |
| `viamagus-form-container` | `wr-form__container` | class | [JS] | |
| `viamagus-form-alignment` | `wr-form__alignment` | class | — | |
| `viamagus-form-vertical-alignment-style` | `wr-form--vertical-align` | class | [JS] | |
| `viamagus-custom-form` | `wr-form--custom` | class | [JS] | |
| `viamagus-form-google-distance-calculator` | `wr-form__google-distance` | class | [JS] | |
| `viamagus-form-google-map` | `wr-form__google-map` | class | [JS] | |
| `viamagus-form-product-summary` | `wr-form__product-summary` | class | [JS] | |
| `viamagus-form-products` | `wr-form__products` | class | [JS] | |
| `viamagus-custom-payment-summary` | `wr-form__payment-summary` | class | [JS] | |
| `viamagus-file-upload` | `wr-file-upload` | class | [JS] | |
| `viamagus-date-picker` | `wr-date-picker` | class | [JS] | |
| `viamagus-date-picker-icon` | `wr-date-picker__icon` | class | — | |
| `viamagus-combobox` | `wr-combobox` | class | [JS] | |
| `viamagus-format-number` | `wr-format--number` | class | [JS] | |
| `viamagus-phone` | `wr-phone` | class | [JS] | |

## Block 11: Contact

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-contact-form-address` | `wr-contact__address` | class | — | |
| `viamagus-contact-form-layout-2` | `wr-contact--layout-2` | class | — | |
| `viamagus-customer-email` | `wr-contact__customer-email` | class | — | |

## Block 12: Address / Google Map

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-address` | `wr-address` | class | [JS] | |
| `viamagus-address-input` | `wr-address__input` | class | [JS] | |
| `viamagus-address-clear-values` | `wr-address__clear` | class | [JS] | |
| `viamagus-google-address` | `wr-google-map__address` | class | [JS] | |
| `viamagus-google-latlng` | `wr-google-map__latlng` | class | [JS] | |
| `viamagus-google-map` | `wr-google-map` | class | [JS] | |
| `viamagus-google-map-canvas` | `wr-google-map__canvas` | class | [JS] | |
| `viamagus-google-mapzoom` | `wr-google-map__zoom` | class | [JS] | |

## Block 13: Ecommerce — cart

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-cart` | `wr-cart` | class | — | |
| `viamagus-cart-container` | `wr-cart__container` | class | — | |
| `viamagus-cart-count` | `wr-cart__count` | class | [JS] | |
| `viamagus-cart-icon` | `wr-cart__icon` | class | [JS] | |
| `viamagus-cart-img` | `wr-cart__img` | class | [JS] | |
| `viamagus-cart-item-row` | `wr-cart__item-row` | class | [JS] | |
| `viamagus-cart-item-remove` | `wr-cart__item-remove` | class | [JS] | |
| `viamagus-cart-minus` | `wr-cart__minus` | class | [JS] | |
| `viamagus-cart-plus` | `wr-cart__plus` | class | [JS] | |
| `viamagus-cart-qty` | `wr-cart__qty` | class | [JS] | |
| `viamagus-cart-qty-` (JS prefix) | `wr-cart__qty-` | string | [JS] | |
| `viamagus-cart-qty-container` | `wr-cart__qty-container` | class | [JS] | |
| `viamagus-shopping-cart` | `wr-shopping-cart` | class | [JS] | |
| `viamagus-shopping-cart-table-content` | `wr-shopping-cart__table` | class | [JS] | |

## Block 14: Ecommerce — checkout / payment / discount

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-checkout-summary` | `wr-checkout__summary` | class | [JS] | |
| `viamagus-order-summary-body` | `wr-checkout__order-summary` | class | [JS] | |
| `viamagus-place-order` | `wr-checkout__place-order` | class | [JS] | |
| `viamagus-recent-order-table-content` | `wr-checkout__recent-orders` | class | [JS] | |
| `viamagus-payment-cancel` | `wr-payment--cancel` | class | [JS] | |
| `viamagus-payment-failure` | `wr-payment--failure` | class | [JS] | |
| `viamagus-payment-success` | `wr-payment--success` | class | [JS] | |
| `viamagus-payment-form` | `wr-payment__form` | class | [JS] | |
| `viamagus-payment-mode-` (JS prefix) | `wr-payment__mode-` | string | [JS] | |
| `viamagus-payment-mode-payu` | `wr-payment__mode--payu` | class | [JS] | |
| `viamagus-payment-mode-section` | `wr-payment__mode-section` | class | [JS] | |
| `viamagus-discount-amount` | `wr-discount__amount` | class | [JS] | |
| `viamagus-discount-checkbox` | `wr-discount__checkbox` | class | [JS] | |
| `viamagus-discount-error-message` | `wr-discount__error` | class | [JS] | |
| `viamagus-apply-ecommerce-discount` | `wr-discount__apply` | class | [JS] | |
| `viamagus-remove-ecommerce-discount` | `wr-discount__remove` | class | [JS] | |
| `viamagus-total-after-discount-section` | `wr-discount__total-after` | class | [JS] | |

## Block 15: Ecommerce — products

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-product-desc` | `wr-product__desc` | class | — | |
| `viamagus-product-image-url` | `wr-product__image-url` | class | [JS] | |
| `viamagus-product-info` | `wr-product__info` | class | [JS] | |
| `viamagus-product-name` | `wr-product__name` | class | — | |
| `viamagus-product-price` | `wr-product__price` | class | [JS] | |
| `viamagus-product-qty` | `wr-product__qty` | class | [JS] | |
| `viamagus-product-select` | `wr-product__select` | class | [JS] | |
| `viamagus-product-subtotal` | `wr-product__subtotal` | class | [JS] | |
| `viamagus-product-summary-row` | `wr-product__summary-row` | class | [JS] | |
| `viamagus-allow-multiple-products-purchase` | `wr-product--allow-multiple` | class | [JS] | |
| `viamagus-allow-single-product-purchase` | `wr-product--allow-single` | class | [JS] | |

## Block 16: Auth (OTP, sign-in)

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-otp-input-validate` | `wr-otp__input` | class | [JS] | |
| `viamagus-otp-section` | `wr-otp__section` | class | [JS] | |
| `viamagus-email-otp-input-validate` | `wr-otp__input--email` | class | [JS] | |
| `viamagus-email-otp-section` | `wr-otp__section--email` | class | [JS] | |
| `viamagus-ecommerce-site` | `wr-ecommerce` | class | [JS] | |
| `viamagus-ecom-my-orders` | `wr-ecom__my-orders` | class | [JS] | |
| `viamagus-ecom-sign-in-link` | `wr-ecom__sign-in-link` | class | [JS] | |
| `viamagus-ecom-sign-in-link-section` | `wr-ecom__sign-in-section` | class | [JS] | |
| `viamagus-ecom-sign-in-success` | `wr-ecom__sign-in-success` | class | [JS] | |
| `viamagus-ecom-sign-out` | `wr-ecom__sign-out` | class | [JS] | |

## Block 17: Misc widgets

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus-clients-list` | `wr-clients-list` | class | [JS] | |
| `viamagus-social-feeds` | `wr-social-feeds` | class | [JS] | |
| `viamagus-audio-gallery` | `wr-audio-gallery` | class | [JS] | |
| `viamagus-background-video-player` | `wr-video--background` | class | [JS] | |
| `viamagus-play-video-icon` | `wr-video__play-icon` | class | [JS] | |
| `viamagus-video-img-container` | `wr-video__container` | class | — | |
| `viamagus-cover-page-pull-down-arrow` | `wr-cover-page__pull-down-arrow` | class | [JS] | |
| `viamagus-collapse-icon` | `wr-collapse__icon` | class | [JS] | |
| `viamagus-star-rating` | `wr-star-rating` | class | [JS] | |
| `viamagus-blog-post-desc` | `wr-blog-post__desc` | class | — | |
| `viamagus-blog-post-title` | `wr-blog-post__title` | class | — | |
| `viamagus-update-next` | `wr-update__next` | class | [JS] | |
| `viamagus-update-prev` | `wr-update__prev` | class | [JS] | |

## Block 18: Loader & overlay (single-underscore legacy)

| Old | New | Type | JS | Notes |
|---|---|---|---|---|
| `viamagus_loader` | `wr-loader` | class | [JS] | |
| `viamagus_overlay` | `wr-overlay` | class | [JS] | |
| `viamagusloader` | `wr-loader` | class | [JS] | Bare typo variant in `main-27.js` — merge. |

---

## Execution plan (after you approve mapping)

| Stage | Files touched | Rollback strategy |
|---|---|---|
| 1 | `css/wr-home.css`, `css/internal-styles.css` — add new BEM rules duplicating the old | The old viamagus-* rules remain; new rules are additive. |
| 2 | All 47 HTML files — swap classes (sed-driven) on a feature branch | `git restore .` |
| 3 | `js/main-*.js` — swap selector strings in the 7 referenced bundles | Per-file diff review |
| 4 | After visual regression passes on all pages, delete the old viamagus-* CSS rules | Final commit |

## Things I'd flag for you before approving

1. **`viamagus-paragraph`** is wildly common (in HTML and JS). The mapping above keeps it a top-level block (`wr-paragraph`), not `wr-component__paragraph`. Confirm.
2. **`viamagus-heading1/2/3`** I'm mapping to block + size modifier (`wr-heading wr-heading--1`). Two-class. Alternative: keep them as plain blocks `wr-heading-1`, `wr-heading-2`, `wr-heading-3`. Tell me which you want.
3. **CMS instance IDs** (Block 3) — I'm preserving the numbers (e.g. `viamagus_Image_Text_7952` → `wr-image-text-7952`). If you want sequential renumbering (1, 2, 3…) that's a separate decision.
4. **Bootstrap framework classes** (`btn`, `navbar`, `dropdown-menu`, `container-fluid`, `span6`) stay as-is. Not in scope.
5. **Behaviour after stage 2 but before stage 3** will look fine but JS event handlers won't fire on renamed elements. Plan to do stage 2 + 3 in one PR.
