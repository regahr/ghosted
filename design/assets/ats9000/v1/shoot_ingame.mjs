// Renders the three.js (game engine) images of ats.glb from ingame.html, and measures it in screen pixels.
// Run from this folder: node shoot_ingame.mjs [test|blockout]   (then python3 make_sheets.py)
// Based on ricky/v1/shoot_ingame.mjs.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const MODE = process.argv.includes('test') ? 'test' : process.argv.includes('blockout') ? 'blockout' : 'final';
const outDir = MODE === 'test' ? path.join(here, 'tests') : MODE === 'blockout' ? path.join(here, 'blockout') : here;
const glb = { test: 'tests/ats_test.glb', blockout: 'blockout/ats_blockout.glb', final: 'ats.glb' }[MODE];
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
page.on('console', m => console.log('console:', m.text()));
await page.goto(`http://127.0.0.1:${srv.address().port}/design/assets/ats9000/v1/ingame.html?glb=${glb}`);
await page.waitForFunction(() => window.__ready, null, { timeout: 180000 });
const shot = async (name) => page.locator('#c').screenshot({ path: path.join(outDir, name + '.png') });
const bbox = () => page.evaluate(() => { const c = document.getElementById('c'), t = document.createElement('canvas'); t.width = c.width; t.height = c.height;
  const x = t.getContext('2d'); x.drawImage(c, 0, 0); const d = x.getImageData(0, 0, t.width, t.height).data; let y0 = 1e9, y1 = -1, x0 = 1e9, x1 = -1;
  for (let y = 0; y < t.height; y++) for (let i = 0; i < t.width; i++) { const k = (y * t.width + i) * 4; const mag = d[k] > 200 && d[k + 1] < 60 && d[k + 2] > 200;
    if (!mag) { y0 = Math.min(y0, y); y1 = Math.max(y1, y); x0 = Math.min(x0, i); x1 = Math.max(x1, i); } }
  return { x0, x1, y0, y1, heightPx: y1 - y0 + 1, widthPx: x1 - x0 + 1 }; });
// neck mask: per column near the centre, the rows that are red (rings) or green (core); the band = first..last neck row
const neckMask = (cx) => page.evaluate((cx) => { const c = document.getElementById('c'), t = document.createElement('canvas'); t.width = c.width; t.height = c.height;
  const x = t.getContext('2d'); x.drawImage(c, 0, 0); const d = x.getImageData(0, 0, t.width, t.height).data;
  const kind = (i, y) => { const k = (y * t.width + i) * 4, r = d[k], g = d[k + 1], b = d[k + 2];
    if (r > 150 && g < 100 && b < 100) return 'R'; if (g > 150 && r < 100 && b < 100) return 'G'; if (r < 60 && g < 60 && b < 60) return 'K';
    if (b > 150 && r < 100 && g < 100) return 'S'; if (r > 200 && g > 200 && b > 200) return 'W'; if (r > 200 && g > 200 && b < 100) return 'Y'; return '.'; };
  const cols = {}; let red = 0, green = 0, rx0 = 1e9, rx1 = -1, ry0 = 1e9, ry1 = -1;
  for (let y = 0; y < t.height; y++) for (let i = 0; i < t.width; i++) { const k = kind(i, y);
    if (k === 'R' || k === 'G') { if (k === 'R') red++; else green++; rx0 = Math.min(rx0, i); rx1 = Math.max(rx1, i); ry0 = Math.min(ry0, y); ry1 = Math.max(ry1, y); } }
  const mid = Math.round((rx0 + rx1) / 2);
  for (const dx of [-4, 0, 4]) { const i = mid + dx; let s = ''; for (let y = ry0 - 14; y <= ry1 + 14; y++) s += kind(i, y); cols[dx] = s; }
  return { neckPixels: { red, green }, neckBox: { x0: rx0, x1: rx1, y0: ry0, y1: ry1, widthPx: rx1 - rx0 + 1, heightPx: ry1 - ry0 + 1 }, centreColumnFromY: ry0 - 14, columns: cols }; }, cx);
const report = {};
if (MODE === 'test') {
  const states = ['idle', 'reading', 'found', 'notfit', 'loading'];
  for (const s of states) { await page.evaluate(s => window.renderChar({ angle: 0, w: 600, h: 400, cam: [0, 1.05, 1.6], target: [0, 1.0, 0], state: { screen: s } }), s); await shot('three-' + s); }
  await page.evaluate(() => window.renderChar({ angle: -60, w: 600, h: 400, cam: [0, 0.6, 1.6], target: [0, 0.3, 0], fov: 26, state: { hub: 0.8, belt: 0.3 } })); await shot('three-34-hub');
} else {
  if (MODE === 'final') {
    for (const [name, cfg] of [['ingame', { angle: -35 }], ['ingame-front', { angle: 0 }], ['ingame-stamp-windup', { angle: -90, state: { theta: 140 } }],
                               ['ingame-slot', { angle: -25, cam: [0, 1.55, 3.2], target: [0, 0.42, 0], h: 1000, state: { cv: 0.5, screen: 'reading', scan: 'sweep_top' } }]]) {
      report[name] = await page.evaluate(c => window.renderChar(c), cfg); await shot(name); }
  }
  for (const [name, cfg] of [['lineup-grass', { ground: 'grass' }], ['lineup-path', { ground: 'path' }]]) {
    report[name] = await page.evaluate(c => window.renderLineup(c), cfg); await shot(name);
    for (const who of ['kit', 'ats']) { await page.evaluate(c => window.renderLineup(c), { ...cfg, only: who }); report[name]['px_' + who] = await bbox(); }
    await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'ats', mask: 'neck' }); await shot('_' + name + '-neckmask');
    report[name].neck = await neckMask();
    await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'ats', atsAtKit: true }); report[name].px_ats_at_kit_spot = await bbox();
    report[name].ratio_ats_to_kit = Math.round(report[name].px_ats.heightPx / report[name].px_kit.heightPx * 1000) / 1000;
    console.log(name, JSON.stringify({ kit: report[name].px_kit.heightPx, ats: report[name].px_ats, ratio: report[name].ratio_ats_to_kit, neck: report[name].neck.neckBox }));
  }
  if (MODE === 'final') {
    report['lineup-grass-turned'] = await page.evaluate(c => window.renderLineup(c), { ground: 'grass', atsYaw: 0 });
    await page.evaluate(c => window.renderLineup(c), { ground: 'grass', atsYaw: 0, only: 'ats' }); report['lineup-grass-turned'].px_ats = await bbox();
    report.visibleTris = {};
    for (const [k, st] of [['rest', {}], ['windup', { theta: 140 }], ['notfit', { screen: 'notfit' }], ['cv_in_slot', { cv: 0.5 }]])
      report.visibleTris[k] = (await page.evaluate(c => window.renderChar(c), { angle: -35, state: st })).visibleTris;
    console.log('visibleTris', JSON.stringify(report.visibleTris));
  }
}
fs.writeFileSync(path.join(outDir, MODE === 'test' ? 'three_test_report.json' : 'ingame_report.json'), JSON.stringify(report, null, 1));
await browser.close(); srv.close();
