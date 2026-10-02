"""Decode a rendered lesson and validate timing, caret, output and mouse fade."""
import argparse
import bisect
import hashlib
import json
import os
import subprocess
import sys
import wave
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--manifest', type=Path, required=True)
parser.add_argument('--runtime-dir', type=Path)
parser.add_argument('--compare-audio', type=Path)
args = parser.parse_args()
if args.runtime_dir:
    sys.path.insert(0, str(args.runtime_dir.resolve()))
manifest = json.loads(args.manifest.read_text(encoding='utf-8-sig'))
os.environ['IDE_VIDEO_CODE_FONT'] = manifest['fonts']['code']
os.environ['IDE_VIDEO_UI_FONT'] = manifest['fonts']['ui']
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import lesson_style as style
import run_click_effect as effect
style.configure(**manifest['style'])
video, work = Path(manifest['video']), Path(manifest['work'])
stages, fps = manifest['stages'], manifest['fps']
ff = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-v','error','-xerror','-i',str(video),'-f','null','-'], check=True)


def audio_hash(path):
    data = subprocess.run([ff,'-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','-'],
                          check=True, capture_output=True).stdout
    return hashlib.sha256(data).hexdigest()


if args.compare_audio:
    assert audio_hash(video) == audio_hash(args.compare_audio), 'Audio changed'
key_interval = round(manifest['timing']['character_seconds'] * fps)
after_typing = round(manifest['timing']['after_typing'] * fps)
selected, extra = {}, set()
fade_offsets = [round((effect.HOLD_SECONDS + fraction * effect.FADE_SECONDS) * fps)
                for fraction in (0, 1/3, 2/3, 1)]
