import streamlit as st
import time
import random
from typing import Dict, List, Optional

# Simplified version without advanced typing for wider compatibility
QUIZ_TITLE = "CFA Exam Preparation Quiz"

CATEGORIES = {
    "Ethical and Professional Standards": {
        "description": "Focuses on ethical principles and professional standards",
        "weight": 0.15,
        "readings": ["Code of Ethics", "Standards of Professional Conduct", "GIPS"]
    },
    # ... (other categories remain the same as your original)
}

questions = [
    {
        "question": "Which action violates CFA Standards?",
        "options": ["Using client brokerage for research", "Disclosing transactions without permission", 
                   "Keeping records for 5 years", "Both A and B", "All of the above"],
        "correct_answer": "Both A and B",
        "category": "Ethical and Professional Standards",
        "difficulty": "High",
        "explanation": "Standard III(A) requires acting for client benefit, III(E) requires confidentiality."
    },
    # ... (other questions remain the same as your original)
]

def initialize_session_state():
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
            'all_questions': questions,
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

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def show_category_selection():
    st.markdown("## Select a CFA Topic Area")
    
    category_counts = {}
    for q in st.session_state.quiz['all_questions']:
        category_counts[q['category']] = category_counts.get(q['category'], 0) + 1
    
    cols = st.columns(2)
    for i, category in enumerate(CATEGORIES):
        with cols[i % 2]:
            if st.button(f"{category} ({category_counts.get(category, 0)} questions)"):
                st.session_state.quiz['current_questions'] = [
                    q for q in st.session_state.quiz['all_questions'] 
                    if q['category'] == category
                ]
                random.shuffle(st.session_state.quiz['current_questions'])
                st.session_state.quiz.update({
                    'current_index': 0,
                    'mode': 'question',
                    'selected_category': category,
                    'question_start': time.time(),
                    'submitted': False,
                    'score': 0,
                    'time_spent': []
                })
                st.rerun()

def display_question():
    if not st.session_state.quiz['current_questions']:
        st.warning("No questions available for this category")
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()
        return
    
    question = st.session_state.quiz['current_questions'][st.session_state.quiz['current_index']]
    
    st.markdown(f"### {question['category']}")
    st.markdown(f"**Question {st.session_state.quiz['current_index'] + 1} of {len(st.session_state.quiz['current_questions'])}**")
    st.markdown(f"*{question['question']}*")
    
    user_answer = st.radio(
        "Select your answer:",
        question['options'],
        key=f"q{st.session_state.quiz['current_index']}",
        index=None
    )
    
    if st.button("Submit Answer", disabled=user_answer is None):
        process_answer(question, user_answer)

def process_answer(question, user_answer):
    time_spent = time.time() - st.session_state.quiz['question_start']
    st.session_state.quiz['time_spent'].append(time_spent)
    st.session_state.quiz['user_answer'] = user_answer
    st.session_state.quiz['submitted'] = True
    
    if user_answer == question['correct_answer']:
        st.session_state.quiz['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question['correct_answer']}")
    
    st.info(f"**Explanation:** {question['explanation']}")

def show_next_button():
    if st.button("Next Question"):
        st.session_state.quiz['current_index'] += 1
        st.session_state.quiz['submitted'] = False
        st.session_state.quiz['question_start'] = time.time()
        
        if st.session_state.quiz['current_index'] >= len(st.session_state.quiz['current_questions']):
            show_results()
        else:
            st.rerun()

def show_results():
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
        st.rerun()

def main():
    st.set_page_config(layout="wide", page_title=QUIZ_TITLE)
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
