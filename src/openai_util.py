# openai_util.py

import openai 
import os
import shutil

openai.api_key = os.getenv("OPENAI_API_KEY") 

def transcribe_audio(audio_file):
  with open(audio_file, "rb") as audio_file:
    response = openai.Audio.transcribe(
      file=audio_file, 
      model="whisper-1", 
      response_format="text"
  )
  return response

def correct_transcription(transcription):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    temperature=0.5, 
    messages=[
      {"role": "system", "content": f"Correct this transcription, return in markdown format with line breaks. At the end, generate 10 relevant tags with a # prefix for storing in notetaking app."},
      {"role": "user", "content": transcription}
    ]
  )
  return response['choices'][0]['message']['content']

def move_file(src, filetype):
    if filetype == 'mp4':
        dst = '../media/video/'
    elif filetype == 'mp3':
        dst = '../media/audio/'
    elif filetype == 'md':
        dst = '../media/text/'
    else:
        print(f"Unsupported file type: {filetype}")
        return

    shutil.move(src, dst)