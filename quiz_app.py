# MUST BE FIRST - PAGE CONFIG
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    layout="wide",
    page_title="CFA Exam Prep Pro",
    page_icon="📊"
)

import os
import time
import json
import matplotlib.pyplot as plt
import random
import uuid
import base64
import numpy as np
from datetime import datetime
from io import BytesIO

# [Previous configuration code remains the same until show_main_menu()...]

def show_main_menu():
    inject_custom_css()
    show_user_profile()
    
    user_key = f"user_{st.session_state.user['id']}"
    progress_data = st.session_state.progress.get(user_key, {})
    
    # Personalized welcome
    if st.session_state.user['name']:
        st.markdown(f"### Welcome back, {st.session_state.user['name']}!")
    else:
        st.markdown("### Welcome to CFA Exam Prep Pro!")
    
    # Enhanced progress summary
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">📊 Your Study Analytics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if progress_data.get('topic_scores'):
        st.markdown(f"""
        <div class='card'>
            {create_topic_performance_chart(progress_data['topic_scores'])}
        </div>
        """, unsafe_allow_html=True)
    elif progress_data.get('attempts'):
        st.markdown("""
        <div class='card'>
            <p>Complete topic-based quizzes to see detailed performance analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Resources section
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">📚 Study Resources</h3>
    </div>
    """, unsafe_allow_html=True)
    
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        if os.path.exists(STUDY_GUIDE_PATH):
            with open(STUDY_GUIDE_PATH, "rb") as pdf_file:
                st.download_button(
                    label="📘 Download Study Guide",
                    data=pdf_file,
                    file_name="CFA_Study_Guide.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.warning("Study guide not found")
    
    with res_col2:
        if st.button("🌐 Register for CFA Exam", 
                    help=REGISTRATION_TIPS,
                    use_container_width=True):
            track_registration_click()
            js = f"window.open('{CFA_REGISTRATION_URL}')"
            components.html(js)
    
    with res_col3:
        if st.button("📈 View Progress Dashboard", use_container_width=True):
            st.session_state.quiz['mode'] = 'progress_tracking'
            st.rerun()
    
    # Practice options
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">🎯 Practice Options</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Custom Practice Exam", 
                   use_container_width=True,
                   help="Tailored exams by difficulty and topic"):
            st.session_state.quiz['mode'] = 'difficulty_selection'
            st.rerun()
    with col2:
        if st.button("📚 Focused Topic Practice", 
                   use_container_width=True,
                   help="Drill specific CFA topics"):
            st.session_state.quiz['mode'] = 'category_selection'
            st.rerun()

# [Rest of your existing functions remain unchanged...]

def main():
    try:
        # First create Data directory if it doesn't exist
        if not os.path.exists('Data'):
            os.makedirs('Data')
            
        initialize_session_state()
        
        if st.session_state.quiz['mode'] == 'main_menu':
            show_main_menu()
        elif st.session_state.quiz['mode'] == 'progress_tracking':
            show_progress_tracking()
        elif st.session_state.quiz['mode'] == 'difficulty_selection':
            show_difficulty_selection()
        elif st.session_state.quiz['mode'] == 'category_selection':
            show_category_selection()
        elif st.session_state.quiz['mode'] == 'question':
            display_question()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.button("Return to Main Menu"):
            st.session_state.quiz['mode'] = 'main_menu'
            st.rerun()

if __name__ == "__main__":
    main()
