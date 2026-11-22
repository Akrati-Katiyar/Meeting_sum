# AI Meeting Summarization & Minutes of Meeting (MoM) Generator
## Comprehensive Project Report & Implementation Guide

---

## 1. Project Title & Abstract

### Title
**Automated Meeting Summarization and Action Item Extraction System Using Deep Learning and Large Language Models**

### Abstract
Meetings are essential communication channels in organizations, but manual documentation of discussions, decisions, and action items is labor-intensive, error-prone, and inconsistent. This project presents an automated AI-driven Meeting Summarization and Minutes of Meeting (MoM) generation pipeline. The system processes either raw spoken audio recordings (via OpenAI Whisper Automatic Speech Recognition) or direct meeting transcripts. It applies context-aware prompt engineering on state-of-the-art Large Language Models (LLMs) alongside local heuristic extractors to distill lengthy dialogues into structured, actionable reports comprising Executive Summaries, Key Decisions, Action Item matrices with assignees and deadlines, and Open Follow-ups. An interactive Streamlit web dashboard allows users to upload recordings or transcripts, preview generated notes, and export professional documentation.

---

## 2. Problem Statement & Motivation
- **Information Overload**: Teams spend hours in syncs, but critical decisions and tasks get lost in verbal exchanges.
- **Manual Overhead**: Assigning designated note-takers distracts participants from engaging actively.
- **Lack of Accountability**: Unstructured notes often lack clear ownership, deadlines, and tracking mechanisms.
- **Objective**: Develop an end-to-end intelligent system that ingests audio or text, produces concise summaries, and structures action items automatically.

---

## 3. System Architecture & Methodology

```text
 ┌───────────────────────┐
 │   Input Ingestion     │ ────> Audio (.wav, .mp3) OR Transcript (.txt, .md)
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │ Speech-to-Text (ASR)  │ ────> OpenAI Whisper Model (Base/Medium)
 └───────────┬───────────┘
             │
             ▼ (Raw Meeting Transcript)
 ┌───────────────────────┐
 │ Preprocessing & Chunk │ ────> Speaker attribution, timestamp filtering, token windowing
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │  LLM Summarizer Core  │ ────> Gemini / OpenAI / Local Heuristic Extractor
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │  Structured Output    │ ────> Executive Summary, Decisions, Action Items Table
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │ User Interface/Export │ ────> Streamlit GUI, Markdown (.md), Plain Text (.txt)
 └───────────────────────┘
```

---

## 4. Key Modules & Technical Stack

| Component | Technology / Library | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit | Clean, responsive interface for uploading, previewing, and downloading |
| **Speech-to-Text** | OpenAI Whisper / Faster-Whisper | Converts spoken dialogue to timestamped text with robust noise handling |
| **Language Engine** | Google Gemini / OpenAI / Heuristic | Synthesizes discussion context and generates structured MoM |
| **Data Processing** | Python, Regular Expressions, Pandas | Transcript normalization and tabular action item formatting |
| **Storage & Export** | Markdown / Text / File I/O | Portable document generation |

---

## 5. Evaluation Metrics

For research and academic evaluation, the system can be assessed using standard Natural Language Processing (NLP) metrics:
1. **ROUGE (Recall-Oriented Understudy for Gesting Evaluation)**:
   - **ROUGE-1**: Unigram overlap between generated summary and human reference.
   - **ROUGE-2**: Bigram overlap, measuring fluency and phrasing accuracy.
   - **ROUGE-L**: Longest Common Subsequence (LCS), evaluating sentence-level structure.
2. **BERTScore**: Computes token-level semantic similarity using contextual embeddings rather than exact surface-form string matching.
3. **Action Item Precision & Recall**:
   $$\text{Precision} = \frac{\text{Correct Action Items Extracted}}{\text{Total Action Items Extracted}}$$
   $$\text{Recall} = \frac{\text{Correct Action Items Extracted}}{\text{Total Ground Truth Action Items}}$$

---

## 6. How to Run the Project

1. **Navigate to the directory**:
   ```bash
   cd "AI meeting summerization"
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```
4. **Test the pipeline**:
   - Click **"Load Sample Meeting Transcript"** in the sidebar.
   - Click **"🚀 Generate Summary & MoM"**.
   - Download the generated report.

---

## 7. Future Enhancements
- **Speaker Diarization**: Integrate `pyannote.audio` to automatically label individual speakers (Speaker A, Speaker B).
- **Calendar & Task Integrations**: One-click sync of identified action items to Jira, Trello, or Google Tasks.
- **Multilingual Support**: Real-time cross-language translation for international meetings.
