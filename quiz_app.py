# MUST BE FIRST - PAGE CONFIG
import streamlit as st
st.set_page_config(layout="wide")

import os
import time
import json
import matplotlib.pyplot as plt

# ===== CFA CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"

# Complete topic mapping
TOPIC_TO_CATEGORY = {
    "Ethical & Professional Standards": "Ethical and Professional Standards",
    "Quantitative Methods": "Quantitative Methods", 
    "Economics": "Economics",
    "Financial Reporting & Analysis": "Financial Statement Analysis",
    "Corporate Issuers": "Corporate Issuers",
    "Equity Investments": "Equity Investments",
    "Fixed Income": "Fixed Income",
    "Derivatives": "Derivatives",
    "Alternative Investments": "Alternative Investments",
    "Portfolio Management": "Portfolio Management"
}

# Complete categories data
CATEGORIES = {
    "Ethical and Professional Standards": {
        "description": "Focuses on ethical principles and professional standards",
        "weight": 0.15
    },
    "Quantitative Methods": {
        "description": "Covers statistical tools for financial analysis",
        "weight": 0.10
    },
    "Economics": {
        "description": "Examines macroeconomic and microeconomic concepts",
        "weight": 0.10
    },
    "Financial Statement Analysis": {
        "description": "Analysis of financial statements", 
        "weight": 0.15
    },
    "Corporate Issuers": {
        "description": "Characteristics of corporate issuers",
        "weight": 0.10
    },
    "Equity Investments": {
        "description": "Valuation of equity securities",
        "weight": 0.11
    },
    "Fixed Income": {
        "description": "Analysis of fixed-income securities",
        "weight": 0.11
    },
    "Derivatives": {
        "description": "Valuation of derivative securities",
        "weight": 0.06
    },
    "Alternative Investments": {
        "description": "Hedge funds, private equity, real estate",
        "weight": 0.06
    },
    "Portfolio Management": {
        "description": "Portfolio construction and risk management",
        "weight": 0.06
    }
}

# ===== LOAD QUESTIONS =====
updated_json_path = 'Data/updated_questions_with_5_options_final.json'

def load_questions():
    try:
        with open(updated_json_path, 'r') as f:
            questions_data = json.load(f)
        
        questions_by_category = {cat: [] for cat in CATEGORIES}
        
        for question in questions_data.get("questions", []):
            topic = question.get("topic", "").strip()
            category = TOPIC_TO_CATEGORY.get(topic, topic)
            if category in questions_by_category:
                questions_by_category[category].append(question)
        
        return questions_by_category
        
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return {cat: [] for cat in CATEGORIES}

# ===== QUIZ ENGINE =====
def initialize_session_state():
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
            'all_questions': load_questions(),
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
    
    if 'sidebar_view' not in st.session_state:
        st.session_state.sidebar_view = 'practice'

