# MUST BE FIRST - PAGE CONFIG
import streamlit as st
st.set_page_config(layout="wide")

import os
import time
import json
import matplotlib.pyplot as plt
import random
from datetime import datetime

# ===== CFA CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"
CFA_REGISTRATION_URL = "https://www.cfainstitute.org/"
STUDY_GUIDE_PATH = "Data/CFA_Study_Guide.pdf"
REGISTRATION_TIPS = """
• Register early for discounted pricing
• Prepare your payment method in advance  
• Have your identification documents ready
• Check the exam schedule carefully
"""

# [Previous code remains exactly the same until the show_main_menu() function]

def show_main_menu():
    st.markdown("""
    <style>
        .stTooltip {
            max-width: 400px !important;
            background-color: #263238 !important;
            color: white !important;
        }
        .stPopover {
            padding: 1rem;
            border-radius: 8px;
        }
        .registration-link {
            display: block;
            width: 100%;
            padding: 0.5rem 1rem;
            text-align: center;
            background-color: #1E88E5;
            color: white !important;
            border-radius: 0.5rem;
            text-decoration: none;
            margin-bottom: 1rem;
        }
        .registration-link:hover {
            background-color: #1565C0;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
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
        # SIMPLIFIED WORKING REGISTRATION BUTTON
        st.markdown(
            f'<a href="{CFA_REGISTRATION_URL}" target="_blank" class="registration-link">🌐 Register for CFA Exam</a>',
            unsafe_allow_html=True
        )
        # Track the click
        if st.session_state.get('registration_button_clicked', False) == False:
            track_registration_click()
            st.session_state.registration_button_clicked = True
    with res_col3:
        if st.button("📈 Track My Progress", use_container_width=True):
            st.session_state.quiz['mode'] = 'progress_tracking'
            st.rerun()
    
    # [Rest of the show_main_menu() function remains exactly the same]

# [All remaining code stays exactly the same]
