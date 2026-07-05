// denylist.js
// ax-mapper - safety denylist (generic).
//
// The mapper is a READ-ONLY cartographer. It must never navigate to, or click,
// any control that could change state, spend money, or end the session. This
// module holds a conservative default denylist and the matcher. Adapters may
// ADD app-specific tokens but should not remove these defaults.

'use strict';

// Matched case-insensitively as a SUBSTRING against BOTH a control's identifier
// and its label (so 'deal' catches 'dealings', 'pay' catches 'payment').
const CORE_DENYLIST = [
  'order', 'trade', 'buy', 'sell', 'deal',
  'alert', 'account', 'setting', 'save', 'delete', 'remove',
  'subscribe', 'payment', 'pay', 'checkout', 'purchase',
  'logout', 'log out', 'signout', 'sign out',
  'send', 'submit', 'publish', 'confirm',
];
// NOTE: bare 'post' is deliberately NOT a core token - it collides with harmless
// text like "post-login". An adapter mapping an app with a destructive "Post"
// button should add 'post' to its own denylist.

/**
 * Build a matcher over the core denylist plus any adapter additions.
 * @param {string[]} [extra]  Extra tokens contributed by an adapter.
 * @returns {(id?: string, label?: string) => boolean}
 */
function makeIsDenied(extra) {
  const tokens = CORE_DENYLIST.concat(Array.isArray(extra) ? extra : []);
  return function isDenied(id, label) {
    const hay = ((id || '') + ' ' + (label || '')).toLowerCase();
    return tokens.some(function (t) { return hay.indexOf(t) > -1; });
  };
}

// Default matcher (core list only), for callers that need no adapter extras.
const isDenied = makeIsDenied([]);

module.exports = { CORE_DENYLIST: CORE_DENYLIST, makeIsDenied: makeIsDenied, isDenied: isDenied };
