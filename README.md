<p align="center">
  <img src="https://raw.githubusercontent.com/your-username/your-repo-name/main/banner.png" alt="AI Finance Accountant Agent Banner">
</p>

<h1 align="center">AI Finance Accountant Agent 💼📊</h1>

<p align="center">
  A simple, local AI agent that can understand and analyze structured financial documents (invoices, transactions, and more) — no embeddings, no vector DBs, no fancy LLMs. Just smart regex, pandas, and clean logic.
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#demo">Demo</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#license">License</a>
</p>

---

## 🚀 Features

- 🧠 Smart data parsing using regex and pandas
- 📂 Supports both income and expense data from plain text files
- 🔍 Handles natural language questions like:
  - *“What is the total income for March 2024?”*
  - *“Which expense category had the highest total?”*
- 🗣️ Optional Text-to-Speech for query answers
- 🖥️ Simple Streamlit GUI included (optional)
- 💡 Lightweight, offline, and private — works without internet or APIs

---

## 🎥 Demo

![AI Finance Agent Demo](demo.gif) <!-- You can upload a GIF and link it here -->

---

## ⚙️ How It Works

1. Reads structured `invoices.txt` with labeled entries for incomes and expenses.
2. Uses regular expressions to extract:
   - Date
   - Category
   - Amount
   - Description
3. Loads into a `pandas.DataFrame`
4. Accepts user questions and parses intent using simple logic (no NLP models needed!)
5. Answers are generated via direct `pandas` operations
6. Optionally, answers are spoken aloud via `pyttsx3`.

---

## 🧰 Tech Stack

- Python 3
- Pandas
- Regex
- pyttsx3 (for TTS)
- Streamlit (for optional GUI)

---

## 📦 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/your-username/ai-finance-accountant-agent.git
cd ai-finance-accountant-agent

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py

# Optional: Launch the Streamlit GUI
streamlit run gui.py
