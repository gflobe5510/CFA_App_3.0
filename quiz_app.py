
import streamlit as st

def inject_custom_css():
    css = '''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');

        html, body, .stApp {
            background-image: url('background.jpg');
            background-size: cover;
            background-position: center;
            font-family: 'Source Sans Pro', sans-serif;
        }
        
        .main, .block-container {
            background-color: rgba(255, 255, 255, 0.80) !important;
            border-radius: 12px !important;
            padding: 2rem !important;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08) !important;
        }

        .header {
            color: #2c3e50 !important;
            font-weight: 700 !important;
            font-size: 2.5rem !important;
            border-bottom: 3px solid #3498db !important;
            padding-bottom: 10px !important;
            margin-bottom: 25px !important;
        }

        .card {
            background-color: rgba(255,255,255,0.95) !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 16px !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.08) !important;
            padding: 1rem !important;
        }

        .stButton>button {
            background-color: #3399ff !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            padding: 0.5rem 1.25rem !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
        }

        .stButton>button:hover {
            background-color: #2c80d3 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15) !important;
        }

        .stProgress>div>div>div {
            background-color: #3399ff !important;
        }

        .stRadio>div {
            background-color: white !important;
            padding: 15px !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        }

        .metric-card {
            background-color: rgba(255,255,255,0.95) !important;
            border-radius: 12px !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.08) !important;
            text-align: center !important;
        }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

def main():
    inject_custom_css()
    st.markdown("<div class='header'>CFA Exam Preparation Pro</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>📚 Study Resources</h3></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>🎯 Practice Options</h3></div>", unsafe_allow_html=True)
    st.button("Start Practice")

if __name__ == "__main__":
    main()
