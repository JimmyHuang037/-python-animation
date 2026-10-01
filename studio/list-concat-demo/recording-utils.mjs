import {readFile, mkdir, writeFile, rm} from 'node:fs/promises';
import path from 'node:path';

export const expectedFirst = "['train', 'bus', 'car', 'ship'] ['subway', 'bicycle']\n['train', 'bus', 'car', 'ship', 'subway', 'bicycle']\n";
export const expectedFinal = expectedFirst + "['train', 'bus', 'car', 'ship', 'subway', 'bicycle', 'bike']\n";
export const outputDir = process.env.CONCAT_OUTPUT_DIR || '/workspace/build/docker/list-concat-demo/v2';

export async function prepareWorkspace(workspace) {
  await mkdir(path.join(workspace, '.vscode'), {recursive: true});
  await writeFile(path.join(workspace, '.vscode/settings.json'),
    await readFile(new URL('../list-demo/editor-settings.json', import.meta.url)));
}

export function ideUrl(workspace) {
  const url = new URL(process.env.IDE_URL || 'http://ide:9042/');
  url.searchParams.set('folder', workspace);
  return url.toString();
}

export async function focusEnd(page) {
  const editor = page.locator('.monaco-editor:visible').first();
  await editor.click({position: {x: 200, y: 70}});
  await page.keyboard.press('Control+End');
}

export async function checkSaved(page, file, expected) {
  await page.keyboard.press('Control+s');
  for (let i = 0; i < 50; i++) {
    if ((await readFile(file, 'utf8')).trimEnd() === expected.trimEnd()) return;
    await page.waitForTimeout(100);
  }
  throw new Error('Saved source mismatch: ' + JSON.stringify(await readFile(file, 'utf8')));
}

export async function executeChecked(page, workspace, filename, expected) {
  if (!/^[\w.-]+\.py$/.test(filename)) throw new Error('Invalid Python filename');
  const result = path.join(workspace, 'vehicle-result.txt');
  const statusFile = path.join(workspace, 'vehicle-exit.txt');
  await rm(result, {force: true});
  await rm(statusFile, {force: true});
  if (await page.locator('.xterm:visible').count() === 0) {
    await page.keyboard.press('Control+j');
  }
  const terminal = page.locator('.xterm:visible').first();
  await terminal.waitFor({state: 'visible'});
  await terminal.click();
  const statusCommand = "; printf '%s' \"${PIPESTATUS[0]}\" > vehicle-exit.txt";
  await page.keyboard.type(`python3 ${filename} | tee vehicle-result.txt` + statusCommand, {delay: 12});
  await page.keyboard.press('Enter');
  for (let i = 0; i < 100; i++) {
    const status = await readFile(statusFile, 'utf8').catch(() => '');
    if (/^\d+$/.test(status)) {
      const stdout = await readFile(result, 'utf8');
      if (Number(status) !== 0) throw new Error(`Python ${filename} exited with code ${status}`);
      if (stdout !== expected) throw new Error('Real terminal output mismatch: ' + JSON.stringify(stdout));
      return {file: filename, exit_code: Number(status), stdout};
    }
    await page.waitForTimeout(100);
  }
  throw new Error(`Python ${filename} did not finish within 10 seconds`);
}