for i, s in enumerate(stages):
    assert s['start_frame'] == (stages[i-1]['end_frame'] if i else 0)
    assert s['typing_start_frame'] == s['start_frame']
    assert s['typing_start_frame'] / fps == s['speech_start']
    assert s['speech_end'] <= s['end_frame'] / fps, 'Narration crosses a stage boundary'
    assert s['result_frame'] - s['typing_end_frame'] == after_typing
    assert all(b-a == key_interval for a,b in zip(s['event_frames'],s['event_frames'][1:]))
    assert s['events'][-1]['lines'] == Path(s['source']).read_text(encoding='utf-8-sig').rstrip('\r\n').split('\n')
    assert hashlib.sha256(Path(s['voice']).read_bytes()).hexdigest() == s['voice_sha256']
    with wave.open(s['voice']) as w:
        assert abs(w.getnframes()/w.getframerate() - s['voice_duration']) < 1e-6
    prior = s['initial']
    for event in s['events']:
        change = len('\n'.join(event['lines'])) - len('\n'.join(prior['lines']))
        assert change == (0 if event['key']=='move' else -1 if event['key']=='backspace' else 1)
        assert 0 <= event['col'] <= len(event['lines'][event['row']])
        prior = event
    click = effect.cursor_state(s['result_frame'],s['result_frame'],fps)
    l,t,r,b = style.RUN_BUTTON_RECT
    assert click['pressed'] and l < click['tip_x'] < r and t < click['tip_y'] < b
    for label,f in [('simultaneous-start',s['typing_start_frame']),
                    ('typing',(s['typing_start_frame']+s['typing_end_frame'])//2),
                    ('click',s['result_frame']),('gone',s['result_frame']+fade_offsets[-1])]:
        selected[f] = (i,label)
    extra.add(s['result_frame']-1)
    extra.update(s['result_frame']+delta for delta in fade_offsets)
reader = imageio_ffmpeg.read_frames(str(video),pix_fmt='rgb24')
metadata = next(reader)
assert tuple(metadata['size']) == (style.WIDTH,style.HEIGHT)
assert abs(metadata['fps']-fps) < .001
frames = {}
count = caret_count = key_count = 0
for f,data in enumerate(reader):
    count += 1
    s = max((s for s in stages if s['start_frame'] <= f),key=lambda s:s['start_frame'])
    typing = s['typing_start_frame'] <= f <= s['typing_end_frame']
    if typing or f in selected or f in extra:
        a = np.frombuffer(data,dtype=np.uint8).reshape((style.HEIGHT,style.WIDTH,3))
        if typing:
            pos = bisect.bisect_right(s['event_frames'],f)-1
            event = s['events'][pos]
            x,y = style.caret_position(event)
            pixels = a[y+3:y+style.CARET_HEIGHT-3,x+1:x+2].astype(np.int16)
            assert np.abs(pixels-np.array(style.CARET_COLOR)).mean() < 38, ('Caret',f,x,y)
            caret_count += 1
            key_count += f == s['event_frames'][pos]
        if f in selected or f in extra:
            frames[f] = a.copy()
reader.close()
assert count == manifest['frames'] == stages[-1]['end_frame']
assert key_count == sum(len(s['events']) for s in stages)


def plain_frame(i,f):
    s = stages[i]
    pos = bisect.bisect_right(s['event_frames'],f)-1
    state = s['initial'] if pos < 0 else s['events'][pos]
    typing = s['typing_start_frame'] <= f <= s['typing_end_frame']
    origin = s['typing_end_frame'] if pos >= 0 else s['start_frame']
    caret = typing or (f-origin)%fps < round(.6*fps)
    output_stage = i if f >= s['result_frame'] else i-1
    return style.render_frame(i,state,output_stage,caret,stages,frame=f)


fade_checks = []
for i,s in enumerate(stages):
    r = s['result_frame']
    energies = []
    cx,cy = effect.CLICK_TIP
    for delta in fade_offsets:
        f = r+delta
        base = plain_frame(i,f)
        expected = np.array(base).astype(np.int16)
        difference = np.abs(frames[f].astype(np.int16)-expected)
        energies.append(float(difference[cy+23:cy+72,cx-2:cx+60].mean()))
        if delta == fade_offsets[-1]:
            assert effect.cursor_state(f,r,fps) is None
            assert np.array_equal(np.array(effect.apply_run_click(base,f,r,fps)),expected)
            assert difference[130:360,1550:1850].mean() < 3, 'Mouse remains beyond encoding tolerance'
    assert all(a>b for a,b in zip(energies,energies[1:])), ('Fade',i,energies)
    assert energies[-1] < 3
    fade_checks.append(energies)
    l,t,rr,b = style.TERMINAL_BODY_RECT
    terminal = []
    for delta in (-1,0):
        f = r+delta
        expected = np.array(plain_frame(i,f))[t:b,l:rr].astype(np.int16)
        actual = frames[f][t:b,l:rr].astype(np.int16)
        assert np.abs(actual-expected).mean() < 3, ('Terminal output timing',i,f)
        terminal.append(actual)
    # Identical outputs can be legitimate; enforce visible change when outputs differ.
    if i==0 or s['output'] != stages[i-1]['output']:
        assert np.abs(terminal[1]-terminal[0]).mean() > .1
for f,(i,label) in selected.items():
    if label in ('simultaneous-start','typing'):
        expected = np.array(plain_frame(i,f))[220:650,180:1500].astype(np.int16)
        actual = frames[f][220:650,180:1500].astype(np.int16)
        assert np.abs(actual-expected).mean() < 3, ('Editor content',i,f)
with wave.open(str(work/'narration.wav')) as w:
    track = w.readframes(w.getnframes())
    assert abs(w.getnframes()/w.getframerate()-count/fps) < .001
with wave.open(str(work/'voice-only.wav')) as w:
    voice_only = w.readframes(w.getnframes())
    assert len(voice_only) == len(track)
with wave.open(str(work/'typing-clicks.wav')) as w:
    typing_clicks = w.readframes(w.getnframes())
    assert len(typing_clicks) == len(track)
    assert any(typing_clicks), 'Typing sound track is empty'
for s in stages:
    with wave.open(str(work/f'voice-{s["stage"]}-48k.wav')) as w:
        clip = w.readframes(w.getnframes())
    start = round(s['speech_start']*48000)*2
    assert start == round(s['typing_start_frame']/fps*48000)*2
    stage_end = round(s['end_frame']/fps*48000)*2
    assert start + len(clip) <= stage_end, 'Narration is truncated or overlaps the next stage'
    assert voice_only[start:start+len(clip)] == clip
    assert not any(voice_only[start+len(clip):stage_end]), 'Unexpected narration after stage'
contact = Image.new('RGB',(1920,294*len(stages)),'#101820')
draw = ImageDraw.Draw(contact)
label_font = ImageFont.truetype(manifest['fonts']['code'],18)
for j,(f,(i,label)) in enumerate(selected.items()):
    x,y = (j%4)*480,(j//4)*294
    contact.paste(Image.fromarray(frames[f]).resize((480,270)),(x,y+24))
    draw.text((x+8,y+2),f'Stage {i+1} | {label} | {f/fps:.2f}s',font=label_font,fill='white')
contact_path = video.with_suffix('.contact.jpg')
contact.save(contact_path,quality=95)
click_contact = Image.new('RGB',(1600,294*len(stages)),'#101820')
draw = ImageDraw.Draw(click_contact)
for i,s in enumerate(stages):
    for j,delta in enumerate(fade_offsets):
        f=s['result_frame']+delta
        x,y=j*400,i*294
        im=Image.fromarray(frames[f]).crop((1530,125,1860,345)).resize((396,264))
        click_contact.paste(im,(x,y+26))
        draw.text((x+8,y+2),f'Stage {i+1} | +{delta/fps:.2f}s',font=label_font,fill='white')
click_path = video.with_suffix('.clicks.jpg')
click_contact.save(click_path,quality=95)
Image.fromarray(frames[stages[-1]['result_frame']]).save(video.with_suffix('.preview.png'))
report = dict(video=str(video),duration_seconds=count/fps,frames=count,stages=len(stages),decode_ok=True,
              character_interval_seconds=key_interval/fps,post_typing_pause_seconds=after_typing/fps,
              caret_typing_frames_checked=caret_count,keystroke_positions_checked=key_count,
              clicks_inside_button=True,outputs_synchronized=True,all_mouse_fades_complete=True,
              fade_difference_by_stage=fade_checks,voice_samples_preserved=True,
              narration_and_typing_start_together=True,
              narration_typing_start_offsets_seconds=[s['typing_start_frame']/fps-s['speech_start'] for s in stages],
              typing_sound_enabled=manifest.get('typing_sound', {}).get('enabled', False),
              typing_sound_verified=True,
              audio_matches_comparison=True if args.compare_audio else None,
              contact_sheet=str(contact_path),click_sheet=str(click_path),sha256=hashlib.sha256(video.read_bytes()).hexdigest())
video.with_suffix('.validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))

