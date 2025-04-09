# MUST BE FIRST - PAGE CONFIG
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    layout="centered",
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

# ===== CUSTOM CSS =====
def inject_custom_css():
    st.markdown("""
    <style>
        /* Title styling with line break support */
        .title-text {
            text-align: center;
            margin-bottom: 1rem;
            line-height: 1.3;
        }
        
        /* Button styling */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            padding: 10px;
            font-weight: 500;
            margin: 5px 0;
        }
        
        /* Section headers */
        .section-header {
            text-align: center;
            margin: 1.5rem 0 0.5rem 0;
        }
        
        /* Divider styling */
        .divider {
            margin: 1rem 0;
            border: none;
            height: 1px;
            background-color: #eee;
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

# ===== TOPIC AND CATEGORY CONFIGURATION =====
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

# ===== INITIALIZATION FUNCTIONS =====
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

# ===== QUESTION LOADING =====
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

# ===== MAIN MENU UI =====
def show_main_menu():
    inject_custom_css()
    
    # Title with line break to match screenshot
    st.markdown(f"""
    <h1 class="title-text">
        Welcome to CFA Exam Preparation<br>Pro!
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Study Resources Section
    st.markdown("### Study Resources")
    if os.path.exists(STUDY_GUIDE_PATH):
        with open(STUDY_GUIDE_PATH, "rb") as pdf_file:
            st.download_button(
                "Download Study Guide",
                data=pdf_file,
                file_name="CFA_Study_Guide.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.warning("Study guide not found in Data folder")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Practice Options Section
    st.markdown("### Practice Options")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Custom Practice Exam",
                   use_container_width=True):
            st.session_state.quiz['mode'] = 'difficulty_selection'
            st.rerun()
        
    with col2:
        if st.button("Focused Topic Practice",
                   use_container_width=True):
            st.session_state.quiz['mode'] = 'category_selection'
            st.rerun()
    
    if st.button("View Progress Dashboard",
               use_container_width=True):
        st.session_state.quiz['mode'] = 'progress_tracking'
        st.rerun()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Registration Section
    if st.button("Register for CFA Exam", 
               use_container_width=True):
        components.html(f"""
            <script>window.open('{CFA_REGISTRATION_URL}')</script>
        """)

# [Rest of your existing functions remain unchanged...]

# ===== MAIN APP =====
def main():
    try:
        # Initialize the app
        initialize_session_state()
        
        # Main app routing
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
