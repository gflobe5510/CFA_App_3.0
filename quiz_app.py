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
    # Add other mappings if needed
}

CATEGORIES = {
    "Ethical and Professional Standards": {
        "description": "Focuses on ethical principles and professional standards",
        "weight": 0.15,
        "readings": ["Code of Ethics", "Standards of Professional Conduct", "GIPS"]
    },
    # ... (rest of your CATEGORIES dictionary remains the same)
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

# ... (rest of your quiz functions remain the same until main())

# ===== MAIN APP =====
def main():
    st.set_page_config(layout="wide")  # This should be the first Streamlit command in the script
    st.title(f"📊 {QUIZ_TITLE}")
    
    # Practice Test section in sidebar - Now all buttons
    with st.sidebar:
        if st.button("Practice Test", use_container_width=True, 
                    help="Start a new practice test"):
            st.session_state.show_practice = True
            st.session_state.show_performance = False
            st.session_state.show_login = False
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Track Performance", use_container_width=True,
                        help="View your performance metrics"):
                st.session_state.show_performance = True
                st.session_state.show_practice = False
                st.session_state.show_login = False
                
        with col2:
            if st.button("Login", use_container_width=True,
                        help="Access your account"):
                st.session_state.show_login = True
                st.session_state.show_practice = False
                st.session_state.show_performance = False
    
    # Display content based on button clicks
    if st.session_state.get('show_practice', True):  # Default to showing practice
        st.sidebar.success("Practice test options will appear here")
        
    if st.session_state.get('show_performance'):
        st.sidebar.info("Performance tracking dashboard will be displayed here")
        
    if st.session_state.get('show_login'):
        st.sidebar.info("Login form will be displayed here")
    
    initialize_session_state()
    
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()
        if st.session_state.quiz['submitted']:
            show_next_button()

if __name__ == "__main__":
    main()
