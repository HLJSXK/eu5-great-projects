// Offline screenshots of real editor controls and atlas rendering. Never commits.
const assert = require('node:assert/strict');
const { spawn, spawnSync } = require('node:child_process');
const { mkdirSync, mkdtempSync, writeFileSync, readFileSync } = require('node:fs');
const { join, resolve } = require('node:path');
const { setTimeout: delay } = require('node:timers/promises');
const root = resolve(__dirname, '..');
const scratch = join(root, 'tmp', 'base-effects-preview');
mkdirSync(scratch, {recursive: true});
const python = process.env.EU5_PYTHON || 'C:/Users/Hades/anaconda3/envs/eu5/python.exe';
const origin = 'http://127.0.0.1:8779';
const children = [];
function launch(command, args) {
  const child = spawn(command, args, {cwd: root, windowsHide: true, stdio: 'ignore'});
  children.push(child);
  return child;
}
async function waitFor(check) {
  const end = Date.now() + 60000;
  while (Date.now() < end) { if (await check()) return; await delay(150); }
  throw new Error('Timed out waiting for offline UI');
}
let ws;
async function main() {
  const fixtureBuild=spawnSync(python,['-c',`
import json
from pathlib import Path
from scripts_engineering_department.wonder_mechanics import _core as core
from scripts_engineering_department.wonder_localization_lib import load_wonder_localization_data
from unique_wonders_site.scripts.build import build_wonders as atlas
wonders, mechanics = core.load_all_wonder_mechanics()
wonder = next(w for w in wonders if not w['is_unique'])
mechanics['base_instant_effects'] = {wonder['key']: [{'type':'gold','value':4}, {'type':'development','value':0.25}]}
record = atlas.build_record(wonder, base_wonders={wonder['key']:wonder}, mechanics=mechanics, loc_data=load_wonder_localization_data(), locations_index={}, reference_loc={}, modifier_index={}, trigger_index={})
Path('tmp/base-effects-preview/atlas-fixture.json').write_text(json.dumps(record,ensure_ascii=False),encoding='utf-8')
`],{cwd:root,windowsHide:true,encoding:'utf8'});
  assert.equal(fixtureBuild.status,0,fixtureBuild.stderr);
  const source = join(root, 'data/wonder_base_modifiers.yaml');
  const before = readFileSync(source);
  launch(python, ['-m','uvicorn','great_projects_editor_web.server:create_app','--factory','--host','127.0.0.1','--port','8779']);
  await waitFor(async () => { try { return (await fetch(origin)).ok; } catch { return false; } });
  launch('C:/Program Files/Google/Chrome/Application/chrome.exe', [
    '--headless','--no-sandbox','--disable-gpu','--no-first-run','--no-default-browser-check',
    '--remote-debugging-port=9349', `--user-data-dir=${mkdtempSync(join(scratch,'profile-'))}`, 'about:blank']);
  let target;
  await waitFor(async () => { try {
    target = (await (await fetch('http://127.0.0.1:9349/json/list')).json()).find(x => x.type === 'page');
    return !!target;
  } catch { return false; } });
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((resolve,reject) => { ws.onopen=resolve; ws.onerror=reject; });
  let id=0; const pending=new Map(), errors=[];
  ws.onmessage=({data}) => {
    const msg=JSON.parse(data);
    if(msg.method==='Runtime.exceptionThrown') errors.push(msg.params.exceptionDetails);
    if(!msg.id) return;
    const task=pending.get(msg.id); pending.delete(msg.id);
    msg.error ? task.reject(msg.error) : task.resolve(msg.result);
  };
  const send=(method,params={})=>new Promise((resolve,reject)=>{
    pending.set(++id,{resolve,reject}); ws.send(JSON.stringify({id,method,params}));
  });
  const evaluate=async expression=>{
    const result=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});
    if(result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
    return result.result.value;
  };
  const screenshot=async name=>{
    await delay(200);
    const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});
    writeFileSync(join(scratch,`${name}.png`),Buffer.from(shot.data,'base64'));
  };
  await send('Runtime.enable'); await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:origin});
  await waitFor(()=>evaluate(`document.readyState==='complete' && !!document.body.dataset.activeTool && !!document.querySelector('.tool-hub-tab-btn[data-tool="wonder-localization"]')`));
  await evaluate(`document.querySelector('.tool-hub-tab-btn[data-tool="wonder-localization"]').click()`);
  assert.equal(await evaluate(`document.body.dataset.activeTool`), 'wonder-localization');
  await waitFor(()=>evaluate(`document.querySelectorAll('#wonder-list .wonder-item').length>0 && !document.querySelector('#save-button').disabled`));
  await evaluate(`[...document.querySelectorAll('#language-tabs button')].find(b=>b.textContent.includes('机制')).click()`);
  await evaluate(`window.instantCard=()=>[...document.querySelectorAll('.language-panel:not(.hidden) .field-card')].find(x=>x.textContent.includes('mechanics.base_instant_effects.'))`);
  await waitFor(()=>evaluate(`!!instantCard()`));
  assert.equal(await evaluate(`instantCard().textContent.includes('No rows yet.')`),true);
  await evaluate(`instantCard().scrollIntoView({block:'center'})`);
  await screenshot('editor-empty-1440');
  await evaluate(`[...instantCard().querySelectorAll('button')].find(x=>x.textContent==='Add reward').click()`);
  await evaluate(`{const row=instantCard().querySelector('.structured-row'); row.children[0].value='gold'; row.children[0].dispatchEvent(new Event('change',{bubbles:true})); row.children[1].value='2.5'; row.children[1].dispatchEvent(new Event('input',{bubbles:true}));}`);
  assert.equal(await evaluate(`instantCard().textContent.includes('type: gold') && !instantCard().textContent.includes('one_shot:')`),true);
  await screenshot('editor-draft-row-1440');
  // Remove the uncommitted test reward before changing selection.
  await evaluate(`[...instantCard().querySelectorAll('button')].find(x=>x.textContent==='Remove').click()`);
  await evaluate(`[...document.querySelectorAll('.kind-switch-button')].find(x=>x.textContent.includes('独特')).click()`);
  await evaluate(`document.querySelector('#wonder-list .wonder-item').click()`);
  await waitFor(()=>evaluate(`!!instantCard() && instantCard().textContent.includes('Inherited from the prototype')`));
  assert.equal(await evaluate(`[...instantCard().querySelectorAll('.structured-editor input,.structured-editor button,.structured-editor select,.structured-editor textarea')].filter(x=>!x.disabled && !x.closest('.readonly-actions')).length`),0);
  await evaluate(`instantCard().scrollIntoView({block:'center'})`);
  await screenshot('editor-inherited-1440');
  await send('Emulation.setDeviceMetricsOverride',{width:900,height:1080,deviceScaleFactor:1,mobile:false});
  await evaluate(`instantCard().scrollIntoView({block:'center'})`);
  await screenshot('editor-inherited-900');
  assert.deepEqual(readFileSync(source),before);
  // Isolate the actual effect renderer and stylesheet from the atlas's CDN map.
  // The fixture is generated from current data; no map mock or authored screenshot.
  await send('Page.navigate',{url:'about:blank'});
  const fixture=JSON.parse(readFileSync(join(scratch,'atlas-fixture.json'),'utf8'));
  const sourceJS=readFileSync(join(root,'unique_wonders_site/dist/app.js'),'utf8');
  const functions=['t','localized','escapeHtml','formatValue','renderRowLabel','renderEffectSection'].map(name=>{
    const start=sourceJS.indexOf(`function ${name}(`);
    const end=sourceJS.indexOf('\nfunction ',start+1);
    return sourceJS.slice(start,end);
  }).join('\n');
  const declarations=sourceJS.slice(0,sourceJS.indexOf('const state ='));
  const stylesheet=readFileSync(join(root,'unique_wonders_site/dist/app.css'),'utf8');
  const html=`<!doctype html><html><head><style>${stylesheet}</style></head><body><section id="detail" style="display:block"><header><h2>Offline fixture / 离线测试样例</h2></header><div id="detail-body"></div></section></body></html>`;
  await evaluate(`document.open();document.write(${JSON.stringify(html)});document.close()`);
  await evaluate(`${declarations}\nwindow.state={lang:'zh'};\n${functions}\nwindow.fixtureWonder=${JSON.stringify(fixture)}`);
  await waitFor(()=>evaluate(`document.styleSheets.length>0`));
  for(const width of [1440,900]) {
    await send('Emulation.setDeviceMetricsOverride',{width,height:1080,deviceScaleFactor:1,mobile:false});
    for(const language of ['zh','en']) {
      await evaluate(`state.lang='${language}'; document.querySelector('#detail-body').innerHTML=fixtureWonder.effects.filter(x=>x.id==='base_instant_effects').map(renderEffectSection).join('')`);
      assert.equal(await evaluate(`getComputedStyle(document.querySelector('.effect-row')).display`),'grid');
      await screenshot(`atlas-fixture-${language}-${width}`);
    }
  }
  assert.deepEqual(errors,[]);
  console.log(`PASS: empty/edit/inherited editor states and bilingual atlas, 1440/900px; no JS errors or source writes. Screenshots: ${scratch}`);
  await send('Browser.close');
}
main().catch(error=>{console.error(error);process.exitCode=1;}).finally(()=>{if(ws)ws.close();for(const child of children)child.kill();});
