// Renders the three.js (game engine) images of ricky.glb from ingame.html, and measures it in screen pixels.
// Run from this folder: node shoot_ingame.mjs [blockout]   (then python3 make_sheets.py)
// Based on ghostie/v7/shoot_ingame.mjs.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const BLOCK = process.argv.includes('blockout');
const outDir = BLOCK ? path.join(here, 'blockout') : here;
const glb = BLOCK ? 'blockout/ricky_blockout.glb' : 'ricky.glb';
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
await page.goto(`http://127.0.0.1:${srv.address().port}/design/assets/ricky/v1/ingame.html?glb=${glb}`);
await page.waitForFunction(() => window.__ready, null, { timeout: 120000 });
// pixel boxes of a flat-background render (magenta = empty), and the hair-vs-eye mask numbers
const bbox = () => page.evaluate(() => { const c = document.getElementById('c'), t = document.createElement('canvas'); t.width = c.width; t.height = c.height;
  const x = t.getContext('2d'); x.drawImage(c, 0, 0); const d = x.getImageData(0, 0, t.width, t.height).data; let y0 = 1e9, y1 = -1, x0 = 1e9, x1 = -1;
  for (let y = 0; y < t.height; y++) for (let i = 0; i < t.width; i++) { const k = (y * t.width + i) * 4; const mag = d[k] > 200 && d[k + 1] < 60 && d[k + 2] > 200;
    if (!mag) { y0 = Math.min(y0, y); y1 = Math.max(y1, y); x0 = Math.min(x0, i); x1 = Math.max(x1, i); } }
  return { x0, x1, y0, y1, heightPx: y1 - y0 + 1, widthPx: x1 - x0 + 1 }; });
const hairMask = (eyeTop, collarY) => page.evaluate(([eyeTop, collarY]) => { const c = document.getElementById('c'), t = document.createElement('canvas'); t.width = c.width; t.height = c.height;
  const x = t.getContext('2d'); x.drawImage(c, 0, 0); const d = x.getImageData(0, 0, t.width, t.height).data;
  let blue = { x0: 1e9, x1: -1, y0: 1e9, y1: -1 }; const red = [];
  for (let y = 0; y < t.height; y++) for (let i = 0; i < t.width; i++) { const k = (y * t.width + i) * 4, r = d[k], g = d[k + 1], b = d[k + 2];
    if (b > 150 && r < 90 && g < 90 && y < collarY) { blue.x0 = Math.min(blue.x0, i); blue.x1 = Math.max(blue.x1, i); blue.y0 = Math.min(blue.y0, y); blue.y1 = Math.max(blue.y1, y); }
    if (r > 150 && g < 90 && b < 90) red.push([i, y]); }
  // the hair's lowest visible pixel in the eye columns (+-3 px), and anywhere in front of the face columns
  let lowEye = -1, lowAll = -1; for (const [i, y] of red) { if (i >= blue.x0 - 3 && i <= blue.x1 + 3) lowEye = Math.max(lowEye, y); lowAll = Math.max(lowAll, y); }
  return { eyePixels: blue, eyeTopPx: blue.y0, hairLowestInEyeColumnsPx: lowEye, hairLowestAnywherePx: lowAll, gapPx: blue.y0 - lowEye }; }, [eyeTop, collarY]);
const report = {};
const jobs = BLOCK ? [] : [
  ['ingame', 'renderChar', { angle: -35 }],
  ['ingame-front', 'renderChar', { angle: 0 }],
  ['ingame-phone', 'renderChar', { angle: 0, pose: 'phone' }],
];
const lineups = [['lineup-grass', { ground: 'grass' }], ['lineup-path', { ground: 'path' }]];
for (const [name, fn, cfg] of jobs) {
  const info = await page.evaluate(([f, c]) => window[f](c), [fn, cfg]);
  await page.locator('#c').screenshot({ path: path.join(outDir, name + '.png') }); console.log(name, JSON.stringify(info)); report[name] = info;
}
for (const [name, cfg] of lineups) {
  report[name] = await page.evaluate(c => window.renderLineup(c), cfg);
  await page.locator('#c').screenshot({ path: path.join(outDir, name + '.png') });
  for (const who of ['kit', 'ricky']) { await page.evaluate(c => window.renderLineup(c), { ...cfg, only: who }); report[name]['px_' + who] = await bbox(); }
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'ricky', mask: 'hair' });
  await page.locator('#c').screenshot({ path: path.join(outDir, '_' + name + '-hairmask.png') });
  report[name].hair = await hairMask(report[name].rickyEyeTopY, report[name].ricky_collar_top[1]);
  report[name].ratio_ricky_to_kit = Math.round(report[name].px_ricky.heightPx / report[name].px_kit.heightPx * 1000) / 1000;
  console.log(name, JSON.stringify({ kit: report[name].px_kit, ricky: report[name].px_ricky, ratio: report[name].ratio_ricky_to_kit, hair: report[name].hair, eyeTop: report[name].rickyEyeTopY }));
}
if (!BLOCK) {
  report['lineup-grass-phone'] = await page.evaluate(c => window.renderLineup(c), { ground: 'grass', rickyPose: 'phone' });
  await page.locator('#c').screenshot({ path: path.join(outDir, 'lineup-grass-phone.png') });
  report.drain = await page.evaluate(c => window.renderDrain(c), {});
  await page.locator('#c').screenshot({ path: path.join(outDir, '_drain-raw.png') });
  report.visibleTris = {};
  for (const [k, cfg] of [['rest', {}], ['phone', { pose: 'phone' }], ['drain_step1', { drain: 1 / 3 }]]) report.visibleTris[k] = (await page.evaluate(c => window.renderChar(c), { angle: -35, ...cfg })).visibleTris;
  console.log('visibleTris', JSON.stringify(report.visibleTris));
}
fs.writeFileSync(path.join(outDir, 'ingame_report.json'), JSON.stringify(report, null, 1));
await browser.close(); srv.close();
