import streamlit as st
import time

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

# ===== SAMPLE QUESTIONS =====
questions = [
    # Ethical and Professional Standards
    {
        "question": "Which action violates CFA Standards?",
        "options": ["Using client brokerage for research", "Disclosing transactions without permission", 
                   "Keeping records for 5 years", "Both A and B", "All of the above"],
        "correct_answer": "Both A and B",
        "category": "Ethical and Professional Standards",
        "difficulty": "High",
        "explanation": "Standard III(A) requires acting for client benefit, III(E) requires confidentiality."
    },
    
    # Quantitative Methods
    {
        "question": "What's the probability of two heads in three coin tosses?",
        "options": ["0.125", "0.250", "0.375", "0.500", "0.625"],
        "correct_answer": "0.375",
        "category": "Quantitative Methods",
        "difficulty": "Medium",
        "explanation": "Binomial formula: C(3,2)*(0.5)^3 = 0.375"
    },
    
    # Economics
    {
        "question": "What shifts short-run aggregate supply right?",
        "options": ["Higher commodity prices", "Lower productivity", 
                   "Lower wages", "Higher taxes", "Tighter monetary policy"],
        "correct_answer": "Lower wages",
        "category": "Economics",
        "difficulty": "Medium",
        "explanation": "Reduction in input costs increases short-run aggregate supply."
    },
    
    # Financial Statement Analysis
    {
        "question": "Switching from FIFO to LIFO in inflation increases which ratio?",
        "options": ["Current ratio", "Debt-to-equity", 
                   "Gross margin", "Inventory turnover", "ROA"],
        "correct_answer": "Inventory turnover",
        "category": "Financial Statement Analysis",
        "difficulty": "High",
        "explanation": "LIFO results in higher COGS and lower ending inventory."
    },
    
    # Corporate Issuers
    {
        "question": "Which is NOT an advantage of debt financing?",
        "options": ["Tax deductibility", "Lower cost than equity", 
                   "No ownership dilution", "Fixed payments", "Financial leverage"],
        "correct_answer": "Fixed payments",
        "category": "Corporate Issuers",
        "difficulty": "Medium",
        "explanation": "Fixed payments are a disadvantage as they create mandatory cash outflows."
    },
    
    # Equity Investments
    {
        "question": "Which valuation method is best for stable dividend payers?",
        "options": ["DCF", "Dividend discount model", 
                   "Residual income", "P/E multiples", "Asset-based"],
        "correct_answer": "Dividend discount model",
        "category": "Equity Investments",
        "difficulty": "Medium",
        "explanation": "DDM is most suitable for companies with stable, predictable dividend policies."
    },
    
    # Fixed Income
    {
        "question": "What increases a bond's duration?",
        "options": ["Higher coupon", "Higher yield", 
                   "Shorter maturity", "Lower payment frequency", "Call feature"],
        "correct_answer": "Lower payment frequency",
        "category": "Fixed Income",
        "difficulty": "High",
        "explanation": "Less frequent payments increase duration as cash flows are received later."
    },
    
    # Derivatives
    {
        "question": "European options can be exercised:",
        "options": ["Anytime", "Only at expiration", 
                   "Monthly", "Weekly", "When in-the-money"],
        "correct_answer": "Only at expiration",
        "category": "Derivatives",
        "difficulty": "Medium",
        "explanation": "European options have this key difference from American options."
    },
    
    # Alternative Investments
    {
        "question": "Hedge funds commonly use:",
        "options": ["High liquidity", "No performance fees", 
                   "Leverage", "Only long positions", "SEC registration"],
        "correct_answer": "Leverage",
        "category": "Alternative Investments",
        "difficulty": "Medium",
        "explanation": "Hedge funds commonly employ leverage to enhance returns."
    },
    
    # Portfolio Management
    {
        "question": "The optimal portfolio maximizes:",
        "options": ["Return", "Risk-adjusted return", 
                   "Alpha", "Diversification", "Liquidity"],
        "correct_answer": "Risk-adjusted return",
        "category": "Portfolio Management",
        "difficulty": "High",
        "explanation": "The optimal portfolio provides the highest return per unit of risk."
    }
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
            'mode': 'category_selection',
            'selected_category': None
        }

def show_category_selection():
    st.markdown("## Select a CFA Topic Area")
    
    # Count questions per category
    category_counts = {}
    for q in st.session_state.quiz['all_questions']:
        category_counts[q['category']] = category_counts.get(q['category'], 0) + 1
    
    # Display buttons for each category
    cols = st.columns(2)
    for i, category in enumerate(CATEGORIES):
        with cols[i % 2]:
            if st.button(f"{category} ({category_counts.get(category, 0)} questions)"):
                # Filter questions for selected category
                st.session_state.quiz['current_questions'] = [
                    q for q in st.session_state.quiz['all_questions'] 
                    if q['category'] == category
                ]
                st.session_state.quiz['current_index'] = 0
                st.session_state.quiz['mode'] = 'question'
                st.session_state.quiz['selected_category'] = category
                st.session_state.quiz['question_start'] = time.time()
                st.session_state.quiz['submitted'] = False
                st.rerun()

def display_question():
    # Check if we have questions to display
    if not st.session_state.quiz['current_questions']:
        st.warning("No questions available for this category")
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()
        return
    
    # Safely get current question
    try:
        question = st.session_state.quiz['current_questions'][st.session_state.quiz['current_index']]
    except IndexError:
        st.error("Question index out of range. Returning to category selection.")
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()
        return
    
    # Display question info
    st.markdown(f"### {question['category']}")
    st.markdown(f"**Question {st.session_state.quiz['current_index'] + 1} of {len(st.session_state.quiz['current_questions'])}**")
    st.markdown(f"*{question['question']}*")
    
    # Display options
    user_answer = st.radio("Select your answer:", question['options'], key=f"q{st.session_state.quiz['current_index']}")
    
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
