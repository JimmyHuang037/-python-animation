from pathlib import Path
import argparse,subprocess,json
root=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser();parser.add_argument('video',nargs='?',type=Path,default=root/'outputs/vehicle-list-150s-v2.mp4');args=parser.parse_args()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(args.video)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['avg_frame_rate'],v['nb_read_frames'])==(1920,1080,'30/1','4500');assert abs(float(v['duration'])-150)<.04;assert a['sample_rate']=='48000'
subprocess.run(['ffmpeg','-v','error','-i',str(args.video),'-f','null','-'],check=True)
print(json.dumps({'video':str(args.video),'duration':150,'frames':4500,'size':[1920,1080],'fps':30,'full_decode':'passed','subjective_playback':'unverified'},ensure_ascii=False))
