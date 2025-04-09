import os
import streamlit as st
import time
import json
import matplotlib.pyplot as plt

# ===== CFA CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"

# Mapping between JSON topics and UI categories
TOPIC_TO_CATEGORY = {
    "Ethical & Professional Standards": "Ethical and Professional Standards",
    "Financial Reporting & Analysis": "Financial Statement Analysis",
    # Add all your other topic mappings here
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
    # Include all your other categories here
    # ...
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
    
    # Initialize sidebar button states
    if 'sidebar_view' not in st.session_state:
        st.session_state.sidebar_view = 'practice'

def show_category_selection():
    st.markdown("## Select a CFA Topic Area")
    
    # Get all available categories that have questions
    available_categories = [
        cat for cat in CATEGORIES 
        if cat in st.session_state.quiz['all_questions'] and 
        len(st.session_state.quiz['all_questions'][cat]) > 0
    ]
    
    # Display all categories in a 2-column layout
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

# ... (keep all your other quiz functions exactly as they were)

# ===== MAIN APP =====
def main():
    st.set_page_config(layout="wide")
    st.title(f"📊 {QUIZ_TITLE}")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar buttons - these won't interfere with the main content
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
        
        # Display sidebar content based on selection
        if st.session_state.sidebar_view == 'practice':
            st.info("Select a topic from the main area to begin")
        elif st.session_state.sidebar_view == 'performance':
            st.info("Performance tracking coming soon!")
        elif st.session_state.sidebar_view == 'login':
            st.info("Login feature coming soon!")
    
    # Main quiz functionality - this runs independently of sidebar
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()  # This will show ALL available categories
    elif st.session_state.quiz['mode'] == 'question':
        display_question()
        if st.session_state.quiz['submitted']:
            show_next_button()

if __name__ == "__main__":
    main()
