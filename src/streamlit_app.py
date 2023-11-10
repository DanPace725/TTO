# streamlit_app.py

import streamlit as st
import openai
import os
import subprocess
import shutil

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY") 

# Function from video_util.py
def save_uploaded_file(uploaded_file):
    try:
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        with open(os.path.join('uploads', uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return os.path.join('uploads', uploaded_file.name)
    except Exception as e:
        print(e)
        return None

# Function from audio_util.py
def convert_to_audio(video_file, audio_file):
    cmd = [
        'ffmpeg', '-i', video_file,  
        '-q:a', '0', 
        '-map', 'a', audio_file
    ]
  
    process = subprocess.run(cmd)
    return process.returncode == 0

# Function from openai_util.py
def transcribe_audio(audio_file):
    with open(audio_file, "rb") as audio_file:
        response = openai.Audio.transcribe(
            file=audio_file, 
            model="whisper-1", 
            response_format="text"
        )
    return response

# Function from openai_util.py
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




# Main app code
def main():
    st.title("Video to Audio Transcription")

    obsidian_vault_path = st.sidebar.text_input("Enter the path to your Obsidian vault:")

    uploaded_file = st.file_uploader("Upload video")

    if uploaded_file is not None:
        video_filename = save_uploaded_file(uploaded_file)

        if st.button("Transcribe"):
            if video_filename:
                with st.spinner("Transcribing..."):
                    audio_filename = f"{video_filename}_audio.mp3"
                    success = convert_to_audio(video_filename, audio_filename)

                    if success:
                        transcription = transcribe_audio(audio_filename)

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

                        else:
                            st.error("Failed to transcribe audio")
                    else:
                        st.error("Failed to convert video to audio")
            else:
                st.error("Failed to save video.")

        elif st.button("Quick Save to Obsidian"):
            if video_filename:
                with st.spinner("Transcribing..."):
                    audio_filename = f"{video_filename}_audio.mp3"
                    success = convert_to_audio(video_filename, audio_filename)

                    if success:
                        transcription = transcribe_audio(audio_filename)

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
                        st.error("Failed to convert video to audio")
            else:
                st.error("Failed to save video.")

if __name__ == "__main__":
    main()
