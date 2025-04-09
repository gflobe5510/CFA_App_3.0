# MUST BE FIRST - PAGE CONFIG
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    layout="wide",
    page_title="CFA Exam Prep Pro",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

import os
import time
import json
import matplotlib.pyplot as plt
import random
from datetime import datetime

# ===== CUSTOM CSS =====
def inject_custom_css():
    st.markdown("""
    <style>
        /* Main styling */
        .main {
            background-color: #f8f9fa;
        }
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
        }
        
        /* Header styling */
        .header {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 25px;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 8px;
            border: 1px solid #3498db;
            background-color: #3498db;
            color: white;
            transition: all 0.3s;
            font-weight: 500;
        }
        .stButton>button:hover {
            background-color: #2980b9;
            border-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Progress bar */
        .stProgress>div>div>div {
            background-color: #3498db;
        }
        
        /* Radio buttons */
        .stRadio>div {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Custom card styling */
        .card {
            background-color: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }
        
        /* Metrics containers */
        .metric-card {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        /* Table styling */
        .stTable {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Chart styling */
        .stPlotlyChart {
            border-radius: 8px;
            background: white;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)

# ===== CFA CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Pro"
CFA_REGISTRATION_URL = "https://www.cfainstitute.org/"
STUDY_GUIDE_PATH = "Data/CFA_Study_Guide.pdf"
REGISTRATION_TIPS = """
• Early registration discounts available
• Prepare payment method in advance  
• Have identification documents ready
• Check exam schedule carefully
"""

# [Keep all your existing TOPIC_TO_CATEGORY and CATEGORIES dictionaries here]
# [Keep all your existing functions but update their display elements]

def show_main_menu():
    inject_custom_css()
    
    # Header with logo placeholder
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 30px;">
        <img src="https://via.placeholder.com/80x80.png?text=CFA" width=80 style="margin-right: 20px;">
        <h1 class='header' style="margin: 0;">{QUIZ_TITLE}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats summary card
    try:
        with open('Data/progress_data.json', 'r') as f:
            progress_data = json.load(f)
        attempts = len(progress_data['attempts'])
        avg_score = f"{sum(progress_data['scores'])/attempts:.1%}" if attempts > 0 else "N/A"
        
        st.markdown(f"""
        <div class='card'>
            <h3 style="color: #2c3e50; margin-top: 0;">📊 Your Progress Summary</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
                <div class='metric-card'>
                    <div style="font-size: 14px; color: #7f8c8d;">Total Attempts</div>
                    <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">{attempts}</div>
                </div>
                <div class='metric-card'>
                    <div style="font-size: 14px; color: #7f8c8d;">Average Score</div>
                    <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">{avg_score}</div>
                </div>
                <div class='metric-card'>
                    <div style="font-size: 14px; color: #7f8c8d;">Questions Answered</div>
                    <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">{sum(len(q) for cat in st.session_state.quiz['all_questions'].values() for diff in cat.values() for q in diff)}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div class='card'>
            <h3 style="color: #2c3e50; margin-top: 0;">📊 Your Progress Summary</h3>
            <p>Complete your first quiz to see stats</p>
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

# [Update other display functions with the same styling approach]
# Example for show_results():
def show_results():
    quiz = st.session_state.quiz
    total_time = time.time() - quiz['start_time']
    avg_time = sum(quiz['time_spent'])/len(quiz['time_spent']) if quiz['time_spent'] else 0
    
    save_progress(quiz['score'], len(quiz['current_questions']), total_time)
    
    st.markdown(f"""
    <div class='card'>
        <h2 style="color: #2c3e50; margin-top: 0;">Quiz Completed!</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0;">
            <div class='metric-card'>
                <div style="font-size: 16px; color: #7f8c8d;">Score</div>
                <div style="font-size: 32px; font-weight: bold; color: #2c3e50;">{quiz['score']}/{len(quiz['current_questions'])}</div>
            </div>
            <div class='metric-card'>
                <div style="font-size: 16px; color: #7f8c8d;">Total Time</div>
                <div style="font-size: 32px; font-weight: bold; color: #2c3e50;">{format_time(total_time)}</div>
            </div>
            <div class='metric-card'>
                <div style="font-size: 16px; color: #7f8c8d;">Avg/Question</div>
                <div style="font-size: 32px; font-weight: bold; color: #2c3e50;">{format_time(avg_time)}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    display_result_chart()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Return to Main Menu", use_container_width=True):
            st.session_state.quiz['mode'] = 'main_menu'
            st.rerun()
    with col2:
        if st.button("View Progress Dashboard", use_container_width=True):
            st.session_state.quiz['mode'] = 'progress_tracking'
            st.rerun()

# [Keep all other functions the same but apply similar styling updates]

if __name__ == "__main__":
    main()
