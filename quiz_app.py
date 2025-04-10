import streamlit as st
import streamlit.components.v1 as components
import os
import time
import json
import matplotlib.pyplot as plt
import random
from datetime import datetime

# MUST BE FIRST - PAGE CONFIG
st.set_page_config(
    layout="wide",
    page_title="CFA Exam Prep Pro",
    page_icon="📊"
)

# ===== CUSTOM CSS =====
def inject_custom_css():
    st.markdown("""
    <style>
        /* Main styling */
        .main {
            background-image: url('https://github.com/your_username/your_repo/raw/main/Data/background.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            color: white;
        }
        .stApp {
            background: #FFFFFF; /* White background */
        }

        /* Header styling */
        .header {
            color: #003D73;  /* CFA dark blue */
            border-bottom: 2px solid #003D73;
            padding-bottom: 10px;
            margin-bottom: 25px;
            font-family: 'Source Sans Pro', sans-serif; /* Clean font */
            font-size: 48px; /* Increased font size for title */
            font-weight: bold;
        }

        /* Button styling */
        .stButton>button {
            border-radius: 8px;
            border: 1px solid #003D73;  /* CFA dark blue border */
            background-color: #003D73;  /* CFA blue */
            color: white;
            transition: all 0.3s;
            font-weight: 500;
            font-family: 'Source Sans Pro', sans-serif;
        }
        .stButton>button:hover {
            background-color: #006BB6; /* Slightly lighter blue for hover */
            border-color: #006BB6;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        /* Progress bar */
        .stProgress>div>div>div {
            background-color: #003D73; /* CFA blue progress */
        }

        /* Radio buttons */
        .stRadio>div {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        /* Custom card styling */
        .card {
            background-color: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }

        /* Metrics containers */
        .metric-card {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
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
def load_questions():
    try:
        with open('Data/updated_questions_with_5_options_final.json', 'r') as f:
            questions_data = json.load(f)
        
        questions_by_category = {cat: {'easy': [], 'medium': [], 'hard': []} for cat in CATEGORIES}
        
        for question in questions_data.get("questions", []):
            topic = question.get("topic", "").strip()
            category = TOPIC_TO_CATEGORY.get(topic, topic)
            difficulty = question.get("difficulty", "medium").lower()
            
            if category in questions_by_category and difficulty in ['easy', 'medium', 'hard']:
                questions_by_category[category][difficulty].append(question)
        
        return questions_by_category
        
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return {cat: {'easy': [], 'medium': [], 'hard': []} for cat in CATEGORIES}

# ===== PROGRESS TRACKING =====
def init_progress_tracking():
    if 'progress' not in st.session_state:
        st.session_state.progress = {
            'attempts': [],
            'scores': [],
            'time_spent': [],
            'dates': [],
            'registration_clicks': 0,
            'last_registration_click': None
        }

def save_progress(score, total_questions, total_time):
    init_progress_tracking()
    st.session_state.progress['attempts'].append(len(st.session_state.progress['attempts']) + 1)
    st.session_state.progress['scores'].append(score/total_questions)
    st.session_state.progress['time_spent'].append(total_time)
    st.session_state.progress['dates'].append(datetime.now().strftime("%Y-%m-%d"))
    
    try:
        with open('Data/progress_data.json', 'w') as f:
            json.dump(st.session_state.progress, f)
    except:
        st.error("Could not save progress data")

def track_registration_click():
    init_progress_tracking()
    st.session_state.progress['registration_clicks'] += 1
    st.session_state.progress['last_registration_click'] = datetime.now().isoformat()
    save_progress(0, 1, 0)

# ===== QUIZ ENGINE =====
def initialize_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.update({
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

def format_time(seconds):
    return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"

def display_result_chart():
    score = st.session_state.quiz['score'] / len(st.session_state.quiz['current_questions'])
    fig, ax = plt.subplots()
    ax.bar(['Your Score', 'Benchmark'], [score, 0.75], color=['#3498db', '#95a5a6'])
    ax.set_ylim([0, 1])
    st.pyplot(fig)

def show_results():
    quiz = st.session_state.quiz
    total_time = time.time() - quiz['start_time']
    avg_time = sum(quiz['time_spent'])/len(quiz['time_spent']) if quiz['time_spent'] else 0
    
    save_progress(quiz['score'], len(quiz['current_questions']), total_time)
    
    st.markdown(f"""
    <div class='card'>
        <h2 style="color: #2c3e50; margin-top: 0;">Quiz Completed!</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0;">
            <div class='metric-card'>
                <div style="font-size: 16px; color: #7f8c8d;">Score</div>
                <div style="font-size: 32px; font-weight: bold; color: #2c3e50;">{quiz['score']}/{len(quiz['current_questions'])}</div>
            </div>
            <div class='metric-card'>
                <div style="font-size: 16px; color: #7f8c8d;">Total Time</div>
                <div style="font-size: 32px; font-weight: bold; color: #2c3e50;">{format_time(total_time)}</div>
            </div>
            <div class='metric-card'>
                <div style="font-size: 16px; color: #7f8c8d;">Avg/Question</div>
                <div style="font-size: 32px; font-weight: bold; color: #2c3e50;">{format_time(avg_time)}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    display_result_chart()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Return to Main Menu", use_container_width=True):
            quiz['mode'] = 'main_menu'
            st.rerun()
    with col2:
        if st.button("View Progress Dashboard", use_container_width=True):
            quiz['mode'] = 'progress_tracking'
            st.rerun()

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
    if st.button("Next Question", use_container_width=True):
        st.session_state.quiz['current_index'] += 1
        st.session_state.quiz['submitted'] = False
        st.session_state.quiz['question_start'] = time.time()
        st.rerun()

def display_question():
    questions = st.session_state.quiz['current_questions']
    if not questions:
        st.warning("No questions available")
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()
        return
    
    idx = st.session_state.quiz['current_index']
    if idx >= len(questions):
        show_results()
        return
    
    question = questions[idx]
    
    st.progress((idx + 1) / len(questions))
    
    exam_type = st.session_state.quiz.get('test_type')
    if exam_type == 'balanced_exam':
        exam_num = st.session_state.quiz.get('exam_number', '')
        st.markdown(f"### Balanced Exam {exam_num}")
    elif exam_type == 'practice_test':
        st.markdown(f"### {st.session_state.quiz['selected_category']}")
    elif exam_type == 'super_hard':
        st.markdown("### Super Hard Exam")
    elif exam_type == 'quick_quiz':
        st.markdown("### Quick Quiz")
    elif exam_type == 'random_mix':
        st.markdown("### Random Mix")
    else:
        st.markdown(f"### {st.session_state.quiz['selected_category']}")
    
    st.markdown(f"**Question {idx + 1} of {len(questions)}**")
    
    if 'difficulty' in question:
        difficulty = question['difficulty'].capitalize()
        st.markdown(f"*Difficulty: {difficulty}*")
    
    st.markdown(f"*{question['question']}*")
    
    options = question.get('options', [])
    user_answer = st.radio("Select your answer:", options, key=f"q{idx}")
    
    if st.button("Submit Answer", use_container_width=True):
        process_answer(question, user_answer)

# ===== MENU FUNCTIONS =====
def show_main_menu():
    inject_custom_css()
    st.title("CFA Exam Preparation Pro")
    st.markdown("Welcome to your CFA exam preparation tool. Select an option below to get started.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Practice by Category", use_container_width=True):
            st.session_state.quiz['mode'] = 'category_selection'
            st.rerun()
        
        if st.button("Take Balanced Exam", use_container_width=True):
            st.session_state.quiz['mode'] = 'difficulty_selection'
            st.session_state.quiz['test_type'] = 'balanced_exam'
            st.rerun()
    
    with col2:
        if st.button("Progress Tracking", use_container_width=True):
            st.session_state.quiz['mode'] = 'progress_tracking'
            st.rerun()
        
        if st.button("Quick Quiz (10 Random Questions)", use_container_width=True):
            st.session_state.quiz['mode'] = 'difficulty_selection'
            st.session_state.quiz['test_type'] = 'quick_quiz'
            st.rerun()
    
    st.markdown("---")
    st.markdown("### CFA Exam Registration")
    st.markdown(REGISTRATION_TIPS)
    
    if st.button("Register for CFA Exam", use_container_width=True):
        track_registration_click()
        components.iframe(CFA_REGISTRATION_URL, width=800, height=600)

def show_progress_tracking():
    st.title("Your Progress")
    init_progress_tracking()
    
    if not st.session_state.progress['attempts']:
        st.warning("No progress data available yet. Complete some quizzes to track your progress.")
    else:
        st.markdown(f"**Total Attempts:** {len(st.session_state.progress['attempts'])}")
        st.markdown(f"**Average Score:** {sum(st.session_state.progress['scores'])/len(st.session_state.progress['scores']):.1%}")
        st.markdown(f"**Last Registration Click:** {st.session_state.progress.get('last_registration_click', 'Never')}")
        
        fig, ax = plt.subplots()
        ax.plot(st.session_state.progress['attempts'], st.session_state.progress['scores'], marker='o')
        ax.set_xlabel("Attempt")
        ax.set_ylabel("Score")
        ax.set_title("Progress Over Time")
        st.pyplot(fig)
    
    if st.button("Return to Main Menu", use_container_width=True):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

def show_difficulty_selection():
    st.title("Select Difficulty")
    
    difficulty = st.radio("Choose difficulty level:", 
                         ["Easy", "Medium", "Hard", "Mixed"], 
                         key="difficulty_select")
    
    test_type = st.session_state.quiz['test_type']
    
    if test_type == 'balanced_exam':
        exam_number = st.selectbox("Select exam number:", list(range(1, 6)))
        st.session_state.quiz['exam_number'] = exam_number
    
    if st.button("Start Quiz", use_container_width=True):
        # Here you would implement logic to select questions based on difficulty
        # For now, we'll just set some dummy questions
        st.session_state.quiz['current_questions'] = [
            {
                'question': 'Sample question 1',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 'A',
                'difficulty': difficulty.lower()
            },
            {
                'question': 'Sample question 2',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 'B',
                'difficulty': difficulty.lower()
            }
        ]
        st.session_state.quiz['mode'] = 'question'
        st.session_state.quiz['current_index'] = 0
        st.session_state.quiz['score'] = 0
        st.session_state.quiz['start_time'] = time.time()
        st.rerun()
    
    if st.button("Back", use_container_width=True):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

def show_category_selection():
    st.title("Select Category")
    
    category = st.selectbox("Choose a category:", list(CATEGORIES.keys()))
    difficulty = st.radio("Choose difficulty level:", 
                         ["Easy", "Medium", "Hard", "Mixed"], 
                         key="category_difficulty")
    
    if st.button("Start Practice", use_container_width=True):
        # Here you would implement logic to select questions based on category and difficulty
        # For now, we'll just set some dummy questions
        st.session_state.quiz['current_questions'] = [
            {
                'question': f'Sample {category} question 1',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 'A',
                'difficulty': difficulty.lower(),
                'topic': category
            },
            {
                'question': f'Sample {category} question 2',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 'B',
                'difficulty': difficulty.lower(),
                'topic': category
            }
        ]
        st.session_state.quiz['selected_category'] = category
        st.session_state.quiz['mode'] = 'question'
        st.session_state.quiz['current_index'] = 0
        st.session_state.quiz['score'] = 0
        st.session_state.quiz['start_time'] = time.time()
        st.rerun()
    
    if st.button("Back", use_container_width=True):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

# Main App
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
