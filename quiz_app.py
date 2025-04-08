import streamlit as st
import time
import random

# Debugging setup
DEBUG = True  # Set to False after testing

def log(message):
    if DEBUG:
        st.sidebar.write(f"DEBUG: {message}")

# ===== SIMPLIFIED QUIZ DATA =====
QUIZ_TITLE = "CFA Quiz (Working Version)"

QUESTIONS = [
    {
        "question": "Which violates CFA Standards?",
        "options": ["Using client brokerage for research", 
                   "Disclosing transactions without permission", 
                   "Proper record keeping"],
        "correct_answer": "Disclosing transactions without permission",
        "explanation": "CFA Standard III(E) requires confidentiality."
    },
    {
        "question": "What's 2+2?",
        "options": ["3", "4", "5"],
        "correct_answer": "4",
        "explanation": "Basic math."
    }
]

# ===== CORE FUNCTIONS =====
def init_state():
    if 'quiz' not in st.session_state:
        log("Initializing new session state")
        st.session_state.quiz = {
            'index': 0,
            'score': 0,
            'started': False
        }

def reset_quiz():
    log("Resetting quiz")
    st.session_state.quiz = {
        'index': 0,
        'score': 0,
        'started': True
    }

def show_question():
    q = QUESTIONS[st.session_state.quiz['index']]
    log(f"Showing question {st.session_state.quiz['index']}")
    
    st.write(f"### Question {st.session_state.quiz['index'] + 1}")
    st.write(q["question"])
    
    user_choice = st.radio("Choose:", q["options"], key=f"q{st.session_state.quiz['index']}")
    
    if st.button("Submit"):
        check_answer(q, user_choice)

def check_answer(q, user_choice):
    log(f"User answered: {user_choice}")
    
    if user_choice == q["correct_answer"]:
        st.session_state.quiz['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. Correct answer: {q['correct_answer']}")
    
    st.info(f"Explanation: {q['explanation']}")
    
    if st.button("Next ➡️"):
        next_question()

def next_question():
    st.session_state.quiz['index'] += 1
    log(f"Moving to question {st.session_state.quiz['index']}")
    
    if st.session_state.quiz['index'] >= len(QUESTIONS):
        show_results()
    else:
        st.rerun()

def show_results():
    st.balloons()
    st.success(f"## Quiz Complete!\nScore: {st.session_state.quiz['score']}/{len(QUESTIONS)}")
    
    if st.button("🔄 Restart Quiz"):
        reset_quiz()
        st.rerun()

# ===== MAIN APP =====
def main():
    st.set_page_config(
        page_title=QUIZ_TITLE,
        page_icon="📊",
        layout="centered"
    )
    
    st.title(f"📊 {QUIZ_TITLE}")
    init_state()
    
    if not st.session_state.quiz['started']:
        if st.button("Start Quiz"):
            reset_quiz()
            st.rerun()
    else:
        if st.session_state.quiz['index'] < len(QUESTIONS):
            show_question()
        else:
            show_results()
    
    # Debug info
    if DEBUG:
        st.sidebar.write("## Debug Info")
        st.sidebar.json(st.session_state.quiz)

if __name__ == "__main__":
    main()
