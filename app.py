import os
import openai
from tempfile import NamedTemporaryFile

import streamlit as st
from pytube import YouTube

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

st.set_page_config(page_title="Interactive AI Video Assistant", layout="wide")
st.title("🎥 Interactive AI Video Assistant")

# Select video source
source = st.radio("Select video input method:", ["Upload MP4", "YouTube Link"])

video_bytes = None
video_file = None

def download_youtube_audio(youtube_url):
    try:
        yt = YouTube(youtube_url)
        stream = yt.streams.filter(only_audio=True).first()
        buffer = NamedTemporaryFile(delete=False, suffix=".mp4")
        stream.stream_to_buffer(buffer)
        buffer.seek(0)
