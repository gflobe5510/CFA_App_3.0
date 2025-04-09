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

# ===== UI COMPONENTS =====
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
    </style>
    """, unsafe_allow_html=True)

# [Rest of your functions would go here...]

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
