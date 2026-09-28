"""Prepare a persistent demo workspace without downloading a host runtime."""
import os
from pathlib import Path

out = Path(os.environ['DEMO_OUTPUT_DIR'])
workspace = out / 'workspace'
settings = Path('/workspace/studio/list-demo/editor-settings.json').read_text()
for target in [workspace / '.vscode/settings.json', out / 'user-data/User/settings.json']:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(settings)
(workspace / 'shopping.py').touch(exist_ok=True)
os.execvp('code-server', [
    'code-server', '--bind-addr', '0.0.0.0:9042', '--auth', 'none',
    '--disable-telemetry', '--disable-update-check',
    '--user-data-dir', str(out / 'user-data'),
    '--extensions-dir', str(out / 'extensions'), str(workspace),
])
