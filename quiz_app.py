import streamlit as st

# 50 questions across 5 categories (10 questions each)
questions = [
    # ===== GEOGRAPHY (10 questions) =====
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome", "Lisbon"],
        "correct_answer": "Paris",
        "category": "Geography"
    },
    {
        "question": "Which country has the largest population?",
        "options": ["India", "USA", "China", "Indonesia", "Brazil"],
        "correct_answer": "China",
        "category": "Geography"
    },
    {
        "question": "What is the longest river in the world?",
        "options": ["Amazon", "Nile", "Yangtze", "Mississippi", "Danube"],
        "correct_answer": "Nile",
        "category": "Geography"
    },
    {
        "question": "Which continent is the largest by area?",
        "options": ["Africa", "North America", "Asia", "Europe", "Antarctica"],
        "correct_answer": "Asia",
        "category": "Geography"
    },
    {
        "question": "What is the capital of Canada?",
        "options": ["Toronto", "Vancouver", "Ottawa", "Montreal", "Calgary"],
        "correct_answer": "Ottawa",
        "category": "Geography"
    },
    {
        "question": "Which desert is the largest in the world?",
        "options": ["Sahara", "Arabian", "Gobi", "Kalahari", "Patagonian"],
        "correct_answer": "Sahara",
        "category": "Geography"
    },
    {
        "question": "What is the smallest country in the world?",
        "options": ["Monaco", "Nauru", "Vatican City", "San Marino", "Liechtenstein"],
        "correct_answer": "Vatican City",
        "category": "Geography"
    },
    {
        "question": "Which country is known as the Land of the Rising Sun?",
        "options": ["China", "Thailand", "Japan", "South Korea", "Vietnam"],
        "correct_answer": "Japan",
        "category": "Geography"
    },
    {
        "question": "What is the capital of Australia?",
        "options": ["Sydney", "Melbourne", "Brisbane", "Canberra", "Perth"],
        "correct_answer": "Canberra",
        "category": "Geography"
    },
    {
        "question": "Which mountain is the highest in the world?",
        "options": ["K2", "Mount Everest", "Kangchenjunga", "Lhotse", "Makalu"],
        "correct_answer": "Mount Everest",
        "category": "Geography"
    },

    # ===== SCIENCE (10 questions) =====
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn", "Venus"],
        "correct_answer": "Mars",
        "category": "Science"
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag", "Pt"],
        "correct_answer": "Au",
        "category": "Science"
    },
    {
        "question": "What is H₂O more commonly known as?",
        "options": ["Hydrogen", "Oxygen", "Water", "Peroxide", "Ozone"],
        "correct_answer": "Water",
        "category": "Science"
    },
    {
        "question": "Which gas do plants absorb from the atmosphere?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", "Methane"],
        "correct_answer": "Carbon Dioxide",
        "category": "Science"
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "options": ["Gold", "Iron", "Diamond", "Quartz", "Graphite"],
        "correct_answer": "Diamond",
        "category": "Science"
    },
    {
        "question": "Which scientist developed the theory of relativity?",
        "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Stephen Hawking", "Marie Curie"],
        "correct_answer": "Albert Einstein",
        "category": "Science"
    },
    {
        "question": "What is the human body's largest organ?",
        "options": ["Liver", "Brain", "Skin", "Heart", "Lungs"],
        "correct_answer": "Skin",
        "category": "Science"
    },
    {
        "question": "Which blood type is the universal donor?",
        "options": ["A", "B", "AB", "O", "AB+"],
        "correct_answer": "O",
        "category": "Science"
    },
    {
        "question": "What is the main component of the Sun?",
        "options": ["Liquid Lava", "Hydrogen", "Oxygen", "Carbon", "Helium"],
        "correct_answer": "Hydrogen",
        "category": "Science"
    },
    {
        "question": "How many bones are in the adult human body?",
        "options": ["150", "206", "300", "412", "106"],
        "correct_answer": "206",
        "category": "Science"
    },

    # ===== HISTORY (10 questions) =====
    {
        "question": "In what year did World War II end?",
        "options": ["1943", "1945", "1950", "1939", "1941"],
        "correct_answer": "1945",
        "category": "History"
    },
    {
        "question": "Who was the first president of the United States?",
        "options": ["Thomas Jefferson", "John Adams", "George Washington", "James Madison", "Benjamin Franklin"],
        "correct_answer": "George Washington",
        "category": "History"
    },
    {
        "question": "Which ancient civilization built the pyramids?",
        "options": ["Greeks", "Romans", "Egyptians", "Mayans", "Aztecs"],
        "correct_answer": "Egyptians",
        "category": "History"
    },
    {
        "question": "When did the Titanic sink?",
        "options": ["1905", "1912", "1918", "1923", "1931"],
        "correct_answer": "1912",
        "category": "History"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo", "Claude Monet"],
        "correct_answer": "Leonardo da Vinci",
        "category": "History"
    },
    {
        "question": "Which year did the Berlin Wall fall?",
        "options": ["1985", "1989", "1991", "1979", "1980"],
        "correct_answer": "1989",
        "category": "History"
    },
    {
        "question": "Who was the first woman to win a Nobel Prize?",
        "options": ["Marie Curie", "Mother Teresa", "Rosalind Franklin", "Jane Addams", "Dorothy Hodgkin"],
        "correct_answer": "Marie Curie",
        "category": "History"
    },
    {
        "question": "Which empire was ruled by Julius Caesar?",
        "options": ["Greek", "Roman", "Egyptian", "Persian", "Ottoman"],
        "correct_answer": "Roman",
        "category": "History"
    },
    {
        "question": "When was the Declaration of Independence signed?",
        "options": ["1776", "1789", "1792", "1801", "1765"],
        "correct_answer": "1776",
        "category": "History"
    },
    {
        "question": "Who invented the telephone?",
        "options": ["Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Guglielmo Marconi", "Samuel Morse"],
        "correct_answer": "Alexander Graham Bell",
        "category": "History"
    },

    # ===== ENTERTAINMENT (10 questions) =====
    {
        "question": "Who played Iron Man in the MCU?",
        "options": ["Chris Evans", "Robert Downey Jr.", "Chris Hemsworth", "Mark Ruffalo", "Tom Holland"],
        "correct_answer": "Robert Downey Jr.",
        "category": "Entertainment"
    },
    {
        "question": "Which movie won the first Academy Award for Best Picture?",
        "options": ["Gone with the Wind", "Sunrise", "Wings", "Metropolis", "The Jazz Singer"],
        "correct_answer": "Wings",
        "category": "Entertainment"
    },
    {
        "question": "Who is known as the King of Pop?",
        "options": ["Elvis Presley", "Michael Jackson", "Prince", "Justin Timberlake", "Bruno Mars"],
        "correct_answer": "Michael Jackson",
        "category": "Entertainment"
    },
    {
        "question": "Which TV show features the characters Ross, Rachel, and Chandler?",
        "options": ["The Office", "Friends", "How I Met Your Mother", "Seinfeld", "Parks and Recreation"],
        "correct_answer": "Friends",
        "category": "Entertainment"
    },
    {
        "question": "Who wrote the Harry Potter book series?",
        "options": ["J.R.R. Tolkien", "J.K. Rowling", "Stephen King", "George R.R. Martin", "Suzanne Collins"],
        "correct_answer": "J.K. Rowling",
        "category": "Entertainment"
    },
    {
        "question": "Which artist painted 'The Starry Night'?",
        "options": ["Pablo Picasso", "Vincent van Gogh", "Claude Monet", "Salvador Dalí", "Andy Warhol"],
        "correct_answer": "Vincent van Gogh",
        "category": "Entertainment"
    },
    {
        "question": "What is the highest-grossing film of all time?",
        "options": ["Avatar", "Avengers: Endgame", "Titanic", "Star Wars: The Force Awakens", "Jurassic World"],
        "correct_answer": "Avatar",
        "category": "Entertainment"
    },
    {
        "question": "Which band was Freddie Mercury the lead singer of?",
        "options": ["The Beatles", "Rolling Stones", "Queen", "Pink Floyd", "Led Zeppelin"],
        "correct_answer": "Queen",
        "category": "Entertainment"
    },
    {
        "question": "What is the name of the fictional wizarding school in Harry Potter?",
        "options": ["Hogwarts", "Beauxbatons", "Durmstrang", "Ilvermorny", "Castelobruxo"],
        "correct_answer": "Hogwarts",
        "category": "Entertainment"
    },
    {
        "question": "Which Shakespeare play features the characters Romeo and Juliet?",
        "options": ["Macbeth", "Hamlet", "Othello", "Romeo and Juliet", "A Midsummer Night's Dream"],
        "correct_answer": "Romeo and Juliet",
        "category": "Entertainment"
    },

    # ===== GENERAL KNOWLEDGE (10 questions) =====
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6", "22"],
        "correct_answer": "4",
        "category": "General Knowledge"
    },
    {
        "question": "How many colors are in a rainbow?",
        "options": ["5", "6", "7", "8", "9"],
        "correct_answer": "7",
        "category": "General Knowledge"
    },
    {
        "question": "What is the square root of 64?",
        "options": ["4", "6", "7", "8", "10"],
        "correct_answer": "8",
        "category": "General Knowledge"
    },
    {
        "question": "How many continents are there?",
        "options": ["5", "6", "7", "8", "4"],
        "correct_answer": "7",
        "category": "General Knowledge"
    },
    {
        "question": "Which language has the most native speakers?",
        "options": ["English", "Spanish", "Hindi", "Arabic", "Mandarin Chinese"],
        "correct_answer": "Mandarin Chinese",
        "category": "General Knowledge"
    },
    {
        "question": "What is the currency of Japan?",
        "options": ["Won", "Yuan", "Yen", "Dollar", "Euro"],
        "correct_answer": "Yen",
        "category": "General Knowledge"
    },
    {
        "question": "How many sides does a hexagon have?",
        "options": ["4", "5", "6", "7", "8"],
        "correct_answer": "6",
        "category": "General Knowledge"
    },
    {
        "question": "Which planet is closest to the Sun?",
        "options": ["Venus", "Earth", "Mars", "Mercury", "Jupiter"],
        "correct_answer": "Mercury",
        "category": "General Knowledge"
    },
    {
        "question": "What is the largest mammal?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Polar Bear", "Hippopotamus"],
        "correct_answer": "Blue Whale",
        "category": "General Knowledge"
    },
    {
        "question": "How many players are on a baseball team?",
        "options": ["7", "8", "9", "10", "11"],
        "correct_answer": "9",
        "category": "General Knowledge"
    }
]

