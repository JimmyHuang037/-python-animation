"""Install pinned local code-server binary and create isolated recording workspace."""
import json,tarfile,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'build/list-demo'
VERSION='4.139.1'
OUT.mkdir(parents=True,exist_ok=True)
archive=OUT/f'code-server-{VERSION}-linux-amd64.tar.gz'
url=f'https://github.com/coder/code-server/releases/download/v{VERSION}/{archive.name}'
binary=OUT/f'tools/code-server-{VERSION}-linux-amd64/bin/code-server'
if not binary.exists():
 if not archive.exists():urllib.request.urlretrieve(url,archive)
 with tarfile.open(archive) as t:t.extractall(OUT/'tools',filter='data')
for p in [OUT/'workspace/.vscode/settings.json',OUT/'user-data/User/settings.json']:
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text((HERE/'editor-settings.json').read_text())
(OUT/'workspace/shopping.py').touch()
(OUT/'server-config.yaml').write_text('bind-addr: 127.0.0.1:9042\nauth: none\ncert: false\n')
print(f'{binary} --config {OUT}/server-config.yaml --disable-telemetry --disable-update-check --user-data-dir {OUT}/user-data --extensions-dir {OUT}/extensions {OUT}/workspace')
