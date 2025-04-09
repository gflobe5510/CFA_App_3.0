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

def load_questions(file_path: str) -> Dict[str, List[dict]]:
    """Load questions from JSON file and organize by category."""
    try:
        with open(file_path, 'r') as f:
            questions_data = json.load(f)
        
        questions_by_category = {}
        for question in questions_data.get("questions", []):
            category = question.get("topic", "Uncategorized")
            if category not in questions_by_category:
                questions_by_category[category] = []
            questions_by_category[category].append(question)
        
        return questions_by_category
    
    except FileNotFoundError:
        st.error("Question database not found. Please check the file path.")
        return {}
    except json.JSONDecodeError:
        st.error("Invalid question database format.")
        return {}

def initialize_session_state():
    """Initialize or reset the session state."""
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
            'all_questions': load_questions('/mnt/data/updated_questions_with_5_options_final.json'),
            'current_questions': [],
            'score': 0,
            'current_index': 0,
            'user_answers': {},
            'submitted': False,
            'start_time': time.time(),
            'question_start': time.time(),
            'time_spent': [],
            'mode': 'category_selection',
            'selected_category': None,
            'marked_for_review': set()
        }

def show_progress_bar():
    """Display progress through current question set."""
    if st.session_state.quiz['current_questions']:
        progress = (st.session_state.quiz['current_index'] + 1) / len(st.session_state.quiz['current_questions'])
        st.progress(min(progress, 1.0))

def show_category_selection():
    """Display category selection interface."""
    st.markdown("## Select a CFA Topic Area")
    
    category_counts = {category: len(questions) 
                      for category, questions in st.session_state.quiz['all_questions'].items()}
    
    cols = st.columns(2)
    for i, category in enumerate(CATEGORIES):
        with cols[i % 2]:
            if st.button(f"{category} ({category_counts.get(category, 0)} questions)"):
                start_quiz(category)

def start_quiz(category: str):
    """Initialize quiz for selected category."""
    st.session_state.quiz.update({
        'current_questions': st.session_state.quiz['all_questions'].get(category, []),
        'current_index': 0,
        'mode': 'question',
        'selected_category': category,
        'question_start': time.time(),
        'submitted': False,
        'score': 0,
        'user_answers': {},
        'time_spent': [],
        'start_time': time.time(),
        'marked_for_review': set()
    })

def display_question():
    """Display current question and handle user interaction."""
    questions = st.session_state.quiz['current_questions']
    if not questions:
        st.warning("No questions available for this category")
        st.session_state.quiz['mode'] = 'category_selection'
        return
    
    current_idx = st.session_state.quiz['current_index']
    if current_idx >= len(questions):
        st.session_state.quiz['mode'] = 'results'
        return
    
    question = questions[current_idx]
    
    # Display question info
    st.markdown(f"### {question['topic']}")
    st.markdown(f"**Question {current_idx + 1} of {len(questions)}**")
    
    # Mark for review toggle
    review_key = f"review_{current_idx}"
    if st.checkbox("Mark for review", key=review_key):
        st.session_state.quiz['marked_for_review'].add(current_idx)
    elif current_idx in st.session_state.quiz['marked_for_review']:
        st.session_state.quiz['marked_for_review'].remove(current_idx)
    
    st.markdown(f"*{question['question']}*")
    
    # Display options (using index as key to maintain state between questions)
    user_answer = st.radio(
        "Select your answer:",
        question['options'],
        key=f"q_{current_idx}"
    )
    
    # Submit button
    if st.button("Submit Answer"):
        process_answer(question, user_answer, current_idx)

