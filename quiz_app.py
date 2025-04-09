import os
import streamlit as st
import time
import json
import random
import matplotlib.pyplot as plt

# Print the current working directory
print("Current working directory:", os.getcwd())

# ===== CFA CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"

# Mapping between JSON topics and UI categories
TOPIC_TO_CATEGORY = {
    "Ethical & Professional Standards": "Ethical and Professional Standards",
    "Financial Reporting & Analysis": "Financial Statement Analysis",
    # Add other mappings if needed
}

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

# ===== LOAD QUESTIONS =====
updated_json_path = 'Data/updated_questions_with_5_options_final.json'

def load_questions():
    try:
        with open(updated_json_path, 'r') as f:
            updated_questions_data = json.load(f)
        
        questions_by_category = {}
        for question in updated_questions_data.get("questions", []):
            topic = question.get("topic", "Uncategorized")
            category = TOPIC_TO_CATEGORY.get(topic, topic)
            if category not in questions_by_category:
                questions_by_category[category] = []
            questions_by_category[category].append(question)
        
        return questions_by_category
        
    except FileNotFoundError:
        st.error(f"❌ Critical Error: JSON file not found at {updated_json_path}")
        st.error(f"Current working directory: {os.getcwd()}")
        st.stop()
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON format in questions file")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected error loading questions: {str(e)}")
        st.stop()

# ===== QUIZ ENGINE =====
def initialize_session_state():
    if 'quiz' not in st.session_state:
        questions_by_category = load_questions()
        
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
    
    available_categories = [
        cat for cat in CATEGORIES 
        if cat in st.session_state.quiz['all_questions'] and 
        len(st.session_state.quiz['all_questions'][cat]) > 0
    ]
    
    cols = st.columns(2)
    for i, category in enumerate(available_categories):
        with cols[i % 2]:
            if st.button(f"{category} ({len(st.session_state.quiz['all_questions'][category])} questions)"):
                st.session_state.quiz.update({
                    'current_questions': st.session_state.quiz['all_questions'][category],
                    'current_index': 0,
                    'mode': 'question',
                    'selected_category': category,
                    'question_start': time.time(),
                    'submitted': False,
                    'score': 0,
                    'time_spent': []
                })
                st.rerun()

def display_question():
    if not st.session_state.quiz['current_questions']:
        st.warning("No questions available for this category")
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()
        return
    
    question = st.session_state.quiz['current_questions'][st.session_state.quiz['current_index']]
    
    st.progress((st.session_state.quiz['current_index'] + 1) / len(st.session_state.quiz['current_questions']))
    st.markdown(f"### {st.session_state.quiz['selected_category']}")
    st.markdown(f"**Question {st.session_state.quiz['current_index'] + 1} of {len(st.session_state.quiz['current_questions'])}**")
    st.markdown(f"*{question['question']}*")
    
    options = question.get('options', question.get('choices', ["Error: No options provided"]))
    user_answer = st.radio("Select your answer:", options, key=f"q{st.session_state.quiz['current_index']}")
    
    if st.button("Submit Answer"):
        process_answer(question, user_answer)

