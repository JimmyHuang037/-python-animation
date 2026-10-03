import json,subprocess,wave
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parent.parent;a=p/'audio/full-v1';rate=48000;n=150*rate
voice=np.zeros(n);music=np.zeros(n);sfx=np.zeros(n);records=[]
for c in json.loads((a/'cues.json').read_text()):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(a/c['file']),'-af','silenceremove=start_periods=1:start_duration=0.03:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_duration=0.03:start_threshold=-45dB,areverse','-f','f32le','-ar',str(rate),'-ac','1','-'])
 signal=np.frombuffer(data,dtype=np.float32);duration=len(signal)/rate;budget=c['end']-c['start']
 if duration>budget:raise Exception('Narration exceeds slot: '+c['file']+' '+str(duration))
 start=round(c['start']*rate);voice[start:start+len(signal)]+=signal*.82;records.append(dict(**c,speech_end=c['start']+duration,trimmed_duration=duration,time_compression=1))
# Original warm plucked instrumental at96BPM; rests preserve the speech foreground.
notes=[130.81,0,196,164.81,146.83,0,220,174.61]
for k in range(240):
 start=round(k*.625*rate);freq=notes[k%8];m=min(round(.9*rate),n-start)
 if not freq:continue
 t=np.arange(m)/rate;env=np.minimum(t/.01,1)*np.exp(-t*5);music[start:start+m]+=.010*env*(np.sin(2*np.pi*freq*t)+.27*np.sin(2*np.pi*freq*3*t))
 if k%4==0:music[start:start+m]+=.0035*np.exp(-t*3)*np.sin(2*np.pi*(freq/2)*t)
# Event frames are rounded on the same30fps export clock, not on approximate text lengths.
events=[(54, 'car-contact'), (60, 'car-contact'), (360, 'chapter-change'), (570, 'door-open'), (624, 'car-contact'), (690, 'door-open'), (744, 'car-contact'), (810, 'door-open'), (864, 'car-contact'), (1140, 'chapter-change'), (1272, 'door-open'), (1320, 'door-open'), (1323, 'car-contact'), (1371, 'car-contact'), (1404, 'door-open'), (1449, 'door-open'), (1455, 'car-contact'), (1500, 'car-contact'), (1800, 'chapter-change'), (1890, 'door-open'), (1944, 'car-contact'), (2070, 'chapter-change'), (2211, 'door-open'), (2316, 'car-contact'), (2550, 'chapter-change'), (2805, 'door-open'), (2859, 'car-contact'), (2925, 'door-open'), (2988, 'car-contact'), (3360, 'chapter-change'), (3666, 'door-open'), (3720, 'car-contact'), (3828, 'car-contact'), (4200, 'chapter-change')]
for frame,kind in events:
 start=round(frame/30*rate);m=round(.22*rate);t=np.arange(m)/rate;rng=np.random.default_rng(frame)
 if 'contact' in kind:signal=.045*np.exp(-t*30)*np.sin(2*np.pi*185*t)+.01*rng.normal(size=m)*np.exp(-t*45)
 else:signal=.010*rng.normal(size=m)*np.sin(np.pi*np.minimum(t/.2,1))*np.exp(-t*15)+.015*np.exp(-t*35)*np.sin(2*np.pi*440*t)
 sfx[start:start+m]+=signal
for begin,end in [(19.3,20.8),(23.3,24.8),(27.3,28.8),(42.7,44.1),(44.3,45.7),(47.1,48.5),(48.6,50),(63.3,64.8),(73.8,77.2),(93.5,95.3),(97.8,99.6),(122.2,124),(125.6,127.6)]:
 start=round(begin*rate);m=round((end-begin)*rate);t=np.arange(m)/m;rng=np.random.default_rng(start);sfx[start:start+m]+=.0012*rng.normal(size=m)*np.sin(np.pi*t)**2
activity=np.convolve((np.abs(voice[::480])>.005).astype(float),np.ones(25)/25,'same');duck=1-.7*np.repeat(activity,480)[:n];music*=duck
fade=np.minimum(np.arange(n)/rate/.2,1)*np.minimum((n-1-np.arange(n))/rate/.35,1);music*=fade
mix=voice+music+sfx
for name,signal in [('narration',voice),('music',music),('events',sfx),('mix',mix)]:
 with wave.open(str(a/(name+'.wav')),'w') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes((np.clip(signal,-1,1)*32767).astype('<i2').tobytes())
def stamp(seconds):
 ms=round(seconds*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
nl=chr(10);cues=json.loads((a/'cues.json').read_text());(p/'subtitles/full-v1.srt').write_text((nl*2).join(f"{i+1}{nl}{stamp(c['start'])} --> {stamp(c['end'])}{nl}{c['text']}" for i,c in enumerate(cues))+nl)
(p/'reviews/full-v1-audio-timing.json').write_text(json.dumps({'cues':records,'bpm':96,'sfx_events':[{'frame':f,'sample_time':f/30,'kind':k} for f,k in events],'peak':float(np.max(np.abs(mix))),'subjective_audition':'unverified; model audio input unavailable'},ensure_ascii=False,indent=2))
print(json.dumps(records,ensure_ascii=False));print('Mix peak',np.max(np.abs(mix)))