def show_category_selection():
    st.markdown("## Select a CFA Topic Area")
    
    cols = st.columns(2)
    for i, category in enumerate(CATEGORIES):
        questions = st.session_state.quiz['all_questions'].get(category, [])
        with cols[i % 2]:
            if st.button(
                f"{category} ({len(questions)} questions)",
                disabled=len(questions) == 0,
                help=CATEGORIES[category]["description"]
            ):
                st.session_state.quiz.update({
                    'current_questions': questions,
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
    questions = st.session_state.quiz['current_questions']
    if not questions:
        st.warning("No questions available")
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()
        return
    
    idx = st.session_state.quiz['current_index']
    if idx >= len(questions):
        show_results()
        return
    
    question = questions[idx]
    
    st.progress((idx + 1) / len(questions))
    st.markdown(f"### {st.session_state.quiz['selected_category']}")
    st.markdown(f"**Question {idx + 1} of {len(questions)}**")
    st.markdown(f"*{question['question']}*")
    
    options = question.get('options', [])
    user_answer = st.radio("Select your answer:", options, key=f"q{idx}")
    
    if st.button("Submit Answer"):
        process_answer(question, user_answer)

def process_answer(question, user_answer):
    time_spent = time.time() - st.session_state.quiz['question_start']
    st.session_state.quiz['time_spent'].append(time_spent)
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
        st.rerun()

def show_results():
    quiz = st.session_state.quiz
    total_time = time.time() - quiz['start_time']
    avg_time = sum(quiz['time_spent'])/len(quiz['time_spent']) if quiz['time_spent'] else 0
    
    st.success(f"""
    ## Quiz Completed!
    **Score:** {quiz['score']}/{len(quiz['current_questions'])}
    **Total Time:** {format_time(total_time)}
    **Avg Time/Question:** {format_time(avg_time)}
    """)
    
    display_result_chart()
    
    if st.button("Return to Category Selection"):
        quiz['mode'] = 'category_selection'
        st.rerun()

def display_result_chart():
    score = st.session_state.quiz['score'] / len(st.session_state.quiz['current_questions'])
    fig, ax = plt.subplots()
    ax.bar(['Your Score', 'Benchmark'], [score, 0.75], color=['green', 'blue'])
    ax.set_ylim([0, 1])
    st.pyplot(fig)

def format_time(seconds):
    return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"

# ===== MAIN APP =====
def main():
    st.title(f"📊 {QUIZ_TITLE}")
    
    # Sidebar
    with st.sidebar:
        st.header("Menu")
        if st.button("Practice Test", use_container_width=True):
            st.session_state.sidebar_view = 'practice'
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Track Performance", use_container_width=True):
                st.session_state.sidebar_view = 'performance'
        with col2:
            if st.button("Login", use_container_width=True):
                st.session_state.sidebar_view = 'login'
        
        if st.session_state.sidebar_view == 'performance':
            st.info("Performance tracking coming soon!")
        elif st.session_state.sidebar_view == 'login':
            st.info("Login feature coming soon!")
    
    # Main content
    initialize_session_state()
    
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()
        if st.session_state.quiz['submitted']:
            show_next_button()

if __name__ == "__main__":
    main()# ... (keep all your imports and configuration constants the same)

def load_questions():
    try:
        with open(updated_json_path, 'r') as f:
            updated_questions_data = json.load(f)
        
        questions_by_category = {}
        
        # First initialize all categories with empty lists
        for category in CATEGORIES:
            questions_by_category[category] = []
        
        # Then populate with actual questions
        for question in updated_questions_data.get("questions", []):
            topic = question.get("topic", "Uncategorized")
            # Use direct mapping or default to the topic name
            category = TOPIC_TO_CATEGORY.get(topic, topic)
            if category in questions_by_category:
                questions_by_category[category].append(question)
            else:
                # If we encounter a new category not in our list, add it
                questions_by_category[category] = [question]
        
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

def show_category_selection():
    st.markdown("## Select a CFA Topic Area")
    
    # Get all categories that actually have questions
    available_categories = [
        (cat, len(st.session_state.quiz['all_questions'][cat])) 
        for cat in st.session_state.quiz['all_questions'] 
        if len(st.session_state.quiz['all_questions'][cat]) > 0
    ]
    
    # Also include categories with zero questions but disabled
    all_categories = [
        (cat, len(st.session_state.quiz['all_questions'].get(cat, []))) 
        for cat in CATEGORIES
    ]
    
    # Display in 2-column layout
    cols = st.columns(2)
    for i, (category, question_count) in enumerate(all_categories):
        with cols[i % 2]:
            if st.button(
                f"{category} ({question_count} questions)",
                disabled=question_count == 0,
                help=f"{CATEGORIES[category]['description']}" if category in CATEGORIES else ""
            ):
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

# ... (keep all other functions exactly the same)

def main():
    st.set_page_config(layout="wide")
    st.title(f"📊 {QUIZ_TITLE}")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar buttons
    with st.sidebar:
        st.header("Menu")
        if st.button("Practice Test", key="practice_btn", use_container_width=True):
            st.session_state.sidebar_view = 'practice'
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Track Performance", key="performance_btn", use_container_width=True):
                st.session_state.sidebar_view = 'performance'
        with col2:
            if st.button("Login", key="login_btn", use_container_width=True):
                st.session_state.sidebar_view = 'login'
        
        if st.session_state.sidebar_view == 'practice':
            st.info("Select a topic from the main area")
        elif st.session_state.sidebar_view == 'performance':
            st.info("Performance tracking coming soon!")
        elif st.session_state.sidebar_view == 'login':
            st.info("Login feature coming soon!")
    
    # Main quiz functionality
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()
        if st.session_state.quiz['submitted']:
            show_next_button()

if __name__ == "__main__":
    main()
