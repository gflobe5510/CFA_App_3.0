import os
import streamlit as st
import time
import json
from typing import Dict, List, Optional, Set

# ===== CFA CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"
CATEGORIES = {
    "Ethical and Professional Standards": {
        "description": "Focuses on ethical principles and professional standards",
        "weight": 0.15,
        "readings": ["Code of Ethics", "Standards of Professional Conduct", "GIPS"]
    },
    "Quantitative Methods": {
        "description": "Covers statistical tools for financial analysis",
        "weight": 0.10,
        "readings": ["Time Value of Money", "Probability Concepts"]
    },
    "Economics": {
        "description": "Examines macroeconomic and microeconomic concepts",
        "weight": 0.10,
        "readings": ["Demand and Supply", "Business Cycles"]
    },
    "Financial Statement Analysis": {
        "description": "Analysis of financial statements",
        "weight": 0.15,
        "readings": ["Income Statements", "Balance Sheets"]
    },
    "Corporate Issuers": {
        "description": "Characteristics of corporate issuers",
        "weight": 0.10,
        "readings": ["Capital Structure", "Corporate Governance"]
    },
    "Equity Investments": {
        "description": "Valuation of equity securities",
        "weight": 0.11,
        "readings": ["Market Organization", "Equity Valuation"]
    },
    "Fixed Income": {
        "description": "Analysis of fixed-income securities",
        "weight": 0.11,
        "readings": ["Bond Valuation", "Yield Measures"]
    },
    "Derivatives": {
        "description": "Valuation of derivative securities",
        "weight": 0.06,
        "readings": ["Forwards and Futures", "Options"]
    },
    "Alternative Investments": {
        "description": "Hedge funds, private equity, real estate",
        "weight": 0.06,
        "readings": ["Private Capital", "Real Estate"]
    },
    "Portfolio Management": {
        "description": "Portfolio construction and risk management",
        "weight": 0.06,
        "readings": ["Portfolio Risk", "Investment Policy"]
    }
}

# ===== LOAD QUESTIONS =====
def load_questions():
    """Load questions from the JSON file in the original format"""
    try:
        # Using your original file path and loading method
        updated_json_path = '/mnt/data/updated_questions_with_5_options_final.json'
        with open(updated_json_path, 'r') as f:
            updated_questions_data = json.load(f)
        
        # Process questions into categories as in your original code
        questions_by_category = {}
        for question in updated_questions_data.get("questions", []):
            category = question.get("topic", "Uncategorized")
            if category not in questions_by_category:
                questions_by_category[category] = []
            questions_by_category[category].append(question)
        
        return questions_by_category
    
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return {}

# ===== QUIZ ENGINE =====
def initialize_session_state():
    """Initialize the session state with your original structure"""
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
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
            'selected_category': None
        }

def show_category_selection():
    """Your original category selection with minor improvements"""
    st.markdown("## Select a CFA Topic Area")
    
    # Count questions per category as in original
    category_counts = {category: len(questions) 
                      for category, questions in st.session_state.quiz['all_questions'].items()}
    
    # Display buttons in columns as before
    cols = st.columns(2)
    for i, category in enumerate(CATEGORIES):
        with cols[i % 2]:
            if st.button(f"{category} ({category_counts.get(category, 0)} questions)"):
                # Original question loading logic
                st.session_state.quiz['current_questions'] = st.session_state.quiz['all_questions'].get(category, [])
                st.session_state.quiz['current_index'] = 0
                st.session_state.quiz['mode'] = 'question'
                st.session_state.quiz['selected_category'] = category
                st.session_state.quiz['question_start'] = time.time()
                st.session_state.quiz['submitted'] = False
                st.experimental_rerun()

def display_question():
    """Your original question display with safe improvements"""
    if not st.session_state.quiz['current_questions']:
        st.warning("No questions available for this category")
        st.session_state.quiz['mode'] = 'category_selection'
        st.experimental_rerun()
        return
    
    try:
        question = st.session_state.quiz['current_questions'][st.session_state.quiz['current_index']]
    except IndexError:
        st.session_state.quiz['mode'] = 'results'
        st.experimental_rerun()
        return
    
    # Original display format
    st.markdown(f"### {question['topic']}")
    st.markdown(f"**Question {st.session_state.quiz['current_index'] + 1} of {len(st.session_state.quiz['current_questions'])}**")
    st.markdown(f"*{question['question']}*")
    
    # Original options display
    user_answer = st.radio("Select your answer:", question['options'], key=f"q{st.session_state.quiz['current_index']}")
    
    # Original submit button
    if st.button("Submit Answer"):
        process_answer(question, user_answer)

def process_answer(question, user_answer):
    """Your original answer processing"""
    time_spent = time.time() - st.session_state.quiz['question_start']
    st.session_state.quiz['time_spent'].append(time_spent)
    
    st.session_state.quiz['user_answer'] = user_answer
    st.session_state.quiz['submitted'] = True
    
    if user_answer == question['correct_answer']:
        st.session_state.quiz['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question['correct_answer']}")
    
    if 'explanation' in question:
        st.info(f"**Explanation:** {question['explanation']}")

def show_next_button():
    """Original navigation logic"""
    if st.session_state.quiz['current_index'] >= len(st.session_state.quiz['current_questions']) - 1:
        show_results()
    else:
        st.session_state.quiz['current_index'] += 1
        st.session_state.quiz['submitted'] = False
        st.session_state.quiz['question_start'] = time.time()
        st.experimental_rerun()

def show_results():
    """Original results display with formatting improvements"""
    total_time = time.time() - st.session_state.quiz['start_time']
    avg_time = sum(st.session_state.quiz['time_spent'])/len(st.session_state.quiz['time_spent']) if st.session_state.quiz['time_spent'] else 0
    
    st.success(f"""
    ## Quiz Completed!
    **Score:** {st.session_state.quiz['score']}/{len(st.session_state.quiz['current_questions'])}
    **Total Time:** {format_time(total_time)}
    **Avg Time/Question:** {format_time(avg_time)}
    """)
    
    if st.button("Return to Category Selection"):
        st.session_state.quiz['mode'] = 'category_selection'
        st.experimental_rerun()

def format_time(seconds):
    """Original time formatting"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

# ===== MAIN APP =====
def main():
    st.set_page_config(layout="wide")
    st.title(f"📊 {QUIZ_TITLE}")
    
    initialize_session_state()
    
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()
        if st.session_state.quiz['submitted']:
            show_next_button()
    else:
        show_results()

if __name__ == "__main__":
    main()
