"""
TalentScout Hiring Assistant
AI-powered technical screening chatbot
"""

import streamlit as st
import time
from pathlib import Path

from config import Config
from utils import (
    validate_email, validate_phone, parse_tech_stack,
    sanitize_input, get_greeting_by_time, generate_session_id
)
from translator import Translator
from sentiment_analyzer import SentimentAnalyzer
from ai_engine import AIEngine
from database import Database
from components import render_progress_tracker, render_sentiment_badge

st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon=Config.APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

def load_css():
    css_file = Path(__file__).parent / "styles.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.language = "English"
    st.session_state.session_id = generate_session_id()
    st.session_state.start_time = time.time()
    st.session_state.conversation_history = []
    st.session_state.sentiment_analyzer = SentimentAnalyzer()
    st.session_state.ai_engine = AIEngine()
    st.session_state.database = Database()
    st.session_state.theme = Config.DEFAULT_THEME

def get_text(key: str) -> str:
    lang_code = Config.get_language_code(st.session_state.language)
    return Translator.get_text(key, lang_code)

def add_to_history(message: str, is_bot: bool = True, sentiment: dict = None):
    st.session_state.conversation_history.append({
        "message": message,
        "is_bot": is_bot,
        "sentiment": sentiment,
        "timestamp": time.time()
    })

def analyze_and_display_sentiment(text: str):
    if Config.ENABLE_SENTIMENT_ANALYSIS and text:
        sentiment = st.session_state.sentiment_analyzer.analyze(text)
        render_sentiment_badge(sentiment)
        return sentiment
    return None

def save_to_database():
    st.session_state.database.save_candidate(
        st.session_state.session_id,
        st.session_state.data
    )
    
    if Config.ENABLE_SENTIMENT_ANALYSIS:
        aggregate = st.session_state.sentiment_analyzer.get_aggregate_sentiment()
        st.session_state.database.save_sentiment(
            st.session_state.session_id,
            aggregate
        )

col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(f"<h1>{Config.APP_ICON} {Config.APP_TITLE}</h1>", unsafe_allow_html=True)
with col2:
    new_language = st.selectbox(
        "Lang",
        list(Config.SUPPORTED_LANGUAGES.keys()),
        index=list(Config.SUPPORTED_LANGUAGES.keys()).index(st.session_state.language),
        key="lang_sel",
        label_visibility="collapsed"
    )
    if new_language != st.session_state.language:
        st.session_state.language = new_language
        st.rerun()

step_names = ["Welcome", "Name", "Email", "Phone", "Experience", "Position", "Location", "Tech Stack", "Confirm", "Results"]
render_progress_tracker(st.session_state.step, len(step_names), step_names)

st.markdown("---")

