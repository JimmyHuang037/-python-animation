"""Generate an original quiet instrumental bed. No sampled or third-party audio."""
from pathlib import Path
import numpy as np
import wave
sr=48000
duration=30
out=np.zeros((sr*duration,2),dtype=np.float64)
def tone(start,length,midi,volume,pan=0):
    start=int(start*sr); length=min(int(length*sr),len(out)-start)
    t=np.arange(length)/sr
    freq=440*2**((midi-69)/12)
    env=(1-np.exp(-t*32))*np.exp(-t*2.8)*np.minimum(1,(length/sr-t)/.15)
    wave=(np.sin(2*np.pi*freq*t)+.18*np.sin(2*np.pi*freq*2*t))*env*volume
    out[start:start+length,0]+=wave*(1-pan*.3)
    out[start:start+length,1]+=wave*(1+pan*.3)
chords=[[60,64,67,74],[57,60,64,71],[53,57,60,67],[55,59,62,69]]
for beat in range(50):
    c=chords[(beat//8)%4]
    tone(beat*.6,1.3,c[beat%4]+12,.055,(-1)**beat)
    if beat%4==0:tone(beat*.6,2,c[0]-12,.11)
for start in [5,6,10,19,25]:
    for j,n in enumerate([72,76,79]):tone(start+j*.07,.7,n,.035,j-1)
t=np.arange(len(out))/sr
out*=np.minimum(1,t/.7)[:,None]*np.minimum(1,(30-t)/1.4)[:,None]
peak=np.max(np.abs(out)); out*=.25/max(peak,1e-9)
p=Path(__file__).resolve().parents[2]/'build/promo30/music-original.wav'
with wave.open(str(p),'wb') as f:
    f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((out*32767).astype('<i2').tobytes())
print(p)
