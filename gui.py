import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
from io import BytesIO
import base64
from modules.intent_parser import parse_intent
from modules.finance_api import execute_action
from modules.rag_engine import get_rag_answer

def autoplay_audio(audio_bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    html = f"""
        <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(html, unsafe_allow_html=True)

st.title("🤖 AI Finance Accountant Agent")
st.markdown("Your smart assistant for analyzing personal financial records using voice or text.")

st.markdown("""
#### 💡 Example Queries:
- "What is the highest income this year?"
- "Show me invoice #003"
- "What’s my net profit for June?"
- "Give me a summary of my expenses in March"
---
""")

for key in ["audio_recording", "audio_filename", "transcript", "response", "audio_response", "should_autoplay"]:
    if key not in st.session_state:
        st.session_state[key] = None if "filename" in key else False if "should_autoplay" in key else ""

def record_audio(duration=5):
    try:
        filename = tempfile.mktemp(suffix=".wav")
        with st.spinner(f"🎙️ Recording for {duration} seconds..."):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.write("🎤 Speak now...")
                audio = r.listen(source, timeout=duration, phrase_time_limit=duration)
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
        return filename
    except Exception as e:
        st.error(f"Error recording audio: {str(e)}")
        return None

def process_audio_file(file_path):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_data)

        intent_data = parse_intent(transcript)
        if intent_data["intent"] == "query_financial_docs":
            result = get_rag_answer(intent_data["query"])
        else:
            result = execute_action(intent_data)

        tts = gTTS(text=result)
        audio_bytes_io = BytesIO()
        tts.write_to_fp(audio_bytes_io)
        audio_bytes_io.seek(0)

        return transcript, result, audio_bytes_io.getvalue()
    except Exception as e:
        return None, f"Error processing audio: {str(e)}", None

st.markdown("### 🎧 Voice Input")
col1, col2 = st.columns(2)

with col1:
    if st.button("🎙️ Record (5 sec)"):
        audio_file = record_audio(5)
        if audio_file:
            st.session_state.audio_filename = audio_file
            st.success("✅ Recording completed!")

with col2:
    if st.button("🧠 Process Recording") and st.session_state.audio_filename:
        with st.spinner("Analyzing your voice input..."):
            transcript, response, audio_response = process_audio_file(st.session_state.audio_filename)
            if transcript:
                st.session_state.transcript = transcript
                st.session_state.response = response
                st.session_state.audio_response = audio_response
                st.session_state.should_autoplay = True
                try:
                    os.remove(st.session_state.audio_filename)
                except:
                    pass
                st.session_state.audio_filename = None
            else:
                st.error("❌ Failed to transcribe audio")

st.markdown("### 📄 Text Input")
text_query = st.text_input("Type your query here:")
if st.button("📩 Submit Text Query") and text_query:
    with st.spinner("Processing your question..."):
        try:
            intent_data = parse_intent(text_query)
            if intent_data["intent"] == "query_financial_docs":
                result = get_rag_answer(intent_data["query"])
            else:
                result = execute_action(intent_data)

            tts = gTTS(text=result)
            audio_bytes_io = BytesIO()
            tts.write_to_fp(audio_bytes_io)
            audio_bytes_io.seek(0)

            st.session_state.transcript = text_query
            st.session_state.response = result
            st.session_state.audio_response = audio_bytes_io.getvalue()
            st.session_state.should_autoplay = True
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

if st.session_state.transcript or st.session_state.response:
    st.markdown("### 🧾 Results")
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.transcript:
            st.markdown("#### 🗣️ You said:")
            st.write(st.session_state.transcript)

    with col2:
        if st.session_state.response:
            st.markdown("#### 💬 Response:")
            st.write(st.session_state.response)

    if st.session_state.audio_response:
        if st.session_state.should_autoplay:
            autoplay_audio(st.session_state.audio_response)
            st.session_state.should_autoplay = False
        else:
            st.audio(st.session_state.audio_response, format="audio/mp3")

st.markdown("---")
st.markdown("### 📂 Upload an Audio File")
uploaded_file = st.file_uploader("Upload a .wav file", type=['wav'])
if uploaded_file:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_file.write(uploaded_file.getvalue())
    temp_file.close()

    if st.button("📤 Process Uploaded File"):
        with st.spinner("Processing uploaded audio..."):
            transcript, response, audio_response = process_audio_file(temp_file.name)
            if transcript:
                st.session_state.transcript = transcript
                st.session_state.response = response
                st.session_state.audio_response = audio_response
                st.session_state.should_autoplay = True
                try:
                    os.remove(temp_file.name)
                except:
                    pass
            else:
                st.error("❌ Failed to process uploaded audio")

st.markdown("---")
st.markdown(
    "Built by [Farhan Dipto](https://github.com/FarhanDipto) · "
    "[View on GitHub](https://github.com/FarhanDipto/AI-Finance-Accountant-Agent)",
    unsafe_allow_html=True
)
