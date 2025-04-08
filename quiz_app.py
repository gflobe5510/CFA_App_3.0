import streamlit as st
import time
from typing import Dict, List, Optional, TypedDict
from dataclasses import dataclass
import random

# ===== DATA STRUCTURES =====
@dataclass
class Category:
    description: str
    weight: float
    readings: List[str]

@dataclass
class Question:
    question: str
    options: List[str]
    correct_answer: str
    category: str
    difficulty: str
    explanation: str

class QuizState(TypedDict):
    all_questions: List[Question]
    current_questions: List[Question]
    score: int
    current_index: int
    user_answer: Optional[str]
    submitted: bool
    start_time: float
    question_start: float
    time_spent: List[float]
    mode: str
    selected_category: Optional[str]
    question_order: List[int]

# ===== APP CONFIGURATION =====
QUIZ_TITLE = "CFA Exam Preparation Quiz"
CATEGORIES: Dict[str, Category] = {
    "Ethical and Professional Standards": Category(
        description="Focuses on ethical principles and professional standards",
        weight=0.15,
        readings=["Code of Ethics", "Standards of Professional Conduct", "GIPS"]
    ),
    "Quantitative Methods": Category(
        description="Covers statistical tools for financial analysis",
        weight=0.10,
        readings=["Time Value of Money", "Probability Concepts"]
    ),
    "Economics": Category(
        description="Examines macroeconomic and microeconomic concepts",
        weight=0.10,
        readings=["Demand and Supply", "Business Cycles"]
    ),
    "Financial Statement Analysis": Category(
        description="Analysis of financial statements",
        weight=0.15,
        readings=["Income Statements", "Balance Sheets"]
    ),
    "Corporate Issuers": Category(
        description="Characteristics of corporate issuers",
        weight=0.10,
        readings=["Capital Structure", "Corporate Governance"]
    ),
    "Equity Investments": Category(
        description="Valuation of equity securities",
        weight=0.11,
        readings=["Market Organization", "Equity Valuation"]
    ),
    "Fixed Income": Category(
        description="Analysis of fixed-income securities",
        weight=0.11,
        readings=["Bond Valuation", "Yield Measures"]
    ),
    "Derivatives": Category(
        description="Valuation of derivative securities",
        weight=0.06,
        readings=["Forwards and Futures", "Options"]
    ),
    "Alternative Investments": Category(
        description="Hedge funds, private equity, real estate",
        weight=0.06,
        readings=["Private Capital", "Real Estate"]
    ),
    "Portfolio Management": Category(
        description="Portfolio construction and risk management",
        weight=0.06,
        readings=["Portfolio Risk", "Investment Policy"]
    )
}

