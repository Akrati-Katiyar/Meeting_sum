@echo off
title AI Meeting Summarizer & MoM Generator - GNIOT
color 0B
echo ======================================================================
echo    AI MEETING SUMMARIZATION & MINUTES OF MEETING (MoM) GENERATOR
echo    Automatic Speech Recognition (Whisper) & LLM Synthesis
echo    B.Tech CSE (AI) Mini Project Prototype | GNIOT (2026-2027)
echo ======================================================================
echo.
echo Launching Streamlit Web Dashboard...
echo Dashboard URL: http://localhost:8501
echo.

python -m streamlit run app.py

pause
