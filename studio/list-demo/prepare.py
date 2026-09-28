"""Prepare checked Python source and Yunxi narration; no synthetic execution output."""
import asyncio,json,subprocess,wave
from pathlib import Path
import edge_tts
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'build/list-demo'
CODE=(Path(__file__).resolve().parent/'shopping.py').read_text().splitlines()
TEXT=['用五行代码，创建一个购物列表。','第一行，用一对空的方括号，创建购物列表。','接着，用 append，把键盘添加到列表末尾。','再添加一个键帽。现在，列表里有两个商品。','如果不买键帽了，就用 remove，把它从列表中删除。','最后，用 print，打印这个购物列表。','运行代码。输出里只剩下键盘，因为键帽已经被删除了。']
async def main():
 OUT.mkdir(parents=True,exist_ok=True)
 source='\n'.join(CODE)+'\n';(OUT/'expected.py').write_text(source)
 result=subprocess.run(['python3',str(OUT/'expected.py')],capture_output=True,text=True,check=True)
 assert result.stdout=="['键盘']\n"
 (OUT/'source-check.json').write_text(json.dumps({'source':source,'stdout':result.stdout,'returncode':result.returncode},ensure_ascii=False,indent=2))
 segments=[]
 for i,text in enumerate(TEXT):
  mp3=OUT/f'voice-{i:02}.mp3';wav=OUT/f'voice-{i:02}.wav'
  if not mp3.exists() or mp3.stat().st_size==0:
   for attempt in range(4):
    try:
     await edge_tts.Communicate(text,'zh-CN-YunxiNeural',rate='+0%').save(str(mp3));break
    except edge_tts.exceptions.NoAudioReceived:
     if attempt==3:raise
     await asyncio.sleep(2)
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(mp3),'-ar','48000','-ac','1',str(wav)],check=True)
  with wave.open(str(wav)) as f:duration=f.getnframes()/f.getframerate()
  segments.append({'index':i,'text':text,'duration':duration,'wav':str(wav),'code':CODE[i-1] if 1<=i<=5 else None})
  print(i,round(duration,2),text,flush=True)
 (OUT/'segments.json').write_text(json.dumps(segments,ensure_ascii=False,indent=2))
asyncio.run(main())
