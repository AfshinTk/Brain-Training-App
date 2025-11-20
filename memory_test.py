import streamlit as st
import time
import random

# Configure page
st.set_page_config(page_title="Word Memory Test", layout="centered")

# Original word list (from image)
master_word_list = [
    "برنج", "وسیله", "ریال", "بند", "سکه", "چشم", "فهرست", "ملت", "میدان", "تمبر",
    "مثال", "هوا", "تخته", "شعر", "جوهر", "باغ", "باد", "حق", "ارزش", "شنا", "قطب", "دهان",
    "پیراهن", "لیتر", "کار", "انگشت", "صبح", "پهل‌و", "ورزش", "قایق",
    "دوچرخه", "مداد", "کیف", "کتاب", "دفتر", "مدرسه", "معلم", "دانش", "رنگ", "زنگ",
    "زمان", "سرعت", "نقشه", "خورشید", "ماه", "ستاره", "دریا", "رود", "پل", "کوه",
    "دشت", "چمن", "گل", "درخت", "میوه", "سیب", "پرتقال", "موز", "هندوانه", "خیار",
    "گوجه", "نارنگی", "شیر", "آب", "نوشابه", "چای", "قهوه", "بستنی", "کیک", "شکلات",
    "پنیر", "تخم‌مرغ", "گوشت", "مرغ", "ماهی", "برق", "تلویزیون", "رادیو", "موبایل", "تبلت",
    "رایانه", "ساعت", "پنکه", "یخچال", "لباس", "شلوار", "کفش", "کلاه", "عینک", "دوست",
    "خانواده", "پدر", "مادر", "برادر", "خواهر", "خانه", "اتاق", "آشپزخانه", "حمام", "سرویس"
]

original_words = random.sample(master_word_list, 30)

# Session init
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'words' not in st.session_state:
    st.session_state.words = random.sample(original_words, len(original_words))  # randomized
if 'show_input' not in st.session_state:
    st.session_state.show_input = False
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Start button
if st.session_state.start_time is None:
    if st.button("🧠 Start Memory Test"):
        st.session_state.start_time = time.time()

# Word display section
if st.session_state.start_time is not None and not st.session_state.show_input:
    st.markdown("<h2 style='text-align:center;'>Memorize These Words</h2>", unsafe_allow_html=True)

    for i in range(0, len(st.session_state.words), 6):
        cols = st.columns(6)
        for j in range(6):
            if i + j < len(st.session_state.words):
                with cols[j]:
                    st.markdown(f"<div style='font-size:28px; text-align:center;'>{st.session_state.words[i + j]}</div>", unsafe_allow_html=True)

    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, int(120 - elapsed))
    st.markdown(f"<p style='text-align:center;'>⏱ Time remaining: {remaining} seconds</p>", unsafe_allow_html=True)

    col_next, _ = st.columns([1, 5])
    with col_next:
        if st.button("Next"):
            st.session_state.show_input = True
            st.rerun()

    if elapsed >= 120:
        st.session_state.show_input = True
        st.rerun()

# Recall section
if st.session_state.show_input and not st.session_state.submitted:
    st.markdown("<h2>✍️ Write as many words as you remember</h2>", unsafe_allow_html=True)
    recalled = st.text_area("Enter words separated by spaces or newlines", height=200)
    if st.button("Submit"):
        recalled_words = set(recalled.replace('\n', ' ').split())
        correct = [w for w in recalled_words if w in original_words]
        score = len(correct)
        st.session_state.submitted = True
        st.session_state.score = score
        st.session_state.correct = correct
        st.session_state.total = len(original_words)
        st.rerun()

# Result section
if st.session_state.submitted:
    st.markdown(f"<h3>✅ You remembered {st.session_state.score} out of {st.session_state.total} words!</h3>", unsafe_allow_html=True)
    if st.session_state.correct:
        st.markdown("Correctly recalled words:")
        st.markdown(f"<p style='font-size:20px;'>{', '.join(st.session_state.correct)}</p>", unsafe_allow_html=True)
    if st.button("🔁 Try Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
