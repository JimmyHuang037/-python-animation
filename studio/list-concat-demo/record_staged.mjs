import {chromium} from '../list-demo/node_modules/playwright/index.mjs';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import path from 'node:path';
import {outputDir as out, prepareWorkspace, ideUrl, focusEnd, checkSaved,
        executeChecked, expectedFirst, expectedFinal} from './recording-utils.mjs';

const workspace = path.join(out, 'workspace');
await prepareWorkspace(workspace);
const file = path.join(workspace, 'vehicle.py');
await writeFile(file, '');
await mkdir(path.join(out, 'raw-staged'), {recursive: true});
const lines = (await readFile(new URL('./lesson.py', import.meta.url), 'utf8')).trimEnd().split('\n');
const additions = [lines.slice(0, 2).concat(lines[3]), [lines[2], lines[4]], lines.slice(5)];
const expected = [expectedFirst.split('\n')[0] + '\n', expectedFirst, expectedFinal];
const browser = await chromium.launch({headless: true, args: ['--no-sandbox']});
const context = await browser.newContext({viewport: {width: 1920, height: 960},
  recordVideo: {dir: path.join(out, 'raw-staged'), size: {width: 1920, height: 960}}});
const page = await context.newPage();
const sleep = ms => page.waitForTimeout(ms);
const stages = [];
async function command(text) {
  await page.keyboard.press('F1');
  const input = page.locator('.quick-input-widget input');
  await input.waitFor({state: 'visible'});
  await input.fill('>' + text);
  await page.locator('.quick-input-list .monaco-list-row').filter({hasText: text}).first().click();
  await input.waitFor({state: 'hidden'});
}
try {
  await page.goto(ideUrl(workspace));
  await page.locator('.monaco-workbench').waitFor();
  await sleep(1500);
  await page.keyboard.press('Control+p');
  const input = page.locator('.quick-input-widget input');
  await input.waitFor({state: 'visible'});
  await input.fill('vehicle.py');
  await page.locator('.quick-input-list .monaco-list-row').filter({hasText: 'vehicle.py'}).first().click();
  await input.waitFor({state: 'hidden'});
  if (await page.locator('.part.sidebar').isVisible()) await page.keyboard.press('Control+b');
  await command('Terminal: Kill All Terminals');
  await command('Terminal: Create New Terminal');
  await page.locator('.xterm:visible').first().waitFor();
  await focusEnd(page);
  await page.keyboard.press('Control+a');
  await page.keyboard.press('Backspace');
  await page.keyboard.press('Control+s');
  await page.screenshot({path: path.join(out, 'staged-blank.png')});
  const saved = [];
  for (let i = 0; i < additions.length; i++) {
    await sleep(4300);
    await focusEnd(page);
    for (const line of additions[i]) {
      for (const ch of line) {await page.keyboard.insertText(ch); await sleep(18);}
      await page.keyboard.press('Enter');
    }
    saved.push(...additions[i]);
    const source = saved.join('\n') + '\n';
    await checkSaved(page, file, source);
    const execution = await executeChecked(page, workspace, 'vehicle.py', expected[i]);
    stages.push({index: i + 1, source, ...execution});
    await page.screenshot({path: path.join(out, `staged-step${i + 1}.png`)});
  }
  await sleep(4300);
  await writeFile(path.join(out, 'staged-events.json'), JSON.stringify({workspace, stages}, null, 2));
  const video = page.video();
  await context.close();
  await video.saveAs(path.join(out, 'recording-staged.webm'));
  console.log('staged_recorded');
} catch (error) {
  await page.screenshot({path: path.join(out, 'staged-failure.png')}).catch(() => {});
  throw error;
} finally {await browser.close();}
