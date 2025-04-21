import gradio as gr
import os
from modules.intent_parser import parse_intent
from modules.finance_api import execute_action
from modules.rag_engine import get_rag_answer
import speech_recognition as sr
import tempfile
from gtts import gTTS
import pygame

def process_audio(audio_file):
    # Return early if no audio file is provided
    if audio_file is None:
        return "No audio input received.", None
    
    # Process the audio to text
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        query = recognizer.recognize_google(audio)
        return process_query(query)
    except Exception as e:
        error_msg = f"Error processing audio: {str(e)}"
        return error_msg, None

def process_query(query):
    try:
        intent_data = parse_intent(query)
        if intent_data["intent"] == "query_financial_docs":
            result = get_rag_answer(intent_data["query"])
        else:
            result = execute_action(intent_data)
        
        # Generate TTS audio
        tts = gTTS(text=result)
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts.save(temp_path)
        
        return result, temp_path
    except Exception as e:
        return f"Error processing query: {str(e)}", None

iface = gr.Interface(
    fn=process_audio,
    inputs=gr.Audio(sources=["microphone"], type="filepath"),  # Specify type="filepath"
    outputs=[
        gr.Text(label="Response"),
        gr.Audio(label="Audio Response", type="filepath")
    ],
    title="🎙️ AI Finance Accountant Agent",
    description="Ask finance questions like 'What is the highest invoice?' or 'Give me a summary for March'."
)

if __name__ == "__main__":
    iface.launch(share=True)