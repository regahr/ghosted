// Renders the three.js (game engine) images of panel.glb from ingame.html, and the landmarks in screen pixels.
// Run from this folder: node shoot.mjs [blockout]   (then python3 make_sheets.py [blockout]). Based on juno/v1/shoot_ingame.mjs.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const BLOCK = process.argv.includes('blockout');
const OD = (process.argv.find(a => a.startsWith('dir=')) || '').slice(4);
const outDir = OD ? path.join(here, OD) : BLOCK ? path.join(here, 'blockout') : here;
const glb = OD ? OD + '/panel_blockout.glb' : BLOCK ? 'blockout/panel_blockout.glb' : 'panel.glb';
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
await page.goto(`http://127.0.0.1:${srv.address().port}/design/assets/panel/v1/ingame.html?glb=${glb}`);
await page.waitForFunction(() => window.__ready, null, { timeout: 240000 });
const shot = async (name) => page.locator('#c').screenshot({ path: path.join(outDir, name + '.png') });
const report = {};
const card = async (name, cfg) => { report[name] = await page.evaluate(c => window.renderCard(c), cfg); await shot(name); };
const lineup = async (name, cfg) => { report[name] = await page.evaluate(c => window.renderLineup(c), cfg); await shot(name); };

const IDLE = { cfExpr: 'talk', wbExpr: 'talk' };       // chair call 3: the idle face in game is the TALK mouth
const SET = { target: [0, 0.72, -0.2], dist: 7.6, elev: 7 };
const CF = [-200 / 300, 1.0, -0.45], WB = [0, 1.0, -0.45], BOX = [200 / 300, 0.88, -0.25];
const HEADF = w => ({ target: [w[0], 1.1, -0.42], dist: 1.45, elev: 4, w: 900, h: 900 });
const PERS = w => ({ target: [w[0], 0.95, -0.35], dist: 2.9, elev: 6, w: 1000, h: 900 });

await card('turn-front', { ...SET, azim: 0 });
await card('turn-34', { ...SET, azim: 35 });
for (const g of ['grass', 'path']) {
  await lineup('lineup-' + g, { ground: g, panelState: IDLE });
  await lineup('_mask-' + g, { ground: g, only: 'panel', look: 'mask', panelState: IDLE });
  await lineup('_kit-' + g, { ground: g, only: 'kit' });
}
if (!BLOCK) {
  await card('turn-side', { ...SET, azim: 90 });
  await card('turn-back', { ...SET, azim: 180 });
  await card('grey-front', { ...SET, azim: 0, look: 'grey' });
  await card('grey-34', { ...SET, azim: 35, look: 'grey' });
  await card('sil-front', { ...SET, azim: 0, look: 'sil' });
  await card('sil-34', { ...SET, azim: 35, look: 'sil' });
  for (const [nm, w] of [['cf', CF], ['wb', WB]]) { await card(nm + '-front', { ...PERS(w), azim: 0 }); await card(nm + '-34', { ...PERS(w), azim: 35 }); }
  await card('box-front', { ...PERS(BOX), target: BOX, azim: 0 });
  // motion
  await card('m-cf-rest', { ...PERS(CF), state: {} });
  await card('m-cf-nod', { ...PERS(CF), state: { cf: 'cf_nod', cfExpr: 'grin' } });
  await card('m-cf-tilt', { ...PERS(CF), state: { cf: 'cf_tilt', cfExpr: 'tilt' } });
  await card('m-wb-up', { ...PERS(WB), state: { wb: 'wb_up' } });
  await card('m-wb-click', { ...PERS(WB), state: { wb: 'wb_click', wbExpr: 'talk' } });
  await card('m-wb-point', { ...PERS(WB), azim: 25, state: { wb: 'wb_point', wbExpr: 'talk' } });
  await card('m-box-camoff', { ...PERS(BOX), target: BOX, state: { icon: 'icon_camoff' } });
  await card('m-box-dark', { ...PERS(BOX), target: BOX, state: { icon: null } });
  await card('m-box-muted', { ...PERS(BOX), target: BOX, state: { icon: 'icon_muted' } });
  await card('m-lean-side', { ...SET, azim: 90, state: { lean: true, cfExpr: 'talk', wbExpr: 'talk' } });
  await card('m-rest-side', { ...SET, azim: 90, state: {} });
  await card('m-lean-34', { ...SET, azim: 35, state: { lean: true, cfExpr: 'talk', wbExpr: 'talk' } });
  // expressions (front, card rest lines)
  for (const [nm, st] of [['cf-rest', { cfExpr: 'rest' }], ['cf-talk', { cfExpr: 'talk' }], ['cf-grin', { cfExpr: 'grin' }], ['cf-tilt', { cfExpr: 'tilt', cf: 'cf_tilt' }]])
    await card('expr-' + nm, { ...HEADF(CF), state: st });
  for (const [nm, st] of [['wb-rest', { wbExpr: 'rest' }], ['wb-talk', { wbExpr: 'talk' }], ['wb-skeptic', { wbExpr: 'skeptic' }]])
    await card('expr-' + nm, { ...HEADF(WB), state: st });
  // game camera: motion beats with Kit in front (grass), faces for the 1x checks
  for (const [nm, st] of [['nod', { ...IDLE, cf: 'cf_nod', cfExpr: 'grin' }], ['point', { ...IDLE, wb: 'wb_point' }], ['click', { ...IDLE, wb: 'wb_click' }],
                          ['muted', { ...IDLE, icon: 'icon_muted' }], ['dark', { ...IDLE, icon: null }], ['lean', { ...IDLE, lean: true }], ['tilt', { ...IDLE, cf: 'cf_tilt', cfExpr: 'tilt' }],
                          ['rest-lines', { cfExpr: 'rest', wbExpr: 'rest' }]]) {
    await lineup('lineup-grass-' + nm, { ground: 'grass', panelState: st });
    await lineup('_mask-grass-' + nm, { ground: 'grass', only: 'panel', look: 'mask', panelState: st });
  }
  await lineup('_mask-path-nod', { ground: 'path', only: 'panel', look: 'mask', panelState: { ...IDLE, cf: 'cf_nod', cfExpr: 'grin' } });
  await lineup('_mask-path-grin', { ground: 'path', only: 'panel', look: 'mask', panelState: { ...IDLE, cfExpr: 'grin' } });
  await lineup('_mask-grass-grin', { ground: 'grass', only: 'panel', look: 'mask', panelState: { ...IDLE, cfExpr: 'grin' } });
  await lineup('_sil-grass', { ground: 'grass', only: 'panel', look: 'sil', panelState: IDLE });
}
fs.writeFileSync(path.join(outDir, 'ingame_report.json'), JSON.stringify(report, null, 1));
console.log('tris', JSON.stringify(report['lineup-grass'].panelTris), 'kit', JSON.stringify(report['_kit-grass'].kitTop), JSON.stringify(report['_kit-grass'].kitBot));
await browser.close(); srv.close();
