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

# Complete categories data
CATEGORIES = {
    "Ethical and Professional Standards": {
        "description": "Focuses on ethical principles and professional standards",
        "weight": 0.15
    },
    "Quantitative Methods": {
        "description": "Covers statistical tools for financial analysis",
        "weight": 0.10
    },
    "Economics": {
        "description": "Examines macroeconomic and microeconomic concepts",
        "weight": 0.10
    },
    "Financial Statement Analysis": {
        "description": "Analysis of financial statements", 
        "weight": 0.15
    },
    "Corporate Issuers": {
        "description": "Characteristics of corporate issuers",
        "weight": 0.10
    },
    "Equity Investments": {
        "description": "Valuation of equity securities",
        "weight": 0.11
    },
    "Fixed Income": {
        "description": "Analysis of fixed-income securities",
        "weight": 0.11
    },
    "Derivatives": {
        "description": "Valuation of derivative securities",
        "weight": 0.06
    },
    "Alternative Investments": {
        "description": "Hedge funds, private equity, real estate",
        "weight": 0.06
    },
    "Portfolio Management": {
        "description": "Portfolio construction and risk management",
        "weight": 0.06
    }
}

# ===== LOAD QUESTIONS =====
def load_questions():
    try:
        # Ensure Data directory exists
        if not os.path.exists('Data'):
            os.makedirs('Data')
            
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
        
        .profile-expander {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #3498db;
        }
    </style>
    """, unsafe_allow_html=True)

# ===== USER PROFILE SYSTEM =====
def init_progress_tracking():
    if 'progress' not in st.session_state:
        st.session_state.progress = {}

def initialize_session_state():
    if 'initialized' not in st.session_state:
        # Ensure Data directory exists
        if not os.path.exists('Data'):
            os.makedirs('Data')
            
        st.session_state.update({
            'user': {
                'name': '',
                'email': '',
                'id': str(uuid.uuid4()),
                'identified': False
            },
            'quiz': {
                'all_questions': load_questions(),
                'current_questions': [],
                'score': 0,
                'current_index': 0,
                'user_answer': None,
                'submitted': False,
                'start_time': time.time(),
                'question_start': time.time(),
                'time_spent': [],
                'mode': 'main_menu',
                'selected_category': None,
                'test_type': None,
                'exam_number': None
            },
            'sidebar_view': 'practice',
            'initialized': True,
            'confirm_registration': True
        })
    init_progress_tracking()

def show_user_profile():
    with st.expander("🔐 Personalize Your Experience", expanded=not st.session_state.user['identified']):
        with st.form("user_profile"):
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Name (optional)", 
                                   value=st.session_state.user['name'],
                                   help="For personalizing your reports")
            with cols[1]:
                email = st.text_input("Email (optional)", 
                                    value=st.session_state.user['email'],
                                    help="For cross-device progress sync")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.form_submit_button("💾 Save Profile"):
                    try:
                        st.session_state.user.update({
                            'name': name.strip(),
                            'email': email.strip(),
                            'identified': bool(name.strip() or email.strip())
                        })
                        
                        # Save profile data separately
                        profile_path = 'Data/user_profile.json'
                        with open(profile_path, 'w') as f:
                            json.dump({
                                'name': st.session_state.user['name'],
                                'email': st.session_state.user['email']
                            }, f)
                            
                        st.success("Preferences saved!")
                    except Exception as e:
                        st.error(f"Could not save profile: {str(e)}")
                    st.rerun()
            with col2:
                if st.button("🔄 Reset My Progress", help="Clear all your progress data"):
                    reset_progress()
            with col3:
                if st.button("👤 Switch Profile", help="Start a new anonymous session"):
                    switch_profile()

def reset_progress():
    try:
        user_key = f"user_{st.session_state.user['id']}"
        if user_key in st.session_state.progress:
            del st.session_state.progress[user_key]
            with open('Data/progress_data.json', 'w') as f:
                json.dump(st.session_state.progress, f)
            st.success("Progress reset successfully!")
    except Exception as e:
        st.error(f"Error resetting progress: {str(e)}")
    st.rerun()

def switch_profile():
    st.session_state.user = {
        'name': '',
        'email': '',
        'id': str(uuid.uuid4()),
        'identified': False
    }
    st.rerun()

def track_registration_click():
    try:
        init_progress_tracking()
        user_key = f"user_{st.session_state.user['id']}"
        if user_key not in st.session_state.progress:
            st.session_state.progress[user_key] = {
                'registration_clicks': 0,
                'last_registration_click': None
            }
        st.session_state.progress[user_key]['registration_clicks'] += 1
        st.session_state.progress[user_key]['last_registration_click'] = datetime.now().isoformat()
        save_progress(0, 1, 0)
    except Exception as e:
        st.error(f"Error tracking registration: {str(e)}")

# ===== ENHANCED PROGRESS TRACKING =====
def save_progress(score, total_questions, total_time, category=None):
    try:
        init_progress_tracking()
        
        user_key = f"user_{st.session_state.user['id']}"
        if user_key not in st.session_state.progress:
            st.session_state.progress[user_key] = {
                'attempts': [],
                'scores': [],
                'time_spent': [],
                'dates': [],
                'topic_scores': {},
                'name': st.session_state.user['name'],
                'email': st.session_state.user['email']
            }
        
        user_progress = st.session_state.progress[user_key]
        user_progress['attempts'].append(len(user_progress['attempts']) + 1)
        user_progress['scores'].append(score/total_questions)
        user_progress['time_spent'].append(total_time)
        user_progress['dates'].append(datetime.now().strftime("%Y-%m-%d"))
        
        if category:
            user_progress['topic_scores'][category] = score/total_questions
        
        with open('Data/progress_data.json', 'w') as f:
            json.dump(st.session_state.progress, f)
    except Exception as e:
        st.error(f"Error saving progress: {str(e)}")

def create_topic_performance_chart(topic_scores):
    try:
        topics = list(CATEGORIES.keys())
        benchmark = [0.75] * len(topics)
        user_scores = [topic_scores.get(topic, 0) for topic in topics]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ind = np.arange(len(topics))
        width = 0.35
        
        ax.barh(ind - width/2, benchmark, width, color='#95a5a6', label='Benchmark (75%)')
        ax.barh(ind + width/2, user_scores, width, color='#3498db', label='Your Score')
        
        ax.set_yticks(ind)
        ax.set_yticklabels(topics)
        ax.set_xlim([0, 1])
        ax.set_title('Topic Performance vs Benchmark', pad=20)
        ax.set_xlabel('Score')
        ax.legend()
        
        for i, (bench, score) in enumerate(zip(benchmark, user_scores)):
            ax.text(bench + 0.01, i - width/2, f'{bench:.0%}', va='center', color='#2c3e50')
            ax.text(score + 0.01, i + width/2, f'{score:.0%}', va='center', color='#2c3e50')
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        plt.close(fig)
        return f"<img src='data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}' style='width:100%'>"
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return ""

# ===== QUIZ FUNCTIONS =====
def show_difficulty_selection():
    st.markdown("""
    <div class='card'>
        <h2 style="color: #2c3e50; margin-top: 0;">Select Practice Mode</h2>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    
    with cols[0]:
        if st.button("⚡ Quick Quiz (5 Random Questions)", use_container_width=True):
            start_quick_quiz()
        
        if st.button("📊 Balanced Exam (Mixed Difficulty)", use_container_width=True):
            start_balanced_exam(1)
            
        if st.button("🧠 Super Hard Exam", use_container_width=True):
            start_super_hard_exam()
    
    with cols[1]:
        if st.button("🎲 Random Mix (20 Questions)", use_container_width=True):
            start_random_mix()
            
        if st.button("📝 Easy Practice Test", use_container_width=True):
            start_practice_test('easy')
            
        if st.button("📝 Medium Practice Test", use_container_width=True):
            start_practice_test('medium')
    
    if st.button("← Back to Main Menu", use_container_width=True):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

# [Rest of your existing functions remain unchanged...]

# ===== MAIN APP =====
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
