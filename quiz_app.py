import os
import json
import time
import streamlit as st

# ===== 1. Load JSON Data =====
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "Data", "updated_questions_with_5_options_final.json")

try:
    with open(json_path, "r", encoding="utf-8") as f:
        updated_questions_data = json.load(f)
    questions_by_category = {}
    for q in updated_questions_data.get("questions", []):
        category = q.get("category", "Uncategorized")
        questions_by_category.setdefault(category, []).append(q)
except Exception as e:
    st.error(f"Error loading questions: {e}")
    questions_by_category = {}

# ===== 2. Initialize Session State =====
if 'quiz' not in st.session_state:
    st.session_state.quiz = {
        'mode': 'category_selection',
        'current_questions': [],
        'current_index': 0,
        'score': 0,
        'submitted': False
    }

# ===== 3. App UI =====
def main():
    st.title("CFA Quiz App")
    
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()

def show_category_selection():
    st.write("## Select a Topic")
    for category, questions in questions_by_category.items():
        if st.button(f"{category} ({len(questions)} questions)"):
            st.session_state.quiz.update({
                'mode': 'question',
                'current_questions': questions,
                'current_index': 0,
                'score': 0
            })

def display_question():
    questions = st.session_state.quiz['current_questions']
    idx = st.session_state.quiz['current_index']
    
    if idx >= len(questions):
        st.success("Quiz complete!")
        return
    
    q = questions[idx]
    st.write(f"**Question {idx + 1}:** {q['question']}")
    
    user_answer = st.radio("Options:", q['options'])
    
    if st.button("Submit"):
        if user_answer == q['correct_answer']:
            st.session_state.quiz['score'] += 1
            st.success("Correct!")
        else:
            st.error(f"Wrong! Correct answer: {q['correct_answer']}")
        
        st.session_state.quiz['current_index'] += 1
        if st.session_state.quiz['current_index'] >= len(questions):
            st.session_state.quiz['mode'] = 'results'

if __name__ == "__main__":
    main()
