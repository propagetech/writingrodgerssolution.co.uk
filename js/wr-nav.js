/* wr-nav.js — vanilla navigation behaviors for index.html
 *
 * Replaces:
 *   - jQuery 1.9 (main-7.js)
 *   - Bootstrap 2 JS dropdown + collapse (main-23.js)
 *   - wr-mobile-nav.js (jQuery + Bootstrap collapse)
 *   - wr-nav-active.js (active link highlighting)
 *
 * Provides:
 *   - Mobile hamburger toggles the M3 navigation drawer
 *   - Dropdown toggles open/close on click (prevents default href scroll)
 *   - Submenu hover with 200ms delay on desktop (handled in CSS)
 *   - Outside-click / Escape closes any open dropdown
 *   - Mobile: tapping a link inside the drawer closes the drawer
 *   - Active link highlighting based on current URL
 */
(function () {
  'use strict';

  var MOBILE_BREAKPOINT = 979; // matches wr-home.css

  function isMobile() {
    return window.innerWidth <= MOBILE_BREAKPOINT;
  }

  // ---------- Hamburger / drawer ----------

  function setupHamburger() {
    var toggle = document.querySelector('.wr-m3-menu-button');
    var drawer = document.querySelector('.wr-m3-navigation-drawer');
    if (!toggle || !drawer) return;

    toggle.setAttribute('aria-controls', drawer.id || 'wr-m3-nav-drawer');
    toggle.setAttribute('aria-expanded', 'false');

    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      var open = document.body.classList.toggle('wr-m3-nav-open');
      drawer.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    // Close drawer when any link inside is clicked (mobile only)
    drawer.addEventListener('click', function (e) {
      if (!isMobile()) return;
      var link = e.target.closest('a.wr-nav-link');
      if (!link) return;
      // Submenu parent links don't close — they expand
      if (link.classList.contains('wr-m3-nav__toggle')) return;
      closeDrawer();
    });

    // Close drawer when the scrim is clicked
    var scrim = document.querySelector('.wr-m3-nav-scrim');
    if (scrim) {
      scrim.addEventListener('click', closeDrawer);
    }

    // Close drawer on Esc
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('wr-m3-nav-open')) {
        closeDrawer();
        toggle.focus();
      }
    });

    // If the viewport grows past mobile, force-close the drawer
    window.addEventListener('resize', function () {
      if (!isMobile()) closeDrawer();
    });

    function closeDrawer() {
      document.body.classList.remove('wr-m3-nav-open');
      drawer.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  }

  // ---------- Dropdown / submenu ----------
  //
  // Markup contract:
  //   <li class="wr-m3-nav__item wr-m3-nav__item--has-submenu">
  //     <a class="wr-nav-link wr-m3-nav__toggle" href="#" aria-haspopup="true" aria-expanded="false">
  //       Label <span class="wr-m3-nav__caret" aria-hidden="true"></span>
  //     </a>
  //     <ul class="wr-m3-nav__submenu"> ... </ul>
  //   </li>

  function setupDropdowns() {
    var toggles = document.querySelectorAll('.wr-m3-nav__toggle');

    toggles.forEach(function (toggle) {
      var item = toggle.closest('.wr-m3-nav__item--has-submenu');
      if (!item) return;

      toggle.addEventListener('click', function (e) {
        // Always prevent the anchor href from scrolling / navigating.
        // The submenu opens instead — selecting a submenu item navigates.
        e.preventDefault();

        var nowOpen = !item.classList.contains('is-open');

        // Close other open dropdowns first (one-at-a-time on desktop)
        if (!isMobile()) {
          closeAllDropdowns();
        }

        item.classList.toggle('is-open', nowOpen);
        toggle.setAttribute('aria-expanded', nowOpen ? 'true' : 'false');
      });
    });

    // Outside-click closes all open dropdowns
    document.addEventListener('click', function (e) {
      if (e.target.closest('.wr-m3-nav__item--has-submenu')) return;
      closeAllDropdowns();
    });

    // Escape closes the dropdown that has focus inside it
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      var openItem = document.querySelector('.wr-m3-nav__item--has-submenu.is-open');
      if (openItem) {
        openItem.classList.remove('is-open');
        var t = openItem.querySelector('.wr-m3-nav__toggle');
        if (t) {
          t.setAttribute('aria-expanded', 'false');
          t.focus();
        }
      }
    });
  }

  function closeAllDropdowns() {
    document.querySelectorAll('.wr-m3-nav__item--has-submenu.is-open').forEach(function (li) {
      li.classList.remove('is-open');
      var t = li.querySelector('.wr-m3-nav__toggle');
      if (t) t.setAttribute('aria-expanded', 'false');
    });
  }

  // ---------- Active link highlighting ----------
  //
  // Adds .is-active to the nav link whose href matches the current path,
  // and .is-active-parent to its dropdown toggle (if any).

  function setupActiveLink() {
    var path = window.location.pathname.replace(/\/$/, ''); // strip trailing slash
    if (!path) return; // root — no specific page link to highlight

    var links = document.querySelectorAll('.wr-nav-link, .wr-m3-nav__submenu a');
    links.forEach(function (a) {
      var href = a.getAttribute('href') || '';
      if (!href || href === '#' || href.charAt(0) === '#') return;

      // Normalise to a comparable path
      var linkPath = href.replace(/#.*$/, '').replace(/\/$/, '');
      // Resolve relative paths against the current page
      try {
        linkPath = new URL(href, window.location.href).pathname.replace(/\/$/, '');
      } catch (_) { /* keep raw */ }

      if (linkPath && linkPath === path) {
        a.classList.add('is-active');
        var parentItem = a.closest('.wr-m3-nav__item--has-submenu');
        if (parentItem) {
          var parentLink = parentItem.querySelector(':scope > .wr-m3-nav__toggle');
          if (parentLink) parentLink.classList.add('is-active-parent');
        }
      }
    });
  }

  // ---------- Auto-hide on scroll down / reveal on scroll up ----------
  //
  // Behaviour:
  //   - Scrolling DOWN > 6px past the top zone hides the nav (slides up)
  //   - Scrolling UP by ANY amount (even 1px) reveals it
  //   - Always visible within SHOW_AT_TOP_THRESHOLD px of the top
  //   - Stays visible while the mobile drawer is open, a submenu is open,
  //     or keyboard focus is inside the menu
  //   - Throttled to one update per animation frame for smoothness

  function setupAutoHide() {
    var header = document.getElementById('menu');
    if (!header) return;

    var SHOW_AT_TOP_THRESHOLD = 80; // px — always visible above this scrollY
    var DOWN_DELTA = 6;             // need >6px down-movement to hide
    var lastY = window.scrollY;
    var ticking = false;

    function shouldStayVisible() {
      if (document.body.classList.contains('wr-m3-nav-open')) return true;
      if (document.querySelector('.wr-m3-nav__item--has-submenu.is-open')) return true;
      var active = document.activeElement;
      if (active && active !== document.body && header.contains(active)) return true;
      return false;
    }

    function update() {
      var currentY = window.scrollY;
      var delta = currentY - lastY;

      if (currentY <= SHOW_AT_TOP_THRESHOLD || shouldStayVisible()) {
        header.classList.remove('is-hidden');
      } else if (delta > DOWN_DELTA) {
        header.classList.add('is-hidden');
      } else if (delta < 0) {
        // Any upward movement reveals
        header.classList.remove('is-hidden');
      }

      lastY = currentY;
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(update);
        ticking = true;
      }
    }, { passive: true });
  }

  // ---------- Init ----------

  function init() {
    setupHamburger();
    setupDropdowns();
    setupActiveLink();
    setupAutoHide();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
