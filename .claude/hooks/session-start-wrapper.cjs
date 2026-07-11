#!/usr/bin/env node
/**
 * Cross-platform wrapper for session-start hook
 * Detects OS and runs appropriate script (PowerShell on Windows, bash on Unix/Mac)
 * Fails gracefully if script execution fails
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const VAULT_ROOT = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const HOOKS_DIR = path.join(VAULT_ROOT, '.claude', 'hooks');

// Detect OS
const isWindows = process.platform === 'win32';

// Determine which script to run
let scriptPath;
let command;
let args;

if (isWindows) {
    // Windows: Use batch file wrapper (avoids PowerShell command parsing issues)
    scriptPath = path.resolve(path.join(HOOKS_DIR, 'session-start.bat'));
    command = 'cmd.exe';
    args = ['/c', scriptPath];
} else {
    // Unix/Mac: Use bash
    scriptPath = path.resolve(path.join(HOOKS_DIR, 'session-start.sh'));
    command = 'bash';
    args = [scriptPath];
}

// Verify script exists
if (!fs.existsSync(scriptPath)) {
    // Fail gracefully - output minimal context and exit
    console.log('=== Dex Session Context ===');
    console.log('');
    console.log('[!]  Session start hook script not found');
    console.log('');
    process.exit(0); // Exit successfully so session can continue
}

// Set environment variable
process.env.CLAUDE_PROJECT_DIR = VAULT_ROOT;

// Execute the command with timeout and error handling
// Use 'pipe' instead of 'inherit' to avoid blocking on stdout/stderr
const child = spawn(command, args, {
    stdio: ['ignore', 'pipe', 'pipe'],
    env: process.env,
    shell: false
});

// Collect output but don't block
let output = '';
let errorOutput = '';

child.stdout.on('data', (data) => {
    output += data.toString();
    // Write to stdout immediately so user sees progress
    process.stdout.write(data);
});

child.stderr.on('data', (data) => {
    errorOutput += data.toString();
    // Write to stderr immediately
    process.stderr.write(data);
});

// Set a shorter timeout to prevent hanging (5 seconds)
const timeout = setTimeout(() => {
    // Force kill on Windows, SIGTERM on Unix
    try {
        if (isWindows) {
            // On Windows, kill the process tree
            spawn('taskkill', ['/F', '/T', '/PID', child.pid.toString()], {
                stdio: 'ignore',
                shell: false
            });
        } else {
            child.kill('SIGTERM');
        }
    } catch (e) {
        // Ignore kill errors
    }
    console.log('\n[!]  Session hook timed out (continuing...)');
    process.exit(0); // Exit successfully so session can continue
}, 5000); // 5 second timeout

child.on('error', (error) => {
    clearTimeout(timeout);
    // Fail gracefully - don't crash the session
    console.log('=== Dex Session Context ===');
    console.log('');
    console.log('[!]  Session hook error (session will continue)');
    console.log('');
    process.exit(0); // Exit successfully so session can continue
});

child.on('exit', (code) => {
    clearTimeout(timeout);
    // Always exit successfully to allow session to continue
    // Even if the hook script failed, we don't want to block the session
    process.exit(0);
});
