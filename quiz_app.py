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
STUDY_GUIDE_PATH = "Data/CFA_Study_Guide.pdf"

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
updated_json_path = 'Data/updated_questions_with_5_options_final.json'

def load_questions():
    try:
        with open(updated_json_path, 'r') as f:
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
            'dates': []
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
            'initialized': True
        })
    init_progress_tracking()

def format_time(seconds):
    return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"

def display_result_chart():
    score = st.session_state.quiz['score'] / len(st.session_state.quiz['current_questions'])
    fig, ax = plt.subplots()
    ax.bar(['Your Score', 'Benchmark'], [score, 0.75], color=['green', 'blue'])
    ax.set_ylim([0, 1])
    st.pyplot(fig)

def show_results():
    quiz = st.session_state.quiz
    total_time = time.time() - quiz['start_time']
    avg_time = sum(quiz['time_spent'])/len(quiz['time_spent']) if quiz['time_spent'] else 0
    
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
    if st.button("Next Question"):
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
    
    if st.button("Submit Answer"):
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
    st.markdown("## Select a CFA Topic Area")
    
    cols = st.columns(2)
    for i, category in enumerate(CATEGORIES):
        total_questions = sum(len(st.session_state.quiz['all_questions'][category][d]) 
                          for d in ['easy', 'medium', 'hard'])
        
        with cols[i % 2]:
            if st.button(
                f"{category} ({total_questions} questions)",
                disabled=total_questions == 0,
                help=CATEGORIES[category]["description"]
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
    
    st.markdown("---")
    if st.button("← Back to Main Menu", use_container_width=True):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

def show_progress_tracking():
    st.markdown("## Your Study Progress")
    
    try:
        with open('Data/progress_data.json', 'r') as f:
            progress_data = json.load(f)
    except:
        progress_data = st.session_state.progress
    
    if not progress_data['attempts']:
        st.info("No progress data yet. Complete some quizzes to track your progress!")
        if st.button("← Back to Main Menu"):
            st.session_state.quiz['mode'] = 'main_menu'
            st.rerun()
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

def show_difficulty_selection():
    st.markdown("## Select Practice Exam Type")
    
    st.markdown("### Balanced Exams (Mixed Difficulty)")
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
    
    st.markdown("### Specialized Exams")
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
    
    st.markdown("### Quick Practice")
    cols = st.columns(2)
    with cols[0]:
        if st.button("🎯 Quick Quiz", use_container_width=True,
                    help="5 random questions from all categories"):
            start_quick_quiz()
    with cols[1]:
        if st.button("🔀 Random Mix", use_container_width=True,
                    help="Completely random question selection"):
            start_random_mix()
    
    st.markdown("---")
    if st.button("← Back to Main Menu", use_container_width=True):
        st.session_state.quiz['mode'] = 'main_menu'
        st.rerun()

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

# ===== MAIN APP =====
def main():
    # Initialize session state
    initialize_session_state()
    
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
