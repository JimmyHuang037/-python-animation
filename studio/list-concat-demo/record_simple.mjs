import {chromium} from '../list-demo/node_modules/playwright/index.mjs';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import path from 'node:path';
import {outputDir as out, prepareWorkspace, ideUrl, checkSaved, executeChecked,
        expectedFinal} from './recording-utils.mjs';

const workspace = path.join(out, 'workspace');
await prepareWorkspace(workspace);
const source = await readFile(new URL('./lesson.py', import.meta.url), 'utf8');
await writeFile(path.join(workspace, 'vehicle.py'), source);
await mkdir(path.join(out, 'raw-simple'), {recursive: true});
const browser = await chromium.launch({headless: true, args: ['--no-sandbox']});
const context = await browser.newContext({viewport: {width: 1920, height: 960},
  recordVideo: {dir: path.join(out, 'raw-simple'), size: {width: 1920, height: 960}}});
const page = await context.newPage();
try {
  await page.goto(ideUrl(workspace));
  await page.locator('.monaco-workbench').waitFor();
  await page.waitForTimeout(1600);
  await page.keyboard.press('Control+p');
  const input = page.locator('.quick-input-widget input');
  await input.waitFor({state: 'visible'});
  await input.fill('vehicle.py');
  await page.locator('.quick-input-list .monaco-list-row').filter({hasText: 'vehicle.py'}).first().click();
  await input.waitFor({state: 'hidden'});
  if (await page.locator('.part.sidebar').isVisible()) await page.keyboard.press('Control+b');
  await page.keyboard.press('F1');
  await input.waitFor({state: 'visible'});
  await input.fill('>Terminal: Create New Terminal');
  await page.locator('.quick-input-list .monaco-list-row').filter({hasText: 'Terminal: Create New Terminal'}).first().click();
  await input.waitFor({state: 'hidden'});
  await checkSaved(page, path.join(workspace, 'vehicle.py'), source);
  const execution = await executeChecked(page, workspace, 'vehicle.py', expectedFinal);
  await page.screenshot({path: path.join(out, 'ide-result.png')});
  await page.waitForTimeout(26000);
  await writeFile(path.join(out, 'simple-events.json'), JSON.stringify({workspace, source, ...execution}, null, 2));
  const video = page.video();
  await context.close();
  await video.saveAs(path.join(out, 'recording-simple.webm'));
  console.log('recorded');
} finally {await browser.close();}
