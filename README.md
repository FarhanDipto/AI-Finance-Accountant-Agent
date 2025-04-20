# 🧠 AI Finance Accountant Agent

> Voice-powered assistant for personal finance insight with sleek UI — powered by RAG-style retrieval & local embeddings.

---

## 🚀 Overview

The AI Finance Accountant Agent is a smart voice-enabled assistant with a clean, minimal UI that lets users:

- 📊 Track income and expenses  
- 🧾 Summarize financial invoices  
- 🧠 Ask questions like "What's my highest income in April?"  
- 🗣️ Interact through **natural voice commands** or direct text input  
- 💻 Enjoy a clutter-free, intuitive user interface  

Designed to run locally using lightweight models — no cloud or API keys required!  

---

## 🧰 Tech Stack

- **Python 3** — Core language  
- **Streamlit** — For the clean, responsive user interface  
- **pandas** — For loading, cleaning, and analyzing invoice data  
- **regex** — To extract structured info from text  
- **dateutil** — For parsing flexible date formats  
- **Speech Recognition**:  
  - `speech_recognition` — For audio input processing  
- **Text-to-Speech**:  
  - `gTTS` — For generating natural voice responses  
- **colorama**, **tqdm** — Terminal styling and progress indicators (optional)  

---

## 🛠️ Features

✅ Clean, minimal Streamlit user interface  
✅ Voice command recording and processing  
✅ Direct text query input option  
✅ Audio file upload capability  
✅ Automatic speech response playback  
✅ Intelligent intent parsing  
✅ Structured financial data processing  
✅ Custom lightweight RAG retrieval using sentence-transformers  
✅ No external API calls – fully offline-capable  
✅ Income, expense, and balance summaries  
✅ Monthly breakdowns  
✅ Natural sounding responses  

---

## 📂 Folder Structure

```bash
ai-finance-accountant-agent/
│
├── main.py                      # Entry point
├── gui.py                       # Streamlit UI interface
├── modules/
│   ├── intent_parser.py         # Detects user intent
│   ├── voice_input.py           # Whisper-based voice capture
│   ├── rag_engine.py            # Core retrieval & analysis engine
│   └── speech_output.py         # Text-to-speech output (optional)
│
├── data/
│   ├── financial_statements.txt # Invoice + income entries
│   └── rag_cache.pkl            # Cached embeddings for performance
│
├── README.md
└── Documentation & Usage Guide.pdf



