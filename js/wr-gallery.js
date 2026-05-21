/* Gallery lightbox — click any photo to open a fullscreen carousel.
   Vanilla JS, no jQuery dependency.
   Keyboard: Esc = close, ← / → = navigate.
   Touch: swipe left/right to navigate. */
(function () {
  'use strict';

  var grid = document.getElementById('wr-gallery-grid');
  var lightbox = document.getElementById('wr-lightbox');
  if (!grid || !lightbox) return;

  var imgEl = document.getElementById('wr-lightbox-img');
  var bgEl = document.getElementById('wr-lightbox-bg');
  var captionEl = document.getElementById('wr-lightbox-caption');

  var items = Array.prototype.map.call(grid.querySelectorAll('.wr-gallery__img'), function (img) {
    return { src: img.getAttribute('src'), alt: img.getAttribute('alt') || '' };
  });

  var currentIndex = 0;
  var lastFocus = null;

  function show(index) {
    if (index < 0) index = items.length - 1;
    if (index >= items.length) index = 0;
    currentIndex = index;
    var item = items[index];
    imgEl.src = item.src;
    imgEl.alt = item.alt;
    bgEl.style.backgroundImage = "url('" + item.src + "')";
    captionEl.textContent = item.alt + '  ·  ' + (index + 1) + ' / ' + items.length;
  }

  function open(index) {
    lastFocus = document.activeElement;
    show(index);
    lightbox.hidden = false;
    lightbox.classList.add('is-open');
    document.body.classList.add('wr-lightbox-open');
    lightbox.querySelector('[data-wr-lightbox-next]').focus();
  }

  function close() {
    lightbox.classList.remove('is-open');
    lightbox.hidden = true;
    document.body.classList.remove('wr-lightbox-open');
    imgEl.src = '';
    bgEl.style.backgroundImage = '';
    if (lastFocus && typeof lastFocus.focus === 'function') {
      lastFocus.focus();
    }
  }

  grid.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-wr-gallery-open]');
    if (!btn) return;
    var index = parseInt(btn.getAttribute('data-wr-gallery-open'), 10) || 0;
    open(index);
  });

  lightbox.addEventListener('click', function (e) {
    if (e.target.closest('[data-wr-lightbox-close]')) {
      close();
    } else if (e.target.closest('[data-wr-lightbox-prev]')) {
      show(currentIndex - 1);
    } else if (e.target.closest('[data-wr-lightbox-next]')) {
      show(currentIndex + 1);
    }
  });

  document.addEventListener('keydown', function (e) {
    if (lightbox.hidden) return;
    if (e.key === 'Escape') { e.preventDefault(); close(); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); show(currentIndex - 1); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); show(currentIndex + 1); }
  });

  // Touch swipe (≥ 40px horizontal, < 60px vertical)
  var touchX = null, touchY = null;
  lightbox.addEventListener('touchstart', function (e) {
    if (!e.touches[0]) return;
    touchX = e.touches[0].clientX;
    touchY = e.touches[0].clientY;
  }, { passive: true });
  lightbox.addEventListener('touchend', function (e) {
    if (touchX === null || !e.changedTouches[0]) return;
    var dx = e.changedTouches[0].clientX - touchX;
    var dy = e.changedTouches[0].clientY - touchY;
    touchX = touchY = null;
    if (Math.abs(dy) > 60) return;
    if (dx < -40) show(currentIndex + 1);
    else if (dx > 40) show(currentIndex - 1);
  });

  // -----------------------------------------------------------------------
  // Auto-rotating carousel for the gallery section.
  // Desktop (≥769px): 3 cards visible, slide one card per tick.
  // Mobile (≤768px):  one card visible, crossfade to the next.
  // Pauses on hover / focus / hidden tab / open lightbox / reduced-motion.
  // -----------------------------------------------------------------------
  (function () {
    var carouselItems = Array.prototype.slice.call(
      grid.querySelectorAll('.wr-gallery__item')
    );
    if (carouselItems.length < 2) return;

    var section = document.getElementById('wr-gallery');
    var VIEW = 3; // cards visible at once on desktop
    var INTERVAL = 4000;
    var idx = 0;
    var timer = null;

    var mqMobile = window.matchMedia('(max-width: 768px)');
    var mqReduce = window.matchMedia('(prefers-reduced-motion: reduce)');

    function render() {
      if (mqMobile.matches) {
        // mobile: crossfade
        for (var k = 0; k < carouselItems.length; k++) {
          carouselItems[k].classList.toggle('is-active', k === idx);
          carouselItems[k].classList.remove('is-middle');
        }
        grid.style.transform = '';
      } else {
        // desktop: slide track + scale-up the centre card of the visible window
        for (var j = 0; j < carouselItems.length; j++) {
          carouselItems[j].classList.remove('is-active');
          // Of the 3 visible cards (idx, idx+1, idx+2), idx+1 is the centre.
          carouselItems[j].classList.toggle('is-middle', j === idx + 1);
        }
        var first = carouselItems[0].getBoundingClientRect();
        var second = carouselItems[1].getBoundingClientRect();
        var step = second.left - first.left; // includes gap
        if (step <= 0) step = first.width + 16;
        grid.style.transform = 'translateX(' + (-idx * step) + 'px)';
      }
    }

    function maxIdx() {
      return mqMobile.matches
        ? carouselItems.length - 1
        : Math.max(carouselItems.length - VIEW, 0);
    }

    function tick() {
      idx = idx >= maxIdx() ? 0 : idx + 1;
      render();
    }

    function goPrev() {
      idx = idx <= 0 ? maxIdx() : idx - 1;
      render();
    }
    function goNext() {
      idx = idx >= maxIdx() ? 0 : idx + 1;
      render();
    }

    function start() {
      if (mqReduce.matches) return;
      stop();
      timer = window.setInterval(tick, INTERVAL);
    }
    function stop() {
      if (timer) {
        window.clearInterval(timer);
        timer = null;
      }
    }

    // Manual prev/next arrows — clicking restarts the timer so we don't
    // immediately auto-advance one step after the user's click.
    var prevBtn = document.getElementById('wr-gallery-prev');
    var nextBtn = document.getElementById('wr-gallery-next');
    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        goPrev();
        start();
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        goNext();
        start();
      });
    }

    // Pause on hover (desktop) and on focus (keyboard nav)
    section.addEventListener('mouseenter', stop);
    section.addEventListener('mouseleave', start);
    section.addEventListener('focusin', stop);
    section.addEventListener('focusout', start);

    // Pause while lightbox is open
    new MutationObserver(function () {
      if (lightbox.classList.contains('is-open')) stop();
      else start();
    }).observe(lightbox, { attributes: true, attributeFilter: ['class'] });

    // Pause when tab hidden (saves CPU / battery)
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stop();
      else start();
    });

    // Reset & re-render on resize / orientation change
    var resizeTimer;
    window.addEventListener('resize', function () {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(function () {
        idx = 0;
        render();
      }, 200);
    });

    render();
    start();
  })();
})();
