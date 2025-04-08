import streamlit as st
import time

# ===== UPDATED CFA CONFIGURATION (2024 EXAM WEIGHTS) =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"
CATEGORIES = {
    "Ethical and Professional Standards": {
        "description": "Focuses on ethical principles and professional standards for investment professionals",
        "weight": 0.15,
        "readings": ["Code of Ethics", "Standards of Professional Conduct", "GIPS"]
    },
    "Quantitative Methods": {
        "description": "Covers statistical tools and techniques for financial analysis",
        "weight": 0.10,
        "readings": ["Time Value of Money", "Probability Concepts", "Sampling and Estimation"]
    },
    "Economics": {
        "description": "Examines macroeconomic and microeconomic concepts relevant to finance",
        "weight": 0.10,
        "readings": ["Demand and Supply Analysis", "Business Cycles", "Monetary and Fiscal Policy"]
    },
    "Financial Statement Analysis": {
        "description": "Analysis of financial statements to assess company performance",
        "weight": 0.15,
        "readings": ["Income Statements", "Balance Sheets", "Cash Flow Statements"]
    },
    "Corporate Issuers": {
        "description": "Characteristics of corporate issuers including structure and governance",
        "weight": 0.10,
        "readings": ["Capital Structure", "Corporate Governance", "Mergers and Acquisitions"]
    },
    "Equity Investments": {
        "description": "Valuation and analysis of equity securities",
        "weight": 0.11,
        "readings": ["Market Organization", "Equity Valuation", "Industry Analysis"]
    },
    "Fixed Income": {
        "description": "Characteristics and analysis of fixed-income securities",
        "weight": 0.11,
        "readings": ["Bond Valuation", "Yield Measures", "Credit Analysis"]
    },
    "Derivatives": {
        "description": "Valuation and use of derivative securities",
        "weight": 0.06,
        "readings": ["Forwards and Futures", "Options", "Swaps"]
    },
    "Alternative Investments": {
        "description": "Covers hedge funds, private equity, and real estate",
        "weight": 0.06,
        "readings": ["Private Capital", "Real Estate", "Commodities"]
    },
    "Portfolio Management": {
        "description": "Principles of portfolio construction and risk management",
        "weight": 0.06,
        "readings": ["Portfolio Risk and Return", "Investment Policy Statements", "Execution"]
    }
}

