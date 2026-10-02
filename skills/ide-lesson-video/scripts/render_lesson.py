"""Tutorial with simultaneous narration/typing, 0.1-second keys and a measured caret."""
import argparse
from array import array
import os
import bisect
import hashlib
import json
import math
import shutil
import subprocess
import sys
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description='Render a narrated Python IDE lesson from a JSON course.')
parser.add_argument('--lesson', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--runtime-dir', type=Path)
parser.add_argument('--preflight', action='store_true')
parser.add_argument('--overwrite', action='store_true')
args = parser.parse_args()
if args.runtime_dir:
    sys.path.insert(0, str(args.runtime_dir.resolve()))
import imageio_ffmpeg
import lesson_style as style
from lesson_style import render_frame as render_styled_frame
from run_click_effect import apply_run_click, phase_frame, FADE_SECONDS, APPROACH_SECONDS, END_SECONDS
FF = imageio_ffmpeg.get_ffmpeg_exe()
LESSON_PATH = args.lesson.resolve()
LESSON_ROOT = LESSON_PATH.parent
LESSON = json.loads(LESSON_PATH.read_text(encoding='utf-8-sig'))
assert LESSON.get('schema_version') == 1 and LESSON.get('stages'), 'Invalid lesson schema'
VIDEO = args.output.resolve()
assert VIDEO.suffix.lower() == '.mp4', 'Output must be MP4'
if VIDEO.exists() and not args.overwrite and not args.preflight:
    raise FileExistsError('Choose a new output name or pass --overwrite: ' + str(VIDEO))
OUT = VIDEO.parent
WORK = OUT / '.work' / VIDEO.stem
WORK.mkdir(parents=True, exist_ok=True)
FPS, WIDTH, HEIGHT = 30, 1920, 1080
TIMING = dict(character_seconds=.1, after_typing=1., result_hold=2.)
configured_timing = dict(LESSON.get('timing', {}))
for legacy_key in ('voice_lead', 'after_voice'):
    assert configured_timing.pop(legacy_key, 0) == 0, f'{legacy_key} is retired: remove it or set it to 0 for simultaneous narration/typing'
assert not configured_timing.keys() - TIMING.keys(), 'Unknown timing field'
TIMING.update(configured_timing)
assert all(isinstance(v, (int,float)) and math.isfinite(v) and v >= 0 for v in TIMING.values())
KEY_INTERVAL_FRAMES = round(TIMING['character_seconds'] * FPS)
assert KEY_INTERVAL_FRAMES > 0 and math.isclose(KEY_INTERVAL_FRAMES / FPS, TIMING['character_seconds']), 'Character interval must align to frames'
POST_TYPE_PAUSE_FRAMES = round(TIMING['after_typing'] * FPS)
RESULT_HOLD_FRAMES = round(TIMING['result_hold'] * FPS)
assert POST_TYPE_PAUSE_FRAMES >= math.ceil(APPROACH_SECONDS * FPS), 'Pause too short for mouse approach'
assert RESULT_HOLD_FRAMES > math.ceil(END_SECONDS * FPS), 'Result hold must allow mouse fade to finish'
STYLE = dict(display_file=LESSON.get('display_file', 'lesson.py'), lesson_label=LESSON.get('lesson_label', 'Python 教学'),
             voice_label=LESSON.get('voice_label', '配音'), stage_count=len(LESSON['stages']))
TYPING_SOUND = dict(enabled=True, volume=.75, source='')
TYPING_SOUND.update(LESSON.get('typing_sound', {}))
assert isinstance(TYPING_SOUND['enabled'], bool)
assert 0 <= float(TYPING_SOUND['volume']) <= 1
style.configure(**STYLE)

def checked(command, **kwargs):
    return subprocess.run(command, check=True, **kwargs)


def snapshot(lines, row, col, key):
    assert 0 <= row < len(lines) and 0 <= col <= len(lines[row])
    return dict(lines=lines.copy(), row=row, col=col, key=key)


def execute_stage(source):
    execution = LESSON.get('execution', {})
    mode = execution.get('mode', 'local')
    timeout = execution.get('timeout_seconds', 15)
    if mode == 'local':
        result = checked([sys.executable, str(source)], cwd=str(source.parent), capture_output=True, text=True, encoding='utf-8', timeout=timeout, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    elif mode == 'docker':
        container = execution.get('container')
        assert container, 'Docker mode requires an existing container name'
        result = checked(['docker', 'exec', '-i', container, execution.get('python', 'python3'), '-'],
                         input=source.read_text(encoding='utf-8-sig'), capture_output=True, text=True, encoding='utf-8', timeout=timeout)
    else:
        raise ValueError('Unsupported execution mode: ' + str(mode))
    if result.stderr.strip():
        raise RuntimeError('Review stderr before rendering: ' + result.stderr)
    return result.stdout.splitlines()


def edit_sequence(stage, previous, target, operations=None):
    lines = previous.copy() if previous else ['']
    row, col = len(lines)-1, len(lines[-1])
    events = []
    def move(r,c):
        nonlocal row,col
        row = len(lines)-1 if r == 'last' else int(r)
        assert 0 <= row < len(lines), 'Move row outside document'
        col = len(lines[row]) if c == 'end' else int(c)
        events.append(snapshot(lines,row,col,'move'))
    def type_text(text):
        nonlocal row,col
        for char in text:
            if char == '\n':
                rest = lines[row][col:]
                lines[row] = lines[row][:col]
                lines.insert(row+1,rest)
                row,col = row+1,0
            else:
                lines[row] = lines[row][:col]+char+lines[row][col:]
                col += 1
            events.append(snapshot(lines,row,col,char))
    def backspace(count):
        nonlocal row,col
        assert isinstance(count,int) and count > 0
        for _ in range(count):
            if col:
                lines[row] = lines[row][:col-1]+lines[row][col:]
                col -= 1
            elif row:
                col = len(lines[row-1])
                lines[row-1] += lines.pop(row)
                row -= 1
            else:
                raise ValueError('Backspace at beginning of document')
            events.append(snapshot(lines,row,col,'backspace'))
    if operations is None:
        target_text = '\n'.join(target)
        previous_text = '\n'.join(previous)
        if not previous:
            type_text(target_text)
        elif target_text.startswith(previous_text):
            type_text(target_text[len(previous_text):])
        else:
            raise ValueError('Stage edits required when code is not append-only')
    else:
        for op in operations:
            if op['op'] == 'move':
                move(op['row'],op['col'])
            elif op['op'] == 'type':
                type_text(op['text'])
            elif op['op'] == 'backspace':
                backspace(op.get('count',1))
            else:
                raise ValueError('Unsupported edit action: ' + str(op['op']))
    assert lines == target, 'Edits do not reproduce stage source exactly'
    assert events, 'Each stage must include an edit'
    return events


def event_frames(events, first):
    # At 30 fps, exactly three frames equals 0.1 seconds per keystroke.
    frames = [first + index * KEY_INTERVAL_FRAMES for index in range(len(events))]
    assert all(b - a == KEY_INTERVAL_FRAMES for a, b in zip(frames, frames[1:]))
    return frames


def draw_frame(stage, state, output_stage, caret_on, frame=None):
    return render_styled_frame(stage, state, output_stage, caret_on, STAGES, frame=frame)


STAGES = []
previous = []
start = 0
for i, specification in enumerate(LESSON['stages']):
    source = (LESSON_ROOT / specification['source']).resolve()
    text = source.read_text(encoding='utf-8-sig').rstrip('\r\n')
    assert '\t' not in text, 'Use spaces instead of tabs'
    lines = text.split('\n')
    assert len(lines) <= 8, 'Split the lesson or adjust layout: too many code lines'
    output = execute_stage(source)
    assert len(output) <= 3, 'Split the lesson or adjust layout: too many output lines'
    voice = (LESSON_ROOT / specification['audio']).resolve()
    with wave.open(str(voice)) as w:
        voice_duration = w.getnframes() / w.getframerate()
    speech_start = start / FPS
    speech_end = speech_start + voice_duration
    first = start
    events = edit_sequence(i, previous, lines, specification.get('edits'))
    frames = event_frames(events, first)
    last = frames[-1]
    circle_frame = last + round(1.0 * FPS)
    bubble_frame = circle_frame + round(1.0 * FPS)
    bubble_end_frame = bubble_frame + round(1.4 * FPS)
    result = bubble_end_frame + round(.4 * FPS)
    end = result + RESULT_HOLD_FRAMES
    bubble_exit_frame = end - round(1.2 * FPS)
    bubble_exit_end_frame = end
    assert first / FPS == speech_start
    assert speech_end <= end / FPS, 'Narration must finish before the next stage; shorten narration, split the stage or increase result_hold'
    assert result - last == POST_TYPE_PAUSE_FRAMES
    initial = snapshot(previous if previous else [''], len(previous) - 1 if previous else 0, len(previous[-1]) if previous else 0, 'idle')
    STAGES.append(dict(stage=i + 1, start_frame=start, typing_start_frame=first, typing_end_frame=last, result_frame=result, end_frame=end,
                       speech_start=speech_start, speech_end=speech_end, voice_duration=voice_duration,
                       source=str(source), voice=str(voice), voice_sha256=hashlib.sha256(voice.read_bytes()).hexdigest(),
                       initial=initial, events=events, event_frames=frames, output=output,
                       annotations=specification.get('annotations', []), circle_frame=circle_frame,
                       bubble_frame=bubble_frame, bubble_end_frame=bubble_end_frame,
                       bubble_exit_frame=bubble_exit_frame, bubble_exit_end_frame=bubble_exit_end_frame))
    previous = lines
    start = end
TOTAL_FRAMES = STAGES[-1]['end_frame']
TOTAL_SECONDS = TOTAL_FRAMES / FPS
for i, stage in enumerate(STAGES):
    preview = draw_frame(i, stage['events'][-1], i, True, frame=stage['typing_end_frame'] + 3)
    preview.save(WORK / f'stage{i+1}-preflight.png')
    for state in stage['events']:
        x,y = style.caret_position(state)
        assert y + style.CARET_HEIGHT < style.EDITOR_RECT[3]-16, 'Transient edit exceeds code height'
        assert all(style.CODE_X + style.FONT.getlength(line) < style.EDITOR_RECT[2]-24 for line in state['lines']), 'Code line exceeds width'
if args.preflight:
    print(json.dumps(dict(preflight_ok=True, stages=len(STAGES), frames=TOTAL_FRAMES, duration=TOTAL_SECONDS, previews=str(WORK)), ensure_ascii=True))
    raise SystemExit(0)



def video_state(f):
    i = max(n for n, stage in enumerate(STAGES) if f >= stage['start_frame'])
    stage = STAGES[i]
    pos = bisect.bisect_right(stage['event_frames'], f) - 1
    state = stage['initial'] if pos < 0 else stage['events'][pos]
    output_stage = i if f >= stage['result_frame'] else i - 1
    typing = stage['typing_start_frame'] <= f <= stage['typing_end_frame']
    blink_origin = stage['typing_end_frame'] if pos >= 0 else stage['start_frame']
    caret_on = typing or (f - blink_origin) % 30 < 18
    return i, state, output_stage, caret_on


silent = WORK / 'typing-silent.mp4'
encoder_log = WORK / 'encode.log'
samples = {}
for stage in STAGES:
    for name, f in [('simultaneous-start', stage['typing_start_frame']),
                    ('typing', (stage['typing_start_frame'] + stage['typing_end_frame']) // 2),
                    ('typed', stage['typing_end_frame']),
                    ('before-result', stage['result_frame'] - 1),
                    ('click-approach', stage['result_frame'] - 9),
                    ('click-pressed', stage['result_frame'] + 2),
                    ('click-fading', stage['result_frame'] + 24),
                    ('click-gone', stage['result_frame'] + 42),
                    ('result', stage['result_frame'])]:
        samples[f] = f'stage{stage["stage"]}-{name}.png'
with encoder_log.open('wb') as log:
    proc = subprocess.Popen([FF, '-hide_banner', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                             '-s', f'{WIDTH}x{HEIGHT}', '-r', str(FPS), '-i', 'pipe:0', '-an',
                             '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-threads', '4',
                             '-pix_fmt', 'yuv420p', str(silent)], stdin=subprocess.PIPE, stderr=log)
    last_signature, raw = None, None
    try:
        for f in range(TOTAL_FRAMES):
            i, state, output_stage, caret_on = video_state(f)
            click_phase = phase_frame(f, STAGES[i]['result_frame'], FPS)
            annotation_phase = (f >= STAGES[i]['circle_frame'],
                                max(-1, min(f - STAGES[i]['bubble_frame'],
                                            STAGES[i]['bubble_end_frame'] - STAGES[i]['bubble_frame'])),
                                max(0, min(f - STAGES[i]['bubble_exit_frame'],
                                           STAGES[i]['bubble_exit_end_frame'] - STAGES[i]['bubble_exit_frame'])))
            signature = (i, tuple(state['lines']), state['row'], state['col'], output_stage, caret_on, click_phase, annotation_phase)
            if signature != last_signature:
                im = draw_frame(i, state, output_stage, caret_on, frame=f)
                im = apply_run_click(im, f, STAGES[i]['result_frame'], FPS)
                raw, last_signature = im.tobytes(), signature
            if f in samples:
                im.save(WORK / samples[f])
            proc.stdin.write(raw)
    finally:
        proc.stdin.close()
        status = proc.wait()
    if status:
        raise RuntimeError(encoder_log.read_text(encoding='utf-8'))

SAMPLE_RATE = 48000
total_samples = round(TOTAL_SECONDS * SAMPLE_RATE)
voice_track = bytearray(total_samples * 2)
for stage in STAGES:
    resampled = WORK / f'voice-{stage["stage"]}-48k.wav'
    checked([FF, '-hide_banner', '-v', 'error', '-y', '-i', stage['voice'], '-ar', '48000', '-ac', '1', '-c:a', 'pcm_s16le', str(resampled)])
    with wave.open(str(resampled)) as w:
        audio = w.readframes(w.getnframes())
    offset = round(stage['speech_start'] * SAMPLE_RATE) * 2
    assert offset + len(audio) <= len(voice_track)
    voice_track[offset:offset + len(audio)] = audio


def load_keyboard_source(sample_rate):
    source = TYPING_SOUND.get('source')
    if not source:
        raise ValueError('A real typing_sound.source WAV is required for this preview')
    path = (LESSON_ROOT / source).resolve()
    with wave.open(str(path)) as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2
        samples = array('h', w.readframes(w.getnframes()))
        original_rate = w.getframerate()
    if original_rate != sample_rate:
        raise ValueError('typing_sound.source must be a 48 kHz mono WAV')
    peak = max(abs(sample) for sample in samples) or 1
    gain = min(3.0, 26000 / peak)
    return array('h', [max(-32768, min(32767, round(sample * gain))) for sample in samples])


typing_track = array('h', [0]) * total_samples
if TYPING_SOUND['enabled']:
    source_samples = load_keyboard_source(SAMPLE_RATE)
    source_start = round(float(TYPING_SOUND.get('source_start_seconds', 0)) * SAMPLE_RATE)
    gain = float(TYPING_SOUND['volume'])
    source_cursor = source_start
    for stage in STAGES:
        stage_samples = round((stage['typing_end_frame'] - stage['typing_start_frame'] + 1) / FPS * SAMPLE_RATE)
        if source_cursor + stage_samples > len(source_samples):
            raise ValueError('typing_sound.source does not contain enough continuous audio for all stages')
        offset = round(stage['typing_start_frame'] / FPS * SAMPLE_RATE)
        for index in range(stage_samples):
            target = offset + index
            value = typing_track[target] + round(source_samples[source_cursor + index] * gain)
            typing_track[target] = max(-32768, min(32767, value))
        source_cursor += stage_samples

with wave.open(str(WORK / 'typing-clicks.wav'), 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SAMPLE_RATE)
    w.writeframes(typing_track.tobytes())

voice_samples = array('h', voice_track)
with wave.open(str(WORK / 'voice-only.wav'), 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SAMPLE_RATE)
    w.writeframes(voice_track)
for index, click_sample in enumerate(typing_track):
    value = voice_samples[index] + click_sample
    voice_samples[index] = max(-32768, min(32767, value))
track = voice_samples.tobytes()
with wave.open(str(WORK / 'narration.wav'), 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SAMPLE_RATE)
    w.writeframes(track)

video = VIDEO
pending = WORK / video.name
checked([FF, '-hide_banner', '-v', 'error', '-y', '-i', str(silent), '-i', str(WORK / 'narration.wav'),
         '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', 'loudnorm=I=-18:TP=-2:LRA=7,aresample=48000',
         '-c:a', 'aac', '-b:a', '192k', '-t', str(TOTAL_SECONDS), '-movflags', '+faststart', str(pending)])
checked([FF, '-hide_banner', '-v', 'error', '-xerror', '-i', str(pending), '-f', 'null', '-'])
frames, duration = imageio_ffmpeg.count_frames_and_secs(str(pending))
reader = imageio_ffmpeg.read_frames(str(pending))
metadata = next(reader)
reader.close()
assert frames == TOTAL_FRAMES and abs(duration - TOTAL_SECONDS) < .02
assert tuple(metadata['size']) == (WIDTH, HEIGHT)
shutil.copy2(pending, video)
stage_report = []
for stage in STAGES:
    stage_report.append({key: stage[key] for key in ['stage', 'start_frame', 'typing_start_frame', 'typing_end_frame', 'result_frame', 'end_frame', 'speech_start', 'speech_end', 'voice_duration', 'voice_sha256']})
    stage_report[-1].update(keystrokes=len(stage['events']), pause_seconds=(stage['result_frame'] - stage['typing_end_frame']) / FPS)
    stage_report[-1].update(click_frame=stage['result_frame'], mouse_fade_seconds=FADE_SECONDS)
    stage_report[-1].update(narration_typing_start_offset_seconds=stage['typing_start_frame'] / FPS - stage['speech_start'])
    gaps = [(b - a) / FPS for a, b, event in zip(stage['event_frames'], stage['event_frames'][1:], stage['events'][1:]) if event['key'] != 'move']
    stage_report[-1].update(character_interval_min=min(gaps) if gaps else None, character_interval_max=max(gaps) if gaps else None, character_interval_mean=sum(gaps) / len(gaps) if gaps else None, output_hold_seconds=RESULT_HOLD_FRAMES / FPS)
verification = dict(video=video.name, duration=duration, width=metadata['size'][0], height=metadata['size'][1], fps=metadata['fps'], frames=frames,
                    decode_ok=True, voice=LESSON.get('voice', 'provided'), provider=LESSON.get('provider', 'provided audio'), stages=stage_report, source_outputs_verified=True,
                    method=f'Narration and typing start together; {KEY_INTERVAL_FRAMES/FPS:g}s per key; click/output {POST_TYPE_PAUSE_FRAMES/FPS:g}s after final key; measured caret.',
                    sha256=hashlib.sha256(video.read_bytes()).hexdigest())
video.with_suffix('.verification.json').write_text(json.dumps(verification, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK / 'edit-events.json').write_text(json.dumps(STAGES, ensure_ascii=False, indent=2), encoding='utf-8')
manifest = dict(schema_version=1, video=str(video), work=str(WORK), fps=FPS, frames=TOTAL_FRAMES, duration=TOTAL_SECONDS,
                lesson=str(LESSON_PATH), style=STYLE, timing=TIMING, stages=STAGES,
                typing_sound=TYPING_SOUND,
                fonts=dict(code=style.CODE_FONT_PATH, ui=style.UI_FONT_PATH),
                execution=LESSON.get('execution', {'mode':'local'}))
manifest_path = video.with_suffix('.manifest.json')
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(dict(video=str(video), manifest=str(manifest_path), duration=TOTAL_SECONDS, verification=verification), ensure_ascii=True, indent=2))
