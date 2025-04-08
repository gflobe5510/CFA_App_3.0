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

# Initialize session state variables
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

# Streamlit app layout
st.title('Quizlet-like App')

# Display the question
question = questions[st.session_state.current_question]
st.subheader(question["question"])

# Options as radio buttons
user_answer = st.radio("Choose an answer:", question["options"])

# Submit button
if st.button("Submit Answer"):
    # Check if the user's answer is correct
    if user_answer == question["correct_answer"]:
        st.write("✅ Correct!")
        st.session_state.score += 1
    else:
        st.write(f"❌ Incorrect! The correct answer is {question['correct_answer']}.")

    # Update to the next question or end the quiz
    if st.session_state.current_question + 1 < len(questions):
        st.session_state.current_question += 1
    else:
        st.write(f"Quiz Over! Your final score is: {st.session_state.score}/{len(questions)}")
