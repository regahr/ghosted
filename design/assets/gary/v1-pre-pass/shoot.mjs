// Renders the three.js (game engine) images of gary.glb from ingame.html, and the landmarks in screen pixels.
// Run from this folder: node shoot.mjs [blockout]   (then python3 make_sheets.py [blockout]). Based on panel/v1/shoot.mjs.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const BLOCK = process.argv.includes('blockout');
const outDir = BLOCK ? path.join(here, 'blockout') : here;
const glb = BLOCK ? 'blockout/gary_blockout.glb' : 'gary.glb';
const root = path.resolve(here, '../../../..');                       // runs/jobless-roguelike
const { chromium } = await import(path.join(root, 'concept/node_modules/playwright/index.mjs'));
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.glb': 'model/gltf-binary', '.png': 'image/png' };
const srv = http.createServer((req, res) => { const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res); }).listen(0, '127.0.0.1');
await new Promise(r => srv.on('listening', r));
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 2100, height: 1300 } });
page.on('pageerror', e => console.log('pageerror:', e.message));
page.on('console', m => { if (!/GPU stall|WebGL/.test(m.text())) console.log('console:', m.text()); });
await page.goto(`http://127.0.0.1:${srv.address().port}/design/assets/gary/v1/ingame.html?glb=${glb}`);
await page.waitForFunction(() => window.__ready, null, { timeout: 240000 });
const shot = async (name) => page.locator('#c').screenshot({ path: path.join(outDir, name + '.png') });
const report = {};
const card = async (name, cfg) => { report[name] = await page.evaluate(c => window.renderCard(c), cfg); await shot(name); };
const lineup = async (name, cfg) => { report[name] = await page.evaluate(c => window.renderLineup(c), cfg); await shot(name); };
const C = { target: [0, 0.25, 0], dist: 2.6, elev: 6 };
const F = { target: [0, 0.30, 0], dist: 4.4, elev: 14 };                 // flight / beat cards (wings out)
const HEAD = { target: [0, 0.37, 0.03], dist: 1.15, elev: 4, w: 800, h: 800 };
const FLY = { beat: 'flap_level' };

for (const [n, a] of [['front', 0], ['34', 35], ['side', 90], ['back', 180]]) await card('turn-' + n, { ...C, azim: a });
if (process.argv.includes('quick')) { await browser.close(); srv.close(); process.exit(0); }
await card('hero', { ...C, azim: 28, elev: 14, w: 1200, h: 1200, dist: 2.3 });
for (const g of ['grass', 'path']) {
  await lineup('lineup-' + g, { ground: g, garyState: {}, flyState: FLY });
  await lineup('_mask-' + g, { ground: g, only: 'gary', look: 'mask', garyState: {} });
  await lineup('_kit-' + g, { ground: g, only: 'kit' });
}
if (!BLOCK) {
  for (const [n, a] of [['front', 0], ['34', 35], ['side', 90]]) {
    await card('grey-' + n, { ...C, azim: a, look: 'grey' }); await card('sil-' + n, { ...C, azim: a, look: 'sil' }); }
  await card('sil-fly', { ...F, azim: 0, look: 'sil', state: FLY });
  for (const k of ['flap_up', 'flap_level', 'flap_down']) { await card('fly-' + k, { ...F, azim: 20, elev: 25, state: { beat: k } }); await card('flyfront-' + k, { ...F, azim: 0, elev: 5, state: { beat: k } }); }
  for (const k of ['land_hop', 'hold', 'sorry', 'happy_hop', 'fly_off']) await card('beat-' + k, { ...F, dist: 3.4, azim: k === 'fly_off' ? 200 : 20, elev: 20, state: { beat: k } });
  await card('beat-hold-front', { ...C, azim: 0, state: { beat: 'hold' } });
  await card('beat-sorry-front', { ...C, azim: 0, state: { beat: 'sorry' } });
  for (const e of ['rest', 'happy', 'sorry', 'oops']) await card('expr-' + e, { ...HEAD, state: { expr: e, pose: e === 'sorry' ? 'sorry' : 'rest' } });
  for (const [nm, st] of [['hold', { beat: 'hold' }], ['sorry', { beat: 'sorry' }], ['happy', { beat: 'happy_hop' }], ['land', { beat: 'land_hop' }]]) {
    await lineup('lineup-grass-' + nm, { ground: 'grass', garyState: st });
    await lineup('lineup-path-' + nm, { ground: 'path', garyState: st });
    await lineup('_mask-grass-' + nm, { ground: 'grass', only: 'gary', look: 'mask', garyState: st });
  }
  await lineup('_mask-fly-grass', { ground: 'grass', only: 'fly', look: 'mask', garyState: {}, flyState: FLY });
  await lineup('_sil-grass', { ground: 'grass', only: 'gary', look: 'sil', garyState: {} });
}
fs.writeFileSync(path.join(outDir, 'ingame_report.json'), JSON.stringify(report, null, 1));
console.log('tris', JSON.stringify(report['lineup-grass'].garyTris), 'kit', JSON.stringify(report['_kit-grass'].kitTop), JSON.stringify(report['_kit-grass'].kitBot));
await browser.close(); srv.close();
