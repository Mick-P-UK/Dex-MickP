// delay.js
// ax-mapper - human-paced random delay helper (generic, no dependencies).
//
// Anti-bot rule (inherited from ax-trees-automation): never actuate a UI at
// machine speed. Every navigation/capture step waits a randomised, human-like
// pause. Ranges match the parent project's delay-helper conventions.

'use strict';

const RANGES = {
  short: [500, 1500],
  medium: [1500, 3000],
  long: [3000, 6000],
};

/**
 * Resolve after a random pause in the named band.
 * @param {'short'|'medium'|'long'} [band='medium']
 * @returns {Promise<void>}
 */
function delay(band) {
  const range = RANGES[band] || RANGES.medium;
  const ms = range[0] + Math.floor(Math.random() * (range[1] - range[0] + 1));
  return new Promise(function (resolve) { setTimeout(resolve, ms); });
}

module.exports = { delay: delay, RANGES: RANGES };
