import { defineConfig } from '@playwright/test';
import 'dotenv/config';

export default defineConfig({
  // Run tests sequentially - we are automating real sessions
  workers: 1,

  use: {
    headless: process.env.PLAYWRIGHT_HEADLESS === 'true',
    slowMo: parseInt(process.env.PLAYWRIGHT_SLOWMO || '0'),

    // Human-paced timeouts
    actionTimeout: 15000,
    navigationTimeout: 30000,

    // Record traces on failure for debugging
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'off',
  },

  // Debug screenshots go here (gitignored)
  outputDir: 'screenshots/debug/',
});