# Initialize session state
if 'quiz' not in st.session_state:
    st.session_state.quiz = {
        'score': 0,
        'current_question': 0,
        'user_answer': None,
        'submitted': False,
        'show_next': False,
        'start_time': None,
        'category_scores': {}
    }

# Quiz layout
st.title('🧠 Mega Quiz (50 Questions)')
st.caption("Test your knowledge across 5 categories!")

# Progress tracker
progress = st.session_state.quiz['current_question'] / len(questions)
st.progress(progress)
st.caption(f"Question {st.session_state.quiz['current_question'] + 1} of {len(questions)}")

# Quiz completion check
if st.session_state.quiz['current_question'] >= len(questions):
    st.balloons()
    percentage = round((st.session_state.quiz['score']/len(questions))*100)
    st.success(f"""
    🎉 Quiz completed!
    Final score: {st.session_state.quiz['score']}/{len(questions)}
    ({percentage}%)
    """)
    
    # Display category breakdown
    st.subheader("Category Breakdown:")
    for category, score in st.session_state.quiz['category_scores'].items():
        st.write(f"- {category}: {score}/10")
    
    if st.button("🔄 Restart Quiz"):
        st.session_state.quiz = {
            'score': 0,
            'current_question': 0,
            'user_answer': None,
            'submitted': False,
            'show_next': False,
            'start_time': None,
            'category_scores': {}
        }
        st.rerun()
