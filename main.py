import os
import sys
import os
import re
import time
import zipfile
import urllib.error
from send_mail import send_mail
os.environ["IMAGEIO_FFMPEG_EXE"] = "ffmpeg"
from youtube_search import YoutubeSearch
from pytube import YouTube, Search, exceptions
from moviepy.editor import VideoFileClip, concatenate_audioclips
import streamlit as st

def download_video(singer, n): 
    count = 0
    query = singer + ' music video'
    results = YoutubeSearch(query, max_results = n + 20).to_dict()
    for v in results:
        try:
            yt = YouTube('https://youtube.com/' + v['url_suffix'])
            video = yt.streams.filter(file_extension='mp4').first()
            destination = 'Video Files'
            out_file = video.download(output_path=destination)
        except (exceptions.VideoUnavailable, urllib.error.HTTPError):
            pass
        else:
            count += 1
            if count == n:
                break
            basePath, extension = os.path.splitext(out_file)
    st.info('Downloaded Videos')

               
def convert_video_to_audio(output_ext="mp3"):
    directory = "Video Files/"
    clips = []
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            file_path = os.path.join(directory, filename)
            clip = VideoFileClip(file_path)
            audioclip=clip.audio
            basePath, extension = os.path.splitext(filename)
            # audioclip.write_audiofile(f"{basePath}.{output_ext}")
            clips.append(audioclip)
    st.info('Converted Videos to Audios')
    return clips

def trimAudioClips(clips, y) :
    subclips = []
    for clip in clips :
        subclip = clip.subclip(10, 10 + y)
        subclips.append(subclip)
    st.info('Trimmed Audios')
    return subclips

def mashup(clips, output = 'mashup') :
    concat = concatenate_audioclips(clips)
    concat.write_audiofile(f"{output}.mp3")
    st.success('Created Mashup')

def createZip(file):
    destination='mashup.zip'
    zip_file=zipfile.ZipFile(destination,'w')
    zip_file.write(file,compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()
    return destination

def script(singer, count, duration, mail, output = 'mashup'):
    download_video(singer, count)
    clips = convert_video_to_audio()
    subclips = trimAudioClips(clips, duration)
    mashup(subclips, output)
    send_mail(mail, createZip('mashup.mp3'))
    st.info('Mail Sent!')
    

st.title('MixItUp')
st.subheader('by Mayank Rawat')



with st.form("my_form"):
    singer = st.text_input('Name of Artist')
    count = st.slider('Number of Videos', 5, 40)
    duration = st.slider('Duration of Each Video (in seconds)', 20, 60)
    mail = st.text_input('Email Id')
    submitted = st.form_submit_button("Generate")
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if submitted:
        if not singer.strip():
            st.error('Please enter the name of Artist')
        elif not re.match(pattern,mail):
            st.error('Invalid email! Please try again.')
        else :
            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            st.success('Voila! Your mashup will arrive shortly in your mailbox')
            folder = 'Video Files'
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)  
                    if os.path.isfile(file_path) or os.path.islink(file_path): 
                        os.unlink(file_path)
                        
            if os.path.exists('mashup.mp3'):
                os.unlink('mashup.mp3')
            
            if os.path.exists('mashup.zip'):
                os.unlink('mashup.zip')
                
            script(singer, count, duration, mail)
            
