import streamlit as st

# Define your questions, options, and correct answers
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

# Initialize session state variables if not already set
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

# Streamlit app layout
st.title('Quizlet-like App')

# Check if quiz is finished
if st.session_state.current_question >= len(questions):
    st.success(f"Quiz completed! Your final score: {st.session_state.score}/{len(questions)}")
    if st.button("Restart Quiz"):
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.user_answer = None
        st.session_state.answered = False
else:
    # Get the current question
    question = questions[st.session_state.current_question]

    # Display the question
    st.subheader(question["question"])

    # Radio buttons for options (only if not answered yet)
    if not st.session_state.answered:
        user_answer = st.radio("Choose an answer:", question["options"], key=f"answer_{st.session_state.current_question}")
        st.session_state.user_answer = user_answer  # Save the user's selected answer

        # Submit button logic
        if st.button("Submit Answer"):
            st.session_state.answered = True
            # No need for a separate submit_answer() function
    else:
        # Show feedback after submission
        if st.session_state.user_answer == question["correct_answer"]:
            st.success("✅ Correct!")
            st.session_state.score += 1  # Update score only once
        else:
            st.error(f"❌ Incorrect! The correct answer is {question['correct_answer']}")

        # Next Question button (appears after feedback)
        if st.button("Next Question"):
            # Move to next question and reset state
            st.session_state.current_question += 1
            st.session_state.answered = False
            st.session_state.user_answer = None
            # Streamlit auto-reruns, so no need for st.rerun()
