/* Highlights the menu link matching the current page.
   Adds `.is-active` to the matching submenu link, and `.is-active-parent`
   to its dropdown trigger so the parent label also reads as selected.
   Vanilla JS, no jQuery dependency. */
(function () {
  'use strict';

  function slugFromHref(href) {
    if (!href) return '';
    // Strip leading "./" or "../" segments
    var s = href.replace(/^(?:\.\.?\/)+/, '');
    // Strip query and fragment
    s = s.replace(/[?#].*$/, '');
    // Strip trailing slash
    s = s.replace(/\/+$/, '');
    return s.toLowerCase();
  }

  function currentSlug() {
    // pathname looks like "/nursing-assignment-help/" or "/" on home
    var p = location.pathname.replace(/^\/+|\/+$/g, '');
    // If served as index.html (rare), strip the filename
    p = p.replace(/(?:^|\/)index\.html?$/, '');
    return p.toLowerCase();
  }

  function apply() {
    var here = currentSlug();
    var links = document.querySelectorAll('#menu-nav a');
    var marked = false;

    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = a.getAttribute('href');
      if (!href) continue;
      var target = slugFromHref(href);

      var isMatch = false;
      if (here === '') {
        // Home page — match the "Home" link (href="#wr-hero" → target "")
        isMatch = target === '' && href.indexOf('#wr-hero') === 0;
      } else {
        // Subpage — exact slug match (e.g., "nursing-assignment-help")
        isMatch = target !== '' && target === here;
      }

      if (isMatch) {
        a.classList.add('is-active');
        marked = true;
        var parentLi = a.closest('li.dropdown');
        if (parentLi) {
          parentLi.classList.add('is-active-parent');
          var trigger = parentLi.children[0];
          if (trigger && trigger.tagName === 'A') {
            trigger.classList.add('is-active-parent');
          }
        }
      }
    }

    // Fallback: if no match found, leave menu untouched (no false-positive highlight)
    return marked;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', apply);
  } else {
    apply();
  }
})();
