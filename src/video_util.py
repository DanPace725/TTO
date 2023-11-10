# src/video_util.py 


import regex as re
import os

def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('uploads', uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return os.path.join('uploads', uploaded_file.name)
    except Exception as e:
        print(e)
        return None

""" def download_video(url):
  "Download video from URL using pyktok"
  
  try:
    save_tiktok(url, True, "../metadata/data.csv", "chrome")
    regex_url = re.findall(r'https://www.tiktok.com/(.*?)\?', url)[0]
    saved_filename = regex_url.replace('/','_') + '.mp4'
    return saved_filename 
  except Exception as e:
    error_string = (f"Failed to download video: {e}")
    return error_string """