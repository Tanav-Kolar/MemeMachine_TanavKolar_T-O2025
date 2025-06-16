
# 🧠 Boudhi Chatbot – Government Scheme Finder & Screener

Boudhi is a multilingual voice- and text-enabled chatbot built to help users discover and understand government schemes. It supports natural language queries, voice input, and multilingual response output — designed with accessibility and local relevance in mind.

---

## 🔧 Features

- 🎤 **Voice Input (Speech-to-Text)** using a custom ASR engine
- 🧾 **Text Input** with language translation support
- 🔍 **Query Matching** using Pinecone vector search
- 🧠 **LLM-Powered Answers** via Groq API
- 🗣 **Text-to-Speech (TTS)** for voice responses
- 🈯 **Multilingual Input/Output Support** (English + Indian languages)
- 📋 **Screening Logic** for personalized scheme recommendations
- **Scraping and GraphDB Collection**  - Scraped scheme informations from publicly available government data sources to create a Vector Database

---

## 🗂 File Overview

| File                  | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `main.py`             | Streamlit-based chatbot frontend with text/voice input and TTS output   |
| `asr.py`              | Audio capture and transcription logic                                   |
| `Scheme Finder.py`    | Alternate interface version for scheme querying                         |
| `pinecone_utils.py`   | Pinecone vector search utilities for scheme documents                   |
| `scheme_upsert.py`    | Script to upload/index schemes into Pinecone                            |
| `Screening.py`        | Handles scheme eligibility filtering logic                              |

---

## 🚀 How It Works

1. **Input Capture**
   - Users type or speak a query in their preferred language.
   - Voice is recorded and transcribed using the `asr.py` module.
   - Input is translated to English if needed.

2. **Scheme Matching**
   - Query is embedded and passed to `pinecone_utils.py` to retrieve semantically relevant schemes.
   - The result is refined and explained using a Groq-hosted LLM.

3. **Response Output**
   - Textual answers are rendered in the chat.
   - An optional TTS button allows responses to be read aloud in the selected language.

4. **Screening**
   - If the user opts to undergo screening, the `Screening.py` module asks a series of filtering questions.
   - Matches are determined by eligibility rules hardcoded per scheme.

---

## 🛠 Setup Instructions

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

> (Make sure to include dependencies like `streamlit`, `sounddevice`, `pyttsx3`, `gtts`, `openai-whisper`, `pinecone-client`, `googletrans`, `dotenv`, etc.)

2. **Configure environment**
   - Create a `.env` file:
     ```
     GROQ_API_KEY=your_groq_key
     PINECONE_API_KEY=your_pinecone_key
     PINECONE_ENVIRONMENT=your_env
     ```

3. **Run the app**
```bash
streamlit run main.py
```

---

## 🌐 Language Support

- ✍️ Input: Text or speech in English, Hindi, Tamil, etc.
- 🧠 Processing: Translated to English for understanding
- 🗣 Output: Text and optional voice (TTS) in original language

---

## 📦 Future Improvements

- UI enhancements for mobile users
- Better regional dialect support
- Backend support for form submissions (e.g., apply for schemes)

---

## 🧑‍💻 Contributors

- **You** – by using, improving, and sharing Boudhi!