def process_answer(question, user_answer):
    time_spent = time.time() - st.session_state.quiz['question_start']
    st.session_state.quiz['time_spent'].append(time_spent)

    # Update score
    if user_answer == question['correct_answer']:
        st.session_state.quiz['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question['correct_answer']}")

    # Move to the next question
    st.session_state.quiz['current_index'] += 1
    st.session_state.quiz['question_start'] = time.time()

    # Reload the next question or finish test
    st.experimental_rerun()

def show_results():
    total_time = time.time() - st.session_state.quiz['start_time']
    avg_time = sum(st.session_state.quiz['time_spent']) / len(st.session_state.quiz['time_spent']) if st.session_state.quiz['time_spent'] else 0
    
    st.success(f"""
    ## Quiz Completed!
    **Score:** {st.session_state.quiz['score']}/{len(st.session_state.quiz['current_questions'])}
    **Total Time:** {format_time(total_time)}
    **Avg Time/Question:** {format_time(avg_time)}
    """)

    if st.button("Return to Category Selection"):
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

# ===== PRACTICE TEST SECTION =====
def show_practice_test():
    st.markdown("## Practice Test")
    st.markdown("Select a topic or take a random test.")

    # Option to select a specific topic or go random
    topic_choice = st.radio("Choose test type:", ["Random Test", "Specific Topic"])

    if topic_choice == "Specific Topic":
        # List of categories from your available topics
        topic_options = list(CATEGORIES.keys())
        selected_topic = st.selectbox("Select a topic:", topic_options)
        
        if st.button("Start Test"):
            start_practice_test(selected_topic)

    elif topic_choice == "Random Test":
        if st.button("Start Random Test"):
            start_practice_test(random.choice(list(CATEGORIES.keys())))

def start_practice_test(selected_topic):
    # Initialize or reset the session state for practice test
    st.session_state.practice_test = {
        'selected_topic': selected_topic,
        'current_questions': st.session_state.quiz['all_questions'][selected_topic],
        'current_index': 0,
        'score': 0,
        'time_spent': [],
        'start_time': time.time(),
        'question_start': time.time(),
    }

    display_practice_test_question()

def display_practice_test_question():
    practice_test = st.session_state.practice_test

    # Check if we have questions left
    if practice_test['current_index'] >= len(practice_test['current_questions']):
        show_practice_test_results()  # Once all questions are completed
        return

    question = practice_test['current_questions'][practice_test['current_index']]

    # Show question
    st.markdown(f"### {question['question']}")
    options = question['options']
    user_answer = st.radio("Select your answer:", options, key=f"q{practice_test['current_index']}")

    # Show submit button for answer
    if st.button("Submit Answer"):
        process_practice_answer(question, user_answer)

def process_practice_answer(question, user_answer):
    practice_test = st.session_state.practice_test
    time_spent = time.time() - practice_test['question_start']
    practice_test['time_spent'].append(time_spent)

    # Update score
    if user_answer == question['correct_answer']:
        practice_test['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: {question['correct_answer']}")

    # Move to the next question
    practice_test['current_index'] += 1
    practice_test['question_start'] = time.time()

    # Reload the next question or finish test
    st.experimental_rerun()

def show_practice_test_results():
    practice_test = st.session_state.practice_test
    total_time = time.time() - practice_test['start_time']
    avg_time = sum(practice_test['time_spent']) / len(practice_test['time_spent']) if practice_test['time_spent'] else 0

    st.success(f"""
    ## Practice Test Completed!
    **Score:** {practice_test['score']}/{len(practice_test['current_questions'])}
    **Total Time:** {format_time(total_time)}
    **Avg Time/Question:** {format_time(avg_time)}
    """)

    # Option to review the missed questions
    if st.button("Review Missed Questions"):
        review_missed_questions(practice_test)

    if st.button("Take Another Test"):
        st.session_state.practice_test = {}
        st.experimental_rerun()

def review_missed_questions(practice_test):
    missed_questions = []
    for idx, question in enumerate(practice_test['current_questions']):
        user_answer = st.session_state.quiz['user_answer']  # Track user's previous answer
        if user_answer != question['correct_answer']:
            missed_questions.append(question)

    if missed_questions:
        st.markdown("## Review Missed Questions")
        for question in missed_questions:
            st.markdown(f"### {question['question']}")
            st.markdown(f"**Explanation:** {question['explanation']}")
            st.markdown(f"**Correct Answer:** {question['correct_answer']}")
            st.markdown("---")
    else:
        st.success("You answered all questions correctly!")

# ===== MAIN APP =====
def main():
    st.set_page_config(layout="wide")
    st.title(f"📊 {QUIZ_TITLE}")
    
    if 'quiz' in st.session_state and 'practice_test' not in st.session_state:
        show_category_selection()  # If no test in progress, show category selection
    elif 'practice_test' in st.session_state:
        display_practice_test_question()  # If a practice test is active, display questions
    else:
        show_practice_test()  # Start Practice Test when the user selects to do so

if __name__ == "__main__":
    main()
