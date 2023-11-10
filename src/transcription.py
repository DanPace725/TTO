# transcription.py
import os
from audio_util import convert_to_audio
from openai_util import transcribe_audio 
from openai_util import correct_transcription

def transcribe_video(video_filename):
  if video_filename is None:
    print("Failed to download video")
    return None
  audio_filename = f"{video_filename}_audio.mp3"
  
  success = convert_to_audio(video_filename, audio_filename)
  
  if not success:
    return None

  transcription = transcribe_audio(audio_filename)
  

  
  return transcription

