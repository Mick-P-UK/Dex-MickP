/**
 * delay-helper.js
 * Shared anti-bot delay utility for all ax-trees-automation scripts.
 *
 * Import in every script that interacts with a browser:
 *   import { randomDelay, pageLoadDelay } from '../skills/delay-helper.js';
 *
 * Rule: Never operate at machine speed. Always use human-paced delays.
 */

/**
 * Wait for a random duration between min and max milliseconds.
 * Use between individual browser actions (clicks, typing, navigation).
 *
 * @param {number} min - Minimum delay in ms (default 800)
 * @param {number} max - Maximum delay in ms (default 2500)
 */
export async function randomDelay(min = 800, max = 2500) {
  const delay = Math.floor(Math.random() * (max - min + 1)) + min;
  await new Promise(resolve => setTimeout(resolve, delay));
}

/**
 * Wait for a page load - longer delay for navigation events.
 * Use after page.goto() or any full-page navigation.
 *
 * @param {number} min - Minimum delay in ms (default 2000)
 * @param {number} max - Maximum delay in ms (default 5000)
 */
export async function pageLoadDelay(min = 2000, max = 5000) {
  await randomDelay(min, max);
}

/**
 * Simulate human typing speed - delay between keystrokes.
 * Use when filling forms character by character.
 *
 * @param {number} min - Minimum delay in ms (default 80)
 * @param {number} max - Maximum delay in ms (default 200)
 */
export async function typingDelay(min = 80, max = 200) {
  await randomDelay(min, max);
}
