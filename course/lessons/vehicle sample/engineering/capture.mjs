import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const from=Number(process.env.RENDER_FROM??0),to=Number(process.env.RENDER_TO??150);
if(!Number.isFinite(from)||!Number.isFinite(to)||from<0||to>150||to<=from)throw Error('Range must satisfy 0 <= from < to <= 150');
const dir=path.resolve(process.env.FRAMES_DIR??'../intermediate/full-v2-frames');fs.mkdirSync(dir,{recursive:true});
if(fs.readdirSync(dir).length)throw Error('Use an empty frames directory to preserve existing captures');
const browser=await chromium.launch({headless:true,args:['--no-sandbox'],...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});
const page=await browser.newPage({viewport:{width:1920,height:1080}});let count=0;const logs=[];
page.on('console',m=>logs.push(m.text()));page.on('pageerror',e=>logs.push('PAGE_ERROR '+e.message));
await page.exposeFunction('saveFrame',async(frame,png)=>{fs.writeFileSync(path.join(dir,`${String(count++).padStart(6,'0')}.png`),Buffer.from(png,'base64'));if(count%450===0)console.log('Frames '+count);});
try{
 await page.goto(process.env.RENDER_URL??'http://127.0.0.1:9031/full-v1.html',{waitUntil:'networkidle',timeout:30000});
 await page.waitForFunction(()=>window.ready,{},{timeout:30000});
 await page.evaluate(options=>window.startRender(options),{from,to});
 fs.writeFileSync(path.join(dir,'capture-log.json'),JSON.stringify({from,to,fps:30,frames_captured:count,logs},null,2));
 if(count<Math.round((to-from)*30)||logs.some(x=>x.startsWith('PAGE_ERROR')))throw Error('Render incomplete or scene error');
 console.log('Captured '+count+' frames');
}finally{await browser.close();}
