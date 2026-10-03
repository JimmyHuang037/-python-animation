from pathlib import Path
import subprocess,argparse
root=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=root/'outputs/vehicle-list-150s-v2.mp4');parser.add_argument('--frames',type=Path,default=root/'intermediate/full-v2-frames');args=parser.parse_args()
args.output.parent.mkdir(parents=True,exist_ok=True)
if args.output.exists():raise SystemExit('Output exists: choose a new --output path; existing video preserved')
subprocess.run(['ffmpeg','-v','error','-n','-framerate','30','-i',str(args.frames/'%06d.png'),'-i',str(root/'audio/full-v1/mix.wav'),'-t','150','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-af','loudnorm=I=-17:TP=-2:LRA=7','-movflags','+faststart',str(args.output)],check=True)
print(args.output)
