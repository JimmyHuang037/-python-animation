import {chromium} from '../list-demo/node_modules/playwright/index.mjs';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import path from 'node:path';
import {outputDir as out, ideUrl, checkSaved, executeChecked} from './recording-utils.mjs';

const plan = JSON.parse(await readFile(path.join(out, 'timeline.json'), 'utf8'));
const workspace = plan.workspace;
await mkdir(path.join(out, 'raw-stages'), {recursive: true});
const browser = await chromium.launch({headless: true, args: ['--no-sandbox']});
const context = await browser.newContext({viewport: {width: 1920, height: 960},
  recordVideo: {dir: path.join(out, 'raw-stages'), size: {width: 1920, height: 960}}});
const page = await context.newPage();
const stages = [];
async function command(text) {
  await page.keyboard.press('F1');
  const input = page.locator('.quick-input-widget input');
  await input.waitFor({state: 'visible'});
  await input.fill('>' + text);
  await page.locator('.quick-input-list .monaco-list-row').filter({hasText: text}).first().click();
  await input.waitFor({state: 'hidden'});
}
async function open(name) {
  await page.keyboard.press('Control+p');
  const input = page.locator('.quick-input-widget input');
  await input.waitFor({state: 'visible'});
  await input.fill(name);
  await page.locator('.quick-input-list .monaco-list-row').filter({hasText: name}).first().click();
  await input.waitFor({state: 'hidden'});
  await page.locator('.monaco-editor:visible').first().waitFor();
}
try {
  await page.goto(ideUrl(workspace));
  await page.locator('.monaco-workbench').waitFor();
  await page.waitForTimeout(1600);
  if (await page.locator('.part.sidebar').isVisible()) await page.keyboard.press('Control+b');
  await command('Terminal: Kill All Terminals');
  await command('Terminal: Create New Terminal');
  await page.locator('.xterm:visible').first().waitFor();
  const start = performance.now();
  const now = () => (performance.now() - start) / 1000;
  const until = async time => page.waitForTimeout(Math.max(0, (time - now()) * 1000));
  for (const stage of plan.stages) {
    await until(stage.start);
    await open(stage.file);
    await checkSaved(page, path.join(workspace, stage.file), stage.source);
    await until(stage.demo_start);
    const executed_at = now();
    const execution = await executeChecked(page, workspace, stage.file, stage.expected_stdout);
    stages.push({index: stage.index, source: stage.source, executed_at, finished_at: now(), ...execution});
    await page.screenshot({path: path.join(out, `stage${stage.index}-result.png`)});
    await until(stage.end);
  }
  await writeFile(path.join(out, 'stages-events.json'), JSON.stringify({workspace, stages}, null, 2));
  const video = page.video();
  await context.close();
  await video.saveAs(path.join(out, 'recording-stages.webm'));
  console.log('stages_recorded');
} catch (error) {
  await page.screenshot({path: path.join(out, 'stages-failure.png')}).catch(() => {});
  throw error;
} finally {await browser.close();}
