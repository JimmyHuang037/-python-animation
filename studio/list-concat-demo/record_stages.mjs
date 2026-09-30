import pkg from '../promo30/node_modules/playwright/index.js';
const {chromium}=pkg;
import {mkdir,rm,writeFile} from 'node:fs/promises';
const out='/workspace/build/docker/list-concat-demo', ws=`${out}/workspace`;
await mkdir(`${out}/raw-stages`,{recursive:true}); await rm(`${ws}/vehicle-result.txt`,{force:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox']}); const ctx=await browser.newContext({viewport:{width:1920,height:960},recordVideo:{dir:`${out}/raw-stages`,size:{width:1920,height:960}}}); const page=await ctx.newPage();
const sleep=ms=>page.waitForTimeout(ms);
await page.goto(`http://ide:9042/?folder=${ws}`); await page.locator('.monaco-workbench').waitFor(); await sleep(1600);
if(await page.locator('.part.sidebar').isVisible()) await page.keyboard.press('Control+b');
await page.keyboard.press('F1'); let q=page.locator('.quick-input-widget input'); await q.waitFor({state:'visible'}); await q.fill('>Terminal: Create New Terminal'); await page.locator('.quick-input-list .monaco-list-row').filter({hasText:'Terminal: Create New Terminal'}).first().click(); await q.waitFor({state:'hidden'}); await sleep(700);
async function open(name){await page.keyboard.press('Control+p');await q.waitFor({state:'visible'});await q.fill(name);await page.locator('.quick-input-list .monaco-list-row').filter({hasText:name}).first().click();await q.waitFor({state:'hidden'});await sleep(500);}
async function run(name){const t=page.locator('.xterm:visible').first();await t.click();await page.keyboard.type(`python3 ${name} | tee vehicle-result.txt`,{delay:15});await page.keyboard.press('Enter');await sleep(1000);}
await open('stage1.py'); await sleep(4500); await run('stage1.py'); await page.screenshot({path:`${out}/stage1-result.png`});
await sleep(4500); await open('stage2.py'); await sleep(4500); await run('stage2.py'); await page.screenshot({path:`${out}/stage2-result.png`});
await sleep(4500); await open('stage3.py'); await sleep(4500); await run('stage3.py'); await page.screenshot({path:`${out}/stage3-result.png`});
await sleep(5000); const v=page.video(); await ctx.close(); await v.saveAs(`${out}/recording-stages.webm`); await browser.close(); console.log('stages_recorded');
