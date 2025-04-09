import streamlit as st
import json
import os

# Load JSON data (with error handling)
def load_questions(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: File '{json_path}' not found.")
        return None
    except json.JSONDecodeError:
        st.error("Error: Invalid JSON format.")
        return None

# Get the correct path (works locally & on Streamlit Cloud)
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "questions.json")

# Load data once and cache it
@st.cache_data
def get_data():
    return load_questions(json_path)

data = get_data()

# --- Streamlit UI ---
st.title("CFA Quiz App")

if not data:
    st.error("Failed to load questions. Check the JSON file.")
else:
    questions = data.get("questions", [])
    st.write(f"Loaded {len(questions)} questions.")

    # Example: Display the first question
    if questions:
        q = questions[0]
        st.subheader(q["question"])
        answer = st.radio("Select an answer:", q["choices"])
        
        if st.button("Submit"):
            if answer == q["correct_answer"]:
                st.success("Correct! ✅")
            else:
                st.error(f"Wrong! Correct answer: {q['correct_answer']}")