# ===== QUESTION BANK =====
def load_questions() -> List[Question]:
    """Load and return all questions with proper typing"""
    return [
        Question(
            question="Which action violates CFA Standards?",
            options=["Using client brokerage for research", "Disclosing transactions without permission", 
                   "Keeping records for 5 years", "Both A and B", "All of the above"],
            correct_answer="Both A and B",
            category="Ethical and Professional Standards",
            difficulty="High",
            explanation="Standard III(A) requires acting for client benefit, III(E) requires confidentiality."
        ),
        Question(
            question="What's the probability of two heads in three coin tosses?",
            options=["0.125", "0.250", "0.375", "0.500", "0.625"],
            correct_answer="0.375",
            category="Quantitative Methods",
            difficulty="Medium",
            explanation="Binomial formula: C(3,2)*(0.5)^3 = 0.375"
        ),
        Question(
            question="What shifts short-run aggregate supply right?",
            options=["Higher commodity prices", "Lower productivity", 
                   "Lower wages", "Higher taxes", "Tighter monetary policy"],
            correct_answer="Lower wages",
            category="Economics",
            difficulty="Medium",
            explanation="Reduction in input costs increases short-run aggregate supply."
        ),
        Question(
            question="Switching from FIFO to LIFO in inflation increases which ratio?",
            options=["Current ratio", "Debt-to-equity", 
                   "Gross margin", "Inventory turnover", "ROA"],
            correct_answer="Inventory turnover",
            category="Financial Statement Analysis",
            difficulty="High",
            explanation="LIFO results in higher COGS and lower ending inventory."
        ),
        Question(
            question="Which is NOT an advantage of debt financing?",
            options=["Tax deductibility", "Lower cost than equity", 
                   "No ownership dilution", "Fixed payments", "Financial leverage"],
            correct_answer="Fixed payments",
            category="Corporate Issuers",
            difficulty="Medium",
            explanation="Fixed payments are a disadvantage as they create mandatory cash outflows."
        ),
        Question(
            question="Which valuation method is best for stable dividend payers?",
            options=["DCF", "Dividend discount model", 
                   "Residual income", "P/E multiples", "Asset-based"],
            correct_answer="Dividend discount model",
            category="Equity Investments",
            difficulty="Medium",
            explanation="DDM is most suitable for companies with stable, predictable dividend policies."
        ),
        Question(
            question="What increases a bond's duration?",
            options=["Higher coupon", "Higher yield", 
                   "Shorter maturity", "Lower payment frequency", "Call feature"],
            correct_answer="Lower payment frequency",
            category="Fixed Income",
            difficulty="High",
            explanation="Less frequent payments increase duration as cash flows are received later."
        ),
        Question(
            question="European options can be exercised:",
            options=["Anytime", "Only at expiration", 
                   "Monthly", "Weekly", "When in-the-money"],
            correct_answer="Only at expiration",
            category="Derivatives",
            difficulty="Medium",
            explanation="European options have this key difference from American options."
        ),
        Question(
            question="Hedge funds commonly use:",
            options=["High liquidity", "No performance fees", 
                   "Leverage", "Only long positions", "SEC registration"],
            correct_answer="Leverage",
            category="Alternative Investments",
            difficulty="Medium",
            explanation="Hedge funds commonly employ leverage to enhance returns."
        ),
        Question(
            question="The optimal portfolio maximizes:",
            options=["Return", "Risk-adjusted return", 
                   "Alpha", "Diversification", "Liquidity"],
            correct_answer="Risk-adjusted return",
            category="Portfolio Management",
            difficulty="High",
            explanation="The optimal portfolio provides the highest return per unit of risk."
        )
    ]

# ===== UTILITY FUNCTIONS =====
def format_time(seconds: float) -> str:
    """Format seconds into MM:SS"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def calculate_performance_metrics(quiz_state: QuizState) -> Dict[str, float]:
    """Calculate various performance metrics"""
    if not quiz_state['time_spent'] or not quiz_state['current_questions']:
        return {}
    
    total_time = time.time() - quiz_state['start_time']
    avg_time = sum(quiz_state['time_spent']) / len(quiz_state['time_spent'])
    accuracy = quiz_state['score'] / len(quiz_state['current_questions']) * 100
    
    return {
        'total_time': total_time,
        'avg_time': avg_time,
        'accuracy': accuracy
    }

# ===== QUIZ ENGINE =====
def initialize_session_state() -> None:
    """Initialize or reset the quiz session state"""
    if 'quiz' not in st.session_state:
        st.session_state.quiz: QuizState = {
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
            'selected_category': None,
            'question_order': []
        }

def shuffle_questions(questions: List[Question]) -> List[Question]:
    """Shuffle questions and return a new list"""
    return random.sample(questions, k=len(questions))

def show_category_selection() -> None:
    """Display category selection interface"""
    st.markdown("## Select a CFA Topic Area")
    
    # Count questions per category
    category_counts = {}
    for q in st.session_state.quiz['all_questions']:
        category_counts[q.category] = category_counts.get(q.category, 0) + 1
    
    # Display category cards
    cols = st.columns(2)
    for i, (category, cat_data) in enumerate(CATEGORIES.items()):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"**{category}**")
                st.caption(cat_data.description)
                st.write(f"📚 Readings: {', '.join(cat_data.readings)}")
                st.write(f"🔢 Weight: {cat_data.weight:.0%}")
                st.write(f"❓ Questions: {category_counts.get(category, 0)}")
                
                if st.button(f"Select {category}", key=f"cat_{i}"):
                    start_quiz_for_category(category)

def start_quiz_for_category(category: str) -> None:
    """Initialize quiz for selected category"""
    st.session_state.quiz['current_questions'] = [
        q for q in st.session_state.quiz['all_questions'] 
        if q.category == category
    ]
    
    # Shuffle questions
    st.session_state.quiz['current_questions'] = shuffle_questions(
        st.session_state.quiz['current_questions']
    )
    
    st.session_state.quiz.update({
        'current_index': 0,
        'mode': 'question',
        'selected_category': category,
        'question_start': time.time(),
        'submitted': False,
        'score': 0,
        'time_spent': []
    })
    st.rerun()

def display_question() -> None:
    """Display current question and handle answers"""
    if not st.session_state.quiz['current_questions']:
        st.warning("No questions available for this category")
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()
        return
    
    try:
        question = st.session_state.quiz['current_questions'][st.session_state.quiz['current_index']]
    except IndexError:
        st.error("Question index out of range. Returning to category selection.")
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()
        return
    
    # Display question header
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Category:** {question.category}")
            st.markdown(f"**Difficulty:** {question.difficulty}")
        with col2:
            st.markdown(f"**Question {st.session_state.quiz['current_index'] + 1} of {len(st.session_state.quiz['current_questions'])}**")
    
    # Display question
    st.markdown(f"#### {question.question}")
    
    # Display options
    user_answer = st.radio(
        "Select your answer:",
        question.options,
        key=f"q{st.session_state.quiz['current_index']}",
        index=None
    )
    
    # Submit button
    if st.button("Submit Answer", disabled=user_answer is None):
        process_answer(question, user_answer)

def process_answer(question: Question, user_answer: str) -> None:
    """Process user's answer and update state"""
    time_spent = time.time() - st.session_state.quiz['question_start']
    st.session_state.quiz['time_spent'].append(time_spent)
    st.session_state.quiz['user_answer'] = user_answer
    st.session_state.quiz['submitted'] = True
    
    if user_answer == question.correct_answer:
        st.session_state.quiz['score'] += 1
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect. The correct answer is: **{question.correct_answer}**")
    
    st.info(f"**Explanation:** {question.explanation}")

