import streamlit as st
import random
import time

st.set_page_config(page_title="Brain Training", layout="centered")
st.markdown("""
    <h1 style='text-align: center; font-size: 38px;'>🧠 Simplified Brain Training</h1>
    
""", unsafe_allow_html=True)

# Configuration
NUM_QUESTIONS = 100
OPERATIONS = ['+', '-', '*', '/']

# Session state init
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Generate random questions with simple 2-digit limits
@st.cache_data
def generate_questions(n):
    questions = []
    while len(questions) < n:
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(OPERATIONS)

        if op == '-':
            if b > a:
                a, b = b, a
            result = a - b
        elif op == '*':
            if a > 12 or b > 12:
                continue  # Limit multiplication size
            result = a * b
        elif op == '/':
            if b == 0 or a % b != 0:
                continue  # Ensure integer division
            result = a // b
            op_symbol = '÷'
        else:
            result = a + b

        display_op = {'+': '+', '-': '-', '*': '×', '/': '÷'}[op]
        question = f"{a} {display_op} {b}"
        questions.append((question, result))
    return questions

# Start the test
if st.button("Start Test"):
    st.session_state.questions = generate_questions(NUM_QUESTIONS)
    st.session_state.answers = {}
    st.session_state.start_time = time.time()

# Display questions
# if st.session_state.questions:
#     st.markdown("<h2 style='font-size: 32px;'>Answer the following:</h2>", unsafe_allow_html=True)
#     for i, (q, _) in enumerate(st.session_state.questions):
#         st.session_state.answers[i] = st.text_input(f"{q} =", key=f"q{i}")
if st.session_state.questions:
    st.markdown("<h2 style='font-size: 40px;'>Answer the following:</h2>", unsafe_allow_html=True)
    for i, (q, _) in enumerate(st.session_state.questions):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"<div style='font-size: 38px; font-weight: bold; padding: 7px;'>{q} =</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("""
                        
                <div style='margin-left: 100px; font-size: 60px; padding: 10px'>
                          
                </div>
            """, unsafe_allow_html=True)

            st.session_state.answers[i] = st.text_input("", key=f"q{i}", label_visibility="collapsed")

    if st.button("Submit"):
        end_time = time.time()
        elapsed = round(end_time - st.session_state.start_time, 2)
        score = 0

        st.markdown("<h2 style='font-size: 48px;'>Results:</h2>", unsafe_allow_html=True)
        for i, (q, answer) in enumerate(st.session_state.questions):
            user_input = st.session_state.answers.get(i)
            try:
                user_answer = int(user_input)
                correct = user_answer == answer
            except:
                correct = False
            score += int(correct)
            st.markdown(f"<p style='font-size: 20px;'>{q} = {answer} | Your answer: {user_input or 'No answer'} | {'✅' if correct else '❌'}</p>", unsafe_allow_html=True)

        st.success(f"⏱ Time Taken: {elapsed} seconds")
        st.success(f"🎯 Score: {score} / {NUM_QUESTIONS}")
        
        if st.button("🔁 Try Again"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()