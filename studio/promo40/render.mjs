import {chromium} from 'playwright';
import {mkdir, writeFile} from 'node:fs/promises';
import path from 'node:path';

const dest = path.resolve(process.env.FRAMES_DIR || '../../build/promo40/frames');
const seconds = Number(process.env.PREVIEW_SECONDS || 5);
if (!Number.isFinite(seconds) || seconds <= 0 || seconds > 5) {
  throw new Error('PREVIEW_SECONDS must be > 0 and <= 5');
}
const expectedFrames = Math.round(seconds * 30);
if (expectedFrames < 1) throw new Error('PREVIEW_SECONDS must include at least one frame');
await mkdir(dest, {recursive: true});
const browser = await chromium.launch({
  headless: true, executablePath: process.env.CHROMIUM_PATH || undefined,
  args: ['--no-sandbox'],
});
try {
  const page = await browser.newPage();
  await page.addInitScript(seconds => {window.renderSeconds = seconds;}, seconds);
  let count = 0;
  let pageFailed = false;
  page.on('console', msg => console.log(msg.text()));
  page.on('pageerror', error => {pageFailed = true; console.error('PAGE_ERROR', error);});
  await page.exposeFunction('saveFrame', async (frame, data) => {
    if (frame >= 0 && frame < expectedFrames) {
      await writeFile(path.join(dest, `${String(frame).padStart(5, '0')}.png`), Buffer.from(data, 'base64'));
      count++;
    }
  });
  const response = await page.goto(process.env.RENDER_URL || 'http://127.0.0.1:9033/render.html');
  if (!response?.ok()) throw new Error(`Render page HTTP ${response?.status()}`);
  await page.waitForFunction(() => window.ready, {timeout: 120000});
  await page.evaluate(() => window.startRender());
  const result = await page.evaluate(() => window.renderResult);
  console.log('DONE', count, result);
  if (pageFailed || result !== 0 || count !== expectedFrames) process.exitCode = 1;
} finally {
  await browser.close();
}