# ===== SAMPLE CFA QUESTIONS (5 OPTIONS EACH) =====
questions = [
    # Ethical and Professional Standards
    {
        "question": "According to the CFA Institute Standards of Professional Conduct, which action is most likely a violation?",
        "options": [
            "Using client brokerage to obtain research reports",
            "Disclosing client transactions to other clients without permission",
            "Maintaining records for 5 years instead of 7 years",
            "Both A and B",
            "All of the above"
        ],
        "correct_answer": "Both A and B",
        "category": "Ethical and Professional Standards",
        "explanation": "Standard III(A) requires members to act for the benefit of clients, and Standard III(E) requires preservation of confidentiality.",
        "difficulty": "High",
        "reading_reference": "Standard III(A) and III(E)"
    },
    
    # Quantitative Methods
    {
        "question": "What is the probability of getting exactly two heads in three tosses of a fair coin?",
        "options": [
            "0.125",
            "0.250",
            "0.375",
            "0.500",
            "0.625"
        ],
        "correct_answer": "0.375",
        "category": "Quantitative Methods",
        "explanation": "Using the binomial formula: C(3,2)*(0.5)^2*(0.5)^1 = 3*0.125 = 0.375",
        "difficulty": "Medium",
        "reading_reference": "Probability Concepts"
    },
    
    # Economics
    {
        "question": "Which of the following would most likely cause the short-run aggregate supply curve to shift to the right?",
        "options": [
            "Increase in commodity prices",
            "Decrease in productivity",
            "Reduction in nominal wages",
            "Increase in corporate taxes",
            "Tightening of monetary policy"
        ],
        "correct_answer": "Reduction in nominal wages",
        "category": "Economics",
        "explanation": "A reduction in input costs (like wages) increases short-run aggregate supply.",
        "difficulty": "Medium",
        "reading_reference": "Aggregate Output and Economic Growth"
    },
    
    # Financial Statement Analysis
    {
        "question": "Which ratio would most likely increase if a company switched from FIFO to LIFO inventory accounting during a period of rising prices?",
        "options": [
            "Current ratio",
            "Debt-to-equity ratio",
            "Gross profit margin",
            "Inventory turnover",
            "Return on assets"
        ],
        "correct_answer": "Inventory turnover",
        "category": "Financial Statement Analysis",
        "explanation": "LIFO results in higher COGS and lower ending inventory, increasing inventory turnover.",
        "difficulty": "High",
        "reading_reference": "Inventories"
    },
    
    # Corporate Issuers
    {
        "question": "Which of the following is least likely an advantage of using debt financing?",
        "options": [
            "Tax deductibility of interest",
            "Lower cost of capital than equity",
            "No dilution of ownership",
            "Fixed payment obligations",
            "Potential for positive financial leverage"
        ],
        "correct_answer": "Fixed payment obligations",
        "category": "Corporate Issuers",
        "explanation": "Fixed payments are a disadvantage as they create mandatory cash outflows.",
        "difficulty": "Medium",
        "reading_reference": "Capital Structure"
    },
    
    # Equity Investments
    {
        "question": "Which valuation approach would be most appropriate for a mature company with stable dividends?",
        "options": [
            "Free cash flow to equity",
            "Dividend discount model",
            "Residual income model",
            "Price-to-book ratio",
            "EV/EBITDA multiple"
        ],
        "correct_answer": "Dividend discount model",
        "category": "Equity Investments",
        "explanation": "DDM is most suitable for companies with stable, predictable dividend policies.",
        "difficulty": "Medium",
        "reading_reference": "Dividend Discount Valuation"
    },
    
    # Fixed Income
    {
        "question": "A bond's duration is most likely to increase when:",
        "options": [
            "Coupon rate increases",
            "Yield to maturity increases",
            "Maturity decreases",
            "Bond is callable",
            "Payment frequency decreases"
        ],
        "correct_answer": "Payment frequency decreases",
        "category": "Fixed Income",
        "explanation": "Less frequent payments increase duration as cash flows are received later.",
        "difficulty": "High",
        "reading_reference": "Understanding Yield Spreads"
    },
    
    # Derivatives
    {
        "question": "Which of the following is true about European-style options?",
        "options": [
            "They can be exercised anytime before expiration",
            "They are always more valuable than American options",
            "They can only be exercised at expiration",
            "They are only traded in Europe",
            "They have higher liquidity than American options"
        ],
        "correct_answer": "They can only be exercised at expiration",
        "category": "Derivatives",
        "explanation": "European options have this key difference from American options.",
        "difficulty": "Medium",
        "reading_reference": "Option Markets and Contracts"
    },
    
    # Alternative Investments
    {
        "question": "Which characteristic is most typical of hedge funds?",
        "options": [
            "High liquidity with daily redemptions",
            "Low management fees with no performance fees",
            "Use of leverage and derivatives",
            "Only accessible to retail investors",
            "Required to be registered with the SEC"
        ],
        "correct_answer": "Use of leverage and derivatives",
        "category": "Alternative Investments",
        "explanation": "Hedge funds commonly employ these strategies to enhance returns.",
        "difficulty": "Medium",
        "reading_reference": "Hedge Funds"
    },
    
    # Portfolio Management
    {
        "question": "According to modern portfolio theory, the optimal portfolio:",
        "options": [
            "Maximizes expected return",
            "Minimizes risk",
            "Maximizes the Sharpe ratio",
            "Contains only risk-free assets",
            "Eliminates all systematic risk"
        ],
        "correct_answer": "Maximizes the Sharpe ratio",
        "category": "Portfolio Management",
        "explanation": "The optimal portfolio provides the highest return per unit of risk.",
        "difficulty": "High",
        "reading_reference": "Portfolio Risk and Return"
    }
]

# ===== ENHANCED QUIZ ENGINE WITH TIMER =====
def initialize_session_state():
    """Initialize all quiz state variables"""
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
            'score': 0,
            'current_question': 0,
            'user_answer': None,
            'submitted': False,
            'show_next': False,
            'category_scores': {cat: 0 for cat in CATEGORIES},
            'category_totals': {cat: 0 for cat in CATEGORIES},
            'difficulty_scores': {"Easy": 0, "Medium": 0, "High": 0},
            'start_time': time.time(),
            'question_start_time': time.time(),
            'time_spent': [],
            'show_category_intros': True
        }
        # Count questions per category
        for q in questions:
            if q['category'] in CATEGORIES:
                st.session_state.quiz['category_totals'][q['category']] += 1

def format_time(seconds):
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def show_category_intro(category):
    """Display category description before first question"""
    st.markdown(f"## {category}")
    st.markdown(f"*{CATEGORIES[category]['description']}*")
    st.markdown(f"**Exam Weight:** {CATEGORIES[category]['weight']*100:.0f}%")
    st.markdown("**Key Readings:**")
    for reading in CATEGORIES[category]['readings']:
        st.markdown(f"- {reading}")
    if st.button(f"Begin {category} Questions"):
        st.session_state.quiz['show_category_intros'] = False
        st.session_state.quiz['question_start_time'] = time.time()
        st.rerun()

