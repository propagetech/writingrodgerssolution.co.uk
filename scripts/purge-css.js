/**
 * Strip unused CSS class definitions site-wide.
 *
 * Run AFTER any HTML/JS content changes to remove rules that no longer match
 * anything in the rendered markup.
 *
 *   cd scripts
 *   npm install purgecss               # one-time
 *   node purge-css.js                  # writes purged CSS in place over css/*.css
 *
 * Safelist keeps:
 *   - Bootstrap collapse/dropdown/fade dynamic state classes
 *   - M3 drawer state classes added by js/wr-mobile-nav.js
 *   - Carousel / slick / backstretch helpers
 *   - All wr-m3-*, wr-mcta*, wr-hero*, wr-step* (used by inline markup or JS)
 *
 * Removed: unused ecommerce/cart/product/form/payment/discount CSS (~33% of
 * internal-styles.css) since this site is brochure-only.
 */
const { PurgeCSS } = require('purgecss');
const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..');

const targets = [
  'css/main-7.css',
  'css/internal-styles.css',
  'css/wr-home.css',
];

(async () => {
  const results = await new PurgeCSS().purge({
    content: [`${REPO}/**/*.html`, `${REPO}/js/**/*.js`],
    css: targets.map(p => `${REPO}/${p}`),
    safelist: {
      standard: [
        /^in$/, /^open$/, /^active$/, /^show$/, /^hide$/, /^fade$/,
        /^collapse$/, /^collapsing$/, /^dropdown$/,
        /^wr-m3-drawer-open$/, /^wr-m3-nav-open$/, /^wr-m3-nav-scrim$/,
        /loader/i, /overlay/i, /sticky/i,
        /^backstretch$/, /^carousel-/, /^slick-/, /^item$/,
        /^error$/, /^success$/, /^warning$/, /^has-error$/,
      ],
      greedy: [/^wr-m3-/, /^wr-mcta/, /^wr-hero/, /^wr-step/],
    },
    keyframes: true,
    fontFace: false,
    variables: false,
  });

  let totalIn = 0, totalOut = 0;
  for (const r of results) {
    const inputSize = fs.statSync(r.file).size;
    const outputSize = Buffer.byteLength(r.css);
    fs.writeFileSync(r.file, r.css);
    totalIn += inputSize;
    totalOut += outputSize;
    const saved = Math.round(((inputSize - outputSize) / inputSize) * 100);
    const name = path.basename(r.file).padEnd(22);
    console.log(`${name} ${String(inputSize).padStart(7)} -> ${String(outputSize).padStart(7)}  (-${saved}%)`);
  }
  const tSaved = Math.round(((totalIn - totalOut) / totalIn) * 100);
  console.log('-'.repeat(50));
  console.log(`TOTAL                  ${String(totalIn).padStart(7)} -> ${String(totalOut).padStart(7)}  (-${tSaved}%)`);
})();
