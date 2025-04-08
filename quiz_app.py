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

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = None
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'score_updated' not in st.session_state:  # To prevent double-counting
    st.session_state.score_updated = False

# Quiz layout
st.title('Quiz App')

# Check if quiz is finished
if st.session_state.current_question >= len(questions):
    st.success(f"🎉 Quiz completed! Final score: {st.session_state.score}/{len(questions)}")
    if st.button("Restart Quiz"):
        # Manually reset session state for restart
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.user_answer = None
        st.session_state.answered = False
        st.session_state.score_updated = False  # Reset score tracking flag
        st.experimental_rerun()  # Restart the app

else:
    question = questions[st.session_state.current_question]
    st.subheader(question["question"])

    # Show radio buttons (disabled if already answered)
    user_answer = st.radio(
        "Choose an answer:", 
        question["options"], 
        key=f"answer_{st.session_state.current_question}",
        disabled=st.session_state.answered
    )
    
    # Submit button (only if not answered)
    submit_button = st.button("Submit Answer")
    if submit_button and not st.session_state.answered:
        st.session_state.user_answer = user_answer
        st.session_state.answered = True  # Mark as answered
        # Update score if correct and prevent multiple updates
        if st.session_state.user_answer == question["correct_answer"] and not st.session_state.score_updated:
            st.session_state.score += 1
            st.session_state.score_updated = True

    # If answered, show feedback and "Next Question" button
    if st.session_state.answered:
        if st.session_state.user_answer == question["correct_answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect! The correct answer is: {question['correct_answer']}")

        # Next Question button (only appears after feedback is shown)
        if st.button("Next Question"):
            st.session_state.current_question += 1
            st.session_state.answered = False  # Reset for next question
            st.session_state.user_answer = None  # Clear previous answer
            st.session_state.score_updated = False  # Reset score update flag
