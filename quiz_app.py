import streamlit as st
import json
import time
import os

# Debugging info
print("App is starting...")

updated_json_path = 'Data/updated_questions_with_5_options_final.json'

# Function to load questions
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
        st.stop()
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON format in questions file")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected error loading questions: {str(e)}")
        st.stop()

# Initialize session state
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

# Handle category selection
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
                print(f"Mode changed to question for {category}")
                st.rerun()

# Display the question
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

def show_results():
    total_time = time.time() - st.session_state.quiz['start_time']
    avg_time = sum(st.session_state.quiz['time_spent'])/len(st.session_state.quiz['time_spent']) if st.session_state.quiz['time_spent'] else 0
    
    st.success(f"""
    ## Quiz Completed!
    **Score:** {st.session_state.quiz['score']}/{len(st.session_state.quiz['current_questions'])}
    **Total Time:** {format_time(total_time)}
    **Avg Time/Question:** {format_time(avg_time)}
    """)

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

# Main app function
def main():
    st.set_page_config(layout="wide")
    st.title("📊 CFA Exam Preparation Quiz")
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
