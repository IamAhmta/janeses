// =======================================================
// extras.js — ADD-ON behaviour (training chapter rail, jingle player).
// Loaded after script.js; it does not change any existing behaviour.
// =======================================================
(function () {
  'use strict';
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* ---- Training: highlight the chapter you're reading ---- */
  var links = $$('.chapter-rail a[data-ch]');
  if (links.length && 'IntersectionObserver' in window) {
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (l) { l.classList.remove('active'); l.removeAttribute('aria-current'); });
        var a = byId[e.target.id];
        if (a) { a.classList.add('active'); a.setAttribute('aria-current', 'true'); }
      });
    }, { rootMargin: '-35% 0px -55% 0px' });
    $$('.chapter').forEach(function (c) { io.observe(c); });
  }

  /* ---- Jingle player (never autoplays) ---- */
  function fmt(t) {
    if (!isFinite(t)) return '0:00';
    var m = Math.floor(t / 60), s = Math.floor(t % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  }
  $$('[data-jingle]').forEach(function (card) {
    var audio = $('audio', card), btn = $('.jingle-play', card),
        seek = $('.jingle-seek', card), time = $('.jingle-time', card);
    function dur() { return audio.duration && isFinite(audio.duration) ? audio.duration : 290; }
    function update() {
      seek.value = (audio.currentTime / dur()) * 100;
      time.textContent = fmt(audio.currentTime) + ' / ' + fmt(dur());
    }
    function state(on) {
      card.classList.toggle('playing', on);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.setAttribute('aria-label', on ? 'Pause the Janeses jingle' : 'Play the Janeses jingle');
    }
    btn.addEventListener('click', function () {
      if (audio.paused) { var p = audio.play(); if (p && p.catch) p.catch(function () { state(false); }); }
      else audio.pause();
    });
    audio.addEventListener('play', function () { state(true); });
    audio.addEventListener('pause', function () { state(false); });
    audio.addEventListener('ended', function () { state(false); audio.currentTime = 0; update(); });
    audio.addEventListener('timeupdate', update);
    audio.addEventListener('loadedmetadata', update);
    seek.addEventListener('pointerdown', function () { if (audio.preload === 'none') { audio.preload = 'metadata'; audio.load(); } });
    seek.addEventListener('input', function () { audio.currentTime = (seek.value / 100) * dur(); update(); });
  });
})();
