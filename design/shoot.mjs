import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
import { chromium } from '../concept/node_modules/playwright/index.mjs';
const root = path.resolve('..');
const types = {'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.png':'image/png','.css':'text/css'};
const srv = http.createServer((req,res)=>{ const u = decodeURIComponent(req.url.split('?')[0]); const p = path.join(root, u);
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, {'content-type': types[path.extname(p)] || 'application/octet-stream'}); fs.createReadStream(p).pipe(res); }).listen(0,'127.0.0.1');
await new Promise(r=>srv.on('listening',r)); const port = srv.address().port;
const jobs = JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
fs.mkdirSync('out/r', {recursive:true});
const browser = await chromium.launch({ args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport:{width:1920,height:1200} });
page.on('pageerror', e => console.log('pageerror:', e.message));
page.on('console', m => { if (m.type()==='error') console.log('console:', m.text()); });
await page.goto(`http://127.0.0.1:${port}/design/render.html`); await page.waitForFunction(()=>window.__ready);
for (const [name, cfg] of Object.entries(jobs)) { const info = await page.evaluate(c => window.render(c), cfg);
  await page.locator('#c').screenshot({path:`out/r/${name}.png`}); console.log(name, JSON.stringify(info)); }
if (process.argv[3]) { await page.setViewportSize({width:1920,height:1080}); await page.goto(`http://127.0.0.1:${port}/design/${process.argv[3]}`); await page.waitForTimeout(800);
  for (const sel of JSON.parse(process.argv[4]||'[]')) { await page.locator(sel[0]).screenshot({path:sel[1]}); console.log('sheet', sel[1]); } }
await browser.close(); srv.close();
