import streamlit as st
import time

# ===== UPDATED CFA CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"
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
    # [...] (other categories remain the same)
}

# ===== EXPANDED QUESTION BANK =====
questions = [
    # Ethical and Professional Standards - Question 1
    {
        "question": "According to CFA Standards, which action violates professional conduct?",
        "options": [
            "Using client brokerage for research reports",
            "Disclosing transactions without permission",
            "Keeping records for 5 instead of 7 years",
            "Both A and B",
            "All of the above"
        ],
        "correct_answer": "Both A and B",
        "category": "Ethical and Professional Standards",
        "explanation": "Standard III(A) requires acting for client benefit, III(E) requires confidentiality.",
        "difficulty": "High",
        "reading_reference": "Standard III(A) and III(E)"
    },
    
    # Ethical and Professional Standards - Question 2
    {
        "question": "Under GIPS, which is required for compliant performance reporting?",
        "options": [
            "Including all fee-paying portfolios",
            "Using cash-basis accounting",
            "Presenting gross-of-fee returns only",
            "Both A and C",
            "All of the above"
        ],
        "correct_answer": "Including all fee-paying portfolios",
        "category": "Ethical and Professional Standards",
        "explanation": "GIPS requires all actual, fee-paying discretionary portfolios in composites.",
        "difficulty": "Medium",
        "reading_reference": "Global Investment Performance Standards"
    },
    
    # Quantitative Methods - Question 1
    {
        "question": "What's the probability of two heads in three coin tosses?",
        "options": ["0.125", "0.250", "0.375", "0.500", "0.625"],
        "correct_answer": "0.375",
        "category": "Quantitative Methods",
        "explanation": "Binomial formula: C(3,2)*(0.5)^3 = 0.375",
        "difficulty": "Medium",
        "reading_reference": "Probability Concepts"
    },
    
    # Quantitative Methods - Question 2
    {
        "question": "If P(A) = 0.4 and P(B) = 0.3, and independent, P(A or B) is:",
        "options": ["0.12", "0.58", "0.70", "0.82", "1.00"],
        "correct_answer": "0.58",
        "category": "Quantitative Methods",
        "explanation": "P(A or B) = P(A) + P(B) - P(A and B) = 0.4 + 0.3 - 0.12 = 0.58",
        "difficulty": "Medium",
        "reading_reference": "Probability Concepts"
    },
    
    # [...] (Add multiple questions for all categories)
]

# ===== KEY FIXES =====
def initialize_session_state():
    """Initialize with all categories enabled"""
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
            'score': 0,
            'current_question': 0,
            'user_answer': None,
            'submitted': False,
            'show_next': False,
            'category_scores': {cat: 0 for cat in CATEGORIES},
            'category_totals': {cat: len([q for q in questions if q['category'] == cat]) for cat in CATEGORIES},
            'difficulty_scores': {"Easy": 0, "Medium": 0, "High": 0},
            'start_time': time.time(),
            'question_start_time': time.time(),
            'time_spent': [],
            'show_category_intros': True,
            'available_categories': list(CATEGORIES.keys())  # Track accessible categories
        }

def show_category_selection():
    """Let users select which category to attempt"""
    st.markdown("## Select a Topic Area")
    for category in st.session_state.quiz['available_categories']:
        if st.button(f"{category} ({st.session_state.quiz['category_totals'][category]} questions)"):
            # Find first question in this category
            for i, q in enumerate(questions):
                if q['category'] == category:
                    st.session_state.quiz['current_question'] = i
                    st.session_state.quiz['show_category_intros'] = False
                    st.session_state.quiz['question_start_time'] = time.time()
                    st.rerun()

# ===== MODIFIED MAIN LOGIC =====
def main():
    st.set_page_config(layout="wide")
    st.title(f"📊 {QUIZ_TITLE}")
    
    initialize_session_state()
    
    # Category selection screen
    if st.session_state.quiz['show_category_intros']:
        show_category_selection()
        return
    
    # [...] (rest of the code remains the same)

if __name__ == "__main__":
    main()
