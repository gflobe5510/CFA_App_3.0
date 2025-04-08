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
if 'feedback_shown' not in st.session_state:
    st.session_state.feedback_shown = False

# Streamlit app layout
st.title('Quizlet-like App')

# Get the current question
question = questions[st.session_state.current_question]

# Display the question
st.subheader(question["question"])

# Radio buttons for options
if not st.session_state.answered:
    user_answer = st.radio("Choose an answer:", question["options"], key="answer")
    st.session_state.user_answer = user_answer  # Save the user's selected answer
else:
    # If the answer was already submitted, show the feedback
    if st.session_state.user_answer == question["correct_answer"]:
        st.write("✅ Correct!")
        st.session_state.score += 1
    else:
        st.write(f"❌ Incorrect! The correct answer is {question['correct_answer']}")
    st.session_state.feedback_shown = True

# Submit button logic (now hidden after answering)
if not st.session_state.answered:
    submit_button = st.button("Submit Answer", on_click=lambda: submit_answer())  # Submit button shows up

# Function to handle answer submission
def submit_answer():
    # Mark the question as answered and hide the submit button
    st.session_state.answered = True

# Show the "Next Question" button after feedback has been shown
if st.session_state.answered and st.session_state.feedback_shown:
    if st.button("Next Question"):
        # Move to the next question by incrementing the current question index
        st.session_state.current_question += 1
        st.session_state.answered = False  # Reset the answered flag for the next question
        st.session_state.user_answer = None  # Clear previous answer
        st.session_state.feedback_shown = False  # Reset the flag for the next question
