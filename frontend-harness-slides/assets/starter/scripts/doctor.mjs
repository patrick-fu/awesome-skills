#!/usr/bin/env node
// Lightweight preflight for a copied frontend-harness-slides starter.
// Keep this script side-effect free: it diagnoses, it does not install or mutate.

import { spawn } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const errors = [];
const warnings = [];

function ok(message) {
  console.log(`OK    ${message}`);
}

function warn(message) {
  warnings.push(message);
  console.warn(`WARN  ${message}`);
}

function error(message) {
  errors.push(message);
  console.error(`ERROR ${message}`);
}

function run(command, args, options = {}) {
  return new Promise((resolve) => {
    const child = spawn(command, args, {
      cwd: root,
      shell: false,
      stdio: ['ignore', 'pipe', 'pipe'],
      ...options,
    });

    let stdout = '';
    let stderr = '';
    child.stdout?.on('data', (chunk) => { stdout += chunk.toString(); });
    child.stderr?.on('data', (chunk) => { stderr += chunk.toString(); });
    child.on('error', (err) => resolve({ code: -1, stdout, stderr: String(err), signal: null }));
    child.on('close', (code, signal) => resolve({ code, stdout, stderr, signal }));
  });
}

function satisfiesMinVersion(actual, range) {
  const match = String(range || '').match(/^>=\s*(\d+)\.(\d+)\.(\d+)$/);
  if (!match) return true;
  const required = match.slice(1).map(Number);
  const current = actual.split('.').map(Number);
  for (let i = 0; i < 3; i += 1) {
    if ((current[i] ?? 0) > required[i]) return true;
    if ((current[i] ?? 0) < required[i]) return false;
  }
  return true;
}

async function checkNodeAndPackage() {
  const packagePath = path.join(root, 'package.json');
  if (!fs.existsSync(packagePath)) {
    error('package.json is missing. Run doctor from the copied deck root.');
    return null;
  }

  const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  const required = pkg.engines?.node;
  if (required && !satisfiesMinVersion(process.versions.node, required)) {
    error(`Node ${process.versions.node} does not satisfy package.json engines.node (${required}).`);
  } else {
    ok(`Node ${process.versions.node}${required ? ` satisfies ${required}` : ''}`);
  }
  return pkg;
}

async function checkChromium() {
  try {
    const { chromium } = await import('@playwright/test');
    const executable = chromium.executablePath();
    if (fs.existsSync(executable)) {
      ok(`Playwright Chromium exists at ${executable}`);
    } else {
      error(`Playwright Chromium is not installed. Run: npx playwright install chromium`);
    }
  } catch (err) {
    error(`Could not load @playwright/test. Run npm install first. ${err?.message ?? err}`);
  }
}

function checkPort(port) {
  return new Promise((resolve) => {
    const server = net.createServer();
    server.once('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        error(`Preview port ${port} is already in use. Stop the process or run with PORT=<free-port>.`);
      } else {
        error(`Could not test preview port ${port}: ${err.message}`);
      }
      resolve();
    });
    server.once('listening', () => {
      server.close(() => {
        ok(`Preview port ${port} is available`);
        resolve();
      });
    });
    server.listen(port, '127.0.0.1');
  });
}

async function checkPlaywrightLoader() {
  const timeoutMs = Number(process.env.DOCTOR_LIST_TIMEOUT_MS || 20_000);
  const command = process.platform === 'win32' ? 'npx.cmd' : 'npx';

  await new Promise((resolve) => {
    const child = spawn(command, ['playwright', 'test', '--list'], {
      cwd: root,
      shell: false,
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env, CI: '1' },
    });

    let output = '';
    let settled = false;
    const finish = () => {
      if (settled) return false;
      settled = true;
      clearTimeout(timer);
      return true;
    };
    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      child.kill('SIGTERM');
      error(`Playwright test loader timed out after ${timeoutMs}ms while running: npx playwright test --list`);
      resolve();
    }, timeoutMs);

    child.stdout?.on('data', (chunk) => { output += chunk.toString(); });
    child.stderr?.on('data', (chunk) => { output += chunk.toString(); });
    child.on('error', (err) => {
      if (!finish()) return;
      error(`Could not run npx playwright test --list: ${err.message}`);
      resolve();
    });
    child.on('close', (code) => {
      if (!finish()) return;
      if (code === 0) {
        const firstLine = output.trim().split('\n').find(Boolean);
        ok(`Playwright test loader works${firstLine ? ` (${firstLine})` : ''}`);
      } else {
        error(`Playwright test loader failed with exit code ${code}.\n${output.trim().slice(0, 1200)}`);
      }
      resolve();
    });
  });
}

async function checkGitAndIgnore() {
  const gitRoot = await run('git', ['rev-parse', '--show-toplevel']);
  if (gitRoot.code !== 0) {
    warn('This deck is not inside a git repository. Visual baselines will be harder to review and reproduce.');
    return;
  }

  const topLevel = gitRoot.stdout.trim();
  if (path.resolve(topLevel) === root) {
    ok('Deck root is the git root');
  } else {
    warn(`Deck root is inside parent git repository ${topLevel}. Consider an independent git repo for this deck.`);
  }

  const pathsToCheck = [
    'package.json',
    'package-lock.json',
    'tests/snapshots/__doctor-placeholder__.png',
  ];
  const ignored = await run('git', ['check-ignore', '-v', '--no-index', ...pathsToCheck]);
  if (ignored.code === 0 && ignored.stdout.trim()) {
    warn(`Some important deck files appear ignored:\n${ignored.stdout.trim()}`);
  } else {
    ok('Key deck files are not ignored by git patterns');
  }
}

await checkNodeAndPackage();
await checkChromium();
await checkPort(Number(process.env.PORT) || 4173);
await checkPlaywrightLoader();
await checkGitAndIgnore();

console.log('');
if (warnings.length > 0) {
  console.log(`${warnings.length} warning(s). Review them before shipping.`);
}
if (errors.length > 0) {
  console.error(`${errors.length} error(s). Fix them before building the deck.`);
  process.exit(1);
}
console.log('Doctor passed.');
