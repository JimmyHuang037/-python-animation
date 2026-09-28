"""Run actual browser recording/rendering and verify persistent MP4 outputs."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path('/workspace')


def run(args, cwd):
    print('RUN', ' '.join(map(str, args)), flush=True)
    process = subprocess.Popen(list(map(str, args)), cwd=cwd)
    while True:
        try:
            code = process.wait(timeout=20)
            break
        except subprocess.TimeoutExpired:
            print('WORKING', args[0], flush=True)
    if code:
        raise subprocess.CalledProcessError(code, args)


def demo():
    cwd = root / 'studio/list-demo'
    run(['python3', 'prepare.py'], cwd)
    run(['node', 'record.mjs'], cwd)
    run(['python3', 'compose.py'], cwd)


def animation():
    cwd = root / 'studio/promo30'
    out = root / 'build/docker/promo30'
    out.mkdir(parents=True, exist_ok=True)
    seconds = float(os.environ.get('PREVIEW_SECONDS') or 30)
    frames = round(seconds * 30)
    run(['node', 'render.mjs'], cwd)
    run(['python3', 'soundtrack.py'], cwd)
    video = out / 'promo30.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-i',
         out / 'frames/%05d.png', '-i', out / 'music-original.wav',
         '-frames:v', str(frames), '-t', str(seconds), '-c:v', 'libx264', '-threads', '2',
         '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-movflags', '+faststart', video], cwd)
    run(['ffmpeg', '-v', 'error', '-i', video, '-f', 'null', '-'], cwd)
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', video]))
    stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    assert (stream['width'], stream['height'], int(stream['nb_frames'])) == (1920, 1080, frames)
    assert abs(float(probe['format']['duration']) - seconds) < 0.1
    (out / 'verification.json').write_text(json.dumps({
        'decode_ok': True, 'frames': frames, 'width': 1920, 'height': 1080,
        'duration': float(probe['format']['duration']),
        'render_url': os.environ['RENDER_URL'], 'continuous_human_review': False,
    }, indent=2))


job = sys.argv[1] if len(sys.argv) > 1 else 'all'
if job not in ('demo', 'animation', 'all'):
    raise SystemExit('Use demo, animation or all')
started = time.time()
if job in ('demo', 'all'):
    demo()
if job in ('animation', 'all'):
    animation()
print(f'COMPLETE {job}: {time.time() - started:.1f}s', flush=True)
