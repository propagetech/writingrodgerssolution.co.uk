/**
 * M3 navigation drawer — scrim, focus trap helpers, drawer chrome.
 * Requires jQuery + Bootstrap 2 collapse (main-7.js).
 */
(function ($) {
  'use strict';

  function initWrMobileNav() {
    var $menu = $('#menu');
    var $collapse = $menu.find('.nav-collapse');
    var $toggle = $menu.find('.btn-navbar');

    if (!$menu.length || !$collapse.length || !$toggle.length) {
      return;
    }

    if ($menu.data('wrM3NavInit')) {
      return;
    }
    $menu.data('wrM3NavInit', true);

    $toggle
      .addClass('wr-m3-menu-button')
      .attr({
        'aria-label': 'Open navigation menu',
        'aria-controls': 'menu-nav',
        'aria-expanded': 'false',
      });

    if (!$('.wr-m3-nav-scrim').length) {
      $('<div class="wr-m3-nav-scrim" aria-hidden="true" tabindex="-1"></div>').appendTo(
        document.body
      );
    }

    if (!$collapse.find('.wr-m3-drawer-header').length) {
      var $header = $(
        '<div class="wr-m3-drawer-header">' +
          '<p class="wr-m3-drawer-title">Menu</p>' +
          '<button type="button" class="wr-m3-drawer-close" aria-label="Close navigation menu">' +
          '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">' +
          '<path d="M18 6L6 18M6 6l12 12"/>' +
          '</svg></button></div>'
      );
      $collapse.prepend($header);
    }

    $collapse.attr('id', 'wr-mobile-nav-drawer');

    function setOpen(isOpen) {
      $('body').toggleClass('wr-m3-nav-open', isOpen);
      $toggle.attr('aria-expanded', isOpen ? 'true' : 'false');
      $toggle.attr('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
      $('.wr-m3-nav-scrim').attr('aria-hidden', isOpen ? 'false' : 'true');
      if (isOpen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    }

    function closeDrawer() {
      $collapse.collapse('hide');
    }

    $collapse.on('show', function () {
      setOpen(true);
      $collapse.addClass('wr-m3-drawer-open');
    });

    $collapse.on('hidden', function () {
      setOpen(false);
      $collapse.removeClass('wr-m3-drawer-open');
    });

    $('.wr-m3-nav-scrim, .wr-m3-drawer-close').on('click', function () {
      closeDrawer();
    });

    $(document).on('keydown.wrM3Nav', function (e) {
      if (e.key === 'Escape' && $('body').hasClass('wr-m3-nav-open')) {
        closeDrawer();
      }
    });

    $collapse.find('[data-toggle="collapse"]').on('click', function () {
      if ($('body').hasClass('wr-m3-nav-open')) {
        closeDrawer();
      }
    });

    $menu.find('.dropdown-toggle').each(function () {
      var $link = $(this);
      $link.addClass('wr-m3-nav-expander');
      if (!$link.find('.wr-m3-expander-icon').length) {
        $link.append(
          '<span class="wr-m3-expander-icon" aria-hidden="true">' +
            '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M6 9l6 6 6-6"/>' +
            '</svg></span>'
        );
      }
      $link.find('b.caret').hide();
    });
  }

  $(function () {
    initWrMobileNav();
    $(window).on('resize', function () {
      if (!window.matchMedia('(max-width: 979px)').matches && $('body').hasClass('wr-m3-nav-open')) {
        $('body').removeClass('wr-m3-nav-open');
        document.body.style.overflow = '';
        $('#menu .nav-collapse').removeClass('wr-m3-drawer-open');
      }
    });
  });
})(window.jQuery);
