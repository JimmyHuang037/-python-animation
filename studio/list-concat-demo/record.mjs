import {chromium} from '../list-demo/node_modules/playwright/index.mjs';
import {readFile, writeFile, mkdir, rm} from 'node:fs/promises';
import path from 'node:path';
import {outputDir, prepareWorkspace, focusEnd, executeChecked} from './recording-utils.mjs';

const root = '/workspace';
const out = outputDir;
const ideWorkspace = path.join(out, 'workspace');
const source = (await readFile(path.join(root, 'studio/list-concat-demo/lesson.py'), 'utf8')).trimEnd().split('\n');
const file = path.join(ideWorkspace, 'vehicle.py');
const result = path.join(ideWorkspace, 'vehicle-result.txt');
const expectedFirst = "['train', 'bus', 'car', 'ship'] ['subway', 'bicycle']\n['train', 'bus', 'car', 'ship', 'subway', 'bicycle']\n";
const expectedFinal = expectedFirst + "['train', 'bus', 'car', 'ship', 'subway', 'bicycle', 'bike']\n";
await mkdir(out, {recursive: true});
await mkdir(path.join(out, 'raw'), {recursive: true});
await prepareWorkspace(ideWorkspace);
await writeFile(file, '');
await rm(result, {force: true});

const browser = await chromium.launch({headless: true, args: ['--no-sandbox']});
const context = await browser.newContext({viewport: {width: 1920, height: 960}, recordVideo: {dir: path.join(out, 'raw'), size: {width: 1920, height: 960}}});
const page = await context.newPage();
const sleep = ms => page.waitForTimeout(ms);
const events = [];
let start;
const now = () => (performance.now() - start) / 1000;
async function until(second) {await sleep(Math.max(0, (second - now()) * 1000));}
async function mark(name) {events.push({name, time: now()});}
async function command(text) {
  await page.keyboard.press('F1');
  const input = page.locator('.quick-input-widget input');
  await input.waitFor({state: 'visible'});
  await input.fill('>' + text);
  const item = page.locator('.quick-input-list .monaco-list-row').filter({hasText: text}).first();
  await item.waitFor({state: 'visible'});
  await item.click();
  await input.waitFor({state: 'hidden'});
}
async function typeLine(line, enter = true) {
  for (const ch of line) {
    await page.keyboard.insertText(ch);
    await sleep(22);
  }
  if (enter) await page.keyboard.press('Enter');
  await page.keyboard.press('Control+s');
}
async function execute(expected) {
  return executeChecked(page, ideWorkspace, 'vehicle.py', expected);
}
async function checkSaved(expected) {
  for (let i = 0; i < 30; i++) {
    if ((await readFile(file, 'utf8')).trimEnd() === expected.trimEnd()) return;
    await sleep(100);
  }
  throw new Error('Saved source mismatch: ' + JSON.stringify(await readFile(file, 'utf8')));
}

try {
  const url = new URL(process.env.IDE_URL || 'http://ide:9042/');
  url.searchParams.set('folder', ideWorkspace);
  await page.goto(url.toString());
  await page.locator('.monaco-workbench').waitFor();
  await sleep(1300);
  await page.keyboard.press('Control+p');
  const input = page.locator('.quick-input-widget input');
  await input.waitFor({state: 'visible'});
  await input.fill('vehicle.py');
  await page.locator('.quick-input-list .monaco-list-row').filter({hasText: 'vehicle.py'}).first().click();
  await input.waitFor({state: 'hidden'});
  if (await page.locator('.part.sidebar').isVisible()) await page.keyboard.press('Control+b');
  if (await page.locator('.part.auxiliarybar').isVisible()) await page.keyboard.press('Control+Alt+b');
  await command('Terminal: Kill All Terminals');
  await command('Terminal: Create New Terminal');
  await page.locator('.xterm:visible').first().waitFor();
  await page.locator('.xterm:visible').first().click();
  await page.keyboard.insertText("export PS1='> '; unset PROMPT_COMMAND; clear");
  await page.keyboard.press('Enter');
  await page.keyboard.press('Control+j');
  await sleep(400);
  await focusEnd(page);
  await page.keyboard.press('Control+a');
  await page.keyboard.press('Backspace');
  await page.keyboard.press('Control+s');
  await page.mouse.move(1900, 950);
  await page.evaluate(() => {const slate = document.createElement('div'); slate.id = 'record-slate'; slate.style.cssText = 'position:fixed;inset:0;background:rgb(0,255,0);z-index:2147483647'; document.body.append(slate);});
  await sleep(600);
  await page.evaluate(() => document.getElementById('record-slate').remove());
  start = performance.now();
  await mark('intro');
  await until(2.5);
  await mark('create');
  await focusEnd(page);
  for (const line of source.slice(0, 2)) await typeLine(line);
  await until(9);
  await mark('concat');
  await focusEnd(page);
  for (const line of source.slice(2, 5)) await typeLine(line);
  const firstSource = source.slice(0, 5).join('\n') + '\n';
  await checkSaved(firstSource);
  await until(17);
  await mark('first_run');
  events.at(-1).execution = await execute(expectedFirst);
  await page.screenshot({path: path.join(out, 'first-run.png')});
  await until(21);
  await mark('augmented');
  await focusEnd(page);
  for (const line of source.slice(5)) await typeLine(line);
  await checkSaved(source.join('\n'));
  await until(26);
  await mark('final_run');
  events.at(-1).execution = await execute(expectedFinal);
  await page.screenshot({path: path.join(out, 'final-run.png')});
  await until(30);
  await writeFile(path.join(out, 'events.json'), JSON.stringify({events, expectedFirst, expectedFinal, actualFinal: await readFile(result, 'utf8'), source: source.join('\n') + '\n'}, null, 2));
  const video = page.video();
  await context.close();
  await video.saveAs(path.join(out, 'recording.webm'));
  console.log('RECORDED', now().toFixed(2));
} catch (error) {
  await page.screenshot({path: path.join(out, 'failure.png')}).catch(() => {});
  throw error;
} finally {
  await browser.close();
}
