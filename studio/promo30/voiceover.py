"""Generate timed Edge TTS narration and mix it with the existing promo music."""
import asyncio
import json
import subprocess
import wave
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'build/promo30/tts-male'
VOICE = 'zh-CN-YunxiNeural'
SEGMENTS = [
    (0.15, 4.85, 'Python 难学，听不懂，也不想动手？'),
    (6.05, 9.85, '从学分要求出发，明确期末目标。'),
    (10.10, 12.90, '用动画，让抽象变直观。'),
    (13.05, 15.90, '把新元素，加到列表末尾。'),
    (16.05, 18.85, '看清每一步，理解变化。'),
    (19.10, 24.85, '结合上海高校考情，熟悉判断、填空和编程。'),
    (25.10, 29.65, '让学习更清楚，向期末目标迈进。'),
]


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def stamp(seconds):
    ms = round(seconds * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sr = 48000
    track = bytearray(sr * 30 * 2)
    records, subtitles = [], []
    for index, (start, end, text) in enumerate(SEGMENTS, 1):
        mp3, wav = OUT / f'{index:02}.mp3', OUT / f'{index:02}.wav'
        for rate in ('+0%', '+10%', '+20%', '+30%'):
            await edge_tts.Communicate(text, VOICE, rate=rate).save(str(mp3))
            run('ffmpeg', '-v', 'error', '-y', '-i', str(mp3), '-ar', str(sr),
                '-ac', '1', '-c:a', 'pcm_s16le', str(wav))
            with wave.open(str(wav), 'rb') as source:
                frames = source.readframes(source.getnframes())
            duration = len(frames) / (sr * 2)
            if duration <= end - start:
                break
        else:
            raise RuntimeError(f'Segment {index} exceeds slot; shorten text, do not truncate.')
        offset = round(start * sr) * 2
        track[offset:offset + len(frames)] = frames
        record = dict(index=index, start=start, end=start + duration,
                      slot_end=end, text=text, voice=VOICE, rate=rate, duration=duration)
        records.append(record)
        subtitles.append(f'{index}\n{stamp(start)} --> {stamp(start+duration)}\n{text}\n')
        print(json.dumps(record, ensure_ascii=False), flush=True)
    narration = OUT / 'narration.wav'
    with wave.open(str(narration), 'wb') as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(sr)
        target.writeframes(track)
    (OUT / 'timing.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n')
    (OUT / 'narration.srt').write_text('\n'.join(subtitles))
    # Quiet music bed, additionally ducked whenever the narration is present.
    mixed = OUT / 'mixed.wav'
    run('ffmpeg', '-v', 'error', '-y', '-i', str(narration),
        '-i', str(OUT.parent / 'music-original.wav'), '-filter_complex',
        '[0:a]loudnorm=I=-18:TP=-2:LRA=7,aresample=48000,asplit=2[v][sc];'
        '[1:a]volume=0.3[m];[m][sc]sidechaincompress=threshold=0.025:ratio=6:'
        'attack=15:release=300[duck];[v][duck]amix=inputs=2:duration=longest:'
        'normalize=0,alimiter=limit=0.89:level=0[out]',
        '-map', '[out]', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', str(mixed))
    video = OUT.parent / 'python-course-promo-30s-tts-male.mp4'
    run('ffmpeg', '-v', 'error', '-y', '-i', str(OUT.parent / 'python-course-promo-30s.mp4'),
        '-i', str(mixed), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy',
        '-c:a', 'aac', '-b:a', '192k', '-t', '30', '-movflags', '+faststart', str(video))
    print(video, flush=True)


if __name__ == '__main__':
    asyncio.run(main())
