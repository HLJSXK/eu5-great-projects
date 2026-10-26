// The retired design browser is replaced by canonical ritual_text fields.
const assert = require('node:assert/strict');

module.exports = async function wonderRitualTextAcceptance({ evaluate, ready }) {
  const page = (fn, ...args) => evaluate('(' + fn.toString() + ')(...' + JSON.stringify(args) + ')');
  const idle = "document.querySelector('.tool-wonder-localization').dataset.busy === 'false'";
  await page(() => {
    document.querySelector('.tool-hub-tab-btn[data-tool="wonder-localization"]').click();
    document.querySelectorAll('#wonder-kind-tabs button')[1].click();
    document.querySelector('[data-wonder-key="unique_trinity_lavra"]').click();
  });
  await ready(idle);
  await page(() => [...document.querySelectorAll('#language-tabs button')].find(b => b.textContent.includes('机制')).click());
  const state = await page(async () => {
    const key = document.querySelector('#wonder-list .active').dataset.wonderKey;
    const resource = await (await fetch('/api/resources/editor.wonder')).json();
    const wonder = resource.draft.wonders.find(w => w.key === key);
    const detail = await (await fetch('/api/wonder-localization/wonders/' + wonder.id)).json();
    const fields = detail.mechanics.sections.flatMap(s => s.fields);
    return {
      texts: fields.filter(f => f.target_kind === 'unique_ritual_text').map(f => f.value),
      directions: fields.filter(f => f.target_kind === 'ritual_direction').map(f => f.editable),
      oldTabs: [...document.querySelectorAll('#language-tabs button')].filter(b => b.textContent.includes('仪式设计')).length,
      oldRequests: __probe.requests.filter(r => r.path.includes('/ritual-designs')).length,
    };
  });
  assert.equal(state.texts.length, 12);
  assert(state.texts.every(Boolean));
  assert.deepEqual(state.directions, [false, false, false]);
  assert.equal(state.oldTabs, 0);
  assert.equal(state.oldRequests, 0);
  await page(() => {
    const input = document.querySelector('[data-ritual-text-input]');
    input.value = 'Canonical ritual text browser check';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    document.querySelector('#save-button').click();
  });
  await ready("document.querySelector('#wonder-preview dialog').open");
  assert.match(await page(() => document.querySelector('#wonder-preview tbody').textContent), /ritual_text/);
  assert.match(await page(() => document.querySelector('#wonder-preview tbody').textContent), /Canonical ritual text browser check/);
  await page(() => document.querySelector('#wonder-preview [data-cancel]').click());
  await ready("!document.querySelector('#save-button').disabled");
  await page(() => document.querySelector('#reload-button').click());
  await ready(idle);
  assert(await page(() => document.querySelector('#dirty-badge').classList.contains('hidden')));
  console.log('Unified ritual text acceptance passed: bilingual fields, inherited directions, preview and reload.');
};
