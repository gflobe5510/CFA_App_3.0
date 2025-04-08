
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

# Initialize score and question index
score = 0
current_question = 0

# Streamlit app layout
st.title('Quizlet-like App')

# Display the question
question = questions[current_question]
st.subheader(question["question"])

# Options as radio buttons
user_answer = st.radio("Choose an answer:", question["options"])

# Submit button
if st.button("Submit Answer"):
    # Check if the user's answer is correct
    if user_answer == question["correct_answer"]:
        st.write("✅ Correct!")
        score += 1
    else:
        st.write(f"❌ Incorrect! The correct answer is {question['correct_answer']}.")

    # Update to the next question
    if current_question + 1 < len(questions):
        current_question += 1
        st.experimental_rerun()
    else:
        st.write(f"Quiz Over! Your final score is: {score}/{len(questions)}")
