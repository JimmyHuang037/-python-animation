import {chromium} from 'playwright';
import {readFile,writeFile,mkdir,unlink} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const out=path.resolve(process.env.DEMO_OUTPUT_DIR || path.join(here,'../../build/list-demo'));
const limit=process.env.PREVIEW_SECONDS ? Number(process.env.PREVIEW_SECONDS) : Infinity;
if(!(limit>0))throw new Error('PREVIEW_SECONDS must be positive');
const segments=JSON.parse(await readFile(path.join(out,'segments.json')));
await mkdir(path.join(out,'raw'),{recursive:true});
await writeFile(path.join(out,'workspace/shopping.py'),'');
await unlink(path.join(out,'workspace/result.txt')).catch(()=>{});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH || undefined,args:['--no-sandbox']});
const context=await browser.newContext({viewport:{width:1920,height:960},recordVideo:{dir:path.join(out,'raw'),size:{width:1920,height:960}}});
const page=await context.newPage();
async function command(text){
 await page.keyboard.press('F1');const input=page.locator('.quick-input-widget input');await input.waitFor({state:'visible'});await input.fill('>'+text);
 await page.locator('.quick-input-list .monaco-list-row').filter({hasText:text}).first().waitFor();
 await page.waitForTimeout(500);await page.locator('.quick-input-list .monaco-list-row').filter({hasText:text}).first().click();await input.waitFor({state:'hidden'});await page.waitForTimeout(500);
}
try{
 const ideUrl=new URL(process.env.IDE_URL || 'http://127.0.0.1:9042/');
 ideUrl.searchParams.set('folder',process.env.IDE_WORKSPACE || path.join(out,'workspace'));
 await page.goto(ideUrl.toString());
 await page.locator('.monaco-workbench').waitFor();await page.waitForTimeout(1500);
 await page.keyboard.press('Control+p');const quick=page.locator('.quick-input-widget input');await quick.waitFor({state:'visible'});await quick.fill('shopping.py');
 const fileResult=page.locator('.quick-input-list .monaco-list-row').filter({hasText:'shopping.py'}).first();
 await fileResult.waitFor({state:'visible'});await fileResult.click();await quick.waitFor({state:'hidden'});
 await page.locator('.monaco-editor').first().waitFor();
 if(await page.locator('.part.sidebar').isVisible())await page.keyboard.press('Control+b');
 if(await page.locator('.part.auxiliarybar').isVisible())await page.keyboard.press('Control+Alt+b');
 await command('Terminal: Kill All Terminals');await page.waitForTimeout(300);
 await command('Terminal: Create New Terminal');await page.locator('.xterm:visible').first().waitFor();await page.waitForTimeout(700);
 await page.locator('.xterm:visible').first().click();await page.keyboard.press('Control+c');await page.keyboard.insertText("export PS1='❯ '; unset PROMPT_COMMAND; clear");await page.keyboard.press('Enter');await page.waitForTimeout(350);
 const editor=page.locator('.monaco-editor').first();await editor.click({position:{x:200,y:70}});await page.keyboard.press('Control+a');await page.keyboard.press('Backspace');await page.keyboard.press('Control+s');
 await page.mouse.move(1900,950);
 await page.screenshot({path:path.join(out,'initial.png')});
 // A green slate marks the exact first frame for post-production trimming.
 await page.evaluate(()=>{const d=document.createElement('div');d.id='record-slate';d.style.cssText='position:fixed;inset:0;background:rgb(0,255,0);z-index:2147483647';document.body.append(d);});
 await page.waitForTimeout(600);
 await page.evaluate(()=>document.getElementById('record-slate').remove());
 const start=performance.now(),events=[];
 for(const segment of segments){
  if((performance.now()-start)/1000>=limit)break;
  const at=(performance.now()-start)/1000;events.push({...segment,start:at});console.log('SEGMENT',segment.index,at.toFixed(2));
  if(segment.code){
   let complete=true;
   for(const ch of segment.code){if((performance.now()-start)/1000>=limit){complete=false;break;}await page.keyboard.insertText(ch);await page.waitForTimeout(48);}
   if(complete&&segment.index<5)await page.keyboard.press('Enter');
   await page.keyboard.press('Control+s');
   await page.screenshot({path:path.join(out,`step-${segment.index}.png`)});
  }
  if(segment.index===6){
   const expected=await readFile(path.join(out,'expected.py'),'utf8');const actual=await readFile(path.join(out,'workspace/shopping.py'),'utf8');
   if(actual.trimEnd()!==expected.trimEnd())throw new Error('Saved source differs from expected: '+JSON.stringify(actual));
   await page.locator('.xterm:visible').first().click();await page.keyboard.type('python3 shopping.py | tee result.txt',{delay:40});await page.keyboard.press('Enter');
   let actualOutput='';for(let i=0;i<100;i++){actualOutput=await readFile(path.join(out,'workspace/result.txt'),'utf8').catch(()=>'');if(actualOutput==="['键盘']\n")break;await page.waitForTimeout(100);}
   if(actualOutput!=="['键盘']\n")throw new Error('Unexpected real output: '+actualOutput);
   events.at(-1).outputReady=(performance.now()-start)/1000;
   await page.screenshot({path:path.join(out,'result.png')});
  }
  const elapsed=(performance.now()-start)/1000-at;
  const remaining=limit-(performance.now()-start)/1000;
  await page.waitForTimeout(Math.max(0,Math.min(segment.duration+0.8-elapsed,remaining)*1000));
 }
 if(!Number.isFinite(limit))await page.waitForTimeout(1800);
 const duration=Math.min(limit,(performance.now()-start)/1000);
 await writeFile(path.join(out,'events.json'),JSON.stringify({duration,preview:Number.isFinite(limit),events,voice:'zh-CN-YunxiNeural',codeServer:'4.139.1',expectedOutput:"['键盘']\n"},null,2));
 await page.screenshot({path:path.join(out,'final.png')});
 const video=page.video();await context.close();await video.saveAs(path.join(out,'recording.webm'));console.log('RECORDED',duration);
}catch(error){
 await page.screenshot({path:path.join(out,'failure.png')}).catch(()=>{});
 throw error;
}finally{await browser.close();}
