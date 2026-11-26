// Renders the three.js (game engine) images of dot.glb from ingame.html, and measures it in screen pixels.
// Run from this folder: node shoot_ingame.mjs [blockout]   (then python3 make_sheets.py)
// Based on ricky/v1/shoot_ingame.mjs and ats9000/v1/shoot_ingame.mjs.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const BLOCK = process.argv.includes('blockout') || process.argv.includes('pre');   // pre: re-measure ../v1-pre-fringe/dot.glb (lineups only)
const PRE = process.argv.includes('pre');
const outDir = PRE ? path.join(here, '_pre-fringe-remeasure') : BLOCK ? path.join(here, 'blockout') : here;
const glb = PRE ? '../v1-pre-fringe/dot.glb' : BLOCK ? 'blockout/dot_blockout.glb' : 'dot.glb';
fs.mkdirSync(outDir, { recursive: true });
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
await page.goto(`http://127.0.0.1:${srv.address().port}/design/assets/auntie-dot/v1/ingame.html?glb=${glb}`);
await page.waitForFunction(() => window.__ready, null, { timeout: 180000 });
const shot = async (name) => page.locator('#c').screenshot({ path: path.join(outDir, name + '.png') });
const bbox = () => page.evaluate(() => { const c = document.getElementById('c'), t = document.createElement('canvas'); t.width = c.width; t.height = c.height;
  const x = t.getContext('2d'); x.drawImage(c, 0, 0); const d = x.getImageData(0, 0, t.width, t.height).data; let y0 = 1e9, y1 = -1, x0 = 1e9, x1 = -1;
  for (let y = 0; y < t.height; y++) for (let i = 0; i < t.width; i++) { const k = (y * t.width + i) * 4; const mag = d[k] > 200 && d[k + 1] < 60 && d[k + 2] > 200;
    if (!mag) { y0 = Math.min(y0, y); y1 = Math.max(y1, y); x0 = Math.min(x0, i); x1 = Math.max(x1, i); } }
  return { x0, x1, y0, y1, heightPx: y1 - y0 + 1, widthPx: x1 - x0 + 1 }; });
// hair vs eyes, and the smile, from the mask render (hair red, open-eye ink blue, smile green)
const hairMask = () => page.evaluate(() => { const c = document.getElementById('c'), t = document.createElement('canvas'); t.width = c.width; t.height = c.height;
  const x = t.getContext('2d'); x.drawImage(c, 0, 0); const d = x.getImageData(0, 0, t.width, t.height).data;
  const box = () => ({ x0: 1e9, x1: -1, y0: 1e9, y1: -1, n: 0 }); const blue = box(), green = box(), yellow = box(); const red = [], orange = [];
  const add = (b, i, y) => { b.x0 = Math.min(b.x0, i); b.x1 = Math.max(b.x1, i); b.y0 = Math.min(b.y0, y); b.y1 = Math.max(b.y1, y); b.n++; };
  for (let y = 0; y < t.height; y++) for (let i = 0; i < t.width; i++) { const k = (y * t.width + i) * 4, r = d[k], g = d[k + 1], b = d[k + 2];
    if (b > 150 && r < 90 && g < 90) add(blue, i, y);
    if (g > r + 50 && g > b + 50) add(green, i, y);          // the smile is thinner than 1 px: blended with white
    if (r > 150 && g < 90 && b < 90) red.push([i, y]);
    if (r > 200 && g > 90 && g < 190 && b < 80) orange.push([i, y]);
    if (r > 200 && g > 200 && b < 80) add(yellow, i, y); }
  let lowEye = -1, lowAll = -1; for (const [i, y] of red) { if (i >= blue.x0 - 3 && i <= blue.x1 + 3) lowEye = Math.max(lowEye, y); lowAll = Math.max(lowAll, y); }
  // forehead: rows of skin between the lowest hair-or-hairline pixel and the brow top, in the eye columns
  let lowEdge = lowEye; for (const [i, y] of orange) if (i >= blue.x0 - 3 && i <= blue.x1 + 3 && y < yellow.y0) lowEdge = Math.max(lowEdge, y);
  // side hair (Rega ts 1795658703.410809): hair or hairline-ink pixels OUTSIDE the eye columns; the lowest of them
  // within the face width, and in the eye rows (eye top - 2 .. eye bottom) the horizontal gap to each outer eye edge
  const ec0 = blue.x0 - 3, ec1 = blue.x1 + 3, side = red.concat(orange).filter(([i]) => i < ec0 || i > ec1);
  let sideLow = -1; for (const [i, y] of side) if (i >= blue.x0 - 25 && i <= blue.x1 + 25) sideLow = Math.max(sideLow, y);
  let leftX = -1, rightX = 1e9; for (const [i, y] of red.concat(orange)) if (y >= blue.y0 - 2 && y <= blue.y1) { if (i < blue.x0) leftX = Math.max(leftX, i); if (i > blue.x1) rightX = Math.min(rightX, i); }
  const sideHair = { lowestSideHairPx: sideLow, lowestSideHairVsEyeTopPx: blue.y0 - sideLow,
    gapLeftPx: leftX < 0 ? null : blue.x0 - leftX - 1, gapRightPx: rightX > 1e8 ? null : rightX - blue.x1 - 1 };
  return { sideHair, eyePixels: blue, eyeTopPx: blue.y0, hairLowestInEyeColumnsPx: lowEye, hairLowestAnywherePx: lowAll, gapPx: blue.y0 - lowEye,
           browPixels: yellow, browTopPx: yellow.y0, hairOrHairlineLowestInEyeColumnsPx: lowEdge, foreheadPx: yellow.y0 - lowEdge - 1,
           smilePixels: green, smileTopBelowEyeBottomPx: green.y0 - blue.y1 }; });
