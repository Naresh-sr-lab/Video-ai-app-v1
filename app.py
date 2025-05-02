import os
import openai
from tempfile import NamedTemporaryFile

import streamlit as st
from pytube import YouTube

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

st.set_page_config(page_title="Interactive AI Video Assistant", layout="wide")
st.title("🎥 Interactive AI Video Assistant")

# Choose video source
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
        return buffer.read(), yt.title
    except Exception as e:
        st.error(f"Error downloading or transcribing YouTube video: {e}")
        return None, None

def transcribe_audio_openai(video_bytes):
    with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_audio:
        temp_audio.write(video_bytes)
        temp_audio_path = temp_audio.name

    with open(temp_audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    os.remove(temp_audio_path)
    return transcript['text']

# Handle video upload or YouTube URL input
if source == "Upload MP4":
    video_file = st.file_uploader("Upload a video file (MP4 only)", type=["mp4"])
    if video_file:
        video_bytes = video_file.read()
        st.video(video_file)

elif source == "YouTube Link":
    youtube_url = st.text_input("Paste YouTube video link")
    if youtube_url:
        with st.spinner("Downloading from YouTube..."):
            video_bytes, yt_title = download_youtube_audio(youtube_url)
            if video_bytes:
                st.success(f"Downloaded: {yt_title}")
                st.audio(video_bytes)

# Proceed with transcription if video bytes are available
if video_bytes:
    st.info("Transcribing audio with Whisper... This may take a while.")
    try:
        transcript = transcribe_audio_openai(video_bytes)
        st.success("Transcription complete!")
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        transcript = ""

    if transcript:
        st.subheader("📄 Transcript")
        st.write(transcript)

        # Generate summary
        st.subheader("📝 Summary")
        with st.spinner("Generating summary with GPT..."):
            prompt = (
                "Summarize the following transcript into key discussion points (5–8 bullets):\n"
                + transcript
            )
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                )
                summary = response.choices[0].message.content
                st.success("Summary ready!")
                st.markdown(summary)
            except Exception as e:
                st.error(f"Summary generation failed: {e}")

        # Ask a question
        st.subheader("❓ Ask a question about the video")
        user_question = st.text_input("What would you like to ask?")
        if user_question:
            with st.spinner("Thinking..."):
                qa_prompt = (
                    "Answer the question based on the transcript below.\n"
                    f"Transcript: {transcript}\n"
                    f"Question: {user_question}"
                )
                try:
                    qa_response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": qa_prompt}],
                        temperature=0.3,
                    )
                    answer = qa_response.choices[0].message.content
                    st.markdown(f"**Answer:** {answer}")
                except Exception as e:
                    st.error(f"Answer generation failed: {e}")
else:
    st.warning("Please upload a video file or enter a valid YouTube link.")