if st.session_state.step == 0:
    greeting = get_greeting_by_time()
    st.markdown(f"### {greeting}")
    st.write(get_text('greeting'))
    st.write(get_text('intro'))
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button(get_text('start_button'), key="start_btn", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.markdown(f"**{get_text('name_prompt')}**")
    name = st.text_input("", placeholder="John Doe", key="name_input", label_visibility="collapsed")
    
    if st.button(get_text('next_button'), key="next_1", use_container_width=True):
        if name and len(name.strip()) > 0:
            sanitized_name = sanitize_input(name)
            st.session_state.data["name"] = sanitized_name
            add_to_history(sanitized_name, is_bot=False)
            st.session_state.step = 2
            st.rerun()
        else:
            st.error(get_text('error_name'))

elif st.session_state.step == 2:
    st.markdown(f"**{get_text('email_prompt')}**")
    email = st.text_input("", placeholder="john.doe@example.com", key="email_input", label_visibility="collapsed")
    
    if st.button(get_text('next_button'), key="next_2", use_container_width=True):
        if validate_email(email):
            st.session_state.data["email"] = email.lower().strip()
            add_to_history(email, is_bot=False)
            st.session_state.step = 3
            st.rerun()
        else:
            st.error(get_text('error_email'))

elif st.session_state.step == 3:
    st.markdown(f"**{get_text('phone_prompt')}**")
    phone = st.text_input("", placeholder="+1 234 567 8900", key="phone_input", label_visibility="collapsed")
    
    if st.button(get_text('next_button'), key="next_3", use_container_width=True):
        if validate_phone(phone):
            st.session_state.data["phone"] = phone.strip()
            add_to_history(phone, is_bot=False)
            st.session_state.step = 4
            st.rerun()
        else:
            st.error(get_text('error_phone'))

elif st.session_state.step == 4:
    st.markdown(f"**{get_text('experience_prompt')}**")
    experience = st.number_input("", min_value=0, max_value=50, value=0, step=1, key="exp_input", label_visibility="collapsed")
    
    if st.button(get_text('next_button'), key="next_4", use_container_width=True):
        st.session_state.data["experience"] = experience
        add_to_history(f"{experience} years", is_bot=False)
        st.session_state.step = 5
        st.rerun()

elif st.session_state.step == 5:
    st.markdown(f"**{get_text('position_prompt')}**")
    position = st.text_input("", placeholder="Full Stack Developer", key="position_input", label_visibility="collapsed")
    
    if st.button(get_text('next_button'), key="next_5", use_container_width=True):
        if position and len(position.strip()) > 0:
            sanitized_position = sanitize_input(position)
            st.session_state.data["position"] = sanitized_position
            add_to_history(sanitized_position, is_bot=False)
            st.session_state.step = 6
            st.rerun()
        else:
            st.error(get_text('error_position'))

elif st.session_state.step == 6:
    st.markdown(f"**{get_text('location_prompt')}**")
    location = st.text_input("", placeholder="San Francisco, CA", key="location_input", label_visibility="collapsed")
    
    if st.button(get_text('next_button'), key="next_6", use_container_width=True):
        if location and len(location.strip()) > 0:
            sanitized_location = sanitize_input(location)
            st.session_state.data["location"] = sanitized_location
            add_to_history(sanitized_location, is_bot=False)
            st.session_state.step = 7
            st.rerun()
        else:
            st.error(get_text('error_location'))

elif st.session_state.step == 7:
    st.markdown(f"**{get_text('tech_stack_prompt')}**")
    tech_stack = st.text_area("", placeholder="Python, React, PostgreSQL, Docker, AWS", key="tech_input", height=100, label_visibility="collapsed")
    
    if tech_stack and Config.ENABLE_SENTIMENT_ANALYSIS:
        sentiment = analyze_and_display_sentiment(tech_stack)
    
    if st.button(get_text('next_button'), key="next_7", use_container_width=True):
        if tech_stack and len(tech_stack.strip()) > 0:
            st.session_state.data["tech"] = tech_stack.strip()
            st.session_state.data["language"] = st.session_state.language
            st.session_state.step = 8
            st.rerun()
        else:
            st.error(get_text('error_tech'))

elif st.session_state.step == 8:
    st.markdown(f"### {get_text('confirm_details')}")
    
    st.write(f"**Name:** {st.session_state.data.get('name', 'N/A')}")
    st.write(f"**Email:** {st.session_state.data.get('email', 'N/A')}")
    st.write(f"**Phone:** {st.session_state.data.get('phone', 'N/A')}")
    st.write(f"**Experience:** {st.session_state.data.get('experience', 0)} years")
    st.write(f"**Position:** {st.session_state.data.get('position', 'N/A')}")
    st.write(f"**Location:** {st.session_state.data.get('location', 'N/A')}")
    st.write(f"**Tech Stack:** {st.session_state.data.get('tech', 'N/A')}")
    
    st.markdown("---")
    
    if st.button(get_text('confirm_button'), key="confirm_btn", use_container_width=True):
        save_to_database()
        st.session_state.step = 9
        st.rerun()

elif st.session_state.step == 9:
    st.markdown(f"### {get_text('generating')}")
    
    with st.spinner("Generating your personalized assessment..."):
        lang_code = Config.get_language_code(st.session_state.language)
        questions = st.session_state.ai_engine.generate_technical_questions(
            st.session_state.data,
            language=lang_code
        )
        
        st.session_state.database.save_questions(
            st.session_state.session_id,
            questions
        )
    
    st.success(get_text('screening_complete'))
    
    st.markdown("---")
    st.markdown(f"### {get_text('ai_assessment')}")
    st.markdown(questions)
    
    if Config.ENABLE_SENTIMENT_ANALYSIS:
        st.markdown("---")
        aggregate_sentiment = st.session_state.sentiment_analyzer.get_aggregate_sentiment()
        st.info(f"**Overall Sentiment:** {aggregate_sentiment['overall_label']} ({aggregate_sentiment['emotional_state']})")
    
    avg_response_time = st.session_state.ai_engine.get_average_response_time()
    total_time = time.time() - st.session_state.start_time
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("AI Response Time", f"{avg_response_time:.2f}s")
    with col2:
        st.metric("Total Time", f"{total_time:.0f}s")
    
    st.markdown("---")
    json_data = st.session_state.database.export_to_json(st.session_state.session_id)
    st.download_button(
        label="Download Results (JSON)",
        data=json_data,
        file_name=f"candidate_{st.session_state.session_id}.json",
        mime="application/json",
        use_container_width=True
    )
    
    st.markdown("---")
    st.success(get_text('thank_you'))
    
    if st.button("Start New Screening", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.markdown("---")
