import {chromium} from 'playwright';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import path from 'node:path';
const dest=path.resolve(process.env.FRAMES_DIR || '../../build/promo30/frames');
const seconds=Number(process.env.PREVIEW_SECONDS || 30);
if(!Number.isFinite(seconds)||seconds<=0||seconds>30)throw new Error('PREVIEW_SECONDS must be > 0 and <= 30');
const expectedFrames=Math.round(seconds*30);
await mkdir(dest,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH || undefined,args:['--no-sandbox']});
const page=await browser.newPage();
await page.addInitScript(seconds=>{window.renderSeconds=seconds;},seconds);
if(process.env.TIMING_PATH){
 const timing=JSON.parse(await readFile(process.env.TIMING_PATH,'utf8'));
 await page.addInitScript(timing=>{window.__promoTiming=timing;},timing);
}
page.on('console',msg=>console.log(msg.text()));
page.on('pageerror',e=>console.error('PAGE_ERROR',e));
let count=0;
await page.exposeFunction('saveFrame',async(frame,data)=>{if(frame<expectedFrames){await writeFile(path.join(dest,`${String(frame).padStart(5,'0')}.png`),Buffer.from(data,'base64'));count++;if(frame%150===0)console.log('FRAME',frame);}});
const response=await page.goto(process.env.RENDER_URL || 'http://127.0.0.1:9030/render.html');
if(!response?.ok()){await browser.close();throw new Error(`Render page HTTP ${response?.status()}`);}
await page.waitForFunction(()=>window.ready,{timeout:120000});
await page.evaluate(()=>window.startRender());
console.log('DONE',count,await page.evaluate(()=>window.renderResult));
await browser.close();
if(count!==expectedFrames)process.exitCode=1;
