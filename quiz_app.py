# MUST BE FIRST - PAGE CONFIG
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    layout="wide",
    page_title="CFA Exam Prep Pro",
    page_icon="📊"
)

import os
import time
import json
import matplotlib.pyplot as plt
import random
import uuid
import base64
import numpy as np
from datetime import datetime
from io import BytesIO

# ===== CUSTOM CSS =====
def inject_custom_css():
    st.markdown("""
    <style>
        /* [Keep all your existing CSS styles] */
        .profile-expander {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #3498db;
        }
    </style>
    """, unsafe_allow_html=True)

# ===== CFA CONFIGURATION ===== 
QUIZ_TITLE = "CFA Exam Preparation Pro"
CFA_REGISTRATION_URL = "https://www.cfainstitute.org/"
STUDY_GUIDE_PATH = "Data/CFA_Study_Guide.pdf"
REGISTRATION_TIPS = """
• Early registration discounts available
• Prepare payment method in advance  
• Have identification documents ready
• Check exam schedule carefully
"""

# [Keep all your existing TOPIC_TO_CATEGORY and CATEGORIES dictionaries]

# ===== USER PROFILE SYSTEM =====
def initialize_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.update({
            'user': {
                'name': '',
                'email': '',
                'id': str(uuid.uuid4()),
                'identified': False
            },
            'quiz': {
                'all_questions': load_questions(),
                'current_questions': [],
                'score': 0,
                'current_index': 0,
                'user_answer': None,
                'submitted': False,
                'start_time': time.time(),
                'question_start': time.time(),
                'time_spent': [],
                'mode': 'main_menu',
                'selected_category': None,
                'test_type': None,
                'exam_number': None
            },
            'sidebar_view': 'practice',
            'initialized': True,
            'confirm_registration': True
        })
    init_progress_tracking()

def show_user_profile():
    with st.expander("🔐 Personalize Your Experience", expanded=not st.session_state.user['identified']):
        with st.form("user_profile"):
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Name (optional)", 
                                   value=st.session_state.user['name'],
                                   help="For personalizing your reports")
            with cols[1]:
                email = st.text_input("Email (optional)", 
                                    value=st.session_state.user['email'],
                                    help="For cross-device progress sync")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.form_submit_button("💾 Save Profile"):
                    st.session_state.user['name'] = name.strip()
                    st.session_state.user['email'] = email.strip()
                    st.session_state.user['identified'] = bool(name.strip() or email.strip())
                    st.success("Preferences saved!")
                    st.rerun()
            with col2:
                if st.button("🔄 Reset My Progress", help="Clear all your progress data"):
                    reset_progress()
            with col3:
                if st.button("👤 Switch Profile", help="Start a new anonymous session"):
                    switch_profile()

def reset_progress():
    user_key = f"user_{st.session_state.user['id']}"
    if user_key in st.session_state.progress:
        del st.session_state.progress[user_key]
        try:
            with open('Data/progress_data.json', 'w') as f:
                json.dump(st.session_state.progress, f)
        except:
            st.error("Could not save progress data")
        st.success("Progress reset successfully!")
        st.rerun()

def switch_profile():
    st.session_state.user = {
        'name': '',
        'email': '',
        'id': str(uuid.uuid4()),
        'identified': False
    }
    st.rerun()

# ===== ENHANCED PROGRESS TRACKING =====
def save_progress(score, total_questions, total_time, category=None):
    init_progress_tracking()
    
    user_key = f"user_{st.session_state.user['id']}"
    if user_key not in st.session_state.progress:
        st.session_state.progress[user_key] = {
            'attempts': [],
            'scores': [],
            'time_spent': [],
            'dates': [],
            'topic_scores': {},
            'name': st.session_state.user['name'],
            'email': st.session_state.user['email']
        }
    
    user_progress = st.session_state.progress[user_key]
    user_progress['attempts'].append(len(user_progress['attempts']) + 1)
    user_progress['scores'].append(score/total_questions)
    user_progress['time_spent'].append(total_time)
    user_progress['dates'].append(datetime.now().strftime("%Y-%m-%d"))
    
    if category:
        user_progress['topic_scores'][category] = score/total_questions
    
    try:
        with open('Data/progress_data.json', 'w') as f:
            json.dump(st.session_state.progress, f)
    except:
        st.error("Could not save progress data")

def create_topic_performance_chart(topic_scores):
    topics = list(CATEGORIES.keys())
    benchmark = [0.75] * len(topics)
    user_scores = [topic_scores.get(topic, 0) for topic in topics]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ind = np.arange(len(topics))
    width = 0.35
    
    # Plot bars
    ax.barh(ind - width/2, benchmark, width, color='#95a5a6', label='Benchmark (75%)')
    ax.barh(ind + width/2, user_scores, width, color='#3498db', label='Your Score')
    
    # Customize chart
    ax.set_yticks(ind)
    ax.set_yticklabels(topics)
    ax.set_xlim([0, 1])
    ax.set_title('Topic Performance vs Benchmark', pad=20)
    ax.set_xlabel('Score')
    ax.legend()
    
    # Add value labels
    for i, (bench, score) in enumerate(zip(benchmark, user_scores)):
        ax.text(bench + 0.01, i - width/2, f'{bench:.0%}', va='center', color='#2c3e50')
        ax.text(score + 0.01, i + width/2, f'{score:.0%}', va='center', color='#2c3e50')
    
    plt.tight_layout()
    
    # Convert to HTML
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    plt.close(fig)
    return f"<img src='data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}' style='width:100%'>"

# [Keep all your existing LOAD QUESTIONS functions]

# ===== MAIN MENU WITH ENHANCED PROGRESS =====
def show_main_menu():
    inject_custom_css()
    show_user_profile()
    
    user_key = f"user_{st.session_state.user['id']}"
    progress_data = st.session_state.progress.get(user_key, {})
    
    # Personalized welcome
    if st.session_state.user['name']:
        st.markdown(f"### Welcome back, {st.session_state.user['name']}!")
    else:
        st.markdown("### Welcome to CFA Exam Prep Pro!")
    
    # Enhanced progress summary
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">📊 Your Study Analytics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if progress_data.get('topic_scores'):
        st.markdown(f"""
        <div class='card'>
            {create_topic_performance_chart(progress_data['topic_scores'])}
        </div>
        """, unsafe_allow_html=True)
    
    # [Rest of your existing show_main_menu content]
    
# [Keep all your existing QUIZ ENGINE functions]
# [Update save_progress calls to include category when applicable]

# ===== MAIN APP =====
def main():
    initialize_session_state()
    
    if st.session_state.quiz['mode'] == 'main_menu':
        show_main_menu()
    elif st.session_state.quiz['mode'] == 'progress_tracking':
        show_progress_tracking()
    elif st.session_state.quiz['mode'] == 'difficulty_selection':
        show_difficulty_selection()
    elif st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()

if __name__ == "__main__":
    main()
