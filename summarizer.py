import os
import re
from typing import Dict, Any, Optional

PROMPT_TEMPLATE = """You are an expert executive assistant and meeting analyst. 
Analyze the following meeting transcript and produce a highly structured, professional Minutes of the Meeting (MoM) report.

TRANSCRIPT:
{transcript}

Please structure your response with the following sections in clean Markdown:

# 📋 Minutes of Meeting (MoM)

## 1. Executive Summary
Provide a concise 2-3 paragraph overview of the meeting purpose, key topics covered, and general progress.

## 2. Key Discussion Topics & Points
Group the discussion by themes or agenda items with bullet points explaining the core rationale.

## 3. Decisions Made
List all concrete, agreed-upon decisions made during the conversation.

## 4. Action Items Table
Create a clean markdown table with the following columns:
| # | Task / Action Item | Owner | Deadline / Timeframe | Priority (High / Med / Low) |

## 5. Risks, Blockers & Open Questions
List any unresolved issues, risks, or questions that require follow-up.

Ensure the summary is objective, professional, and directly derived from the transcript.
"""


def summarize_with_gemini(transcript: str, api_key: str, model_name: str = "gemini-1.5-flash") -> str:
    """Summarize transcript using Google Gemini API."""
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    prompt = PROMPT_TEMPLATE.format(transcript=transcript)
    response = model.generate_content(prompt)
    return response.text


def summarize_with_openai(transcript: str, api_key: str, model_name: str = "gpt-4o-mini") -> str:
    """Summarize transcript using OpenAI API."""
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    prompt = PROMPT_TEMPLATE.format(transcript=transcript)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a professional meeting analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content


def summarize_offline(transcript: str) -> str:
    """
    Intelligent offline fallback summarizer when no API key is provided.
    Extracts speakers, key sentences, agenda mentions, and creates a structured MoM.
    """
    lines = [line.strip() for line in transcript.split("\n") if line.strip()]
    
    # Extract potential speakers
    speaker_pattern = re.compile(r"^([A-Z][a-zA-Z\s]{1,25}):")
    speakers = set()
    action_candidates = []
    decision_candidates = []
    discussion_points = []

    for line in lines:
        match = speaker_pattern.match(line)
        if match:
            speaker = match.group(1).strip()
            if speaker.lower() not in ["date", "time", "meeting", "attendees", "agenda", "topic", "meeting title", "title", "location", "note", "notes"]:
                speakers.add(speaker)
        
        lower_line = line.lower()
        if any(kw in lower_line for kw in ["will", "owns", "recap", "action", "by tomorrow", "by thursday", "by friday", "deadline", "deploy", "finalize"]):
            action_candidates.append(line)
        elif any(kw in lower_line for kw in ["decided", "decision", "approved", "agreed", "we can do that"]):
            decision_candidates.append(line)
        elif len(line) > 50 and not line.startswith("["):
            discussion_points.append(line)

    attendee_str = ", ".join(sorted(speakers)) if speakers else "Identified from transcript text"
    
    # Formulate offline summary
    summary = []
    summary.append("# 📋 Minutes of Meeting (MoM) *(Offline Analysis Mode)*\n")
    summary.append(f"> **Note**: Generated using local heuristic extractor. Connect Gemini or OpenAI in the sidebar for full LLM synthesis.\n")
    summary.append("## 1. Executive Summary")
    summary.append(f"The meeting involved key stakeholders ({attendee_str}) to review project deliverables, operational performance, and roadmap milestones.")
    summary.append("The discussion covered functional architecture, timeline alignment, technical challenges, and infrastructure optimizations.\n")

    summary.append("## 2. Key Discussion Topics")
    if discussion_points:
        for pt in discussion_points[:6]:
            summary.append(f"- {pt}")
    else:
        for line in lines[:5]:
            summary.append(f"- {line}")
    summary.append("")

    summary.append("## 3. Decisions Made")
    if decision_candidates:
        for dec in decision_candidates[:4]:
            summary.append(f"- **Agreed**: {dec}")
    else:
        summary.append("- Architectural and timeline proposals reviewed and acknowledged by the team.")
    summary.append("")

    summary.append("## 4. Action Items Table")
    summary.append("| # | Task / Action Item | Identified Context | Priority |")
    summary.append("|---|---|---|---|")
    if action_candidates:
        for idx, act in enumerate(action_candidates[:6], 1):
            clean_act = act.replace("|", "/")
            priority = "High" if any(w in clean_act.lower() for w in ["today", "production", "urgent", "staging"]) else "Medium"
            summary.append(f"| {idx} | {clean_act} | Follow-up Required | {priority} |")
    else:
        summary.append("| 1 | Review and follow up on meeting transcript points | All Stakeholders | Medium |")
    summary.append("")

    summary.append("## 5. Next Steps & Follow-ups")
    summary.append("- Verify completion of assigned milestones before the next scheduled synchronization.")
    summary.append("- Continuous monitoring of operational performance metrics.")

    return "\n".join(summary)


def generate_meeting_summary(
    transcript: str,
    provider: str = "offline",
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> str:
    """Main entry point to summarize meeting transcript."""
    if not transcript or not transcript.strip():
        raise ValueError("Transcript text cannot be empty.")

    if provider == "gemini" and api_key:
        model = model_name or "gemini-1.5-flash"
        return summarize_with_gemini(transcript, api_key, model)
    elif provider == "openai" and api_key:
        model = model_name or "gpt-4o-mini"
        return summarize_with_openai(transcript, api_key, model)
    else:
        return summarize_offline(transcript)


def transcribe_audio_file(audio_path: str) -> str:
    """
    Transcribe audio file using OpenAI Whisper locally.
    Falls back gracefully if whisper is not installed.
    """
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result.get("text", "")
    except ImportError:
        raise ImportError(
            "The `whisper` library is required for audio transcription. "
            "Install it with: `pip install openai-whisper` and ensure FFmpeg is installed."
        )
