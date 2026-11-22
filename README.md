# AI Meeting Summarizer & MoM Generator

An end-to-end AI-powered meeting summarization system that converts meeting audio recordings or transcripts into structured **Minutes of the Meeting (MoM)**, key decisions, and actionable tasks.

---

## 🌟 Key Features

- **Multi-Input Support**:
  - 🎙️ **Audio Recordings**: Upload `.mp3`, `.wav`, or `.m4a` files for automatic speech-to-text (STT) transcription using OpenAI Whisper.
  - 📄 **Text Transcripts**: Paste raw text or upload `.txt` meeting notes and chat logs.
- **Structured Minutes of Meeting (MoM)**:
  - **Executive Summary**: High-level overview of meeting objectives and outcomes.
  - **Key Discussion Points**: Breakdown by topic or speaker.
  - **Decisions Made**: Formal list of agreed points.
  - **Action Items Table**: Explicit tasks with assigned owner, priority, and deadline.
  - **Open Questions & Blockers**: Unresolved issues needing follow-up.
- **Export Options**: One-click download of generated summaries as Markdown (`.md`) or Plain Text (`.txt`).
- **Flexible Backend**: Works with Google Gemini API, OpenAI API, Hugging Face Transformers, or offline fallback mode.

---

## 🏗️ System Architecture

```text
       [ Meeting Audio (WAV/MP3) ]          [ Text Transcript (.txt) ]
                     │                                   │
                     ▼                                   │
      ┌─────────────────────────────┐                    │
      │   Speech-to-Text (STT)      │                    │
      │   (OpenAI Whisper Model)    │                    │
      └──────────────┬──────────────┘                    │
                     │ (Transcribed Text)                │
                     └─────────────────┬─────────────────┘
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │   Prompt Engineering & LLM Engine │
                     │   (Gemini / GPT / HuggingFace)    │
                     └─────────────────┬─────────────────┘
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │   Structured Output Generation    │
                     │   - Executive Summary             │
                     │   - Key Decisions                 │
                     │   - Action Items Table            │
                     │   - Next Steps & Blockers         │
                     └─────────────────┬─────────────────┘
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │   Streamlit Web Interface / Export│
                     └───────────────────────────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Install Dependencies
Open your terminal in this directory and run:
```bash
pip install -r requirements.txt
```

*(Optional for audio processing)*: If using Whisper for local audio transcription, ensure [FFmpeg](https://ffmpeg.org/download.html) is installed and available in your system `PATH`.

### 3. Configure API Key (Optional)
Create a `.env` file or enter your API key directly in the Streamlit sidebar:
```env
# Choose one of the following:
GEMINI_API_KEY="your_gemini_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"
```
> **Note**: If no API key is provided, the application includes a built-in offline summarizer so you can test it immediately without any setup.

### 4. Run the Application
Launch the web interface:
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
AI meeting summerization/
│
├── app.py                  # Main Streamlit web application
├── summarizer.py           # Core summarization logic & prompt pipelines
├── sample_meeting.txt      # Sample meeting transcript for quick testing
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation & instructions
```

---

## 📊 Evaluation & Research Metrics
For academic evaluation of summarization quality:
- **ROUGE-1, ROUGE-2, ROUGE-L**: Overlap of n-grams between generated summary and human reference.
- **BERTScore**: Semantic similarity leveraging contextual embeddings.
- **Action Item Extraction Accuracy**: Precision/Recall of identified task assignments.
