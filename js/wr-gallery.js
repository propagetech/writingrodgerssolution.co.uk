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
})();
