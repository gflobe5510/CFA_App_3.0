import streamlit as st

# Define questions, options, and correct answers
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome", "London"],  # Added a 5th option
        "correct_answer": "Paris"
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6", "7"],  # Added a 5th option
        "correct_answer": "4"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn", "Venus"],  # Added a 5th option
        "correct_answer": "Mars"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific", "Southern"],  # Added a 5th option
        "correct_answer": "Pacific"
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["Newton", "Einstein", "Galileo", "Darwin", "Tesla"],  # Added a 5th option
        "correct_answer": "Einstein"
    }
]

# Initialize session state if not already set
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

# Quiz layout
st.title('Quiz App')

# Check if quiz is finished
if st.session_state.current_question >= len(questions):
    # Show success message and final score
    st.success(f"🎉 Quiz completed! Final score: {st.session_state.score}/{len(questions)}")
    if st.button("Restart Quiz"):
        # Reset the session state for the quiz
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.user_answer = None
        st.session_state.answered = False
        st.experimental_rerun()  # Restart the app and reset everything

else:
    question = questions[st.session_state.current_question]
    st.subheader(question["question"])

    # Show radio buttons only if not answered
    if not st.session_state.answered:
        user_answer = st.radio(
            "Choose an answer:", 
            question["options"], 
            key=f"answer_{st.session_state.current_question}"  # Unique key per question
        )
        
        # Submit button
        if st.button("Submit Answer"):
            st.session_state.user_answer = user_answer
            st.session_state.answered = True  # Mark as answered

    # If answered, show feedback and "Next Question" button
    else:
        if st.session_state.user_answer == question["correct_answer"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrect! The correct answer is: {question['correct_answer']}")

        # Next Question button
        if st.button("Next Question"):
            # Move to the next question
            st.session_state.current_question += 1
            st.session_state.answered = False  # Reset for next question
            st.session_state.user_answer = None  # Clear previous answer
            st.experimental_rerun()  # Restart the app and move to the next question
