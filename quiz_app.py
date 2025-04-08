import streamlit as st
import time
import random

# ===== CFA CONFIGURATION =====
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

# ===== SAMPLE QUESTIONS FOR ALL CATEGORIES =====
questions = [
    # Ethical and Professional Standards (3 questions)
    {
        "question": "Which action violates CFA Standards?",
        "options": ["Using client brokerage for research", "Disclosing transactions without permission", 
                   "Keeping records for 5 years", "Both A and B", "All of the above"],
        "correct_answer": "Both A and B",
        "category": "Ethical and Professional Standards",
        "difficulty": "High"
    },
    {
        "question": "Under GIPS, what must be included?",
        "options": ["All fee-paying portfolios", "Cash-basis accounting", 
                   "Gross-of-fee returns only", "Both A and C", "All of the above"],
        "correct_answer": "All fee-paying portfolios",
        "category": "Ethical and Professional Standards",
        "difficulty": "Medium"
    },
    {
        "question": "What does Standard III(A) require?",
        "options": ["Loyalty to employer", "Duty to clients", 
                   "Fair dealing", "Disclosure of conflicts", "All of the above"],
        "correct_answer": "Duty to clients",
        "category": "Ethical and Professional Standards",
        "difficulty": "Medium"
    },
    
    # Quantitative Methods (3 questions)
    {
        "question": "Probability of two heads in three coin tosses?",
        "options": ["0.125", "0.250", "0.375", "0.500", "0.625"],
        "correct_answer": "0.375",
        "category": "Quantitative Methods",
        "difficulty": "Medium"
    },
    {
        "question": "If P(A)=0.4, P(B)=0.3, independent, P(A or B) is:",
        "options": ["0.12", "0.58", "0.70", "0.82", "1.00"],
        "correct_answer": "0.58",
        "category": "Quantitative Methods",
        "difficulty": "Medium"
    },
    {
        "question": "What is the mean of: 5, 7, 9, 11?",
        "options": ["7", "8", "9", "10", "11"],
        "correct_answer": "8",
        "category": "Quantitative Methods",
        "difficulty": "Easy"
    },
    
    # Economics (3 questions)
    {
        "question": "What shifts short-run aggregate supply right?",
        "options": ["Higher commodity prices", "Lower productivity", 
                   "Lower wages", "Higher taxes", "Tighter monetary policy"],
        "correct_answer": "Lower wages",
        "category": "Economics",
        "difficulty": "Medium"
    },
    
    # Add 2 more Economics questions...
    
    # Financial Statement Analysis (3 questions)
    {
        "question": "Switching from FIFO to LIFO in inflation increases which ratio?",
        "options": ["Current ratio", "Debt-to-equity", 
                   "Gross margin", "Inventory turnover", "ROA"],
        "correct_answer": "Inventory turnover",
        "category": "Financial Statement Analysis",
        "difficulty": "High"
    },
    
    # Add 2 more FSA questions...
    
    # Corporate Issuers (3 questions)
    {
        "question": "Which is NOT an advantage of debt financing?",
        "options": ["Tax deductibility", "Lower cost than equity", 
                   "No ownership dilution", "Fixed payments", "Financial leverage"],
        "correct_answer": "Fixed payments",
        "category": "Corporate Issuers",
        "difficulty": "Medium"
    },
    
    # Add 2 more Corporate Issuers questions...
    
    # Continue with 3 questions each for remaining categories...
]

# ===== QUIZ ENGINE =====
def initialize_session_state():
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
            'all_questions': questions,
            'current_questions': [],
            'score': 0,
            'current_index': 0,
            'user_answer': None,
            'submitted': False,
            'start_time': time.time(),
            'question_start': time.time(),
            'time_spent': [],
            'mode': 'category_selection'  # New state to track navigation
        }

def show_category_selection():
    st.markdown("## Select a CFA Topic Area")
    
    # Group questions by category
    category_counts = {}
    for q in st.session_state.quiz['all_questions']:
        category_counts[q['category']] = category_counts.get(q['category'], 0) + 1
    
    # Display buttons for each category
    for category in CATEGORIES:
        count = category_counts.get(category, 0)
        if st.button(f"{category} ({count} questions)"):
            # Filter questions for selected category
            st.session_state.quiz['current_questions'] = [
                q for q in st.session_state.quiz['all_questions'] 
                if q['category'] == category
            ]
            st.session_state.quiz['current_index'] = 0
            st.session_state.quiz['mode'] = 'question'
            st.session_state.quiz['question_start'] = time.time()
            st.rerun()

def display_question():
    if not st.session_state.quiz['current_questions']:
        st.warning("No questions available for this category")
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()
        return
    
    question = st.session_state.quiz['current_questions'][st.session_state.quiz['current_index']]
    
    # Display question info
    st.markdown(f"### {question['category']}")
    st.markdown(f"**Question {st.session_state.quiz['current_index'] + 1} of {len(st.session_state.quiz['current_questions']}**")
    st.markdown(f"*{question['question']}*")
    
    # Display options
    user_answer = st.radio("Select your answer:", question['options'])
    
    # Submit button
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
    total_time = time.time() - st.session_state.quiz['start_time']
    avg_time = sum(st.session_state.quiz['time_spent'])/len(st.session_state.quiz['time_spent']) if st.session_state.quiz['time_spent'] else 0
    
    st.success(f"""
    ## Quiz Completed!
    **Score:** {st.session_state.quiz['score']}/{len(st.session_state.quiz['current_questions'])}
    **Total Time:** {format_time(total_time)}
    **Avg Time/Question:** {format_time(avg_time)}
    """)
    
    if st.button("Return to Category Selection"):
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()

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
