import assert from 'node:assert/strict';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {spawn} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const lesson = await readFile(path.join(here, '../lesson.py'), 'utf8');
const out = process.env.CONCAT_OUTPUT_DIR || '/workspace/build/docker/list-concat-demo/v2';
const workspace = path.join(out, 'workspace');
await mkdir(path.join(workspace, '.vscode'), {recursive: true});
await writeFile(path.join(workspace, '.vscode/settings.json'),
  await readFile('/workspace/studio/list-demo/editor-settings.json'));
const process = spawn('node', [path.join(here, '../record_staged.mjs')], {stdio: 'inherit'});
const code = await new Promise(resolve => process.once('exit', resolve));
assert.equal(code, 0, 'Recording process failed');
const actual = await readFile(path.join(workspace, 'vehicle.py'), 'utf8');
// Python semantics, rather than a success log, decide whether the recording passed.
const run = spawn('python3', [path.join(workspace, 'vehicle.py')], {stdio: 'pipe'});
let stdout = '', stderr = '';
run.stdout.on('data', chunk => stdout += chunk);
run.stderr.on('data', chunk => stderr += chunk);
const status = await new Promise(resolve => run.once('exit', resolve));
assert.equal(status, 0, stderr + '\nSaved source:\n' + actual);
assert.equal(stdout, "['train', 'bus', 'car', 'ship'] ['subway', 'bicycle']\n['train', 'bus', 'car', 'ship', 'subway', 'bicycle']\n['train', 'bus', 'car', 'ship', 'subway', 'bicycle', 'bike']\n");
console.log('STAGED_SOURCE_AND_OUTPUT_VERIFIED');