def display_question():
    """Display the current question with timing"""
    question = questions[st.session_state.quiz['current_question']]
    category = question['category']
    
    # Calculate time spent on current question
    current_time = time.time()
    time_spent = current_time - st.session_state.quiz['question_start_time']
    
    # Header with category and timing
    col1, col2, col3 = st.columns([2, 2, 1])
    col1.markdown(f"**Category:** {category}")
    col2.markdown(f"**Time Spent:** {format_time(time_spent)}")
    col3.markdown(f"**Difficulty:** {question.get('difficulty', 'N/A')}")
    
    # Question display
    st.markdown(f"### Question {st.session_state.quiz['current_question'] + 1}")
    st.markdown(f"**{question['question']}**")
    
    # Answer options
    user_answer = st.radio(
        "Select your answer:",
        question['options'],
        key=f"q{st.session_state.quiz['current_question']}"
    )
    
    # Submit button
    if st.button("Submit Answer"):
        process_answer(question, user_answer, time_spent)

def process_answer(question, user_answer, time_spent):
    """Handle answer submission and scoring"""
    st.session_state.quiz['user_answer'] = user_answer
    st.session_state.quiz['submitted'] = True
    st.session_state.quiz['show_next'] = True
    st.session_state.quiz['time_spent'].append(time_spent)
    
    # Update scores if correct
    if user_answer == question["correct_answer"]:
        st.session_state.quiz['score'] += 1
        st.session_state.quiz['category_scores'][question["category"]] += 1
        st.session_state.quiz['difficulty_scores'][question.get("difficulty", "Medium")] += 1
    
    st.rerun()

def show_answer_feedback(question):
    """Show detailed feedback after answering"""
    if st.session_state.quiz['user_answer'] == question["correct_answer"]:
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect! The correct answer is: **{question['correct_answer']}**")
    
    if "explanation" in question:
        st.info(f"**Explanation:** {question['explanation']}")
    if "reading_reference" in question:
        st.markdown(f"📚 **Reference:** {question['reading_reference']}")

def show_results():
    """Display comprehensive results"""
    st.balloons()
    total_time = time.time() - st.session_state.quiz['start_time']
    avg_time = sum(st.session_state.quiz['time_spent'])/len(questions) if questions else 0
    
    st.success(f"""
    ## CFA Quiz Completed!
    **Overall Score:** {st.session_state.quiz['score']}/{len(questions)} ({st.session_state.quiz['score']/len(questions)*100:.1f}%)
    **Total Time:** {format_time(total_time)}
    **Average Time per Question:** {format_time(avg_time)}
    """)
    
    # Category performance analysis
    st.markdown("### Performance by Topic Area")
    for category in CATEGORIES:
        correct = st.session_state.quiz['category_scores'][category]
        total = st.session_state.quiz['category_totals'][category]
        if total > 0:
            performance = correct/total
            st.markdown(
                f"- **{category}:** {correct}/{total} ({performance:.0%}) "
                f"(Target: {CATEGORIES[category]['weight']*100:.0f}% of exam)"
            )
            st.progress(performance)

# ===== MAIN APP =====
def main():
    st.set_page_config(layout="wide")
    st.title(f"📊 {QUIZ_TITLE}")
    
    initialize_session_state()
    
    # Category introduction screen
    if st.session_state.quiz['show_category_intros'] and st.session_state.quiz['current_question'] < len(questions):
        current_category = questions[st.session_state.quiz['current_question']]['category']
        show_category_intro(current_category)
        return
    
    # Quiz progress
    if questions:
        progress = st.session_state.quiz['current_question'] / len(questions)
        st.progress(progress)
    
    # Question or results display
    if st.session_state.quiz['current_question'] >= len(questions):
        show_results()
        if st.button("🔄 Restart Quiz"):
            st.session_state.clear()
            st.rerun()
    else:
        display_question()
        if st.session_state.quiz['submitted']:
            question = questions[st.session_state.quiz['current_question']]
            show_answer_feedback(question)
            if st.session_state.quiz['show_next'] and st.button("⏭️ Next Question"):
                st.session_state.quiz['current_question'] += 1
                st.session_state.quiz['submitted'] = False
                st.session_state.quiz['show_next'] = False
                st.session_state.quiz['user_answer'] = None
                st.session_state.quiz['question_start_time'] = time.time()
                st.rerun()

if __name__ == "__main__":
    main()
