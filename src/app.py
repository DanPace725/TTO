# app.py

import streamlit as st
from video_util import save_uploaded_file
from openai_util import move_file
from audio_util import convert_to_audio
from openai_util import transcribe_audio 
import openai
import os

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

def correct_transcription(transcription):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    temperature=0, 
    messages=[
      {"role": "system", "content": f"orrect this transcription, return in markdown format with line breaks. At the end, generate 10 relevant tags with a # prefix for storing in notetaking app."},
      {"role": "user", "content": transcription}
    ]
  )
  return response['choices'][0]['message']['content']

st.title("Video to Audio Transcription")

obsidian_vault_path = st.sidebar.text_input("Enter the path to your Obsidian vault:")

uploaded_file = st.file_uploader("Upload video")

if uploaded_file is not None:
    video_filename = save_uploaded_file(uploaded_file)

    if st.button("Transcribe"):
        if video_filename:
            with st.spinner("Transcribing..."):
                transcription = transcribe_video(video_filename)

            if transcription:
                with st.spinner("Correcting Transcription..."):
                    corrected_trans = correct_transcription(transcription)

                st.subheader("Transcription:")
                st.write(corrected_trans)
                clean_video_filename = video_filename.replace(".mp4", "")
                with open(clean_video_filename + "_transcript.md", "w") as f:
                    f.write(corrected_trans)

                st.download_button(
                    label="Download Transcript",
                    data=corrected_trans,
                    file_name=clean_video_filename + "_transcript.md",
                    mime="text/markdown",
                )

                move_file(video_filename + "_transcript.md", 'md')
                move_file(video_filename + "_audio.mp3", 'mp3')
                move_file(video_filename , 'mp4')
            else:
                st.error("Failed to transcribe audio")

    
    elif st.button("Quick Save to Obsidian"):
            if video_filename:
                with st.spinner("Transcribing..."):
                    transcription = transcribe_video(video_filename)

                if transcription:
                    with st.spinner("Correcting Transcription..."):
                        corrected_trans = correct_transcription(transcription)

                    clean_filename = os.path.basename(video_filename)
                    transcript_path = os.path.join(obsidian_vault_path, clean_filename + "_transcript.md")
                    with open(transcript_path, "w") as f:
                        f.write(corrected_trans)

                    st.success(f"Transcript saved to {transcript_path}")
                else:
                    st.error("Failed to transcribe audio")
            else:
                st.error("Failed to save video.")