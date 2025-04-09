import os
import streamlit as st
import time
import json

# Print the current working directory
print("Current working directory:", os.getcwd())

# ===== CFA CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"
CATEGORIES = {
    "Ethical and Professional Standards": {
        "description": "Focuses on ethical principles and professional standards",
        "weight": 0.15,
        "readings": ["Code of Ethics", "Standards of Professional Conduct", "GIPS"]
    },
    "Quantitative Methods": {
        "description": "Covers statistical tools for financial analysis",
        "weight": 0.10,
        "readings": ["Time Value of Money", "Probability Concepts"]
    },
    "Economics": {
        "description": "Examines macroeconomic and microeconomic concepts",
        "weight": 0.10,
        "readings": ["Demand and Supply", "Business Cycles"]
    },
    "Financial Statement Analysis": {
        "description": "Analysis of financial statements",
        "weight": 0.15,
        "readings": ["Income Statements", "Balance Sheets"]
    },
    "Corporate Issuers": {
        "description": "Characteristics of corporate issuers",
        "weight": 0.10,
        "readings": ["Capital Structure", "Corporate Governance"]
    },
    "Equity Investments": {
        "description": "Valuation of equity securities",
        "weight": 0.11,
        "readings": ["Market Organization", "Equity Valuation"]
    },
    "Fixed Income": {
        "description": "Analysis of fixed-income securities",
        "weight": 0.11,
        "readings": ["Bond Valuation", "Yield Measures"]
    },
    "Derivatives": {
        "description": "Valuation of derivative securities",
        "weight": 0.06,
        "readings": ["Forwards and Futures", "Options"]
    },
    "Alternative Investments": {
        "description": "Hedge funds, private equity, real estate",
        "weight": 0.06,
        "readings": ["Private Capital", "Real Estate"]
    },
    "Portfolio Management": {
        "description": "Portfolio construction and risk management",
        "weight": 0.06,
        "readings": ["Portfolio Risk", "Investment Policy"]
    }
}

# ===== LOAD QUESTIONS BY CATEGORY =====
# Load the updated JSON file with 5 options
updated_json_path = 'Data/updated_questions_with_5_options_final.json'  # Correct path to the file

# Check if the file path is correct by printing the file path
print("Loading JSON file from:", updated_json_path)

with open(updated_json_path, 'r') as f:
    updated_questions_data = json.load(f)

# Extract questions by category
questions_by_category = {}
for question in updated_questions_data.get("questions", []):
    category = question.get("category", "Uncategorized")
    if category not in questions_by_category:
        questions_by_category[category] = []
    questions_by_category[category].append(question)

# ===== QUIZ ENGINE =====
def initialize_session_state():
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
            'all_questions': questions_by_category,
            'current_questions': [],
            'score': 0,
            'current_index': 0,
            'user_answer': None,
            'submitted': False,
            'start_time': time.time(),
            'question_start': time.time(),
            'time_spent': [],
            'mode': 'category_selection',
            'selected_category': None
        }

def show_category_selection():
    st.markdown("## Select a CFA Topic Area")
    
    # Count questions per category
    category_counts = {category: len(questions) for category, questions in questions_by_category.items()}
    
    # Display buttons for each category
    cols = st.columns(2)
    for i, category in enumerate(CATEGORIES):
        with cols[i % 2]:
            if st.button(f"{category} ({category_counts.get(category, 0)} questions)"):
                # Filter questions for selected category
                st.session_state.quiz['current_questions'] = questions_by_category.get(category, [])
                st.session_state.quiz['current_index'] = 0
                st.session_state.quiz['mode'] = 'question'
                st.session_state.quiz['selected_category'] = category
                st.session_state.quiz['question_start'] = time.time()
                st.session_state.quiz['submitted'] = False
                st.experimental_rerun()

def display_question():
    # Check if we have questions to display
    if not st.session_state.quiz['current_questions']:
        st.warning("No questions available for this category")
        st.session_state.quiz['mode'] = 'category_selection'
        st.experimental_rerun()  # Only call rerun here when the mode changes
        return
    
    # Safely get current question
    try:
        question = st.session_state.quiz['current_questions'][st.session_state.quiz['current_index']]
    except IndexError:
        st.error("Question index out of range. Returning to category selection.")
        st.session_state.quiz['mode'] = 'category_selection'
        st.experimental_rerun()  # Only call rerun here when the mode changes
        return
    
    # Display question info
    st.markdown(f"### {question['category']}")
    st.markdown(f"**Question {st.session_state.quiz['current_index'] + 1} of {len(st.session_state.quiz['current_questions'])}**")
    st.markdown(f"*{question['question']}*")
    
    # Display options
    user_answer = st.radio("Select your answer:", question['options'], key=f"q{st.session_state.quiz['current_index']}")
    
    # Submit button
    if st.button("Submit Answer"):
        process_answer(question, user_answer)

def process_answer(question, user_answer):
    time_spent = time.time() - st.session_state.quiz['question_start']
    st.session_state.quiz['time_spent'].append(time_spent)
    
    st.session_state.quiz['user_answer'] = user_answer
    st.session_state.quiz['submitted'] = True
    
    if user_answer == question['correct_answer']:
        st.session_state.quiz['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question['correct_answer']}")
    
    if 'explanation' in question:
        st.info(f"**Explanation:** {question['explanation']}")

def show_next_button():
    if st.button("Next Question"):
        st.session_state.quiz['current_index'] += 1
        st.session_state.quiz['submitted'] = False
        st.session_state.quiz['question_start'] = time.time()
        
        if st.session_state.quiz['current_index'] >= len(st.session_state.quiz['current_questions']):
            show_results()
        else:
            st.experimental_rerun()  # Only call rerun here when the mode changes

def show_results():
    total_time = time.time() - st.session_state.quiz['start_time']
    avg_time = sum(st.session_state.quiz['time_spent'])/len(st.session_state.quiz['time_spent']) if st.session_state.quiz['time_spent'] else 0
    
    st.success(f"""
    ## Quiz Completed!
    **Score:** {st.session_state.quiz['score']}/{len(st.session_state.quiz['current_questions'])}
    **Total Time:** {format_time(total_time)}
    **Avg Time/Question:** {format_time(avg_time)}
    """)
    
    if st.button("Return to Category Selection"):
        st.session_state.quiz['mode'] = 'category_selection'
        st.experimental_rerun()  # Only call rerun here when the mode changes

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

# ===== MAIN APP =====
def main():
    st.set_page_config(layout="wide")
    st.title(f"📊 {QUIZ_TITLE}")
    
    initialize_session_state()
    
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()
        if st.session_state.quiz['submitted']:
            show_next_button()
    else:
        show_results()

if __name__ == "__main__":
    main()
