import assert from 'node:assert/strict';
import {mkdir, writeFile} from 'node:fs/promises';
import {chromium} from '../../list-demo/node_modules/playwright/index.mjs';
import {prepareWorkspace, ideUrl, executeChecked} from '../recording-utils.mjs';
const workspace = '/workspace/build/docker/pr2-fix/exit-check/workspace';
await prepareWorkspace(workspace);
for (const [file, source] of Object.entries({
  'good.py': "print('ready')\n",
  'failed.py': "print('ready')\nraise SystemExit(7)\n",
  'wrong.py': "print('wrong')\n",
  'broken.py': 'invalid python source\n',
})) await writeFile(`${workspace}/${file}`, source);
const browser = await chromium.launch({headless: true, args: ['--no-sandbox']});
const page = await browser.newPage({viewport: {width: 1920, height: 960}});
try {
  await page.goto(ideUrl(workspace));
  await page.locator('.monaco-workbench').waitFor();
  await page.waitForTimeout(1500);
  await page.keyboard.press('F1');
  const input = page.locator('.quick-input-widget input');
  await input.waitFor({state: 'visible'});
  await input.fill('>Terminal: Create New Terminal');
  await page.locator('.quick-input-list .monaco-list-row').filter({hasText: 'Terminal: Create New Terminal'}).first().click();
  await input.waitFor({state: 'hidden'});
  await page.locator('.xterm:visible').first().waitFor();
  await page.keyboard.press('Control+j');
  await page.waitForTimeout(400);
  assert.equal(await page.locator('.xterm:visible').count(), 0);
  const result = await executeChecked(page, workspace, 'good.py', 'ready\n');
  assert.equal(result.exit_code, 0);
  assert.equal(result.stdout, 'ready\n');
  await assert.rejects(executeChecked(page, workspace, 'failed.py', 'ready\n'), /exited with code 7/);
  await assert.rejects(executeChecked(page, workspace, 'wrong.py', 'ready\n'), /output mismatch/);
  await assert.rejects(executeChecked(page, workspace, 'broken.py', 'ready\n'), /exited with code 1/);
  await page.screenshot({path: '/workspace/build/docker/pr2-fix/exit-check/verified.png'});
  console.log('HIDDEN_TERMINAL_AND_EXECUTION_FAILURES_VERIFIED');
} finally {await browser.close();}
