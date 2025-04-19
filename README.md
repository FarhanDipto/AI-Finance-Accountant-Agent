# 🧠 AI Finance Accountant Agent

> Voice-powered assistant for personal finance insight — powered by RAG-style retrieval & local embeddings.

---

## 🚀 Overview

The AI Finance Accountant Agent is a smart voice-enabled assistant that lets users:

- 📊 Track income and expenses
- 🧾 Summarize financial invoices
- 🧠 Ask questions like “What’s my highest income in April?”
- 🗣️ All through **natural voice commands**

Designed to run locally using lightweight models — no cloud or API keys required!

---

## 🧰 Tech Stack

- **Python 3** — Core language
- **pandas** — For loading, cleaning, and analyzing invoice data
- **regex** — To extract structured info from text
- **dateutil** — For parsing flexible date formats
- **Text-to-Speech**:
  - `pyttsx3` (offline) or `gTTS` + `pygame` (online option)
- **colorama**, **tqdm** — Terminal styling and progress indicators (optional)

---

## 🛠️ Features

✅ Voice command interface  
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



