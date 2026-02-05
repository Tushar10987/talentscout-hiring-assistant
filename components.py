import streamlit as st
from typing import Dict, List

def render_progress_tracker(current_step: int, total_steps: int, step_names: List[str] = None):
    progress = current_step / total_steps
    st.progress(progress)
    if step_names and current_step < len(step_names):
        st.caption(f"Step {current_step + 1} of {total_steps}: {step_names[current_step]}")
    else:
        st.caption(f"Step {current_step + 1} of {total_steps}")

def render_sentiment_badge(sentiment: Dict):
    label = sentiment.get('label', 'Neutral')
    polarity = sentiment.get('polarity', 0.0)
    st.caption(f"Sentiment: {label} ({polarity:+.2f})")