def process_answer(question: dict, user_answer: str, question_idx: int):
    """Process user's answer and update quiz state."""
    time_spent = time.time() - st.session_state.quiz['question_start']
    st.session_state.quiz['time_spent'].append(time_spent)
    
    st.session_state.quiz['user_answers'][question_idx] = {
        'answer': user_answer,
        'correct': user_answer == question['correct_answer'],
        'time': time_spent
    }
    
    st.session_state.quiz['submitted'] = True
    
    if user_answer == question['correct_answer']:
        st.session_state.quiz['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question['correct_answer']}")
    
    if 'explanation' in question:
        st.info(f"**Explanation:** {question['explanation']}")

def show_navigation_buttons():
    """Display navigation buttons (Next, Previous, etc.)."""
    col1, col2, col3 = st.columns([1, 1, 2])
    
    current_idx = st.session_state.quiz['current_index']
    total_questions = len(st.session_state.quiz['current_questions'])
    
    with col1:
        if current_idx > 0:
            if st.button("◀ Previous"):
                navigate_question(-1)
    
    with col2:
        if current_idx < total_questions - 1:
            if st.button("Next ▶"):
                navigate_question(1)
        else:
            if st.button("Finish Quiz"):
                st.session_state.quiz['mode'] = 'results'
    
    with col3:
        if st.button("🚪 Exit to Categories"):
            st.session_state.quiz['mode'] = 'category_selection'

def navigate_question(direction: int):
    """Move to next/previous question."""
    st.session_state.quiz['current_index'] += direction
    st.session_state.quiz['submitted'] = False
    st.session_state.quiz['question_start'] = time.time()
    st.experimental_rerun()

def show_results():
    """Display quiz results and statistics."""
    total_questions = len(st.session_state.quiz['current_questions'])
    score = st.session_state.quiz['score']
    total_time = time.time() - st.session_state.quiz['start_time']
    avg_time = sum(st.session_state.quiz['time_spent']) / total_questions if total_questions > 0 else 0
    
    st.success(f"""
    ## Quiz Completed! 🎉
    **Category:** {st.session_state.quiz['selected_category']}
    **Score:** {score}/{total_questions} ({score/total_questions:.0%})
    **Total Time:** {format_time(total_time)}
    **Avg Time/Question:** {format_time(avg_time)}
    """)
    
    # Performance breakdown
    st.markdown("### Performance Breakdown")
    correct_counts = {cat: 0 for cat in CATEGORIES}
    total_counts = {cat: 0 for cat in CATEGORIES}
    
    for idx, answer in st.session_state.quiz['user_answers'].items():
        category = st.session_state.quiz['current_questions'][idx]['topic']
        total_counts[category] = total_counts.get(category, 0) + 1
        if answer['correct']:
            correct_counts[category] = correct_counts.get(category, 0) + 1
    
    st.write("**Accuracy by Topic:**")
    for category, correct in correct_counts.items():
        total = total_counts.get(category, 1)
        st.write(f"- {category}: {correct}/{total} ({correct/total:.0%})")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Review Questions"):
            st.session_state.quiz['mode'] = 'review'
    with col2:
        if st.button("📚 Return to Categories"):
            st.session_state.quiz['mode'] = 'category_selection'

def format_time(seconds: float) -> str:
    """Format time in MM:SS format."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def main():
    st.set_page_config(layout="wide", page_title=QUIZ_TITLE)
    st.title(f"📊 {QUIZ_TITLE}")
    
    initialize_session_state()
    
    # Sidebar - only show in question mode
    if st.session_state.quiz['mode'] == 'question':
        with st.sidebar:
            st.markdown(f"**Category:** {st.session_state.quiz['selected_category']}")
            show_progress_bar()
            if st.session_state.quiz['submitted']:
                current = st.session_state.quiz['current_index'] + 1
                total = len(st.session_state.quiz['current_questions'])
                st.markdown(f"**Progress:** {current}/{total}")
                st.markdown(f"**Score:** {st.session_state.quiz['score']}/{current}")
    
    # Main content area
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()
        if st.session_state.quiz['submitted']:
            show_navigation_buttons()
    elif st.session_state.quiz['mode'] == 'results':
        show_results()

if __name__ == "__main__":
    main()
