// Renders ingame.png / ingame-front.png / ingame-world.png from ingame.html (kit.glb in three.js r170).
// Run from this folder: node shoot_ingame.mjs
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');                       // runs/jobless-roguelike
const { chromium } = await import(path.join(root, 'concept/node_modules/playwright/index.mjs'));
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.glb': 'model/gltf-binary', '.png': 'image/png' };
const srv = http.createServer((req, res) => { const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res); }).listen(0, '127.0.0.1');
await new Promise(r => srv.on('listening', r));
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 1700, height: 1300 } });
page.on('pageerror', e => console.log('pageerror:', e.message));
page.on('console', m => console.log('console:', m.text()));
await page.goto(`http://127.0.0.1:${srv.address().port}/design/assets/kit/ingame.html`);
await page.waitForFunction(() => window.__ready, null, { timeout: 60000 });
const jobs = [
  ['ingame', 'renderChar', { angle: -35 }],
  ['ingame-front', 'renderChar', { angle: 0 }],
  ['ingame-expr-ghosted', 'renderChar', { angle: -8, w: 600, h: 600, expr: 'ghosted', cam: [0, 0.90, 1.55], target: [0, 0.845, 0] }],
  ['ingame-world', 'renderWorld', {}],
  ['ingame-world-grass', 'renderWorld', { pos: [-3.3, 0.12, 2.7], kitYaw: -20 }],
];
const report = {};
for (const [name, fn, cfg] of jobs) {
  const info = await page.evaluate(([f, c]) => window[f](c), [fn, cfg]);
  await page.locator('#c').screenshot({ path: path.join(here, name + '.png') }); console.log(name, JSON.stringify(info)); report[name] = info;
}
// visible hero triangles per expression, measured in three.js (what the GPU draws for Kit)
report.visibleTris = {};
for (const e of ['hopeful', 'ghosted', 'rejected', 'focused', 'offer_joy']) {
  const info = await page.evaluate(c => window.renderChar(c), { angle: -35, expr: e });
  report.visibleTris[e] = info.visibleHeroTris;
}
console.log('visibleTris', JSON.stringify(report.visibleTris));
// the 5 expressions at the real 26 m follow camera (Kit faces the camera a little), cropped 3x
const crops = [];
for (const e of ['hopeful', 'ghosted', 'rejected', 'focused', 'offer_joy']) {
  const info = await page.evaluate(c => window.renderWorld(c), { expr: e, kitYaw: 10 });
  const file = path.join(here, `_gc_${e}.png`);
  await page.locator('#c').screenshot({ path: file });   // cropped around Kit by make_strips.py
  crops.push(file); report['gamecam_' + e] = info;
}
fs.writeFileSync(path.join(here, 'ingame_report.json'), JSON.stringify(report, null, 1));
await browser.close(); srv.close();
