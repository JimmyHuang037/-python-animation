"""Synthesize the promo script through Qwen TTS; no local model required.

Outputs per-sentence WAVs and a measured 30-second timeline for the next render.
API credentials and temporary signed audio URLs are never written to output.
"""
import argparse
import hashlib
import json
import math
import os
import re
from pathlib import Path
import subprocess
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
MODEL = 'qwen3-tts-instruct-flash-2026-01-26'
SCRIPT = [
    (0, 5, 'Python 难学，听不懂，也不想动手？'),
    (5, 6, '一站式解决！'),
    (6, 10, '从学分要求出发，明确期末目标。'),
    (10, 13, '用动画，让抽象变直观。'),
    (13, 16, '把新元素，加到列表末尾。'),
    (16, 19, '看清每一步，理解变化。'),
    (19, 25, '结合上海高校考情，熟悉判断、填空和编程。'),
    (25, 30, '让学习更清楚，向期末目标迈进。'),
]
BASE_URLS = {
    'beijing': 'https://dashscope.aliyuncs.com/api/v1',
    'singapore': 'https://dashscope-intl.aliyuncs.com/api/v1',
}


def request_audio(payload, key, region):
    req = urllib.request.Request(
        BASE_URLS[region] + '/services/aigc/multimodal-generation/generation',
        data=json.dumps(payload).encode(),
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'},
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'API HTTP {exc.code}; check key, region and model access.') from None
    url = data.get('output', {}).get('audio', {}).get('url')
    if not url:
        raise RuntimeError('API did not return audio; no video has been generated.')
    # The documented endpoint may return an HTTP OSS URL; use HTTPS for download.
    if url.startswith('http://'):
        url = 'https://' + url[len('http://'):]
    with urllib.request.urlopen(url, timeout=90) as response:
        audio = response.read()
    return audio, {'request_id': data.get('request_id'), 'usage': data.get('usage')}


def allocate_timeline(records):
    # 0.1 seconds before speech and >=0.1 seconds after; never crop speech.
    minimum = [math.ceil((r['duration'] + .2) * 30) for r in records]
    spare = 900 - sum(minimum)
    if spare < 0:
        raise RuntimeError('Speech exceeds 30 seconds. Review pacing before re-generating; WAVs retained.')
    weights = [max(0, round((r['source_end'] - r['source_start']) * 30) - n)
               for r, n in zip(records, minimum)]
    total = sum(weights)
    extras = [int(spare * w / total) if total else spare // len(records) for w in weights]
    for i in range(spare - sum(extras)):
        extras[i % len(extras)] += 1
    cursor = 0
    for record, count, extra in zip(records, minimum, extras):
        record.update(start_frame=cursor, end_frame=cursor + count + extra,
                      speech_start=cursor / 30 + .1)
        cursor += count + extra
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--key-file', type=Path)
    parser.add_argument('--region', choices=BASE_URLS, default='beijing')
    parser.add_argument('--voice', choices=['Ethan', 'Cherry'], default='Ethan')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps({'model': MODEL, 'voice': args.voice, 'region': args.region,
                          'script': SCRIPT, 'characters': sum(len(s[2]) for s in SCRIPT)},
                         ensure_ascii=False, indent=2))
        return
    key = os.getenv('DASHSCOPE_API_KEY', '')
    if args.key_file:
        candidates=set(re.findall(r'sk-[A-Za-z0-9_-]+', args.key_file.expanduser().read_text()))
        if len(candidates) != 1:
            parser.error('Key file must contain exactly one API key.')
        key=candidates.pop()
    if not key:
        parser.error('Provide DASHSCOPE_API_KEY or --key-file; do not put the key in chat or source.')
    out = ROOT / 'build/promo30' / f'qwen-{args.voice.lower()}'
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for index, (start, end, text) in enumerate(SCRIPT, 1):
        instruction = '普通话，清晰自然，有亲和力的课程宣传口播。节奏明快紧凑，停顿简短，不拖长尾音，准确朗读所有文字。'
        if index == 2:
            instruction += '这一句自信有力，强调一站式解决。'
        payload = {'model': MODEL, 'input': {'text': text, 'voice': args.voice,
                   'language_type': 'Chinese', 'instructions': instruction,
                   'optimize_instructions': True}}
        signature = hashlib.sha256(json.dumps([args.region, payload], sort_keys=True).encode()).hexdigest()
        wav, metadata = out / f'{index:02}.wav', out / f'{index:02}.json'
        cached = json.loads(metadata.read_text()) if metadata.exists() else {}
        if not wav.exists() or cached.get('signature') != signature:
            audio, result = request_audio(payload, key, args.region)
            wav.write_bytes(audio)
            metadata.write_text(json.dumps(dict(signature=signature, **result), indent=2))
        probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                '-of', 'json', str(wav)], check=True, capture_output=True, text=True)
        duration = float(json.loads(probe.stdout)['format']['duration'])
        records.append(dict(index=index, text=text, source_start=start, source_end=end,
                            duration=duration, audio=wav.name, voice=args.voice, model=MODEL))
        print(f'{index:02}: {duration:.3f}s {text}', flush=True)
    timeline = allocate_timeline(records)
    (out / 'timing-proposed.json').write_text(json.dumps(timeline, ensure_ascii=False, indent=2)+'\n')
    print(f'Audio and proposed timeline ready: {out}; video render still required.')


if __name__ == '__main__':
    main()
