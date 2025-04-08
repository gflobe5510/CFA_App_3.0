import streamlit as st
import random
from datetime import datetime

# Initialize all session state variables
if 'quiz_started' not in st.session_state:
    st.session_state.update({
        'questions': [],  # This will store all our questions
        'current_question': 0,
        'score': 0,
        'quiz_started': False,
        'user_answers': {},
        'show_results': False
    })

# Define all the questions (your complete additional_questions list)
additional_questions = [
    # Ethical and Professional Standards
    {
        "question": "According to the GIPS standards, which of the following must be included in a compliant presentation?",
        "options": [
            "All actual, fee-paying discretionary portfolios",
            "Only portfolios that outperformed the benchmark",
            "Composite returns gross of management fees",
            "Both A and C",
            "All of the above"
        ],
        "correct_answer": "All actual, fee-paying discretionary portfolios",
        "category": "Ethical and Professional Standards",
        "difficulty": "High",
        "explanation": "GIPS requires all actual, fee-paying discretionary portfolios to be included in composites."
    },
    # ... (include all your other questions here)
    # Portfolio Management
    {
        "question": "The primary goal of asset allocation is to:",
        "options": [
            "Maximize returns",
            "Minimize risk",
            "Maximize risk-adjusted returns",
            "Outperform the benchmark",
            "Minimize taxes"
        ],
        "correct_answer": "Maximize risk-adjusted returns",
        "category": "Portfolio Management",
        "difficulty": "Medium",
        "explanation": "Asset allocation aims to optimize the risk-return tradeoff."
    }
]

# Initialize questions if empty
if not st.session_state.questions:
    st.session_state.questions = additional_questions.copy()

def start_quiz():
    st.session_state.update({
        'quiz_started': True,
        'current_question': 0,
        'score': 0,
        'user_answers': {},
        'show_results': False
    })
    random.shuffle(st.session_state.questions)

def next_question():
    if st.session_state.current_question < len(st.session_state.questions) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.show_results = True

def previous_question():
    if st.session_state.current_question > 0:
        st.session_state.current_question -= 1

def check_answer(question_idx, selected_option):
    question = st.session_state.questions[question_idx]
    if selected_option == question["correct_answer"]:
        st.session_state.score += 1
    st.session_state.user_answers[question_idx] = selected_option

def display_question():
    question = st.session_state.questions[st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}")
    st.markdown(f"**Category:** {question['category']} | **Difficulty:** {question['difficulty']}")
    st.markdown(f"**{question['question']}**")
    
    answer_key = f"q_{st.session_state.current_question}"
    if answer_key not in st.session_state.user_answers:
        st.session_state.user_answers[answer_key] = None
    
    selected_option = st.radio(
        "Select your answer:",
        options=question["options"],
        index=question["options"].index(st.session_state.user_answers[answer_key]) 
        if st.session_state.user_answers[answer_key] in question["options"] else 0,
        key=answer_key
    )
    
    if st.button("Submit Answer") and st.session_state.user_answers[answer_key] is None:
        st.session_state.user_answers[answer_key] = selected_option
        check_answer(st.session_state.current_question, selected_option)
        st.experimental_rerun()

def display_results():
    st.header("Quiz Results")
    score_percentage = (st.session_state.score / len(st.session_state.questions)) * 100
    st.metric("Your Score", f"{st.session_state.score}/{len(st.session_state.questions)} ({score_percentage:.1f}%)")
    
    for i, question in enumerate(st.session_state.questions):
        st.subheader(f"Question {i+1}")
        st.markdown(f"**{question['question']}**")
        
        user_answer = st.session_state.user_answers.get(f"q_{i}", "Not answered")
        is_correct = user_answer == question["correct_answer"]
        
        st.markdown(f"Your answer: {'✅' if is_correct else '❌'} {user_answer}")
        if not is_correct:
            st.markdown(f"Correct answer: {question['correct_answer']}")
        st.markdown(f"*Explanation:* {question['explanation']}")
        st.write("---")

def main():
    st.title("CFA Quiz App")
    st.write("Test your knowledge of CFA Level I concepts")
    
    if not st.session_state.quiz_started:
        st.write(f"Total questions: {len(st.session_state.questions)}")
        st.write("Click below to begin the quiz:")
        if st.button("Start Quiz"):
            start_quiz()
    else:
        if st.session_state.show_results:
            display_results()
            if st.button("Retake Quiz"):
                start_quiz()
        else:
            display_question()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.current_question > 0:
                    st.button("Previous Question", on_click=previous_question)
            with col2:
                if st.session_state.current_question < len(st.session_state.questions) - 1:
                    st.button("Next Question", on_click=next_question)
                else:
                    st.button("Finish Quiz", on_click=lambda: st.session_state.update({'show_results': True}))

if __name__ == "__main__":
    main()
