import streamlit as st
import streamlit.components.v1 as components
import os
import time
import json
import matplotlib.pyplot as plt
import random
from datetime import datetime

# MUST BE FIRST - PAGE CONFIG
st.set_page_config(
    layout="wide",
    page_title="CFA Exam Prep Pro",
    page_icon="📊"
)

# ===== CUSTOM CSS =====
def inject_custom_css():
    st.markdown("""
    <style>
        /* Apply background image to all pages */
        .stApp {
            background: url('https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/Data/background.jpg') no-repeat center center fixed;
            background-size: cover;
        }

        /* Header styling */
        .header {
            color: white;  /* White text for header */
            font-size: 48px;
            font-family: 'Source Sans Pro', sans-serif;
            margin-bottom: 20px;
            text-align: center;
        }

        /* Button styling */
        .stButton>button {
            border-radius: 8px;
            border: 1px solid #003D73;  /* CFA dark blue border */
            background-color: #003D73;  /* CFA blue */
            color: white;
            transition: all 0.3s;
            font-weight: 500;
            font-family: 'Source Sans Pro', sans-serif;
        }
        .stButton>button:hover {
            background-color: #006BB6; /* Slightly lighter blue for hover */
            border-color: #006BB6;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        /* Progress bar */
        .stProgress>div>div>div {
            background-color: #003D73; /* CFA blue progress */
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

        /* Add margin to page content */
        .stMarkdown, .stText {
            margin-top: 20px;
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

# Complete topic mapping
TOPIC_TO_CATEGORY = {
    "Ethical & Professional Standards": "Ethical and Professional Standards",
    "Quantitative Methods": "Quantitative Methods", 
    "Economics": "Economics",
    "Financial Reporting & Analysis": "Financial Statement Analysis",
    "Corporate Issuers": "Corporate Issuers",
    "Equity Investments": "Equity Investments",
    "Fixed Income": "Fixed Income",
    "Derivatives": "Derivatives",
    "Alternative Investments": "Alternative Investments",
    "Portfolio Management": "Portfolio Management"
}

# ===== LOAD QUESTIONS =====
def load_questions():
    try:
        with open('Data/updated_questions_with_5_options_final.json', 'r') as f:
            questions_data = json.load(f)
        
        questions_by_category = {cat: {'easy': [], 'medium': [], 'hard': []} for cat in CATEGORIES}
        
        for question in questions_data.get("questions", []):
            topic = question.get("topic", "").strip()
            category = TOPIC_TO_CATEGORY.get(topic, topic)
            difficulty = question.get("difficulty", "medium").lower()
            
            if category in questions_by_category and difficulty in ['easy', 'medium', 'hard']:
                questions_by_category[category][difficulty].append(question)
        
        return questions_by_category
        
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return {cat: {'easy': [], 'medium': [], 'hard': []} for cat in CATEGORIES}

# ===== MAIN APP =====
def show_main_menu():
    inject_custom_css()

    # Header with title
    st.markdown(f"""
    <div class='header'>{QUIZ_TITLE}</div>
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

# ===== MAIN APP =====
def main():
    initialize_session_state()
    
    if st.session_state.quiz['mode'] == 'main_menu':
        show_main_menu()

if __name__ == "__main__":
    main()
