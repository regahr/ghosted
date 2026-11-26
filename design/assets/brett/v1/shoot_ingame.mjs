// Renders the three.js (game engine) images of brett.glb from ingame.html, and measures it in screen pixels.
// Run from this folder: node shoot_ingame.mjs [blockout] [bxg=.. bzg=.. bxp=.. bzp=..]   (then python3 make_sheets.py)
// Based on auntie-dot/v1/shoot_ingame.mjs.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const BLOCK = process.argv.includes('blockout');
const extra = process.argv.filter(a => /^b[xz][gp]=/.test(a)).map(a => '&' + a).join('');
const outDir = BLOCK ? path.join(here, 'blockout') : here;
const glb = BLOCK ? 'blockout/brett_blockout.glb' : 'brett.glb';
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
await page.goto(`http://127.0.0.1:${srv.address().port}/design/assets/brett/v1/ingame.html?glb=${glb}${extra}`);
await page.waitForFunction(() => window.__ready, null, { timeout: 180000 });
const shot = async (name) => page.locator('#c').screenshot({ path: path.join(outDir, name + '.png') });
const bbox = () => page.evaluate(() => { const c = document.getElementById('c'), t = document.createElement('canvas'); t.width = c.width; t.height = c.height;
  const x = t.getContext('2d'); x.drawImage(c, 0, 0); const d = x.getImageData(0, 0, t.width, t.height).data; let y0 = 1e9, y1 = -1, x0 = 1e9, x1 = -1;
  for (let y = 0; y < t.height; y++) for (let i = 0; i < t.width; i++) { const k = (y * t.width + i) * 4; const mag = d[k] > 200 && d[k + 1] < 60 && d[k + 2] > 200;
    if (!mag) { y0 = Math.min(y0, y); y1 = Math.max(y1, y); x0 = Math.min(x0, i); x1 = Math.max(x1, i); } }
  return { x0, x1, y0, y1, heightPx: y1 - y0 + 1, widthPx: x1 - x0 + 1 }; });
// hair vs eyes, the grin and the halo from the mask render (hair red, eye ink blue, grin line green, teeth cyan, halo yellow)
const hairMask = () => page.evaluate(() => { const c = document.getElementById('c'), t = document.createElement('canvas'); t.width = c.width; t.height = c.height;
  const x = t.getContext('2d'); x.drawImage(c, 0, 0); const d = x.getImageData(0, 0, t.width, t.height).data;
  const box = () => ({ x0: 1e9, x1: -1, y0: 1e9, y1: -1, n: 0 }); const blue = box(), green = box(), cyan = box(), yel = box(), brow = box(); const red = [], browPts = [];
  const add = (b, i, y) => { b.x0 = Math.min(b.x0, i); b.x1 = Math.max(b.x1, i); b.y0 = Math.min(b.y0, y); b.y1 = Math.max(b.y1, y); b.n++; };
  for (let y = 0; y < t.height; y++) for (let i = 0; i < t.width; i++) { const k = (y * t.width + i) * 4, r = d[k], g = d[k + 1], b = d[k + 2];
    if (r > 200 && g > 90 && g < 170 && b < 70) { add(brow, i, y); browPts.push([i, y]); }
    else if (b > 150 && r < 90 && g < 90) add(blue, i, y);
    else if (g > 150 && b > 150 && r < 90) add(cyan, i, y);
    else if (g > 150 && r < 90 && b < 90) add(green, i, y);
    else if (r > 150 && g > 150 && b < 90) add(yel, i, y);
    else if (r > 150 && g < 90 && b < 90) red.push([i, y]); }
  let lowEye = -1, lowAll = -1; for (const [i, y] of red) { if (y >= blue.y0) continue; if (i >= blue.x0 - 3 && i <= blue.x1 + 3) lowEye = Math.max(lowEye, y); lowAll = Math.max(lowAll, y); }   // red above the eyes only (the part and hairline ink are red; the vest ribs are below)
  // forehead band: per column across the brows, the skin rows between the lowest hair pixel and the top brow pixel
  const colTop = {}; for (const [i, y] of browPts) colTop[i] = Math.min(colTop[i] ?? 1e9, y);
  const colHair = {}; for (const [i, y] of red) if (colTop[i] !== undefined && y < colTop[i]) colHair[i] = Math.max(colHair[i] ?? -1, y);
  const bands = Object.keys(colTop).filter(i => colHair[i] !== undefined).map(i => colTop[i] - colHair[i] - 1);
  const forehead = { browPixels: brow, columns: bands.length, minPx: bands.length ? Math.min(...bands) : null, maxPx: bands.length ? Math.max(...bands) : null,
                     medianPx: bands.length ? bands.sort((a, b) => a - b)[bands.length >> 1] : null };
  return { eyePixels: blue, eyeTopPx: blue.y0, hairLowestInEyeColumnsPx: lowEye, hairLowestAnywherePx: lowAll, gapPx: blue.y0 - lowEye,
           grinLinePixels: green, teethPixels: cyan, haloPixels: yel, grinTopBelowEyeBottomPx: Math.min(green.y0, cyan.y0) - blue.y1, forehead }; });
