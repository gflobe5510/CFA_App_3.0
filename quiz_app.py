# ... (keep all your imports and configuration constants the same)

def load_questions():
    try:
        with open(updated_json_path, 'r') as f:
            updated_questions_data = json.load(f)
        
        questions_by_category = {}
        
        # First initialize all categories with empty lists
        for category in CATEGORIES:
            questions_by_category[category] = []
        
        # Then populate with actual questions
        for question in updated_questions_data.get("questions", []):
            topic = question.get("topic", "Uncategorized")
            # Use direct mapping or default to the topic name
            category = TOPIC_TO_CATEGORY.get(topic, topic)
            if category in questions_by_category:
                questions_by_category[category].append(question)
            else:
                # If we encounter a new category not in our list, add it
                questions_by_category[category] = [question]
        
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

def show_category_selection():
    st.markdown("## Select a CFA Topic Area")
    
    # Get all categories that actually have questions
    available_categories = [
        (cat, len(st.session_state.quiz['all_questions'][cat])) 
        for cat in st.session_state.quiz['all_questions'] 
        if len(st.session_state.quiz['all_questions'][cat]) > 0
    ]
    
    # Also include categories with zero questions but disabled
    all_categories = [
        (cat, len(st.session_state.quiz['all_questions'].get(cat, []))) 
        for cat in CATEGORIES
    ]
    
    # Display in 2-column layout
    cols = st.columns(2)
    for i, (category, question_count) in enumerate(all_categories):
        with cols[i % 2]:
            if st.button(
                f"{category} ({question_count} questions)",
                disabled=question_count == 0,
                help=f"{CATEGORIES[category]['description']}" if category in CATEGORIES else ""
            ):
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

# ... (keep all other functions exactly the same)

def main():
    st.set_page_config(layout="wide")
    st.title(f"📊 {QUIZ_TITLE}")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar buttons
    with st.sidebar:
        st.header("Menu")
        if st.button("Practice Test", key="practice_btn", use_container_width=True):
            st.session_state.sidebar_view = 'practice'
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Track Performance", key="performance_btn", use_container_width=True):
                st.session_state.sidebar_view = 'performance'
        with col2:
            if st.button("Login", key="login_btn", use_container_width=True):
                st.session_state.sidebar_view = 'login'
        
        if st.session_state.sidebar_view == 'practice':
            st.info("Select a topic from the main area")
        elif st.session_state.sidebar_view == 'performance':
            st.info("Performance tracking coming soon!")
        elif st.session_state.sidebar_view == 'login':
            st.info("Login feature coming soon!")
    
    # Main quiz functionality
    if st.session_state.quiz['mode'] == 'category_selection':
        show_category_selection()
    elif st.session_state.quiz['mode'] == 'question':
        display_question()
        if st.session_state.quiz['submitted']:
            show_next_button()

if __name__ == "__main__":
    main()
