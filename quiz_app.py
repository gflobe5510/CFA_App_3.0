import streamlit as st
import time
import random

# ===== QUIZ DATA =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"

QUESTIONS = [
    {
        "question": "Which action violates CFA Standards?",
        "options": ["Using client brokerage for research", 
                   "Disclosing transactions without permission", 
                   "Keeping records for 5 years", 
                   "Both A and B"],
        "correct_answer": "Both A and B",
        "category": "Ethical Standards",
        "explanation": "Both A and B violate CFA Standards of Professional Conduct."
    },
    {
        "question": "What's the probability of two heads in three coin tosses?",
        "options": ["0.125", "0.250", "0.375", "0.500"],
        "correct_answer": "0.375",
        "category": "Quantitative Methods",
        "explanation": "Use binomial probability formula."
    }
]

# ===== QUIZ FUNCTIONS =====
def init_session_state():
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
            'current_question': 0,
            'score': 0,
            'answers': []
        }

def show_question():
    q = QUESTIONS[st.session_state.quiz['current_question']]
    
    st.subheader(f"Question {st.session_state.quiz['current_question'] + 1}")
    st.write(q["question"])
    
    user_answer = st.radio("Select your answer:", 
                          q["options"], 
                          key=f"q{st.session_state.quiz['current_question']}")
    
    if st.button("Submit"):
        check_answer(q, user_answer)

def check_answer(question, user_answer):
    is_correct = user_answer == question["correct_answer"]
    
    st.session_state.quiz['answers'].append({
        'question': question["question"],
        'user_answer': user_answer,
        'correct_answer': question["correct_answer"],
        'is_correct': is_correct
    })
    
    if is_correct:
        st.session_state.quiz['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question['correct_answer']}")
    
    st.info(f"Explanation: {question['explanation']}")
    
    if st.button("Next Question"):
        next_question()

def next_question():
    st.session_state.quiz['current_question'] += 1
    if st.session_state.quiz['current_question'] >= len(QUESTIONS):
        show_results()
    else:
        st.rerun()

def show_results():
    st.balloons()
    st.success(f"## Quiz Complete!\nScore: {st.session_state.quiz['score']}/{len(QUESTIONS)}")
    
    if st.button("Restart Quiz"):
        st.session_state.quiz['current_question'] = 0
        st.session_state.quiz['score'] = 0
        st.session_state.quiz['answers'] = []
        st.rerun()

# ===== MAIN APP =====
def main():
    st.set_page_config(page_title=QUIZ_TITLE, layout="wide")
    st.title(f"📊 {QUIZ_TITLE}")
    
    init_session_state()
    
    if st.session_state.quiz['current_question'] < len(QUESTIONS):
        show_question()
    else:
        show_results()

if __name__ == "__main__":
    main()
