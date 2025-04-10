# MUST BE FIRST - PAGE CONFIG
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    layout="wide",
    page_title="CFA Level I Exam Prep Pro",
    page_icon="📊"
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
        /* Import CFA Institute font */
        @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');
        
        /* NUCLEAR OPTION FOR BACKGROUND COLORS */
        html, body, .stApp, .main, .block-container, 
        div[data-testid="stVerticalBlock"], 
        div[data-testid="stHorizontalBlock"],
        div[data-testid="stVerticalBlockBorderWrapper"],
        section[data-testid="stSidebar"],
        div.stButton > button,
        div[data-baseweb="select"] > div,
        .st-emotion-cache-1dp5vir {
            background-color: white !important;
            color: #2c3e50 !important;
        }
        
        /* Special background for selection pages */
        div[data-testid="stVerticalBlock"] > div > div > div > div > div {
            background-color: #f8f9fa !important;
            border-radius: 10px !important;
            padding: 15px !important;
            margin-bottom: 15px !important;
        }
        
        /* Card styling */
        .card {
            background-color: white !important;
            border: 1px solid #e0e0e0 !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08) !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
        }
        
        /* Header styling */
        .header {
            color: #2c3e50 !important;
            border-bottom: 2px solid #3498db !important;
            padding-bottom: 10px !important;
            margin-bottom: 25px !important;
            font-size: 2.5rem !important;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 8px !important;
            border: 1px solid #3498db !important;
            background-color: #3498db !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #2980b9 !important;
            border-color: #2980b9 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        }
        
        /* Progress bar */
        .stProgress>div>div>div {
            background-color: #3498db !important;
        }
        
        /* Radio buttons */
        .stRadio>div {
            background-color: white !important;
            padding: 15px !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
            font-size: 1rem !important;
        }
        
        /* Metrics containers */
        .metric-card {
            background-color: white !important;
            border-radius: 10px !important;
            padding: 15px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
            text-align: center !important;
            font-size: 1rem !important;
            border: 1px solid #e0e0e0 !important;
        }
        
        /* Animation for important elements */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.03); }
            100% { transform: scale(1); }
        }
        
        .pulse-animation {
            animation: pulse 2s infinite;
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

def start_random_mix():
    questions = []
    for category in CATEGORIES:
        for difficulty in ['easy', 'medium', 'hard']:
            category_questions = st.session_state.quiz['all_questions'][category].get(difficulty, [])
            if category_questions:
                questions.extend(category_questions)
    
    if not questions:
        st.error("No questions available")
        return
    
    random.shuffle(questions)
    questions = questions[:20]
    
    st.session_state.quiz.update({
        'current_questions': questions,
        'current_index': 0,
        'mode': 'question',
        'selected_category': "Random Mix",
        'question_start': time.time(),
        'submitted': False,
        'score': 0,
        'time_spent': [],
        'test_type': 'random_mix'
    })
    st.rerun()

def start_quick_quiz():
    questions = []
    for category in CATEGORIES:
        for difficulty in ['easy', 'medium', 'hard']:
            category_questions = st.session_state.quiz['all_questions'][category].get(difficulty, [])
            if category_questions:
                questions.extend(category_questions)
    
    if len(questions) < 5:
        st.error("Not enough questions available")
        return
    
    questions = random.sample(questions, 5)
    
    st.session_state.quiz.update({
        'current_questions': questions,
        'current_index': 0,
        'mode': 'question',
        'selected_category': "Quick Quiz",
        'question_start': time.time(),
        'submitted': False,
        'score': 0,
        'time_spent': [],
        'test_type': 'quick_quiz'
    })
    st.rerun()

def start_super_hard_exam():
    questions = []
    for category in CATEGORIES:
        category_questions = st.session_state.quiz['all_questions'][category].get('hard', [])
        if category_questions:
            questions.extend(random.sample(category_questions, min(3, len(category_questions))))
    
    if not questions:
        st.error("No hard questions available")
        return
    
    random.shuffle(questions)
    
    st.session_state.quiz.update({
        'current_questions': questions,
        'current_index': 0,
        'mode': 'question',
        'selected_category': "Super Hard Exam",
        'question_start': time.time(),
        'submitted': False,
        'score': 0,
        'time_spent': [],
        'test_type': 'super_hard'
    })
    st.rerun()

def start_balanced_exam(exam_number):
    questions = []
    target_per_difficulty = 10
    
    for difficulty in ['easy', 'medium', 'hard']:
        difficulty_questions = []
        for category in CATEGORIES:
            cat_questions = st.session_state.quiz['all_questions'][category].get(difficulty, [])
            if cat_questions:
                difficulty_questions.extend(random.sample(cat_questions, min(2, len(cat_questions))))
        
        if difficulty_questions:
            questions.extend(random.sample(difficulty_questions, min(target_per_difficulty, len(difficulty_questions))))
    
    if len(questions) < 15:
        st.error("Not enough questions available for a balanced exam")
        return
    
    random.shuffle(questions)
    
    st.session_state.quiz.update({
        'current_questions': questions,
        'current_index': 0,
        'mode': 'question',
        'selected_category': f"Balanced Exam {exam_number}",
        'question_start': time.time(),
        'submitted': False,
        'score': 0,
        'time_spent': [],
        'test_type': 'balanced_exam',
        'exam_number': exam_number
    })
    st.rerun()

def start_practice_test(difficulty):
    questions = []
    for category in CATEGORIES:
        category_questions = st.session_state.quiz['all_questions'][category].get(difficulty, [])
        if category_questions:
            questions.extend(random.sample(category_questions, min(2, len(category_questions))))
    
    if not questions:
        st.error(f"No {difficulty} questions available for practice test")
        return
    
    random.shuffle(questions)
    
    st.session_state.quiz.update({
        'current_questions': questions,
        'current_index': 0,
        'mode': 'question',
        'selected_category': f"{difficulty.capitalize()} Exam",
        'question_start': time.time(),
        'submitted': False,
        'score': 0,
        'time_spent': [],
        'test_type': 'practice_test'
    })
    st.rerun()

def show_category_selection():
    st.markdown("""
    <style>
        div[data-testid="stVerticalBlock"] > div > div > div > div {
            background-color: #f8f9fa !important;
            padding: 20px !important;
            border-radius: 10px !important;
            margin-bottom: 15px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h2 style="color: #2c3e50; margin-top: 0;">Select a CFA Topic Area</h2>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, category in enumerate(CATEGORIES):
        total_questions = sum(len(st.session_state.quiz['all_questions'][category][d]) 
                          for d in ['easy', 'medium', 'hard'])
        
        with cols[i % 2]:
            if st.button(
                f"{category} ({total_questions} questions)",
                disabled=total_questions == 0,
                help=CATEGORIES[category]["description"],
                use_container_width=True
            ):
                questions = []
                for difficulty in ['easy', 'medium', 'hard']:
                    questions.extend(st.session_state.quiz['all_questions'][category][difficulty])
                
                st.session_state.quiz.update({
                    'current_questions': questions,
                    'current_index': 0,
                    'mode': 'question',
                    'selected_category': category,
                    'question_start': time.time(),
                    'submitted': False,
                    'score': 0,
                    'time_spent': [],
                    'test_type': 'category'
                })
                st.rerun()
    
    if st.button("← Back to Main Menu", use_container_width=True):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

def show_registration_stats():
    progress = st.session_state.progress
    st.markdown("""
    <div class='metric-card'>
        <div style="font-size: 16px; color: #7f8c8d;">Total Registration Clicks</div>
        <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">{}</div>
    </div>
    """.format(progress.get('registration_clicks', 0)), unsafe_allow_html=True)
    
    last_click = progress.get('last_registration_click')
    if last_click:
        last_click = datetime.fromisoformat(last_click).strftime("%Y-%m-%d %H:%M")
    else:
        last_click = "Never"
    
    st.markdown("""
    <div class='metric-card'>
        <div style="font-size: 16px; color: #7f8c8d;">Last Registration Click</div>
        <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">{}</div>
    </div>
    """.format(last_click), unsafe_allow_html=True)

def show_progress_tracking():
    st.markdown("""
    <div class='card'>
        <h2 style="color: #2c3e50; margin-top: 0;">Your Study Progress</h2>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with open('Data/progress_data.json', 'r') as f:
            progress_data = json.load(f)
    except:
        progress_data = st.session_state.progress
    
    if not progress_data.get('attempts'):
        st.markdown("""
        <div class='card'>
            <p>No progress data yet. Complete some quizzes to track your progress!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Back to Main Menu", use_container_width=True):
            st.session_state.quiz['mode'] = 'main_menu'
            st.rerun()
        return
    
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">Progress Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div style="font-size: 16px; color: #7f8c8d;">Total Attempts</div>
            <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">{}</div>
        </div>
        """.format(len(progress_data['attempts'])), unsafe_allow_html=True)
    with col2:
        avg_score = sum(progress_data['scores'])/len(progress_data['scores'])
        st.markdown("""
        <div class='metric-card'>
            <div style="font-size: 16px; color: #7f8c8d;">Average Score</div>
            <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">{:.1%}</div>
        </div>
        """.format(avg_score), unsafe_allow_html=True)
    with col3:
        total_time = sum(progress_data['time_spent'])/60
        st.markdown("""
        <div class='metric-card'>
            <div style="font-size: 16px; color: #7f8c8d;">Total Study Time</div>
            <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">{:.1f} min</div>
        </div>
        """.format(total_time), unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">Registration Interest</h3>
    </div>
    """, unsafe_allow_html=True)
    show_registration_stats()
    
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">Progress Charts</h3>
    </div>
    """, unsafe_allow_html=True)
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    
    ax[0].plot(progress_data['attempts'], progress_data['scores'], marker='o', color='#3498db')
    ax[0].set_title("Score Improvement Over Time", pad=20)
    ax[0].set_xlabel("Attempt Number")
    ax[0].set_ylabel("Score (%)")
    ax[0].set_ylim(0, 1)
    ax[0].grid(True, alpha=0.3)
    
    ax[1].bar(progress_data['attempts'], progress_data['time_spent'], color='#3498db')
    ax[1].set_title("Time Spent per Attempt", pad=20)
    ax[1].set_xlabel("Attempt Number")
    ax[1].set_ylabel("Time (seconds)")
    ax[1].grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">Detailed Progress History</h3>
    </div>
    """, unsafe_allow_html=True)
    
    progress_table = {
        "Attempt": progress_data['attempts'],
        "Date": progress_data['dates'],
        "Score": [f"{s:.1%}" for s in progress_data['scores']],
        "Time Spent": [f"{t//60}m {t%60}s" for t in progress_data['time_spent']]
    }
    st.table(progress_table)
    
    if st.button("← Back to Main Menu", use_container_width=True):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

def show_difficulty_selection():
    st.markdown("""
    <style>
        div[data-testid="stVerticalBlock"] > div > div > div > div {
            background-color: #f8f9fa !important;
            padding: 20px !important;
            border-radius: 10px !important;
            margin-bottom: 15px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h2 style="color: #2c3e50; margin-top: 0;">Select Practice Exam Type</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">Balanced Exams (Mixed Difficulty)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(5)
    with cols[0]:
        if st.button("Balanced Exam 1", use_container_width=True,
                    help="1/3 Easy, 1/3 Medium, 1/3 Hard questions"):
            start_balanced_exam(1)
    with cols[1]:
        if st.button("Balanced Exam 2", use_container_width=True,
                    help="1/3 Easy, 1/3 Medium, 1/3 Hard questions"):
            start_balanced_exam(2)
    with cols[2]:
        if st.button("Balanced Exam 3", use_container_width=True,
                    help="1/3 Easy, 1/3 Medium, 1/3 Hard questions"):
            start_balanced_exam(3)
    with cols[3]:
        if st.button("Balanced Exam 4", use_container_width=True,
                    help="1/3 Easy, 1/3 Medium, 1/3 Hard questions"):
            start_balanced_exam(4)
    with cols[4]:
        if st.button("Balanced Exam 5", use_container_width=True,
                    help="1/3 Easy, 1/3 Medium, 1/3 Hard questions"):
            start_balanced_exam(5)
    
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">Specialized Exams</h3>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    with cols[0]:
        if st.button("📗 Easy Exam", use_container_width=True):
            start_practice_test('easy')
    with cols[1]:
        if st.button("📘 Medium Exam", use_container_width=True):
            start_practice_test('medium')
    with cols[2]:
        if st.button("📕 Hard Exam", use_container_width=True):
            start_practice_test('hard')
    with cols[3]:
        if st.button("💀 Super Hard", use_container_width=True,
                    help="Only the most challenging questions"):
            start_super_hard_exam()
    
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">Quick Practice</h3>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    with cols[0]:
        if st.button("🎯 Quick Quiz", use_container_width=True,
                    help="5 random questions from all categories"):
            start_quick_quiz()
    with cols[1]:
        if st.button("🔀 Random Mix", use_container_width=True,
                    help="Completely random question selection"):
            start_random_mix()
    
    if st.button("← Back to Main Menu", use_container_width=True):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

def show_main_menu():
    inject_custom_css()
    
    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #005baa, #003366); 
                padding: 2rem; 
                border-radius: 12px;
                color: white;
                margin-bottom: 2rem;">
        <div style="display: flex; align-items: center; gap: 1.5rem;">
            <div style="flex: 1;">
                <h1 style="color: white; margin: 0; font-size: 2.5rem;">CFA® Level I Exam Prep Pro</h1>
                <p style="font-size: 1.1rem; opacity: 0.9;">Master the 2024 CFA curriculum with adaptive practice exams and performance analytics</p>
            </div>
            <div style="flex: 0 0 100px;">
                <img src="https://www.cfainstitute.org/-/media/images/logo/cfa-institute-logo.svg" 
                     style="width: 100%; filter: brightness(0) invert(1);">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress Metrics
    attempts = len(st.session_state.progress['attempts'])
    avg_score = (sum(st.session_state.progress['scores'])/attempts)*100 if attempts > 0 else 0

    st.markdown(f"""
    <div style="display: grid; 
                grid-template-columns: repeat(3, 1fr); 
                gap: 1rem; 
                margin-bottom: 2rem;">
                
        <div style="background: white; 
                    border-radius: 10px; 
                    padding: 1.5rem;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    border-left: 4px solid #3498db;">
            <div style="font-size: 0.9rem; color: #7f8c8d;">Your Progress</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{attempts} Tests</div>
            <div style="height: 4px; background: #ecf0f1; margin-top: 8px;">
                <div style="height: 100%; width: {min(100, attempts*10)}%; background: #3498db;"></div>
            </div>
        </div>
        
        <div style="background: white; 
                    border-radius: 10px; 
                    padding: 1.5rem;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    border-left: 4px solid #2ecc71;">
            <div style="font-size: 0.9rem; color: #7f8c8d;">Average Score</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{avg_score:.1f}%</div>
            <div style="height: 4px; background: #ecf0f1; margin-top: 8px;">
                <div style="height: 100%; width: {avg_score}%; background: #2ecc71;"></div>
            </div>
        </div>
        
        <div style="background: white; 
                    border-radius: 10px; 
                    padding: 1.5rem;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    border-left: 4px solid #9b59b6;">
            <div style="font-size: 0.9rem; color: #7f8c8d;">Topics Mastered</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{(avg_score/100*10):.1f}/10</div>
            <div style="height: 4px; background: #ecf0f1; margin-top: 8px;">
                <div style="height: 100%; width: {avg_score/10}%; background: #9b59b6;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Resources Section
    st.markdown("""
    <div class='card'>
        <h3 style="color: #2c3e50; margin-top: 0;">📚 Study Resources</h3>
    </div>
    """, unsafe_allow_html=True)
    
    res_col1, res_col2, res_col3, res_col4 = st.columns(4)
    
    with res_col1:
        if os.path.exists(STUDY
