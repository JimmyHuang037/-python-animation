"""Trim calibration slate, align narration to recorded actions, burn readable captions."""
import json,subprocess,wave,hashlib,os
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(os.environ.get('DEMO_OUTPUT_DIR',ROOT/'build/list-demo')).resolve()
def run(*args):return subprocess.run(args,check=True,capture_output=True)
def stamp(t):
 cs=round(t*100);return f'{cs//360000:01}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
def srt(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
data=json.loads((OUT/'events.json').read_text());duration=data['duration']
probe=json.loads(run('ffprobe','-v','error','-show_streams','-of','json',str(OUT/'recording.webm')).stdout)
fps=float(Fraction(probe['streams'][0]['avg_frame_rate']))
pixels=run('ffmpeg','-v','error','-i',str(OUT/'recording.webm'),'-vf','crop=4:4:0:0,scale=1:1','-pix_fmt','rgb24','-f','rawvideo','-').stdout
slate=[i//3 for i in range(0,len(pixels),3) if pixels[i]<40 and pixels[i+1]>210 and pixels[i+2]<40]
assert slate,'No calibration slate';trim=(slate[-1]+1)/fps
sr=48000;track=bytearray(round(duration*sr)*2)
ass='''[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Caption,Noto Sans CJK SC,34,&H00FFFFFF,&H00FFFFFF,&H00191919,&H00191919,0,0,0,0,100,100,0,0,1,0,0,2,40,40,54,1\nStyle: Label,Noto Sans CJK SC,19,&H0092A49F,&H00FFFFFF,&H00191919,&H00191919,0,0,0,0,100,100,0,0,1,0,0,2,40,40,17,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
ass+=f'Dialogue: 0,0:00:00.00,{stamp(duration)},Label,,0,0,0,,AI 自动输入 · Python 真实运行\n'
subs=[]
for i,e in enumerate(data['events'],1):
 start=e['start'];end=min(duration,start+e['duration'])
 if start>=duration:continue
 with wave.open(str(OUT/Path(e['wav']).name)) as f:frames=f.readframes(f.getnframes())
 offset=round(start*sr)*2;frames=frames[:max(0,len(track)-offset)];track[offset:offset+len(frames)]=frames
 ass+=f"Dialogue: 1,{stamp(start)},{stamp(end)},Caption,,0,0,0,,{e['text']}\n"
 subs.append(f"{i}\n{srt(start)} --> {srt(end)}\n{e['text']}\n")
with wave.open(str(OUT/'narration.wav'),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(track)
(OUT/'captions.ass').write_text(ass);(OUT/'captions.srt').write_text('\n'.join(subs))
video=OUT/'shopping-list-yunxi.mp4'
run('ffmpeg','-v','error','-y','-ss',str(trim),'-i',str(OUT/'recording.webm'),'-i',str(OUT/'narration.wav'),'-vf',f"pad=1920:1080:0:0:color=0x171c22,ass={OUT/'captions.ass'},fps=30",'-af','loudnorm=I=-18:TP=-2:LRA=7,aresample=48000','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(duration),'-movflags','+faststart',str(video))
run('ffmpeg','-v','error','-i',str(video),'-f','null','-')
final=json.loads(run('ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)).stdout)
preview=data.get('preview',False)
source=(OUT/'workspace/shopping.py').read_bytes()
if preview:assert (OUT/'expected.py').read_bytes().startswith(source.rstrip()),'Recorded preview differs from expected source prefix'
execution=run('python3',str(OUT/('expected.py' if preview else 'workspace/shopping.py')))
assert execution.stdout.decode()=="['键盘']\n"
check={'preview':preview,'source_sha256':hashlib.sha256(source).hexdigest(),'real_recorded_output':(OUT/'workspace/result.txt').read_text() if (OUT/'workspace/result.txt').exists() else None,'independent_execution_source':'expected.py' if preview else 'workspace/shopping.py','independent_execution_stdout':execution.stdout.decode(),'independent_execution_exit_code':execution.returncode,'slate_trim_seconds':trim,'recording_fps':fps,'duration':float(final['format']['duration']),'width':final['streams'][0]['width'],'height':final['streams'][0]['height'],'decode_ok':True,'voice':'zh-CN-YunxiNeural','audio_method':'Reuse existing edge-tts 7.2.8 environment and voice; generate lesson-specific narration','continuous_human_review':False}
(OUT/'verification.json').write_text(json.dumps(check,ensure_ascii=False,indent=2));print(json.dumps(check,ensure_ascii=False,indent=2))
