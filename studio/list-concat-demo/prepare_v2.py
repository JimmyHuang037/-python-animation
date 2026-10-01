"""Validate three lesson stages in the IDE container and measure cached Ali narration."""
import hashlib
import json
import subprocess
import wave
from pathlib import Path

ROOT = Path('/workspace')
OUT = ROOT / 'build/docker/list-concat-demo/v2'
WS = OUT / 'workspace'
WS.mkdir(parents=True, exist_ok=True)
settings = json.loads((ROOT / 'studio/list-demo/editor-settings.json').read_text())
settings.update({'editor.occurrencesHighlight': 'off', 'editor.selectionHighlight': False,
                 'terminal.integrated.enablePersistentSessions': False})
(WS / '.vscode').mkdir(exist_ok=True)
(WS / '.vscode/settings.json').write_text(json.dumps(settings, indent=2))
(WS / 'start.py').write_text('')
lines = (ROOT / 'studio/list-concat-demo/lesson.py').read_text().splitlines()
sources = [lines[:2] + [lines[3]], lines[:5], lines]
expected = [
    "['train', 'bus', 'car', 'ship'] ['subway', 'bicycle']\n",
    "['train', 'bus', 'car', 'ship'] ['subway', 'bicycle']\n['train', 'bus', 'car', 'ship', 'subway', 'bicycle']\n",
    "['train', 'bus', 'car', 'ship'] ['subway', 'bicycle']\n['train', 'bus', 'car', 'ship', 'subway', 'bicycle']\n['train', 'bus', 'car', 'ship', 'subway', 'bicycle', 'bike']\n",
]
texts = ['先创建两个列表，vehicle1 和 vehicle2。',
         '使用加号连接两个列表，会生成一个新列表，原来的两个列表不会改变。',
         '使用复合赋值加等号，把 bike 添加到 vehicle 列表中。']
titles = ['创建两个列表', '+ 生成新列表，原列表不变', '+= 向列表末尾添加元素']
boundaries = [0, 10, 21, 30]
records = []
for i, parts in enumerate(sources):
    filename = f'stage{i+1}.py'
    source = '\n'.join(parts) + '\n'
    (WS / filename).write_text(source)
    result = subprocess.run(['python3', str(WS / filename)], capture_output=True, text=True, check=True)
    want = expected[i]
    assert result.stdout == want, (filename, result.stdout)
    audio = OUT.parent / 'audio' / f'{i+1:02}.audio'
    with wave.open(str(audio)) as wav:
        duration = wav.getnframes() / wav.getframerate()
    speech_start = boundaries[i] + 0.25
    speech_end = speech_start + duration
    demo_start = speech_end + 0.3
    assert demo_start + 3 < boundaries[i+1], 'Insufficient time for demonstration'
    records.append(dict(index=i+1, file=filename, title=titles[i], text=texts[i],
                        source=source, source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                        expected_stdout=want, independent_exit_code=result.returncode,
                        audio=str(audio), audio_sha256=hashlib.sha256(audio.read_bytes()).hexdigest(),
                        audio_duration=duration, start=boundaries[i], end=boundaries[i+1],
                        speech_start=speech_start, speech_end=speech_end, demo_start=demo_start))
plan = dict(duration=30, width=1920, height=1080, fps=30, voice='Ethan',
            provider='Alibaba Cloud Bailian', workspace=str(WS), stages=records)
(OUT / 'timeline.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2))
# Repair the corrupted scratch example left by the abandoned typing attempt.
(OUT.parent / 'workspace/vehicle.py').write_text('\n'.join(lines) + '\n')
print(json.dumps([dict(stage=r['index'], speech=[r['speech_start'], r['speech_end']],
                       demonstrate=r['demo_start'], end=r['end']) for r in records], ensure_ascii=False))
