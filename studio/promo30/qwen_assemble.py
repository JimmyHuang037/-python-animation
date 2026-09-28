"""Prepare the Qwen timeline or mix/encode its separately rendered frames."""
import argparse
import json
from pathlib import Path
import subprocess
import wave

ROOT = Path(__file__).resolve().parents[2]


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def stamp(seconds):
    ms = round(seconds * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--voice', choices=['ethan', 'cherry'], default='ethan')
    parser.add_argument('--prepare', action='store_true')
    args = parser.parse_args()
    out = ROOT / 'build/promo30' / f'qwen-{args.voice}'
    if args.prepare:
        records = json.loads((out / 'timing-proposed.json').read_text())
        # Hold the slogan for 2 seconds; preserve subsequent major scene anchors.
        boundaries = [0, 5, 7, 10, 13, 16, 19, 25, 30]
        for i, r in enumerate(records):
            r.update(start_frame=boundaries[i]*30, end_frame=boundaries[i+1]*30,
                     speech_start=boundaries[i]+(.4 if i == 1 else .15))
            if r['speech_start'] + r['duration'] > boundaries[i+1] - .1:
                raise RuntimeError(f'Segment {i+1} needs a timing revision; never crop speech.')
        (out / 'timing.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n')
        print(out / 'timing.json')
        return
    records = json.loads((out / 'timing.json').read_text())
    sr = 48000
    track = bytearray(sr * 30 * 2)
    subtitles = []
    for r in records:
        pcm = out / f"{r['index']:02}-pcm.wav"
        run('ffmpeg', '-v', 'error', '-y', '-i', str(out/r['audio']),
            '-ar', str(sr), '-ac', '1', '-c:a', 'pcm_s16le', str(pcm))
        with wave.open(str(pcm), 'rb') as source:
            data = source.readframes(source.getnframes())
        offset = round(r['speech_start']*sr)*2
        if offset + len(data) > round(r['end_frame']/30*sr)*2:
            raise RuntimeError('Narration exceeds its scene.')
        track[offset:offset+len(data)] = data
        subtitles.append(f"{r['index']}\n{stamp(r['speech_start'])} --> "
                         f"{stamp(r['speech_start']+len(data)/(sr*2))}\n{r['text']}\n")
    with wave.open(str(out/'narration.wav'), 'wb') as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(sr)
        target.writeframes(track)
    (out/'narration.srt').write_text('\n'.join(subtitles))
    run('ffmpeg', '-v', 'error', '-y', '-i', str(out/'narration.wav'),
        '-i', str(out/'music.wav'), '-filter_complex',
        '[0:a]loudnorm=I=-18:TP=-2:LRA=7,aresample=48000,asplit=2[v][sc];'
        '[1:a]volume=0.3[m];[m][sc]sidechaincompress=threshold=0.025:ratio=6:'
        'attack=15:release=300[duck];[v][duck]amix=inputs=2:duration=longest:'
        'normalize=0,alimiter=limit=0.89:level=0[out]',
        '-map', '[out]', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', str(out/'mixed.wav'))
    frames = out/'frames'
    if not all((frames/f'{i:05}.png').is_file() for i in range(900)):
        raise RuntimeError('Render all 900 frames with this voice timing before encoding.')
    video = out.parent/f'python-course-promo-30s-qwen-{args.voice}.mp4'
    run('ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-i', str(frames/'%05d.png'),
        '-i', str(out/'mixed.wav'), '-frames:v', '900', '-t', '30', '-c:v', 'libx264',
        '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
        '-b:a', '192k', '-movflags', '+faststart', str(video))
    print(video)


if __name__ == '__main__':
    main()
