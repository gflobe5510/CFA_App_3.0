# MUST BE FIRST - PAGE CONFIG
import streamlit as st
st.set_page_config(layout="wide")

import os
import time
import json
import matplotlib.pyplot as plt
import random
import webbrowser
from datetime import datetime

# ===== CFA CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"
CFA_REGISTRATION_URL = "https://www.cfainstitute.org/en/programs/cfa/exam"
STUDY_GUIDE_PATH = "Data/CFA_Study_Guide.pdf"  # Update with your actual PDF path

# Complete topic mapping and categories data remain the same...

# ===== NEW PROGRESS TRACKING SYSTEM =====
def init_progress_tracking():
    if 'progress' not in st.session_state:
        st.session_state.progress = {
            'attempts': [],
            'scores': [],
            'time_spent': [],
            'dates': []
        }

def save_progress(score, total_questions, total_time):
    init_progress_tracking()
    st.session_state.progress['attempts'].append(len(st.session_state.progress['attempts']) + 1)
    st.session_state.progress['scores'].append(score/total_questions)
    st.session_state.progress['time_spent'].append(total_time)
    st.session_state.progress['dates'].append(datetime.now().strftime("%Y-%m-%d"))
    
    # Save to JSON file
    try:
        with open('Data/progress_data.json', 'w') as f:
            json.dump(st.session_state.progress, f)
    except:
        st.error("Could not save progress data")

def show_progress_tracking():
    st.markdown("## Your Study Progress")
    
    # Load progress data
    try:
        with open('Data/progress_data.json', 'r') as f:
            progress_data = json.load(f)
    except:
        progress_data = st.session_state.progress
    
    if not progress_data['attempts']:
        st.info("No progress data yet. Complete some quizzes to track your progress!")
        return
    
    # Progress Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Attempts", len(progress_data['attempts']))
    with col2:
        avg_score = sum(progress_data['scores'])/len(progress_data['scores'])
        st.metric("Average Score", f"{avg_score:.1%}")
    with col3:
        total_time = sum(progress_data['time_spent'])/60
        st.metric("Total Study Time", f"{total_time:.1f} minutes")
    
    # Progress Charts
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    
    # Score progression
    ax[0].plot(progress_data['attempts'], progress_data['scores'], marker='o')
    ax[0].set_title("Score Improvement Over Time")
    ax[0].set_xlabel("Attempt Number")
    ax[0].set_ylabel("Score (%)")
    ax[0].set_ylim(0, 1)
    ax[0].grid(True)
    
    # Time spent
    ax[1].bar(progress_data['attempts'], progress_data['time_spent'])
    ax[1].set_title("Time Spent per Attempt")
    ax[1].set_xlabel("Attempt Number")
    ax[1].set_ylabel("Time (seconds)")
    ax[1].grid(True)
    
    st.pyplot(fig)
    
    # Detailed Progress Table
    st.markdown("### Detailed Progress History")
    progress_table = {
        "Attempt": progress_data['attempts'],
        "Date": progress_data['dates'],
        "Score": [f"{s:.1%}" for s in progress_data['scores']],
        "Time Spent": [f"{t//60}m {t%60}s" for t in progress_data['time_spent']]
    }
    st.table(progress_table)
    
    st.markdown("---")
    if st.button("← Back to Main Menu"):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

# ===== UPDATED MAIN MENU =====
def show_main_menu():
    st.markdown(f"## {QUIZ_TITLE}")
    
    # New Resources Section
    st.markdown("### 📚 Study Resources")
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        if os.path.exists(STUDY_GUIDE_PATH):
            with open(STUDY_GUIDE_PATH, "rb") as pdf_file:
                st.download_button(
                    label="📘 Download Study Guide",
                    data=pdf_file,
                    file_name="CFA_Study_Guide.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.warning("Study guide not found", help="Please ensure STUDY_GUIDE_PATH is correct")
    with res_col2:
        if st.button("🌐 Register for CFA Exam", use_container_width=True):
            webbrowser.open_new_tab(CFA_REGISTRATION_URL)
    with res_col3:
        if st.button("📈 Track My Progress", use_container_width=True):
            st.session_state.quiz['mode'] = 'progress_tracking'
            st.rerun()
    
    # Practice Options
    st.markdown("### 🎯 Practice Options")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Practice Exams", use_container_width=True, 
                    help="Full-length practice tests"):
            st.session_state.quiz['mode'] = 'difficulty_selection'
            st.rerun()
    with col2:
        if st.button("📚 Practice by Topic", use_container_width=True,
                    help="Select specific topics to practice"):
            st.session_state.quiz['mode'] = 'category_selection'
            st.rerun()
    
    # Quick Stats
    st.markdown("---")
    st.markdown("### Your Quick Stats")
    try:
        with open('Data/progress_data.json', 'r') as f:
            progress_data = json.load(f)
        attempts = len(progress_data['attempts'])
        avg_score = f"{sum(progress_data['scores'])/attempts:.1%}" if attempts > 0 else "N/A"
        st.write(f"📊 Total Attempts: {attempts} | 🎯 Average Score: {avg_score}")
    except:
        st.info("Complete your first quiz to see stats here")

# ===== MODIFIED SHOW RESULTS =====
def show_results():
    quiz = st.session_state.quiz
    total_time = time.time() - quiz['start_time']
    avg_time = sum(quiz['time_spent'])/len(quiz['time_spent']) if quiz['time_spent'] else 0
    
    # Save progress
    save_progress(quiz['score'], len(quiz['current_questions']), total_time)
    
    st.success(f"""
    ## Quiz Completed!
    **Score:** {quiz['score']}/{len(quiz['current_questions'])}
    **Total Time:** {format_time(total_time)}
    **Avg Time/Question:** {format_time(avg_time)}
    """)
    
    display_result_chart()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Return to Main Menu"):
            quiz['mode'] = 'main_menu'
            st.rerun()
    with col2:
        if st.button("View Progress Dashboard"):
            st.session_state.quiz['mode'] = 'progress_tracking'
            st.rerun()

# ===== MAIN APP =====
def main():
    # Initialize session state
    initialize_session_state()
    init_progress_tracking()
    
    # Main content routing
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
        if st.session_state.quiz['submitted']:
            show_next_button()

if __name__ == "__main__":
    main()
