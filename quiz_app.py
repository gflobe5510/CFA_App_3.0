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
    # Additional categories can be added similarly
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
            'selected_category': None,
            'incorrect_answers': []  # Store incorrect answers for the result section
        }

def display_question():
    if not st.session_state.quiz['current_questions']:
        st.warning("No questions available for this category")
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()
        return
    
    question = st.session_state.quiz['current_questions'][st.session_state.quiz['current_index']]
    
    st.progress((st.session_state.quiz['current_index'] + 1) / len(st.session_state.quiz['current_questions']))
    st.markdown(f"### {st.session_state.quiz['selected_category']}")
    st.markdown(f"**Question {st.session_state.quiz['current_index'] + 1} of {len(st.session_state.quiz['current_questions'])}**")
    st.markdown(f"*{question['question']}*")
    
    options = question.get('options', question.get('choices', ["Error: No options provided"]))
    user_answer = st.radio("Select your answer:", options, key=f"q{st.session_state.quiz['current_index']}")
    
    if st.button("Submit Answer"):
        process_answer(question, user_answer)

def process_answer(question, user_answer):
    time_spent = time.time() - st.session_state.quiz['question_start']
    st.session_state.quiz['time_spent'].append(time_spent)
    st.session_state.quiz['user_answer'] = user_answer
    st.session_state.quiz['submitted'] = True
    
    if user_answer == question['correct_answer']:
        st.session_state.quiz['score'] += 1
        st.success("✅ Correct!")
    else:
        st.session_state.quiz['incorrect_answers'].append(question)  # Add incorrect answers to the list
        st.error(f"❌ Incorrect. The correct answer is: {question['correct_answer']}")
    
    if 'explanation' in question:
        st.info(f"**Explanation:** {question['explanation']}")

def show_results():
    total_time = time.time() - st.session_state.quiz['start_time']
    avg_time = sum(st.session_state.quiz['time_spent']) / len(st.session_state.quiz['time_spent']) if st.session_state.quiz['time_spent'] else 0
    
    score = st.session_state.quiz['score']
    total_questions = len(st.session_state.quiz['current_questions'])
    percentage = (score / total_questions) * 100
    
    # Show performance
    st.success(f"""
    ## Quiz Completed!
    **Score:** {score}/{total_questions} ({percentage:.2f}%)
    **Total Time:** {format_time(total_time)}
    **Avg Time/Question:** {format_time(avg_time)}
    """)

    # Show the benchmark comparison with 75% correct
    show_benchmark_comparison(percentage)

    # List topics to study based on incorrect answers
    study_recommendations()

def show_benchmark_comparison(user_percentage):
    benchmark = 75
    st.markdown(f"### Benchmark Comparison")
    
    # Bar chart for performance
    fig, ax = plt.subplots()
    ax.bar(['You', 'Benchmark'], [user_percentage, benchmark], color=['blue', 'green'])
    ax.set_ylim([0, 100])
    ax.set_ylabel('Percentage')
    ax.set_title('Your Performance vs Benchmark')
    st.pyplot(fig)

def study_recommendations():
    st.markdown("### Topics to Review")
    if st.session_state.quiz['incorrect_answers']:
        topics_to_study = set()
        
        for question in st.session_state.quiz['incorrect_answers']:
            topic = question.get("topic", "Unknown")
            topics_to_study.add(topic)
        
        for topic in topics_to_study:
            st.markdown(f"- **{topic}**")
    else:
        st.markdown("You got everything correct! No topics to review.")

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

# ===== MAIN APP =====
def main():
    st.set_page_config(layout="wide")
    st.title(f"📊 {QUIZ_TITLE}")
    
    initialize_session_state()
    
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()
        if st.session_state.quiz['submitted']:
            show_next_button()
    else:
        show_results()

if __name__ == "__main__":
    main()
