# audio_util.py 

import subprocess

def convert_to_audio(video_file, audio_file):
  cmd = [
    'ffmpeg', '-i', video_file,  
    '-q:a', '0', 
    '-map', 'a', audio_file
  ]
  
  process = subprocess.run(cmd)
  return process.returncode == 0