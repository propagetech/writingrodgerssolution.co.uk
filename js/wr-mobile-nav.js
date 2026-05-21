/**
 * M3 mobile menu — top app bar + panel expands below; desktop horizontal nav.
 * Requires jQuery + Bootstrap 2 collapse (main-7.js).
 */
(function ($) {
  'use strict';

  function isMobileNav() {
    return window.matchMedia('(max-width: 979px)').matches;
  }

  function getDrawerHomeParent() {
    return $('#menu .navbar-inner');
  }

  function placeDrawer($collapse) {
    if (!$collapse.length) {
      return;
    }

    var $home = getDrawerHomeParent();
    if (!$home.length) {
      return;
    }

    var $row = $home.find('.wr-m3-app-bar__row').first();
    if ($row.length) {
      if ($collapse.prev()[0] !== $row[0]) {
        $collapse.insertAfter($row);
      }
      return;
    }

    if ($collapse.parent()[0] !== $home[0]) {
      $collapse.appendTo($home);
    }
  }

  function initWrMobileNav() {
    var $menu = $('#menu');
    var $collapse = $menu.find('.nav-collapse').add('body > .nav-collapse').first();
    var $toggle = $menu.find('.btn-navbar');

    if (!$menu.length || !$collapse.length || !$toggle.length) {
      return;
    }

    if ($menu.data('wrM3NavInit')) {
      placeDrawer($collapse);
      return;
    }
    $menu.data('wrM3NavInit', true);

    placeDrawer($collapse);

    $toggle
      .addClass('wr-m3-menu-button')
      .attr({
        'aria-label': 'Open navigation menu',
        'aria-controls': 'wr-mobile-nav-drawer',
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
      document.body.style.overflow = isOpen ? 'hidden' : '';
    }

    function closeDrawer() {
      $collapse.collapse('hide');
    }

    $collapse.on('show', function () {
      if (isMobileNav()) {
        $collapse.css('height', 'auto');
      }
      setOpen(true);
      $collapse.addClass('wr-m3-drawer-open');
    });

    $collapse.on('shown', function () {
      if (isMobileNav()) {
        $collapse.css('overflow-y', 'auto');
      }
    });

    $collapse.on('hidden', function () {
      if (isMobileNav()) {
        $collapse.css({ height: '', overflow: '' });
      }
      setOpen(false);
      $collapse.removeClass('wr-m3-drawer-open');
    });

    $('.wr-m3-nav-scrim').on('click', function () {
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
    });

    bindMobileDropdowns($menu, $collapse);
    syncNavChrome($menu);
  }

  function bindMobileDropdowns($menu, $collapse) {
    $menu.find('.dropdown-toggle').off('click.wrM3Dropdown').on('click.wrM3Dropdown', function (e) {
      var href = $(this).attr('href') || '';
      // Desktop: Bootstrap's dropdown JS skips toggling when href points to a real
      // anchor (e.g. "#wr-services"). Take over so the menu both opens AND scrolls.
      if (!isMobileNav()) {
        if (href.length > 1 && href.charAt(0) === '#') {
          e.preventDefault();
          var $item = $(this).closest('.dropdown');
          var wasOpen = $item.hasClass('open');
          $menu.find('.dropdown.open').removeClass('open');
          if (!wasOpen) {
            $item.addClass('open');
          }
          var target = document.querySelector(href);
          if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }
        return;
      }

      e.preventDefault();
      e.stopPropagation();

      var $item = $(this).closest('.dropdown');
      var isOpen = $item.hasClass('open');

      $menu.find('.dropdown.open').removeClass('open');
      if (!isOpen) {
        $item.addClass('open');
      }
    });

    $collapse.find('.dropdown-menu a').off('click.wrM3Subnav').on('click.wrM3Subnav', function () {
      if (!isMobileNav()) {
        return;
      }
      $collapse.collapse('hide');
    });
  }

  function syncNavChrome($menu) {
    if (isMobileNav()) {
      $menu.find('.dropdown-toggle .caret').hide();
      $menu.find('.wr-m3-expander-icon').show();
      return;
    }

    $menu.find('.dropdown-toggle .caret').show();
    $menu.find('.wr-m3-expander-icon').hide();
  }

  function syncDesktopNavState() {
    var $menu = $('#menu');
    var $collapse = $('#wr-mobile-nav-drawer');
    if (!$collapse.length) {
      $collapse = $menu.find('.nav-collapse').add('body > .nav-collapse').first();
    }
    if (!$collapse.length) {
      return;
    }

    if (!isMobileNav()) {
      $menu.find('.dropdown.open').removeClass('open');
      $('body').removeClass('wr-m3-nav-open');
      document.body.style.overflow = '';
      $collapse.removeClass('wr-m3-drawer-open collapsing');
      $collapse.css({ height: '', overflow: '' });
      if ($collapse.hasClass('collapse') && !$collapse.hasClass('in')) {
        $collapse.addClass('in');
      }
      return;
    }

    if ($collapse.hasClass('in') && !$('body').hasClass('wr-m3-nav-open')) {
      $collapse.removeClass('in wr-m3-drawer-open');
    }
  }

  $(function () {
    initWrMobileNav();
    syncNavChrome($('#menu'));
    syncDesktopNavState();

    $(window).on('resize.wrM3Nav', function () {
      var $menu = $('#menu');
      var $collapse = $('#wr-mobile-nav-drawer');
      if (!$collapse.length) {
        $collapse = $('#menu .nav-collapse').add('body > .nav-collapse').first();
      }
      placeDrawer($collapse);
      bindMobileDropdowns($menu, $collapse);
      syncNavChrome($menu);
      syncDesktopNavState();
    });
  });
})(window.jQuery);
