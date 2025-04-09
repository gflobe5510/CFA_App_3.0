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
    # ... (other categories remain the same)
}

# ===== CORE FUNCTIONS =====
def load_questions():
    try:
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

def init_progress_tracking():
    if 'progress' not in st.session_state:
        st.session_state.progress = {}

def initialize_session_state():
    if 'initialized' not in st.session_state:
        if not os.path.exists('Data'):
            os.makedirs('Data')
        st.session_state.update({
            'user': {'name': '', 'email': '', 'id': str(uuid.uuid4()), 'identified': False},
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
            'initialized': True
        })
    init_progress_tracking()

# ===== UI COMPONENTS =====
def inject_custom_css():
    st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%); }
        .stButton>button { border-radius: 8px; transition: all 0.3s; }
        .card { background-color: white; border-radius: 10px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

def show_main_menu():
    inject_custom_css()
    
    st.markdown(f"## Welcome to {QUIZ_TITLE}!")
    
    # Resources Section
    with st.container():
        st.markdown("### 📚 Study Resources")
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists(STUDY_GUIDE_PATH):
                with open(STUDY_GUIDE_PATH, "rb") as f:
                    st.download_button("Download Study Guide", f, "CFA_Study_Guide.pdf")
        with col2:
            if st.button("Register for CFA Exam"):
                components.html(f"<script>window.open('{CFA_REGISTRATION_URL}')</script>")
    
    # Practice Options
    with st.container():
        st.markdown("### 🎯 Practice Options")
        if st.button("Custom Practice Exam"):
            st.session_state.quiz['mode'] = 'difficulty_selection'
            st.rerun()
        if st.button("Focused Topic Practice"):
            st.session_state.quiz['mode'] = 'category_selection'
            st.rerun()
        if st.button("View Progress Dashboard"):
            st.session_state.quiz['mode'] = 'progress_tracking'
            st.rerun()

def show_difficulty_selection():
    st.markdown("## Select Practice Mode")
    if st.button("Quick Quiz (5 Questions)"):
        start_quick_quiz()
    if st.button("Balanced Exam"):
        start_balanced_exam(1)
    if st.button("Super Hard Exam"):
        start_super_hard_exam()
    if st.button("Back to Main Menu"):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

def show_category_selection():
    st.markdown("## Select a Topic Area")
    for category in CATEGORIES:
        if st.button(category):
            questions = []
            for difficulty in ['easy', 'medium', 'hard']:
                questions.extend(st.session_state.quiz['all_questions'][category][difficulty])
            st.session_state.quiz.update({
                'current_questions': questions,
                'mode': 'question',
                'selected_category': category
            })
            st.rerun()
    if st.button("Back to Main Menu"):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

# ===== QUIZ FUNCTIONS =====
def display_question():
    questions = st.session_state.quiz['current_questions']
    idx = st.session_state.quiz['current_index']
    
    if idx >= len(questions):
        show_results()
        return
    
    question = questions[idx]
    st.write(f"Question {idx+1} of {len(questions)}")
    st.write(question['question'])
    
    options = question.get('options', [])
    user_answer = st.radio("Select your answer:", options, key=f"q{idx}")
    
    if st.button("Submit"):
        if user_answer == question['correct_answer']:
            st.success("Correct!")
            st.session_state.quiz['score'] += 1
        else:
            st.error(f"Incorrect. The correct answer is: {question['correct_answer']}")
        st.session_state.quiz['current_index'] += 1
        st.rerun()

def show_results():
    st.markdown("## Quiz Completed!")
    st.write(f"Score: {st.session_state.quiz['score']}/{len(st.session_state.quiz['current_questions'])}")
    if st.button("Return to Main Menu"):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

# ===== MAIN APP =====
def main():
    try:
        initialize_session_state()
        
        if st.session_state.quiz['mode'] == 'main_menu':
            show_main_menu()
        elif st.session_state.quiz['mode'] == 'difficulty_selection':
            show_difficulty_selection()
        elif st.session_state.quiz['mode'] == 'category_selection':
            show_category_selection()
        elif st.session_state.quiz['mode'] == 'question':
            display_question()
        elif st.session_state.quiz['mode'] == 'progress_tracking':
            show_progress_tracking()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.button("Return to Main Menu"):
            st.session_state.quiz['mode'] = 'main_menu'
            st.rerun()

if __name__ == "__main__":
    main()
