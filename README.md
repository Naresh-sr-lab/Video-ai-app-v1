# 🎥 Interactive AI Video Assistant

This app allows you to:
- Upload a video or paste a YouTube link
- Transcribe its audio using OpenAI Whisper
- Generate a summary with GPT-4
- Ask questions based on the transcript

## 💻 How to Use

1. Upload an MP4 file OR paste a YouTube link.
2. The app will:
   - Extract and transcribe audio
   - Summarize it
   - Let you ask questions

## 🚀 Deployment

To deploy this on Streamlit Cloud:

1. Push the following files to a GitHub repo:
   - `app.py`
   - `requirements.txt`
   - `README.md`

2. Go to [Streamlit Cloud](https://streamlit.io/cloud), sign in, and choose:
   - **Deploy an app from GitHub**
   - Connect your repo and select `app.py` as the entry point.

3. Done! Your app is live.

## 🧪 Example Questions

- What are the main takeaways?
- What was discussed at 3 minutes?
- What did the speaker say about AI?

---

**Note:** Ensure your OpenAI API key is set via Streamlit Secrets or environment variables.