const report = {};
if (!BLOCK) {
  for (const [name, cfg] of [['ingame', { angle: -35 }], ['ingame-front', { angle: 0 }], ['ingame-talk', { angle: 0, state: { pose: 'talk' } }],
                             ['ingame-card', { angle: 0, state: { pose: 'card' } }], ['ingame-sway', { angle: 0, state: { sway: 4 } }]]) {
    report[name] = await page.evaluate(c => window.renderChar(c), cfg); await shot(name); }
}
for (const [name, cfg] of [['lineup-grass', { ground: 'grass' }], ['lineup-path', { ground: 'path' }]]) {
  report[name] = await page.evaluate(c => window.renderLineup(c), cfg); await shot(name);
  for (const who of ['kit', 'dot']) { await page.evaluate(c => window.renderLineup(c), { ...cfg, only: who }); report[name]['px_' + who] = await bbox(); }
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'dot', dotAtKit: true }); report[name].px_dot_at_kit_spot = await bbox();
  await page.evaluate(c => window.renderLineup(c), { ...cfg, only: 'dot', mask: 'hair' }); await shot('_' + name + '-hairmask');
  report[name].hair = await hairMask();
  report[name].ratio_dot_to_kit = Math.round(report[name].px_dot.heightPx / report[name].px_kit.heightPx * 1000) / 1000;
  report[name].ratio_dot_at_kit_spot = Math.round(report[name].px_dot_at_kit_spot.heightPx / report[name].px_kit.heightPx * 1000) / 1000;
  console.log(name, JSON.stringify({ kit: report[name].px_kit.heightPx, dot: report[name].px_dot, atKit: report[name].px_dot_at_kit_spot.heightPx,
    ratio: report[name].ratio_dot_to_kit, ratioAtKit: report[name].ratio_dot_at_kit_spot, hair: report[name].hair }));
}
if (!BLOCK) {
  report['lineup-grass-talk'] = await page.evaluate(c => window.renderLineup(c), { ground: 'grass', dotState: { pose: 'talk' } }); await shot('lineup-grass-talk');
  report['lineup-grass-card'] = await page.evaluate(c => window.renderLineup(c), { ground: 'grass', dotState: { pose: 'card' } }); await shot('lineup-grass-card');
  report.visibleTris = {};
  for (const [k, st] of [['rest', {}], ['talk', { pose: 'talk' }], ['card', { pose: 'card' }], ['happy', { expr: 'happy' }]])
    report.visibleTris[k] = (await page.evaluate(c => window.renderChar(c), { angle: -35, state: st })).visibleTris;
  console.log('visibleTris', JSON.stringify(report.visibleTris));
}
fs.writeFileSync(path.join(outDir, 'ingame_report.json'), JSON.stringify(report, null, 1));
await browser.close(); srv.close();
