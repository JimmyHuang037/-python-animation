import asyncio,json,edge_tts,subprocess
from pathlib import Path
async def main():
 p=Path(__file__).resolve().parent.parent/'audio/full-v1';cues=json.loads((p/'cues.json').read_text())
 for c in cues:
  dest=p/c['file']
  if c.get('source_duration') and dest.exists() and dest.stat().st_size>1000:continue
  for rate in ['+10%','+20%','+30%']:
   for attempt in range(3):
    try:
     await edge_tts.Communicate(c['text'],'zh-CN-YunxiNeural',rate=rate).save(str(dest));break
    except Exception as e:
     print('TTS retry',c['file'],type(e).__name__,flush=True)
     if attempt==2:raise
     await asyncio.sleep(2)
   raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(dest),'-af','silenceremove=start_periods=1:start_duration=0.03:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_duration=0.03:start_threshold=-45dB,areverse','-f','f32le','-ar','48000','-ac','1','-']);sec=len(raw)/4/48000
   if sec<=c['end']-c['start']:
    c['tts_rate']=rate;c['source_duration']=sec;break
  else: print('BUDGET_FAILURE',c['file'],sec,flush=True);c['over_budget']=True
  print(c['file'],rate,round(sec,2),flush=True);(p/'cues.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
 (p/'cues.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
asyncio.run(main())
