/**
 * Cookie consent for coldcallx.app — Google Consent Mode v2.
 *
 * WHY: GA4 (G-0CKNY5PSV1) stores an identifier on the visitor's device. Under
 * UK PECR reg. 6 and the EU ePrivacy Directive that needs prior opt-in consent
 * — analytics is not "strictly necessary". This site ran GA4 on 21 pages with
 * no banner and no consent signal at all, which set those identifiers before
 * anyone had agreed to anything.
 *
 * TWO INDEPENDENT LAYERS, deliberately:
 *
 *   1. The Consent Mode defaults below, scoped by `region`. Google evaluates
 *      these server-side against the visitor's IP, so storage is denied for
 *      UK/EEA visitors whether or not the banner ever renders. This is the
 *      layer that has to be right, and it does not depend on any guess made
 *      in this file.
 *
 *   2. The banner, shown when we believe the visitor is covered. Its job is to
 *      offer the CHOICE to opt in. If the guess below is wrong in the cautious
 *      direction, a visitor sees a banner they did not strictly need; wrong in
 *      the other direction, they see none and analytics simply stays denied by
 *      layer 1. Both failures are safe. That asymmetry is the whole design.
 *
 * THIS FILE MUST LOAD SYNCHRONOUSLY AND BEFORE gtag.js. Consent defaults have
 * to be in the dataLayer before the tag reads them; `defer` or `async` here
 * would let the tag boot with no signal and set cookies regardless.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'ccx-cookie-consent';

  // Analytics only. The advertising categories stay denied for everyone,
  // everywhere, because this site carries no advertising or remarketing tags —
  // and the banner tells people so. If an ad tag is ever added, that promise
  // has to be revisited here AND in the copy on /cookies before it ships.
  var GRANTABLE = ['analytics_storage'];

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  /* ---------------------------------------------------------------- signal */

  // The UK plus the EEA, and Switzerland. Consent Mode matches these against
  // the visitor's IP on Google's side.
  var CONSENT_REGIONS = [
    'GB', 'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE',
    'GR', 'HU', 'IS', 'IE', 'IT', 'LV', 'LI', 'LT', 'LU', 'MT', 'NL', 'NO',
    'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'CH'
  ];

  // Declared first so it wins for those regions; the unscoped default below
  // covers everywhere else.
  gtag('consent', 'default', {
    region: CONSENT_REGIONS,
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });

  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'granted',
    functionality_storage: 'granted',
    security_storage: 'granted'
  });

  function apply(state) {
    var update = {};
    for (var i = 0; i < GRANTABLE.length; i++) update[GRANTABLE[i]] = state;
    gtag('consent', 'update', update);
  }

  /* --------------------------------------------------------------- storage */

  function read() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (!parsed || parsed.v !== 1) return null;
      return parsed.state === 'granted' || parsed.state === 'denied' ? parsed : null;
    } catch (e) {
      // Private browsing, or storage disabled. Treat it as no decision on
      // record: the banner reappears, which is the honest outcome when we
      // cannot remember what someone told us.
      return null;
    }
  }

  function write(state) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify({
        state: state,
        at: new Date().toISOString(),
        // Bump when the categories, or what they cover, change. A new value
        // makes every stored decision stale and re-asks — which is what a
        // material change to what is being consented to requires.
        v: 1
      }));
    } catch (e) { /* nothing to do; the choice still applies to this page view */ }
  }

  /**
   * Best-effort, network-free guess at whether this visitor is covered.
   * Timezone rather than an IP lookup on purpose: querying a geolocation
   * service about someone in order to decide whether to ask their permission
   * to track them would rather defeat the point.
   */
  function probablyCovered() {
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
      return /^(Europe\/|Atlantic\/(Canary|Faroe|Madeira|Azores|Reykjavik))/.test(tz);
    } catch (e) {
      return true; // Cannot tell — so ask. The cautious direction.
    }
  }

  /* ---------------------------------------------------------------- banner */

  var STYLE = [
    '.ccx-consent{position:fixed;left:0;right:0;bottom:0;z-index:2147483000;',
      'display:flex;justify-content:center;padding:0 1rem 1rem;pointer-events:none;',
      'font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}',
    '.ccx-consent__card{pointer-events:auto;width:100%;max-width:44rem;',
      'display:flex;flex-wrap:wrap;align-items:center;gap:1rem 1.5rem;',
      'padding:1.125rem 1.375rem;border-radius:1.25rem;',
      'background:linear-gradient(135deg,rgba(255,255,255,.94) 0%,rgba(255,255,255,.82) 100%);',
      'backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);',
      'border:1px solid rgba(255,255,255,.85);',
      'box-shadow:0 24px 48px -12px rgba(15,23,42,.22),0 0 0 1px rgba(255,255,255,.6) inset;',
      'animation:ccx-consent-in .32s cubic-bezier(.22,1,.36,1) both;}',
    '@keyframes ccx-consent-in{from{opacity:0;transform:translateY(1.25rem);}to{opacity:1;transform:none;}}',
    '@media (prefers-reduced-motion:reduce){.ccx-consent__card{animation:none;}}',
    '.ccx-consent__copy{flex:1 1 20rem;min-width:0;}',
    '.ccx-consent__title{margin:0 0 .25rem;font-size:.9375rem;font-weight:600;color:#0F172A;}',
    '.ccx-consent__text{margin:0;font-size:.8125rem;line-height:1.55;color:#64748B;font-weight:400;}',
    '.ccx-consent__link{color:#0284c7;text-decoration:underline;text-underline-offset:2px;}',
    '.ccx-consent__link:hover{color:#0369a1;}',
    '.ccx-consent__actions{display:flex;gap:.625rem;flex:0 0 auto;}',
    // Both buttons are the same size and weight on purpose. A banner where
    // "Accept" is a button and "Reject" is a faint link is the dark pattern
    // the ICO and the EDPB actually enforce against.
    '.ccx-consent__btn{flex:1 1 auto;min-width:7rem;padding:.625rem 1.125rem;border-radius:.75rem;',
      'font-family:inherit;font-size:.8125rem;font-weight:600;line-height:1.2;cursor:pointer;',
      'transition:transform .15s ease,box-shadow .15s ease,background-color .15s ease;}',
    '.ccx-consent__btn:hover{transform:translateY(-1px);}',
    '.ccx-consent__btn:focus-visible{outline:2px solid #00AEEF;outline-offset:2px;}',
    '.ccx-consent__btn--ghost{background:rgba(255,255,255,.7);color:#0F172A;',
      'border:1px solid rgba(100,116,139,.35);}',
    '.ccx-consent__btn--ghost:hover{background:#fff;}',
    '.ccx-consent__btn--solid{background:#00AEEF;color:#fff;border:1px solid #00AEEF;',
      'box-shadow:0 8px 18px -6px rgba(0,174,239,.6);}',
    '.ccx-consent__btn--solid:hover{background:#009fdb;}',
    '@media (max-width:30rem){.ccx-consent__actions{width:100%;}}'
  ].join('');

  var banner = null;
  var styled = false;

  function injectStyle() {
    if (styled) return;
    styled = true;
    var tag = document.createElement('style');
    tag.appendChild(document.createTextNode(STYLE));
    document.head.appendChild(tag);
  }

  function build(focusFirst) {
    if (banner) return;
    injectStyle();

    var el = document.createElement('div');
    el.className = 'ccx-consent';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-label', 'Cookie choices');
    el.innerHTML =
      '<div class="ccx-consent__card">' +
        '<div class="ccx-consent__copy">' +
          '<p class="ccx-consent__title">Analytics cookies</p>' +
          '<p class="ccx-consent__text">We’d like to use Google Analytics to see which pages people find useful. ' +
          'It stores an identifier on your device, so we only do it if you say yes — and the site works exactly the same if you say no. ' +
          '<a class="ccx-consent__link" href="/cookies">What we store</a></p>' +
        '</div>' +
        '<div class="ccx-consent__actions">' +
          '<button type="button" class="ccx-consent__btn ccx-consent__btn--ghost" data-ccx-consent="denied">Reject</button>' +
          '<button type="button" class="ccx-consent__btn ccx-consent__btn--solid" data-ccx-consent="granted">Accept</button>' +
        '</div>' +
      '</div>';

    el.addEventListener('click', function (event) {
      var node = event.target;
      var choice = node && node.getAttribute && node.getAttribute('data-ccx-consent');
      if (choice) decide(choice);
    });

    document.body.appendChild(el);
    banner = el;

    // Only pull focus when the visitor asked for the banner. Stealing it on
    // page load would yank people out of the page they came to read.
    if (focusFirst) {
      var first = el.querySelector('.ccx-consent__btn');
      if (first) first.focus();
    }
  }

  function show(focusFirst) {
    if (document.body) build(focusFirst);
    else document.addEventListener('DOMContentLoaded', function () { build(focusFirst); });
  }

  function decide(state) {
    write(state);
    apply(state);
    if (banner && banner.parentNode) banner.parentNode.removeChild(banner);
    banner = null;
  }

  /* ----------------------------------------------------------------- start */

  var stored = read();
  if (stored) apply(stored.state);
  else if (probablyCovered()) show(false);

  /**
   * Withdrawing consent has to be as easy as giving it, so every page footer
   * carries a "Cookies" link pointing at /cookies, and that page reopens this.
   * Reopening clears the stored decision and drops to denied first — otherwise
   * someone who accepted, then came back to reconsider, would stay tracked
   * while they were in the middle of reconsidering.
   */
  window.ccxConsent = {
    open: function () {
      try { window.localStorage.removeItem(STORAGE_KEY); } catch (e) {}
      apply('denied');
      show(true);
    },
    state: function () {
      var s = read();
      return s ? s.state : 'unset';
    }
  };
})();
