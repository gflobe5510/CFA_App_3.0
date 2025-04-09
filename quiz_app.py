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
    "Quantitative Methods": {
        "description": "Covers statistical tools for financial analysis",
        "weight": 0.10,
        "readings": ["Time Value of Money", "Probability Concepts"]
    },
    "Economics": {
        "description": "Examines macroeconomic and microeconomic concepts",
        "weight": 0.10,
        "readings": ["Demand and Supply", "Business Cycles"]
    },
    "Financial Statement Analysis": {
        "description": "Analysis of financial statements",
        "weight": 0.15,
        "readings": ["Income Statements", "Balance Sheets"]
    },
    "Corporate Issuers": {
        "description": "Characteristics of corporate issuers",
        "weight": 0.10,
        "readings": ["Capital Structure", "Corporate Governance"]
    },
    "Equity Investments": {
        "description": "Valuation of equity securities",
        "weight": 0.11,
        "readings": ["Market Organization", "Equity Valuation"]
    },
    "Fixed Income": {
        "description": "Analysis of fixed-income securities",
        "weight": 0.11,
        "readings": ["Bond Valuation", "Yield Measures"]
    },
    "Derivatives": {
        "description": "Valuation of derivative securities",
        "weight": 0.06,
        "readings": ["Forwards and Futures", "Options"]
    },
    "Alternative Investments": {
        "description": "Hedge funds, private equity, real estate",
        "weight": 0.06,
        "readings": ["Private Capital", "Real Estate"]
    },
    "Portfolio Management": {
        "description": "Portfolio construction and risk management",
        "weight": 0.06,
        "readings": ["Portfolio Risk", "Investment Policy"]
    }
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
            'selected_category': None
        }

def show_category_selection():
    st.markdown("## Select a CFA Topic Area")
    
    available_categories = [
        cat for cat in CATEGORIES 
        if cat in st.session_state.quiz['all_questions'] and 
        len(st.session_state.quiz['all_questions'][cat]) > 0
    ]
    
    cols = st.columns(2)
    for i, category in enumerate(available_categories):
        with cols[i % 2]:
            if st.button(f"{category} ({len(st.session_state.quiz['all_questions'][category])} questions)"):
                st.session_state.quiz.update({
                    'current_questions': st.session_state.quiz['all_questions'][category],
                    'current_index': 0,
                    'mode': 'question',
                    'selected_category': category,
                    'question_start': time.time(),
                    'submitted': False,
                    'score': 0,
                    'time_spent': []
                })
                st.rerun()

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
        st.error(f"❌ Incorrect. The correct answer is: {question['correct_answer']}")
    
    if 'explanation' in question:
        st.info(f"**Explanation:** {question['explanation']}")

def show_next_button():
    if st.button("Next Question"):
        st.session_state.quiz['current_index'] += 1
        st.session_state.quiz['submitted'] = False
        st.session_state.quiz['question_start'] = time.time()
        
        if st.session_state.quiz['current_index'] >= len(st.session_state.quiz['current_questions']):
            show_results()
        else:
            st.rerun()

def show_results():
    total_questions = len(st.session_state.quiz['current_questions'])
    correct_answers = st.session_state.quiz['score']
    user_score_percentage = correct_answers / total_questions

    # Show the result message
    st.success(f"""
    ## Quiz Completed!
    **Your Score:** {correct_answers}/{total_questions}
    **Your Score Percentage:** {user_score_percentage * 100:.2f}%
    """)

    # Plot a comparison with the benchmark score
    fig, ax = plt.subplots()
    categories = ['Your Score', 'Benchmark (75%)']
    scores = [user_score_percentage, 0.75]
    ax.bar(categories, scores, color=['blue', 'red'])

    # Display the bar chart
    st.pyplot(fig)

    # Provide a list of topics to study based on incorrect answers
    topics_to_study = get_topics_to_study()
    st.write("### Topics to Study Based on Incorrect Answers:")
    for topic in topics_to_study:
        st.write(f"- {topic}")

    # Provide an option to return to category selection or retry
    if st.button("Return to Category Selection"):
        reset_quiz_state()
        st.rerun()

def get_topics_to_study():
    # Determine which topics the user answered incorrectly
    topics_to_study = []
    for question in st.session_state.quiz['current_questions']:
        if question['correct_answer'] != st.session_state.quiz['user_answer']:
            topics_to_study.append(question['topic'])
    return set(topics_to_study)  # Remove duplicates

def reset_quiz_state():
    st.session_state.quiz = {
        'all_questions': load_questions(),
        'current_questions': [],
        'score': 0,
        'current_index': 0,
        'user_answer': None,
        'submitted': False,
        'start_time': time.time(),
        'question_start': time.time(),
        'time_spent': [],
        'mode': 'category_selection',
        'selected_category': None
    }

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