const report = {};
if (!BLOCK) {
  for (const [name, cfg] of [['ingame', { angle: -35, state: { carry: false } }], ['ingame-front', { angle: 0, state: { carry: false } }],
                             ['ingame-idle', { angle: 0, state: { beat: 'idle', puff: 1 } }], ['ingame-like', { angle: 0, state: { beat: 'like' } }],
                             ['ingame-bullets', { angle: 0, state: { beat: 'bullets', hand: 'fingers_3' } }]]) {
    report[name] = await page.evaluate(c => window.renderChar(c), cfg); await shot(name); }
}
for (const [name, cfg] of [['lineup-grass', { ground: 'grass' }], ['lineup-path', { ground: 'path' }]]) {
  report[name] = await page.evaluate(c => window.renderLineup(c), cfg); await shot(name);
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'kit' }); report[name].px_kit = await bbox();
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'brett' }); report[name].px_brett_with_halo = await bbox();
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'brett', brettState: { noHalo: true } }); report[name].px_brett = await bbox();
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'brett', brettAtKit: true, brettState: { noHalo: true } }); report[name].px_brett_at_kit_spot = await bbox();
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'brett', brettAtKit: true }); report[name].px_brett_at_kit_spot_with_halo = await bbox();
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'brett', brettAtKit: true, brettState: { noHalo: true, carry: false } }); report[name].px_brett_at_kit_spot_no_carry = await bbox();
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'brett', mask: 'hair' }); await shot('_' + name + '-hairmask');
  report[name].hair = await hairMask();
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'brett', mask: 'hair', brettState: { carry: false } }); await shot('_' + name + '-hairmask-nocarry');
  report[name].hair_no_carry = await hairMask();
  const r = report[name], kh = r.px_kit.heightPx;
  r.ratio_brett_at_kit_spot = Math.round(r.px_brett_at_kit_spot.heightPx / kh * 1000) / 1000;
  r.ratio_brett_own_spot = Math.round(r.px_brett.heightPx / kh * 1000) / 1000;
  console.log(name, JSON.stringify({ kit: kh, atKit: r.px_brett_at_kit_spot.heightPx, atKitHalo: r.px_brett_at_kit_spot_with_halo.heightPx,
    atKitNoCarry: r.px_brett_at_kit_spot_no_carry.heightPx, own: r.px_brett, ratio: r.ratio_brett_at_kit_spot, hair: r.hair }));
}
// the game-camera beats (grass lineup) and the no-carry grin test
for (const [nm, st] of [['idle', { beat: 'idle' }], ['like', { beat: 'like' }], ['bullets', { beat: 'bullets', hand: 'fingers_3' }], ['nocarry', { carry: false }]]) {
  report['lineup-grass-' + nm] = await page.evaluate(c => window.renderLineup(c), { ground: 'grass', brettState: st }); await shot('lineup-grass-' + nm);
}
for (const [nm, st] of [['idle', { beat: 'idle' }], ['like', { beat: 'like' }], ['bullets', { beat: 'bullets', hand: 'fingers_3' }]]) {
  report['lineup-path-' + nm] = await page.evaluate(c => window.renderLineup(c), { ground: 'path', brettState: st }); await shot('lineup-path-' + nm);
}
if (!BLOCK) {
  report.visibleTris = {};
  for (const [k, st] of [['rest', {}], ['idle', { beat: 'idle' }], ['like', { beat: 'like' }], ['bullets', { beat: 'bullets', hand: 'fingers_3' }],
                         ['talk', { expr: 'talk' }], ['lost', { expr: 'lost' }]])
    report.visibleTris[k] = (await page.evaluate(c => window.renderChar(c), { angle: -35, state: st })).visibleTris;
  console.log('visibleTris', JSON.stringify(report.visibleTris));
}
fs.writeFileSync(path.join(outDir, 'ingame_report.json'), JSON.stringify(report, null, 1));
await browser.close(); srv.close();
