// Read-only browser acceptance for one independent workspace; no image APIs or commits.
const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const { mkdirSync, mkdtempSync, writeFileSync } = require('node:fs');
const { join, resolve } = require('node:path');
const { setTimeout: delay } = require('node:timers/promises');
const PACKAGE = 'great_projects_editor_web';
const DOMAIN = 'editor.wonder';
const ABSENT = 'editor.victory_paths';
const TABS = ["cost-reward", "wonder-localization", "media-studio", "wonder-cropper", "generators", "localization"];
const PORT = 8768;
const DEBUG_PORT = 9338;

async function waitFor(check, label) {
  const end = Date.now() + 60000;
  while (Date.now() < end) { if (await check()) return; await delay(100); }
  throw new Error(`Timed out: ${label}`);
}

async function main() {
  const root = resolve(__dirname, '..');
  const scratch = join(root, 'tmp', 'browser-split');
  mkdirSync(scratch, { recursive: true });
  const origin = `http://127.0.0.1:${PORT}`;
  let launchError;
  const server = spawn(process.env.EU5_PYTHON || 'C:/Users/Hades/anaconda3/envs/eu5/python.exe',
    ['-m', 'uvicorn', `${PACKAGE}.server:create_app`, '--factory', '--host', '127.0.0.1', '--port', `${PORT}`],
    { cwd: root, windowsHide: true, stdio: 'ignore' });
  server.on('error', error => { launchError = error; });
  let chrome, ws;
  try {
    await waitFor(async () => {
      if (launchError) throw launchError;
      try { return (await fetch(origin)).ok; } catch { return false; }
    }, 'workspace server');
    chrome = spawn(process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
      ['--headless', '--no-sandbox', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
        `--remote-debugging-port=${DEBUG_PORT}`, `--user-data-dir=${mkdtempSync(join(scratch, 'profile-'))}`, 'about:blank'],
      { windowsHide: true, stdio: 'ignore' });
    chrome.on('error', error => { launchError = error; });
    let target;
    await waitFor(async () => {
      if (launchError) throw launchError;
      try { target = (await (await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/list`)).json()).find(row => row.type === 'page'); return !!target; }
      catch { return false; }
    }, 'headless Chrome');
    ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
    let id = 0;
    const pending = new Map(), errors = [];
    ws.onmessage = ({ data }) => {
      const result = JSON.parse(data);
      if (result.method === 'Runtime.exceptionThrown') errors.push(result.params.exceptionDetails);
      if (!result.id) return;
      const waiter = pending.get(result.id); pending.delete(result.id);
      result.error ? waiter.reject(new Error(JSON.stringify(result.error))) : waiter.resolve(result.result);
    };
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      pending.set(++id, { resolve, reject }); ws.send(JSON.stringify({ id, method, params }));
    });
    const evaluate = async expression => {
      const result = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
      if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
      return result.result.value;
    };
    await send('Runtime.enable'); await send('Page.enable');
    await send('Page.navigate', { url: origin });
    await waitFor(() => evaluate(`document.readyState === 'complete' && document.querySelectorAll('.tool-hub-tab-btn').length === ${TABS.length}`), 'tool shell');
    assert.deepEqual(await evaluate(`[...document.querySelectorAll('.tool-hub-tab-btn')].map(b => b.dataset.tool)`), TABS);
    assert.equal(await evaluate("document.querySelector('.rail-mark').textContent"), 'GP');
    for (const tab of TABS) {
      await evaluate(`document.querySelector('[data-tool="${tab}"].tool-hub-tab-btn').click()`);
      assert.equal(await evaluate('document.body.dataset.activeTool'), tab);
      assert.equal(await evaluate(`document.querySelectorAll('.tool-panel.active').length`), 1);
    }
    // Exercise the actual resource loader and read-only preview over HTTP.
    const cost = await (await fetch(`${origin}/api/resources/editor.cost_reward`)).json();
    const base = Object.fromEntries(cost.change_set.base.map(row => [row.path, row.sha256]));
    const preview = await fetch(`${origin}/api/resources/editor.cost_reward/preview`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ edits: {}, base }),
    });
    assert.equal(preview.status, 200, await preview.text());
    const after = await (await fetch(`${origin}/api/resources/editor.cost_reward`)).json();
    assert.deepEqual(after.change_set.base, cost.change_set.base);
    assert.equal((await fetch(`${origin}/api/resources/${DOMAIN}`)).status, 200);
    assert.equal((await fetch(`${origin}/api/resources/${ABSENT}`)).status, 404);
    const focus = TABS.includes('wonder-localization') ? 'wonder-localization' : 'victory-paths';
    await evaluate(`document.querySelector('[data-tool="${focus}"].tool-hub-tab-btn').click()`);
    await waitFor(() => evaluate(focus === 'wonder-localization'
      ? `document.querySelectorAll('#wonder-list button, #wonder-list .wonder-item').length > 0 && !document.querySelector('#save-button').disabled && document.querySelector('#retry-detail-button').hidden && !document.querySelector('#status-badge').textContent.includes('正在')`
      : `document.querySelector('#vp-status') && !document.querySelector('#vp-status').textContent.includes('加载中')`), 'domain panel');
    for (const width of [1440, 900]) {
      await send('Emulation.setDeviceMetricsOverride', { width, height: 960, deviceScaleFactor: 1, mobile: false });
      const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
      writeFileSync(join(scratch, `${width}.png`), Buffer.from(shot.data, 'base64'));
    }
    assert.deepEqual(errors, [], 'No JavaScript exceptions after independent shell initialization');
    console.log(`PASS ${PACKAGE}: ${TABS.length} tabs, owned resource, absent foreign route, read-only preview, two viewports, no JS exceptions.`);
    await send('Browser.close');
  } finally { if (ws) ws.close(); if (chrome) chrome.kill(); server.kill(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
