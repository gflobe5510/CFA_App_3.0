import streamlit as st

# Define questions, options, and correct answers
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome", "London"],
        "correct_answer": "Paris"
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6", "7"],
        "correct_answer": "4"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn", "Venus"],
        "correct_answer": "Mars"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific", "Southern"],
        "correct_answer": "Pacific"
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["Newton", "Einstein", "Galileo", "Darwin", "Tesla"],
        "correct_answer": "Einstein"
    }
]

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.update({
        'score': 0,
        'current_question': 0,
        'user_answer': None,
        'answered': False,
        'score_updated': False,
        'show_next_button': False  # New state to control button display
    })

# Quiz layout
st.title('Quiz App')

# Check if quiz is finished
if st.session_state.current_question >= len(questions):
    st.success(f"🎉 Quiz completed! Final score: {st.session_state.score}/{len(questions)}")
    if st.button("Restart Quiz"):
        # Reset all quiz-related state
        st.session_state.update({
            'score': 0,
            'current_question': 0,
            'user_answer': None,
            'answered': False,
            'score_updated': False,
            'show_next_button': False
        })
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
    
    # Submit button logic
    if not st.session_state.answered:
        if st.button("Submit Answer"):
            st.session_state.user_answer = user_answer
            st.session_state.answered = True
            st.session_state.show_next_button = True
            # Check answer immediately
            if user_answer == question["correct_answer"]:
                st.session_state.score += 1
                st.session_state.score_updated = True

    # Show feedback after answer submission
    if st.session_state.answered:
        if st.session_state.user_answer == question["correct_answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect! The correct answer is: {question['correct_answer']}")

        # Next Question button - only show when appropriate
        if st.session_state.show_next_button and st.button("Next Question"):
            # Move to next question
            st.session_state.current_question += 1
            # Reset question-specific state
            st.session_state.update({
                'user_answer': None,
                'answered': False,
                'score_updated': False,
                'show_next_button': False
            })
