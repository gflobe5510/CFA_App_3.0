# MUST BE FIRST - PAGE CONFIG
import streamlit as st
st.set_page_config(layout="wide")

import os
import time
import json
import matplotlib.pyplot as plt
import random

# ===== CFA CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"

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
updated_json_path = 'Data/updated_questions_with_5_options_final.json'

def load_questions():
    try:
        with open(updated_json_path, 'r') as f:
            questions_data = json.load(f)
        
        questions_by_category = {cat: {'easy': [], 'medium': [], 'hard': []} for cat in CATEGORIES}
        
        for question in questions_data.get("questions", []):
            topic = question.get("topic", "").strip()
            category = TOPIC_TO_CATEGORY.get(topic, topic)
            difficulty = question.get("difficulty", "medium").lower()  # Default to medium if not specified
            
            if category in questions_by_category and difficulty in ['easy', 'medium', 'hard']:
                questions_by_category[category][difficulty].append(question)
        
        return questions_by_category
        
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return {cat: {'easy': [], 'medium': [], 'hard': []} for cat in CATEGORIES}

# ===== QUIZ ENGINE =====
def initialize_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.update({
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
                'mode': 'category_selection',
                'selected_category': None,
                'test_type': None  # 'category' or 'practice_test'
            },
            'sidebar_view': 'practice',
            'initialized': True
        })

def show_category_selection():
    st.markdown("## Select a CFA Topic Area")
    
    cols = st.columns(2)
    for i, category in enumerate(CATEGORIES):
        # Calculate total questions across all difficulties
        total_questions = sum(len(st.session_state.quiz['all_questions'][category][d]) 
                          for d in ['easy', 'medium', 'hard'])
        
        with cols[i % 2]:
            if st.button(
                f"{category} ({total_questions} questions)",
                disabled=total_questions == 0,
                help=CATEGORIES[category]["description"]
            ):
                # Combine questions from all difficulties for category practice
                questions = []
                for difficulty in ['easy', 'medium', 'hard']:
                    questions.extend(st.session_state.quiz['all_questions'][category][difficulty])
                
                st.session_state.quiz.update({
                    'current_questions': questions,
                    'current_index': 0,
                    'mode': 'question',
                    'selected_category': category,
                    'question_start': time.time(),
                    'submitted': False,
                    'score': 0,
                    'time_spent': [],
                    'test_type': 'category'
                })
                st.rerun()

def start_practice_test(difficulty):
    questions = []
    for category in CATEGORIES:
        category_questions = st.session_state.quiz['all_questions'][category].get(difficulty, [])
        if category_questions:
            # Take up to 2 questions per category for the practice test
            questions.extend(random.sample(category_questions, min(2, len(category_questions))))
    
    if not questions:
        st.error(f"No {difficulty} questions available for practice test")
        return
    
    random.shuffle(questions)  # Mix questions from different categories
    
    st.session_state.quiz.update({
        'current_questions': questions,
        'current_index': 0,
        'mode': 'question',
        'selected_category': f"Practice Test ({difficulty})",
        'question_start': time.time(),
        'submitted': False,
        'score': 0,
        'time_spent': [],
        'test_type': 'practice_test'
    })
    st.rerun()

def display_question():
    questions = st.session_state.quiz['current_questions']
    if not questions:
        st.warning("No questions available")
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()
        return
    
    idx = st.session_state.quiz['current_index']
    if idx >= len(questions):
        show_results()
        return
    
    question = questions[idx]
    
    st.progress((idx + 1) / len(questions))
    st.markdown(f"### {st.session_state.quiz['selected_category']}")
    st.markdown(f"**Question {idx + 1} of {len(questions)}**")
    
    # Display difficulty if available
    if 'difficulty' in question:
        difficulty = question['difficulty'].capitalize()
        st.markdown(f"*Difficulty: {difficulty}*")
    
    st.markdown(f"*{question['question']}*")
    
    options = question.get('options', [])
    user_answer = st.radio("Select your answer:", options, key=f"q{idx}")
    
    if st.button("Submit Answer"):
        process_answer(question, user_answer)

# ... (keep process_answer, show_next_button, show_results, display_result_chart, format_time the same)

# ===== MAIN APP =====
def main():
    st.title(f"📊 {QUIZ_TITLE}")
    
    # Initialize session state first
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.header("Practice Tests")
        st.markdown("**Full-length practice tests by difficulty:**")
        
        if st.button("Easy Practice Test", use_container_width=True):
            start_practice_test('easy')
        
        if st.button("Medium Practice Test", use_container_width=True):
            start_practice_test('medium')
        
        if st.button("Hard Practice Test", use_container_width=True):
            start_practice_test('hard')
        
        st.markdown("---")
        st.markdown("**Practice by topic:**")
        if st.button("Show All Topics", use_container_width=True):
            st.session_state.quiz['mode'] = 'category_selection'
            st.rerun()
    
    # Main content
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()
        if st.session_state.quiz['submitted']:
            show_next_button()

if __name__ == "__main__":
    main()
