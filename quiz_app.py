import streamlit as st

# Define questions, options, and correct answers
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "correct_answer": "Paris"
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": "4"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "correct_answer": "Mars"
    }
]

# Initialize all session state variables at once
if 'quiz' not in st.session_state:
    st.session_state.quiz = {
        'score': 0,
        'current_question': 0,
        'user_answer': None,
        'submitted': False,
        'show_next': False  # New state to control button visibility
    }

st.title('Quiz App')

# Quiz completion check
if st.session_state.quiz['current_question'] >= len(questions):
    st.success(f"🎉 Quiz completed! Final score: {st.session_state.quiz['score']}/{len(questions)}")
    if st.button("Restart Quiz"):
        st.session_state.quiz = {
            'score': 0,
            'current_question': 0,
            'user_answer': None,
            'submitted': False,
            'show_next': False
        }
        st.rerun()
else:
    question = questions[st.session_state.quiz['current_question']]
    st.subheader(question["question"])

    # Answer submission phase
    if not st.session_state.quiz['submitted']:
        user_answer = st.radio(
            "Choose your answer:",
            question["options"],
            key=f"q{st.session_state.quiz['current_question']}"
        )
        
        if st.button("Submit Answer"):
            st.session_state.quiz['user_answer'] = user_answer
            st.session_state.quiz['submitted'] = True
            st.session_state.quiz['show_next'] = True
            
            # Update score if correct
            if user_answer == question["correct_answer"]:
                st.session_state.quiz['score'] += 1
            
            # Force immediate UI update
            st.rerun()

    # Feedback and next question phase
    if st.session_state.quiz['submitted']:
        if st.session_state.quiz['user_answer'] == question["correct_answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect! The correct answer is: {question['correct_answer']}")

        # Next question button - will work with single click
        if st.session_state.quiz['show_next'] and st.button("Next Question"):
            st.session_state.quiz['current_question'] += 1
            st.session_state.quiz['submitted'] = False
            st.session_state.quiz['show_next'] = False
            st.session_state.quiz['user_answer'] = None
            # Force immediate UI update
            st.rerun()