def show_next_button() -> None:
    """Display navigation buttons after answer submission"""
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Next Question"):
            move_to_next_question()
    
    # Show progress bar
    with col2:
        progress = (st.session_state.quiz['current_index'] + 1) / len(st.session_state.quiz['current_questions'])
        st.progress(min(progress, 1.0))  # Ensure doesn't exceed 100%

def move_to_next_question() -> None:
    """Advance to next question or show results"""
    st.session_state.quiz['current_index'] += 1
    st.session_state.quiz['submitted'] = False
    st.session_state.quiz['question_start'] = time.time()
    
    if st.session_state.quiz['current_index'] >= len(st.session_state.quiz['current_questions']):
        st.session_state.quiz['mode'] = 'results'
    st.rerun()

def show_results() -> None:
    """Display quiz results and performance metrics"""
    metrics = calculate_performance_metrics(st.session_state.quiz)
    
    st.success("## 🎉 Quiz Completed!")
    
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", 
                     f"{st.session_state.quiz['score']}/{len(st.session_state.quiz['current_questions'])}",
                     f"{metrics.get('accuracy', 0):.1f}%")
        with col2:
            st.metric("Total Time", format_time(metrics.get('total_time', 0)))
        with col3:
            st.metric("Avg Time/Question", format_time(metrics.get('avg_time', 0)))
    
    if st.button("Return to Category Selection"):
        st.session_state.quiz['mode'] = 'category_selection'
        st.rerun()

# ===== MAIN APP =====
def main():
    """Main application function"""
    st.set_page_config(
        layout="wide",
        page_title=QUIZ_TITLE,
        page_icon="📊"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .stProgress > div > div > div > div {
            background-color: #4CAF50;
        }
        .stButton button {
            width: 100%;
        }
        .stRadio div[role='radiogroup'] > label {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title(f"📊 {QUIZ_TITLE}")
    st.caption("Test your CFA knowledge with this interactive quiz")
    
    initialize_session_state()
    
    # Router for different app modes
    app_modes = {
        'category_selection': show_category_selection,
        'question': display_question,
        'results': show_results
    }
    
    current_mode = st.session_state.quiz['mode']
    if current_mode in app_modes:
        app_modes[current_mode]()
        
        # Show navigation after answer submission
        if current_mode == 'question' and st.session_state.quiz['submitted']:
            show_next_button()

if __name__ == "__main__":
    main()
