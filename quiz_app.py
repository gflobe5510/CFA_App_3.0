# MUST BE FIRST - PAGE CONFIG
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    layout="centered",
    page_title="CFA Exam Prep Pro",
    page_icon="📊"
)

import os
import uuid
from datetime import datetime

# ===== APP CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Pro"
CFA_REGISTRATION_URL = "https://www.cfainstitute.org/"
STUDY_GUIDE_PATH = "Data/CFA_Study_Guide.pdf"

# ===== SESSION STATE INITIALIZATION =====
def initialize_app():
    if 'initialized' not in st.session_state:
        st.session_state.update({
            'user': {
                'name': '',
                'id': str(uuid.uuid4()),
                'identified': False
            },
            'app_mode': 'main_menu',  # Controls navigation
            'initialized': True
        })

# ===== MAIN MENU UI =====
def show_main_menu():
    st.markdown(f"# Welcome to {QUIZ_TITLE}!")
    st.markdown("---")
    
    # Study Resources Section
    st.markdown("### 📚 Study Resources")
    if os.path.exists(STUDY_GUIDE_PATH):
        with open(STUDY_GUIDE_PATH, "rb") as pdf_file:
            st.download_button(
                "Download Study Guide",
                data=pdf_file,
                file_name="CFA_Study_Guide.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Study guide not found in Data folder")
    
    st.markdown("---")
    
    # Practice Options Section
    st.markdown("### 🎯 Practice Options")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Custom Practice Exam", 
                   help="Create a custom exam with selected topics"):
            st.session_state.app_mode = 'custom_exam'
            st.rerun()
        
    with col2:
        if st.button("Focused Topic Practice",
                   help="Practice specific topic areas"):
            st.session_state.app_mode = 'topic_practice'
            st.rerun()
    
    if st.button("View Progress Dashboard",
               help="Track your learning progress"):
        st.session_state.app_mode = 'progress'
        st.rerun()
    
    st.markdown("---")
    
    # Registration Section
    if st.button("Register for CFA Exam", 
               help="Official CFA registration portal"):
        components.html(f"""
            <script>window.open('{CFA_REGISTRATION_URL}')</script>
        """)

# ===== OTHER SCREENS (PLACEHOLDERS) =====
def show_custom_exam():
    st.markdown("## Custom Practice Exam")
    if st.button("← Back to Main Menu"):
        st.session_state.app_mode = 'main_menu'
        st.rerun()

def show_topic_practice():
    st.markdown("## Focused Topic Practice")
    if st.button("← Back to Main Menu"):
        st.session_state.app_mode = 'main_menu'
        st.rerun()

def show_progress():
    st.markdown("## Progress Dashboard")
    if st.button("← Back to Main Menu"):
        st.session_state.app_mode = 'main_menu'
        st.rerun()

# ===== MAIN APP ROUTING =====
def main():
    initialize_app()
    
    # Route to the appropriate screen
    if st.session_state.app_mode == 'main_menu':
        show_main_menu()
    elif st.session_state.app_mode == 'custom_exam':
        show_custom_exam()
    elif st.session_state.app_mode == 'topic_practice':
        show_topic_practice()
    elif st.session_state.app_mode == 'progress':
        show_progress()

if __name__ == "__main__":
    main()
