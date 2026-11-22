import os
import tempfile
import streamlit as st
from summarizer import generate_meeting_summary, transcribe_audio_file

# Page Configuration
st.set_page_config(
    page_title="AI Meeting Summarizer & MoM Generator",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .highlight-card {
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #2563EB;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("⚙️ Engine Configuration")

provider = st.sidebar.selectbox(
    "Choose AI Provider",
    options=["Offline / Built-in Extractor", "Google Gemini", "OpenAI"],
    index=0,
    help="Select 'Offline' to test without an API key, or choose Gemini/OpenAI for full generative LLM synthesis."
)

api_key = None
model_name = None

if provider == "Google Gemini":
    api_key = st.sidebar.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
    model_name = st.sidebar.selectbox("Gemini Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.sidebar.caption("Get a free API key at [Google AI Studio](https://aistudio.google.com/).")
elif provider == "OpenAI":
    api_key = st.sidebar.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    model_name = st.sidebar.selectbox("OpenAI Model", ["gpt-4o-mini", "gpt-4o"])
    st.sidebar.caption("Get an API key at [OpenAI Platform](https://platform.openai.com/).")
else:
    st.sidebar.info("💡 **Offline Mode Active**: Generates structured MoM, attendees, and action items using local extraction heuristics without requiring internet or API keys.")

st.sidebar.markdown("---")
st.sidebar.subheader("📄 Quick Test Data")
load_sample = st.sidebar.button("Load Sample Meeting Transcript", use_container_width=True)

# Main Header
st.markdown('<div class="main-title">🎙️ AI Meeting Summarizer & MoM Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Transform meeting audio recordings and transcripts into structured Minutes of Meeting (MoM), decisions, and action items.</div>', unsafe_allow_html=True)

# Session state initialization for transcript
if "transcript" not in st.session_state:
    st.session_state["transcript"] = ""

if load_sample:
    sample_path = os.path.join(os.path.dirname(__file__), "sample_meeting.txt")
    if os.path.exists(sample_path):
        with open(sample_path, "r", encoding="utf-8") as f:
            st.session_state["transcript"] = f.read()
        st.sidebar.success("Sample meeting loaded!")

tab1, tab2, tab3 = st.tabs(["📝 Text Transcript", "🎙️ Audio Recording", "ℹ️ System Architecture"])

with tab1:
    st.markdown("##### Paste or Upload Meeting Transcript")
    uploaded_text_file = st.file_uploader("Upload a text file (.txt, .md)", type=["txt", "md"])
    if uploaded_text_file is not None:
        st.session_state["transcript"] = uploaded_text_file.read().decode("utf-8")

    transcript_input = st.text_area(
        "Meeting Transcript",
        value=st.session_state["transcript"],
        height=260,
        placeholder="Paste your meeting notes, chat log, or speaker transcript here..."
    )
    st.session_state["transcript"] = transcript_input

with tab2:
    st.markdown("##### Transcribe Audio Recording")
    st.caption("Upload meeting audio to transcribe speech into text using local OpenAI Whisper.")
    uploaded_audio = st.file_uploader("Upload Audio File (.wav, .mp3, .m4a)", type=["wav", "mp3", "m4a"])
    
    if uploaded_audio is not None:
        st.audio(uploaded_audio)
        if st.button("Transcribe Audio with Whisper", type="secondary"):
            with st.spinner("Transcribing audio file... (this may take a minute depending on file size)"):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_audio.name)[1]) as tmp:
                        tmp.write(uploaded_audio.read())
                        tmp_path = tmp.name
                    
                    transcription = transcribe_audio_file(tmp_path)
                    os.unlink(tmp_path)
                    st.session_state["transcript"] = transcription
                    st.success("Transcription complete! You can view and edit it in the 'Text Transcript' tab.")
                    st.text_area("Extracted Transcript", value=transcription, height=180)
                except Exception as e:
                    st.error(f"Transcription failed: {str(e)}")

with tab3:
    st.markdown("""
    ### 🏗️ How It Works
    1. **Input Stage**: Accepts raw meeting audio (WAV/MP3/M4A) or text transcripts.
    2. **Transcription Stage**: Employs OpenAI Whisper (Automatic Speech Recognition - ASR) to convert spoken dialogue into timestamped text.
    3. **NLP & Summarization Engine**:
       - Extracts key topics, attendee statements, and dialogue turns.
       - Identifies explicit commitments, deadlines, and assigned responsibilities.
       - Formats into a professional Minutes of Meeting (MoM) report.
    4. **Output Stage**: Displays interactive tables and markdown reports ready for export.
    """)

st.markdown("---")

col1, col2 = st.columns([1, 4])
with col1:
    generate_btn = st.button("🚀 Generate Summary & MoM", type="primary", use_container_width=True)

if generate_btn:
    current_transcript = st.session_state.get("transcript", "").strip()
    if not current_transcript:
        st.warning("⚠️ Please provide a meeting transcript or upload an audio file first.")
    else:
        provider_key = "gemini" if provider == "Google Gemini" else ("openai" if provider == "OpenAI" else "offline")
        
        if provider_key in ["gemini", "openai"] and not api_key:
            st.error(f"⚠️ Please enter an API key for {provider} in the sidebar, or switch to 'Offline / Built-in Extractor'.")
        else:
            with st.spinner("Analyzing transcript and generating Minutes of Meeting..."):
                try:
                    summary_result = generate_meeting_summary(
                        transcript=current_transcript,
                        provider=provider_key,
                        api_key=api_key,
                        model_name=model_name
                    )
                    st.session_state["summary_result"] = summary_result
                except Exception as ex:
                    st.error(f"Error during summarization: {str(ex)}")

if "summary_result" in st.session_state and st.session_state["summary_result"]:
    st.markdown("### 📋 Generated Minutes of Meeting (MoM)")
    st.markdown(st.session_state["summary_result"])
    
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        st.download_button(
            label="📥 Download MoM as Markdown (.md)",
            data=st.session_state["summary_result"],
            file_name="Minutes_of_Meeting.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col_d2:
        st.download_button(
            label="📥 Download MoM as Plain Text (.txt)",
            data=st.session_state["summary_result"],
            file_name="Minutes_of_Meeting.txt",
            mime="text/plain",
            use_container_width=True
        )
