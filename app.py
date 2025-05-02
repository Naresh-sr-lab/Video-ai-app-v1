import os
import openai
from tempfile import NamedTemporaryFile
import streamlit as st
from pytube import YouTube  # Import pytube for YouTube video download

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

st.set_page_config(page_title="Interactive AI Video Assistant", layout="wide")
st.title("🎥 Interactive AI Video Assistant")

# Option to input YouTube URL or upload video file
video_option = st.radio("Choose an option", ["Upload a video file", "Provide a YouTube link"])

if video_option == "Upload a video file":
    video_file = st.file_uploader("Upload a video file (MP4 only)", type=["mp4"])
    video_url = None
elif video_option == "Provide a YouTube link":
    video_url = st.text_input("Enter YouTube video URL")
    video_file = None

def transcribe_audio_openai(video_bytes):
    with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_audio:
        temp_audio.write(video_bytes)
        temp_audio_path = temp_audio.name

    with open(temp_audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    os.remove(temp_audio_path)
    return transcript['text']

# Handle video based on user choice
if video_file:
    video_bytes = video_file.read()
    with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_bytes)
        temp_video_path = temp_video.name

    st.video(temp_video_path)

    # Transcribe using OpenAI Whisper API
    st.info("Transcribing video... This may take a while.")
    try:
        transcript = transcribe_audio_openai(video_bytes)
        st.success("Transcription complete!")
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        transcript = ""

    if transcript:
        st.subheader("📄 Transcript")
        st.write(transcript)

elif video_url:
    st.info("Downloading video... Please wait.")
    try:
        # Download YouTube video
        yt = YouTube(video_url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_file_path = video_stream.download(output_path="temp_video.mp4")

        # Transcribe downloaded video
        with open(video_file_path, "rb") as video_file:
            transcript = transcribe_audio_openai(video_file.read())
        st.success("Transcription complete!")
        st.video(video_file_path)

        # Display transcript
        st.subheader("📄 Transcript")
        st.write(transcript)
    except Exception as e:
        st.error(f"Error downloading or transcribing YouTube video: {e}")
else:
    st.warning("Please upload a video file or provide a YouTube URL.")
