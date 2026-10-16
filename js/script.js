// =======================================================
// JANESES INTEGRATED SERVICES LTD — Site Script
// =======================================================
(function () {
  'use strict';

  /* ---------------- CONFIG: edit these ---------------- */
  var CONFIG = {
    // Where lead-magnet emails are sent. Paste a form-service URL (Formspree, Getform, a Google
    // Apps Script web-app...). While empty, visitors still get the PDF but emails are NOT stored.
    leadEndpoint: '',
    // Same idea for the contact form. While empty, the form opens WhatsApp with the details filled in.
    inquiryEndpoint: '',
    whatsapp: '2348038893499',
    kitUrl: 'downloads/janeses-event-planning-kit.pdf',
    modalDelayMs: 40000          // timed pop-up for the free kit (once per visit)
  };

  /* ---------------- helpers ---------------- */
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function ssGet(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function ssSet(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]; }); }
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var page = (location.pathname.split('/').pop() || 'index.html');

  function postJSON(url, data) {
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    }).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r; });
  }

  /* ---------------- nav ---------------- */
  var nav = $('.jan-nav');
  function onScroll() { if (nav) nav.classList.toggle('scrolled', window.scrollY > 40); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  var toggle = $('.jan-toggle'), links = $('.jan-links');
  function setMenu(open) {
    if (!toggle || !links) return;
    links.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  if (toggle && links) {
    toggle.addEventListener('click', function () { setMenu(!links.classList.contains('open')); });
    $$('a', links).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }

  /* ---------------- scroll reveal ---------------- */
  var reveals = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add('in'); }); }

  /* ---------------- contact form ---------------- */
  var form = $('#janForm');
  if (form) {
    // pre-select event type from ?type=Wedding (used by the home-page occasion chips and service buttons)
    var typeParam = new URLSearchParams(location.search).get('type');
    var sel = $('#eventType');
    if (typeParam && sel) {
      $$('option', sel).forEach(function (o) { if (o.text.toLowerCase() === typeParam.toLowerCase()) sel.value = o.value || o.text; });
    }
    var dateInput = $('#eventDate');
    if (dateInput) dateInput.min = new Date().toISOString().split('T')[0];

    $$('[data-required]', form).forEach(function (f) {
      f.addEventListener('input', function () { var w = f.closest('.form-field'); if (w) w.classList.remove('field-invalid'); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstBad = null;
      $$('[data-required]', form).forEach(function (f) {
        var v = f.value.trim(), ok = !!v;
        if (ok && f.type === 'email') ok = EMAIL_RE.test(v);
        if (ok && f.type === 'tel') ok = /^[0-9+\-\s()]{7,}$/.test(v);
        var w = f.closest('.form-field');
        if (w) w.classList.toggle('field-invalid', !ok);
        if (!ok && !firstBad) firstBad = f;
      });
      if (firstBad) { firstBad.focus(); return; }

      var d = {}; $$('input,select,textarea', form).forEach(function (f) { if (f.name) d[f.name] = f.value.trim(); });
      var success = $('#formSuccess');
      function done(html) {
        form.reset();
        success.innerHTML = html; success.classList.add('show');
        success.scrollIntoView({ behavior: 'smooth', block: 'center' }); success.focus();
      }
      if (CONFIG.inquiryEndpoint) {
        postJSON(CONFIG.inquiryEndpoint, d).then(function () {
          done('<strong>Thank you, ' + esc(d.name.split(' ')[0]) + '!</strong> Your inquiry has been received. Our team will reach out within one working day.');
        }).catch(function () {
          done('Something went wrong sending your inquiry. Please message us on WhatsApp on +234 803 889 3499 and we will help right away.');
        });
      } else {
        var msg = 'Hello Janeses, I would like to book a consultation.\n\n' +
          'Name: ' + d.name + '\nPhone: ' + d.phone + '\nEmail: ' + d.email + '\nEvent: ' + d.eventType +
          '\nDate: ' + d.eventDate + (d.budget ? '\nBudget: ' + d.budget : '') + '\n\n' + d.message;
        var url = 'https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(msg);
        done('<strong>Almost done, ' + esc(d.name.split(' ')[0]) + '!</strong> We have opened WhatsApp with your details filled in. Just press send and our team will reply shortly. ' +
          '<a href="' + url + '" target="_blank" rel="noopener">Didn\'t open? Tap here.</a>');
        window.open(url, '_blank', 'noopener');
      }
    });
  }

  /* ---------------- lead magnet ---------------- */
  function successHTML(sent) {
    return '<div class="kit-success" role="status">' +
      '<div class="kit-check" aria-hidden="true">&#10003;</div>' +
      '<h3>Your kit is ready</h3>' +
      '<p>' + (sent ? 'We have noted your email. ' : '') + 'Download the 4-page PDF below. It works on your phone, or print it out for your planning folder.</p>' +
      '<a class="btn-jan btn-gold" href="' + CONFIG.kitUrl + '" download>Download the PDF</a>' +
      '<a class="alt" href="contact.html#form">Or book a free consultation &rarr;</a></div>';
  }

  function bindLeadForm(f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = $('[name=email]', f), err = $('.kit-error', f);
      var ok = EMAIL_RE.test(email.value.trim());
      err.hidden = ok;
      if (!ok) { email.focus(); return; }
      var wrap = f.closest('[data-lead-wrap]');
      var btn = $('button[type=submit]', f); btn.disabled = true; btn.textContent = 'Preparing your kit...';
      var data = {
        name: ($('[name=name]', f) || {}).value || '', email: email.value.trim(),
        eventType: ($('[name=type]', f) || {}).value || '', source: f.getAttribute('data-source') || page, page: page
      };
      function finish(sent) {
        lsSet('janeses_kit', 'done');
        // keep the section heading, replace the rest with the success state
        var heading = $('.eyebrow', wrap);
        wrap.innerHTML = (heading ? heading.outerHTML : '') + successHTML(sent);
        var dl = $('a[download]', wrap); if (dl) dl.focus();
      }
      if (CONFIG.leadEndpoint) {
        postJSON(CONFIG.leadEndpoint, data).then(function () { finish(true); })
          .catch(function () { finish(false); });   // never block the download if the service is down
      } else { finish(false); }
    });
  }
  $$('[data-lead-form]').forEach(bindLeadForm);

  /* modal (built here so every page shares one copy) */
  var modal, lastFocus;
  function buildModal() {
    if (modal) return;
    modal = document.createElement('div');
    modal.className = 'kit-modal'; modal.hidden = true;
    modal.setAttribute('role', 'dialog'); modal.setAttribute('aria-modal', 'true'); modal.setAttribute('aria-labelledby', 'kitModalTitle');
    modal.innerHTML =
      '<div class="kit-dialog">' +
        '<button type="button" class="kit-close" aria-label="Close">&times;</button>' +
        '<div class="kit-side" aria-hidden="true"><div class="kit-cover"><img src="images/logo-mark-375.webp" alt="" width="68" height="68"><em>A free guide from Janeses</em><strong>The Event Planning<br>Starter Kit</strong><span class="kit-rule"></span><small>Checklist &middot; Budget &middot; Timeline</small></div></div>' +
        '<div class="kit-main" data-lead-wrap>' +
          '<div class="eyebrow">Free download</div>' +
          '<h2 id="kitModalTitle">Planning an event? Start here.</h2>' +
          '<p>Get our free 4-page <strong>Event Planning Starter Kit</strong>: a 12-week checklist, budget planner and day-of timeline.</p>' +
          '<form class="kit-form" data-lead-form data-source="popup" novalidate>' +
            '<div class="mb-3"><label for="kmName">First name</label><input id="kmName" name="name" type="text" class="form-control" autocomplete="given-name" placeholder="Your first name"></div>' +
            '<div class="mb-1"><label for="kmEmail">Email address</label><input id="kmEmail" name="email" type="email" class="form-control" autocomplete="email" placeholder="you@example.com" required>' +
            '<div class="kit-error" role="alert" hidden>Please enter a valid email address.</div></div>' +
            '<button type="submit" class="btn-jan btn-gold mt-3 w-100">Send me the free kit</button>' +
            '<p class="kit-fine">Free PDF, instant download. We may email occasional planning tips; unsubscribe any time.</p>' +
          '</form>' +
        '</div>' +
      '</div>';
    document.body.appendChild(modal);
    bindLeadForm($('[data-lead-form]', modal));
    $('.kit-close', modal).addEventListener('click', closeModal);
    modal.addEventListener('mousedown', function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', function (e) {
      if (modal.hidden) return;
      if (e.key === 'Escape') closeModal();
      if (e.key === 'Tab') {   // keep focus inside the dialog
        var f = $$('button, a[href], input, select', modal).filter(function (n) { return !n.disabled && n.offsetParent !== null; });
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }
  function openModal() {
    buildModal();
    if (!modal.hidden) return;
    lastFocus = document.activeElement;
    modal.hidden = false; document.body.style.overflow = 'hidden';
    ssSet('janeses_kit_seen', '1');
    var i = $('input[name=name]', modal); if (i) i.focus();
  }
  function closeModal() {
    modal.hidden = true; document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  $$('[data-open-kit]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      // on the home page the section itself is the destination; elsewhere open the pop-up
      var inline = $('#kit');
      if (inline && a.getAttribute('href') && a.getAttribute('href').indexOf('#kit') !== -1) return;
      e.preventDefault(); openModal();
    });
  });

  // automatic pop-up: once per visit, never after download, never on the contact page or home page's kit section
  var autoOK = lsGet('janeses_kit') !== 'done' && !ssGet('janeses_kit_seen') && page !== 'contact.html';
  if (autoOK) {
    var armedAt = Date.now();
    setTimeout(function () { if (!ssGet('janeses_kit_seen') && !document.activeElement.matches('input,textarea,select')) openModal(); }, CONFIG.modalDelayMs);
    if (window.matchMedia('(hover:hover)').matches) {
      document.addEventListener('mouseout', function (e) {
        if (e.clientY <= 0 && !e.relatedTarget && Date.now() - armedAt > 15000 && !ssGet('janeses_kit_seen')) openModal();
      });
    }
  }

  /* ---------------- portfolio: filters + lightbox ---------------- */
  var chips = $$('.filter-btn');
  if (chips.length) {
    var tiles = $$('.pf-item, .pf-ph'), empty = $('.pf-empty');
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        var f = c.getAttribute('data-filter'), shown = 0;
        chips.forEach(function (x) { var on = x === c; x.classList.toggle('active', on); x.setAttribute('aria-pressed', on ? 'true' : 'false'); });
        tiles.forEach(function (t) {
          var match = f === 'all' || t.getAttribute('data-cat') === f;
          t.hidden = !match; if (match) shown++;
        });
        if (empty) empty.hidden = shown > 0;
      });
    });
  }

  var items = $$('.pf-item');
  if (items.length) {
    var lb, idx = 0, startX = 0;
    var visible = function () { return items.filter(function (i) { return !i.hidden; }); };
    var build = function () {
      lb = document.createElement('div'); lb.className = 'lb'; lb.hidden = true;
      lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Photo viewer');
      lb.innerHTML = '<button class="lb-btn lb-close" type="button" aria-label="Close">&times;</button>' +
        '<button class="lb-btn lb-prev" type="button" aria-label="Previous photo">&larr;</button>' +
        '<img alt=""><div class="lb-cap"></div>' +
        '<button class="lb-btn lb-next" type="button" aria-label="Next photo">&rarr;</button>';
      document.body.appendChild(lb);
      $('.lb-close', lb).addEventListener('click', close);
      $('.lb-prev', lb).addEventListener('click', function () { step(-1); });
      $('.lb-next', lb).addEventListener('click', function () { step(1); });
      lb.addEventListener('mousedown', function (e) { if (e.target === lb) close(); });
      lb.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
      lb.addEventListener('touchend', function (e) { var dx = e.changedTouches[0].clientX - startX; if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1); });
      document.addEventListener('keydown', function (e) {
        if (lb.hidden) return;
        if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') step(1); if (e.key === 'ArrowLeft') step(-1);
      });
    };
    var show = function () {
      var v = visible(), it = v[idx];
      var im = $('img', lb); im.src = it.getAttribute('data-full'); im.alt = it.querySelector('img').alt;
      $('.lb-cap', lb).innerHTML = '<small>' + it.getAttribute('data-type') + '</small><b>' + it.getAttribute('data-title') + '</b>' + it.getAttribute('data-desc');
      var multi = v.length > 1; $('.lb-prev', lb).hidden = !multi; $('.lb-next', lb).hidden = !multi;
    };
    var step = function (d) { var n = visible().length; idx = (idx + d + n) % n; show(); };
    var close = function () { lb.hidden = true; document.body.style.overflow = ''; if (items[0]) { var r = visible()[idx]; if (r) r.focus(); } };
    items.forEach(function (it) {
      it.addEventListener('click', function () {
        if (!lb) build();
        idx = visible().indexOf(it); show();
        lb.hidden = false; document.body.style.overflow = 'hidden'; $('.lb-close', lb).focus();
      });
    });
  }
})();
