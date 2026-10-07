"""Join lesson MP4s with a three-phase glitch transition: RGB split, blue sweep, bloom."""
import argparse
import pathlib
import subprocess
import tempfile

import numpy as np
from imageio_ffmpeg import get_ffmpeg_exe

FPS = 30
SECONDS = 1.5
P1, P2 = .28, .72
HALF, CORE = 62, 12
WIDTH, HEIGHT = 1920, 1080
VIGNETTE = None


def ease_in_out(value):
    return 2 * value * value if value < .5 else 1 - (-2 * value + 2) ** 2 / 2


def ease_out(value):
    return 1 - (1 - value) ** 3


def vignette():
    ny, nx = np.mgrid[0:HEIGHT, 0:WIDTH].astype(np.float64)
    nx = (nx / (WIDTH - 1) - .5) * 2
    ny = (ny / (HEIGHT - 1) - .5) * 2
    return np.clip(1 - (nx * nx + ny * ny) * .24, .44, 1.)[..., None].astype(np.float32)


def edge_frame(ffmpeg, path, last):
    command = [ffmpeg, '-v', 'error']
    if last:
        command += ['-sseof', '-0.2']
    command += ['-i', str(path), '-frames:v', '1', '-vf', f'scale={WIDTH}:{HEIGHT}',
                '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    result = subprocess.run(command, capture_output=True)
    if result.returncode:
        raise ValueError('Cannot read a boundary frame: ' + result.stderr.decode('utf-8', errors='replace'))
    pixels = np.frombuffer(result.stdout, np.uint8).astype(np.float32)
    return pixels.reshape(HEIGHT, WIDTH, 3)


def render_frame(source, target, t):
    out = np.empty_like(source)
    x = np.arange(WIDTH)
    if t < P1:
        progress = ease_in_out(t / P1)
        shift = round(progress * 50)
        y = np.arange(HEIGHT)
        wave = np.sin(y * .055 + t / P1 * 28) * shift * .55 + np.cos(y * .12 + t / P1 * 18) * shift * .45
        if progress > .35:
            wave += np.round(np.sin((y // 14) * 7.1 + t / P1 * 44) * shift * .7)
        row_shift = np.round(wave).astype(np.int64)
        red_x = np.clip(x[None, :] - row_shift[:, None], 0, WIDTH - 1)
        blue_x = np.clip(x[None, :] + np.round(row_shift * .42).astype(np.int64)[:, None], 0, WIDTH - 1)
        rows = y[:, None]
        out[..., 0] = source[rows, red_x, 0] * (1 - progress * .28)
        out[..., 1] = source[..., 1] * (1 - progress * .28)
        out[..., 2] = source[rows, blue_x, 2] * (1 - progress * .28)
        rng = np.random.default_rng(int(t * 9999))
        if progress > .32:
            for _ in range(int((progress - .32) / .68 * 12) + 1):
                row, high = int(rng.random() * HEIGHT), int(rng.random() * 3) + 1
                col, wide = int(rng.random() * (WIDTH - 100)), int(rng.random() * 160) + 40
                block = out[row:row + high, col:col + wide]
                draw = rng.random(block.shape)
                block[..., 0] = np.where(draw[..., 0] < .4, draw[..., 0] * 140 + 80, block[..., 0])
                block[..., 1] = np.where(draw[..., 1] < .3, draw[..., 1] * 100 + 30, block[..., 1])
                block[..., 2] = np.where(draw[..., 2] < .6, 160 + draw[..., 2] * 95, block[..., 2])
        if progress > .58:
            for _ in range(int((progress - .58) / .42 * 4) + 1):
                row = int(rng.random() * HEIGHT)
                tear = int((rng.random() - .5) * WIDTH * .36)
                out[row] = source[row, np.clip(x + tear, 0, WIDTH - 1)]
    elif t < P2:
        progress = ease_in_out((t - P1) / (P2 - P1))
        edge = int(progress * WIDTH)
        left, right = x < edge - HALF, x > edge + HALF
        mid = ~(left | right)
        lit = target.copy()
        lit[::3] *= 1.04
        out[:, left] = lit[:, left]
        out[:, right] = source[:, right] * (1 - progress * .5)
        blend = np.clip((x - (edge - HALF)) / (HALF * 2), 0, 1)[None, :, None]
        swept = source * (1 - blend) + target * blend
        glow = np.clip(1 - np.abs(x - edge) / HALF, 0, 1) ** 1.7 * 3.
        swept[..., 1] += 127 * glow * .45
        swept[..., 2] += 255 * glow * .9
        core = np.clip(1 - np.abs(x - edge) / CORE, 0, 1) ** 2
        swept[..., 0] += 215 * core
        swept[..., 1] += 232 * core
        swept[..., 2] += 255 * core
        swept[::2] += (14, 22, 40)
        out[:, mid] = swept[:, mid]
        rng = np.random.default_rng(int(t * 9999))
        for _ in range(8):
            row, wide = int(rng.random() * HEIGHT), int(rng.random() * 90) + 16
            alpha = rng.random() * .12 * progress
            cols = slice(max(0, edge - wide), edge)
            out[row, cols, 2] += 255 * alpha * 2.2
            out[row, cols, 1] += 127 * alpha * 1.4
    else:
        progress = ease_out((t - P2) / (1 - P2))
        peak = max(0., 1 - progress * 1.8)
        out[...] = target * (1 + peak * .4)
        ghost = max(0., 1 - progress * 2.6) * .25
        if ghost:
            out = out * (1 - ghost) + source * ghost
        flash = (peak - .5) / .5 * .5 if peak > .5 else 0.
        if flash:
            out = out * (1 - flash) + 255 * flash
    return np.clip(out * VIGNETTE, 0, 255).astype(np.uint8)


def write_transition(raw_path, ffmpeg, before, after):
    frames = round(SECONDS * FPS)
    source = edge_frame(ffmpeg, before, True)
    target = edge_frame(ffmpeg, after, False)
    with raw_path.open('wb') as handle:
        for index in range(frames):
            handle.write(render_frame(source, target, index / (frames - 1)).tobytes())


def main():
    global VIGNETTE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', nargs='+', required=True, type=pathlib.Path)
    parser.add_argument('--output', required=True, type=pathlib.Path)
    args = parser.parse_args()
    if len(args.inputs) < 2:
        parser.error('at least two inputs are required')
    VIGNETTE = vignette()
    ffmpeg = get_ffmpeg_exe()
    count = len(args.inputs)
    with tempfile.TemporaryDirectory(prefix='glitch-concat-') as work:
        command = [ffmpeg, '-y', '-v', 'error']
        for clip in args.inputs:
            command += ['-i', str(clip)]
        for index in range(count - 1):
            raw = pathlib.Path(work) / f'transition{index}.rgb'
            write_transition(raw, ffmpeg, args.inputs[index], args.inputs[index + 1])
            command += ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WIDTH}x{HEIGHT}',
                        '-r', str(FPS), '-i', str(raw)]
            command += ['-f', 'lavfi', '-t', str(SECONDS), '-i', 'anullsrc=r=48000:cl=mono']
        parts, segments = [], []
        for index in range(count):
            parts.append(f'[{index}:v]fps={FPS},format=yuv420p,setsar=1[v{index}]')
            parts.append(f'[{index}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono[a{index}]')
            segments.append(f'[v{index}][a{index}]')
            if index < count - 1:
                video, audio = count + 2 * index, count + 2 * index + 1
                parts.append(f'[{video}:v]format=yuv420p,setsar=1[v{video}]')
                parts.append(f'[{audio}:a]aformat=sample_fmts=fltp:channel_layouts=mono[a{audio}]')
                segments.append(f'[v{video}][a{audio}]')
        command += ['-filter_complex', ';'.join(parts) + ';' + ''.join(segments) +
                    f'concat=n={2 * count - 1}:v=1:a=1[v][a]',
                    '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '153k', '-ar', '48000', '-ac', '1',
                    '-movflags', '+faststart', str(args.output)]
        result = subprocess.run(command, capture_output=True)
        if result.returncode:
            raise SystemExit(result.stderr.decode('utf-8', errors='replace'))
    print(f'wrote {args.output}')


if __name__ == '__main__':
    main()
