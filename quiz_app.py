# ===== MAIN APP =====
def main():
    st.set_page_config(layout="wide")  # Move this to the very top of the function
    st.title(f"📊 {QUIZ_TITLE}")
    
    # Debug panel
    if st.sidebar.checkbox("Show debug info"):
        st.sidebar.write("### Debug Information")
        st.sidebar.write(f"JSON path: {updated_json_path}")
        if 'quiz' in st.session_state:
            st.sidebar.json({
                "current_mode": st.session_state.quiz['mode'],
                "selected_category": st.session_state.quiz['selected_category'],
                "question_count": len(st.session_state.quiz.get('current_questions', [])),
                "loaded_categories": list(st.session_state.quiz.get('all_questions', {}).keys())
            })
    
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
