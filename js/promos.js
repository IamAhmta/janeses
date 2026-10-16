// =======================================================
// promos.js: renders the home-page promotions from js/promos-data.js
// (see that file for how to add / remove / schedule promos)
// =======================================================
(function () {
  'use strict';
  var host = document.querySelector('[data-promos]');
  var list = window.JANESES_PROMOS;
  if (!host || !list) return;
  var cfg = window.JANESES_PROMOS_CONFIG || {};
  var IMG = window.JANESES_IMAGES || {};

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]; }); }
  function today() { var d = new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function live(p) {
    if (p.active === false) return false;
    var t = today();
    if (p.start && t < p.start) return false;
    if (p.end && t > p.end) return false;
    return true;
  }
  function img(p, sizes) {
    var m = IMG[p.image];
    if (!m) { if (window.console) console.warn('[promos] image not found in manifest:', p.image); return ''; }
    var ws = m.widths, set = ws.map(function (w) { return 'images/' + p.image + '-' + w + '.webp ' + w + 'w'; }).join(', ');
    return '<img src="images/' + p.image + '-' + ws[ws.length - 1] + '.webp" srcset="' + set + '" sizes="' + sizes + '" width="' + m.w +
      '" height="' + m.h + '" alt="' + esc(p.alt || '') + '" loading="lazy" decoding="async">';
  }
  function buttons(p) {
    return (p.buttons || []).slice(0, 3).map(function (b) {
      var cls = 'btn-jan ' + (b.style === 'outline' ? 'btn-outline-light' : b.style === 'navy' ? 'btn-navy' : 'btn-gold');
      if (b.whatsapp) return '<a href="https://wa.me/' + esc(cfg.whatsapp) + '?text=' + encodeURIComponent(b.whatsapp) + '" class="' + cls + '" target="_blank" rel="noopener">' + esc(b.label) + '</a>';
      return '<a href="' + esc(b.href || '#') + '" class="' + cls + '">' + esc(b.label) + '</a>';
    }).join('');
  }
  function table(t) {
    if (!t) return '';
    var head = (t.head || []).map(function (h) { return '<th scope="col">' + esc(h) + '</th>'; }).join('');
    var rows = (t.rows || []).map(function (r) {
      return '<tr><th scope="row">' + esc(r[0]) + '</th>' + r.slice(1).map(function (c) { return '<td>' + esc(c) + '</td>'; }).join('') + '</tr>';
    }).join('');
    return '<div class="deal-table-wrap"><table class="deal-table"><caption class="visually-hidden">' + esc(t.caption || 'Prices') +
      '</caption><thead><tr>' + head + '</tr></thead><tbody>' + rows + '</tbody></table></div>';
  }
  function eyebrow(p) { return p.eyebrow ? '<div class="eyebrow">' + esc(p.eyebrow) + '</div>' : ''; }

  var layouts = {
    feature: function (p) {
      return '<section class="section-pad" data-promo="' + esc(p.id) + '"><div class="container-xl"><div class="promo reveal"><div class="row g-5 align-items-center">' +
        '<div class="col-lg-7 order-2 order-lg-1">' + eyebrow(p) + '<h2 class="section-title">' + esc(p.title) + '</h2>' +
        '<p class="section-lead mb-4">' + esc(p.text) + '</p><div class="d-flex flex-wrap gap-3">' + buttons(p) + '</div></div>' +
        '<div class="col-lg-5 order-1 order-lg-2"><div class="promo-img arch-frame">' + img(p, '(min-width:992px) 420px, 80vw') + '</div></div>' +
        '</div></div></div></section>';
    },
    menu: function (p) {
      return '<section class="section-pad deal-section" id="' + esc(p.id === 'special-combo-deal' ? 'deals' : p.id) + '" data-promo="' + esc(p.id) + '"><div class="container-xl"><div class="row g-5 align-items-center">' +
        '<div class="col-lg-6 reveal"><div class="deal-img">' + img(p, '(min-width:992px) 520px, 90vw') + '</div></div>' +
        '<div class="col-lg-6 reveal">' + eyebrow(p) + '<h2 class="section-title">' + esc(p.title) + '</h2>' +
        '<p class="section-lead mb-4">' + esc(p.text) + '</p>' + table(p.table) +
        '<div class="d-flex flex-wrap gap-3 mt-4 align-items-center">' + buttons(p) + (p.note ? '<span class="deal-note">' + esc(p.note) + '</span>' : '') + '</div>' +
        '</div></div></div></section>';
    },
    notice: function (p) {
      return '<section class="promo-notice-wrap" data-promo="' + esc(p.id) + '"><div class="container-xl"><div class="promo-notice reveal"><div>' +
        eyebrow(p) + '<h2>' + esc(p.title) + '</h2>' + (p.text ? '<p>' + esc(p.text) + '</p>' : '') + '</div>' +
        '<div class="d-flex flex-wrap gap-3">' + buttons(p) + '</div></div></div></section>';
    }
  };

  var html = list.filter(live).map(function (p) { return (layouts[p.layout] || layouts.feature)(p); }).join('');
  if (!html) { host.hidden = true; return; }
  host.innerHTML = html;

  // fade-in on scroll, same behaviour as the rest of the site
  var els = host.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: 0.12 });
    Array.prototype.forEach.call(els, function (el) { io.observe(el); });
  } else { Array.prototype.forEach.call(els, function (el) { el.classList.add('in'); }); }
})();
