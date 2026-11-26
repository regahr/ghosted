// Renders the three.js (game engine) images of ghostie.glb from ingame.html, and measures triangles per variant.
// Run from this folder: node shoot_ingame.mjs   (then python3 make_sheets.py)
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../..');                       // runs/jobless-roguelike
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
await page.goto(`http://127.0.0.1:${srv.address().port}/design/assets/ghostie/v6/ingame.html`);
await page.waitForFunction(() => window.__ready, null, { timeout: 60000 });
const jobs = [
  ['ingame', 'renderChar', { angle: -35 }],
  ['ingame-front', 'renderChar', { angle: 0 }],
  ['ingame-rest-front', 'renderChar', { angle: 0, upright: false }],
  ['_ingame-wave', 'renderChar', { angle: -40, w: 1200, h: 1200, cam: [0, 0.55, 1.35], target: [0, 0.40, 0], wave: 40 }],
  ['lineup-grass', 'renderLineup', { ground: 'grass' }],
  ['lineup-path', 'renderLineup', { ground: 'path' }],
  ['lineup-grass-wave20', 'renderLineup', { ground: 'grass', wave: 20 }],
  ['lineup-grass-wave40', 'renderLineup', { ground: 'grass', wave: 40 }],
  ['lineup-path-wave40', 'renderLineup', { ground: 'path', wave: 40 }],
];
const report = {};
for (const [name, fn, cfg] of jobs) {
  const info = await page.evaluate(([f, c]) => window[f](c), [fn, cfg]);
  await page.locator('#c').screenshot({ path: path.join(here, name + '.png') }); console.log(name, JSON.stringify(info)); report[name] = info;
}
report.visibleTris = {};
for (const v of ['tie', 'glasses', 'headset']) {
  const info = await page.evaluate(c => window.renderChar(c), { angle: -35, variant: v });
  report.visibleTris[v] = info.visibleGhostTris;
}
console.log('visibleTris', JSON.stringify(report.visibleTris));
fs.writeFileSync(path.join(here, 'ingame_report.json'), JSON.stringify(report, null, 1));
await browser.close(); srv.close();
