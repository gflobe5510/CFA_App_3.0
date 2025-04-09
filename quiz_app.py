# MUST BE FIRST - PAGE CONFIG
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    layout="wide",
    page_title="CFA Exam Prep Pro",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

import os
import time
import json
import matplotlib.pyplot as plt
import random
from datetime import datetime

# ===== CUSTOM CSS =====
def inject_custom_css():
    st.markdown("""
    <style>
        /* Main styling */
        .main {
            background-color: #f8f9fa;
        }
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
        }
        
        /* Header styling */
        .header {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 25px;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 8px;
            border: 1px solid #3498db;
            background-color: #3498db;
            color: white;
            transition: all 0.3s;
            font-weight: 500;
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

# Initialize session state
if 'quiz' not in st.session_state:
    st.session_state.quiz = {
        'mode': 'main_menu',
        'score': 0,
        'current_index': 0
    }

def main():
    inject_custom_css()
    
    # Header with logo placeholder
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 30px;">
        <h1 class='header' style="margin: 0;">{QUIZ_TITLE}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.quiz['mode'] == 'main_menu':
        show_main_menu()
    elif st.session_state.quiz['mode'] == 'question':
        show_question()

def show_main_menu():
    st.markdown("""
    <div style="background-color: white; border-radius: 10px; padding: 25px; margin-bottom: 25px;">
        <h3 style="color: #2c3e50; margin-top: 0;">📚 Study Resources</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Start New Quiz", use_container_width=True):
            st.session_state.quiz['mode'] = 'question'
            st.rerun()
    with col2:
        if st.button("🌐 Register for CFA Exam", 
                    help=REGISTRATION_TIPS,
                    use_container_width=True):
            js = f"window.open('{CFA_REGISTRATION_URL}')"
            components.html(js)

def show_question():
    st.write("Question content will appear here")
    if st.button("Return to Main Menu"):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

if __name__ == "__main__":
    main()
