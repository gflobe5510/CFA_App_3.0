import streamlit as st

# Expanded 50-question quiz with 5 options each
questions = [
    # Geography (10 questions)
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome", "Lisbon"],
        "correct_answer": "Paris",
        "category": "Geography"
    },
    {
        "question": "Which country has the largest population?",
        "options": ["India", "USA", "China", "Indonesia", "Brazil"],
        "correct_answer": "China",
        "category": "Geography"
    },
    # Add more questions following the same format...
    
    # Sample additional questions
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag", "Pt"],
        "correct_answer": "Au",
        "category": "Science"
    },
    {
        "question": "In what year did World War II end?",
        "options": ["1943", "1945", "1950", "1939", "1941"],
        "correct_answer": "1945",
        "category": "History"
    }
    # Continue adding questions until you reach 50...
]

# Initialize session state
if 'quiz' not in st.session_state:
    st.session_state.quiz = {
        'score': 0,
        'current_question': 0,
        'user_answer': None,
        'submitted': False,
        'show_next': False,
        'start_time': None,
        'category_scores': {}
    }

# Quiz layout
st.title('🧠 Mega Quiz (50 Questions)')
st.caption("Test your knowledge across multiple categories!")

# Progress tracker
if len(questions) > 0:  # Prevent division by zero
    progress = st.session_state.quiz['current_question'] / len(questions)
    st.progress(progress)
    st.caption(f"Question {st.session_state.quiz['current_question'] + 1} of {len(questions)}")

# Quiz completion check
if st.session_state.quiz['current_question'] >= len(questions):
    st.balloons()
    percentage = round((st.session_state.quiz['score']/len(questions))*100) if len(questions) > 0 else 0
    st.success(f"""
    🎉 Quiz completed!
    Final score: {st.session_state.quiz['score']}/{len(questions)}
    ({percentage}%)
    """)
    
    if st.button("🔄 Restart Quiz"):
        st.session_state.quiz = {
            'score': 0,
            'current_question': 0,
            'user_answer': None,
            'submitted': False,
            'show_next': False,
            'start_time': None,
            'category_scores': {}
        }
        st.rerun()
else:
    question = questions[st.session_state.quiz['current_question']]
    
    # Display category tag
    if 'category' in question:
        st.markdown(f"**Category:** {question['category']}")
    
    st.subheader(question["question"])

    # Answer submission phase
    if not st.session_state.quiz['submitted']:
        user_answer = st.radio(
            "Select your answer:",
            question["options"],
            key=f"q{st.session_state.quiz['current_question']}"
        )
        
        if st.button("📥 Submit Answer"):
            st.session_state.quiz['user_answer'] = user_answer
            st.session_state.quiz['submitted'] = True
            st.session_state.quiz['show_next'] = True
            
            # Update scores
            if user_answer == question["correct_answer"]:
                st.session_state.quiz['score'] += 1
                # Track category scores
                if 'category' in question:
                    category = question['category']
                    st.session_state.quiz['category_scores'][category] = st.session_state.quiz['category_scores'].get(category, 0) + 1
            
            st.rerun()

    # Feedback phase
    if st.session_state.quiz['submitted']:
        if st.session_state.quiz['user_answer'] == question["correct_answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect! The correct answer is: **{question['correct_answer']}**")
        
        # Next question button
        if st.session_state.quiz['show_next'] and st.button("⏭️ Next Question"):
            st.session_state.quiz['current_question'] += 1
            st.session_state.quiz['submitted'] = False
            st.session_state.quiz['show_next'] = False
            st.session_state.quiz['user_answer'] = None
            st.rerun()