else:
    question = questions[st.session_state.quiz['current_question']]
    
    # Display category tag
    if 'category' in question:
        st.markdown(f"**Category:** {question['category']}")
    
    st.subheader(question["question"])

    # Answer submission phase
    if not st.session_state.quiz['submitted']:
        user_answer = st.radio(
            "Select your answer:",
            question["options"],
            key=f"q{st.session_state.quiz['current_question']}"
        )
        
        if st.button("📥 Submit Answer"):
            st.session_state.quiz['user_answer'] = user_answer
            st.session_state.quiz['submitted'] = True
            st.session_state.quiz['show_next'] = True
            
            # Update scores
            if user_answer == question["correct_answer"]:
                st.session_state.quiz['score'] += 1
                # Track category scores
                if 'category' in question:
                    category = question['category']
                    st.session_state.quiz['category_scores'][category] = st.session_state.quiz['category_scores'].get(category, 0) + 1
            
            st.rerun()

    # Feedback phase
    if st.session_state.quiz['submitted']:
        if st.session_state.quiz['user_answer'] == question["correct_answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect! The correct answer is: **{question['correct_answer']}**")
        
        # Next question button
        if st.session_state.quiz['show_next'] and st.button("⏭️ Next Question"):
            st.session_state.quiz['current_question'] += 1
            st.session_state.quiz['submitted'] = False
            st.session_state.quiz['show_next'] = False
            st.session_state.quiz['user_answer'] = None
            st.rerun()
