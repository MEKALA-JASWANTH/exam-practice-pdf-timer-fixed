import streamlit as st
import PyPDF2
import re
import time
from datetime import datetime
import io
from PIL import Image

st.set_page_config(page_title="📚 Exam Practice", page_icon="📝", layout="wide")

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'duration' not in st.session_state:
    st.session_state.duration = 30
if 'exam_active' not in st.session_state:
    st.session_state.exam_active = False
if 'exam_done' not in st.session_state:
    st.session_state.exam_done = False

def extract_questions(pdf_file):
    """
    Enhanced question extraction with better pattern matching
    to prevent missing questions like Q11
    """
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # Enhanced patterns to match various question formats
        patterns = [
            # Q. 1, Q.1, Q1, Question 1, Q 1 with various separators
            r'Q(?:uestion)?[.:]?\s*(\d+)[.:)\s]+(.+?)(?=Q(?:uestion)?[.:]?\s*\d+[.:)\s]|$)',
            # 1. , 1) format
            r'(\d+)[.:]\s+(.+?)(?=\d+[.:]\s|$)',
        ]
        
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            if len(found) > 0:
                matches = found
                break  # Use first successful pattern
        
        questions = []
        for num, q_text in matches:
            q_clean = q_text.strip()
            # Enhanced option pattern to catch more formats
            opt_pattern = r'([A-D])[.:\s)]\s*([^\n]+)'
            options = re.findall(opt_pattern, q_clean)
            
            if options:
                # Clean question text by removing options
                for letter, opt in options:
                    # Remove PDF filename artifacts from options
                    opt_cleaned = re.sub(r'SSC-CGL.*?\.pdf', '', opt, flags=re.IGNORECASE).strip()
                    opt_cleaned = re.sub(r'Adda247', '', opt_cleaned, flags=re.IGNORECASE).strip()
                    q_clean = q_clean.replace(f"{letter}){opt}", "").replace(f"{letter}.{opt}", "")
                
                # Further clean the options dictionary
                cleaned_options = {}
                for letter, opt in options:
                    opt_cleaned = re.sub(r'SSC-CGL.*?\.pdf', '', opt, flags=re.IGNORECASE).strip()
                    opt_cleaned = re.sub(r'Adda247', '', opt_cleaned, flags=re.IGNORECASE).strip()
                    cleaned_options[letter] = opt_cleaned
                
                questions.append({
                    'question': q_clean.strip(), 
                    'options': cleaned_options
                })
            else:
                # No clear options found, store as single-option
                questions.append({'question': q_clean, 'options': {'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'}})
        
        return questions
    except Exception as e:
        st.error(f"Error extracting questions: {str(e)}")
        return []

def get_time_left():
    if st.session_state.start_time:
        elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
        return max(0, st.session_state.duration * 60 - elapsed)
    return st.session_state.duration * 60

def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

st.title("📚 Exam Practice Tool")

if not st.session_state.exam_active and not st.session_state.exam_done:
    st.markdown("### Upload Your PDF Exam")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        pdf = st.file_uploader("Choose PDF file", type=['pdf'])
    with col2:
        duration = st.number_input("Duration (min)", 1, 180, 30, 5)
    
    if pdf:
        st.success(f"✅ {pdf.name} uploaded ({pdf.size/1024:.1f} KB)")
        if st.button("🚀 Start Exam", type="primary"):
            with st.spinner('Extracting questions...'):
                qs = extract_questions(pdf)
                if qs:
                    st.session_state.questions = qs
                    st.session_state.duration = duration
                    st.session_state.start_time = datetime.now()
                    st.session_state.exam_active = True
                    st.success(f"✅ Found {len(qs)} questions!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ No questions found")

elif st.session_state.exam_active:
    time_left = get_time_left()
    if time_left <= 0:
        st.warning("⏰ Time's up!")
        time.sleep(2)
        st.session_state.exam_done = True
        st.session_state.exam_active = False
        st.rerun()
    
    c1, c2, c3 = st.columns([1, 2, 1])
    answered = len(st.session_state.answers)
    total = len(st.session_state.questions)
    c1.metric("Answered", f"{answered}/{total}")
    with c2:
        st.markdown(f"### ⏱️ Time Left: {format_time(time_left)}")
    
    # Question display
    current_question = st.session_state.questions[st.session_state.current_idx]
    st.markdown(f"### Question {st.session_state.current_idx + 1} of {len(st.session_state.questions)}")
    st.markdown(f"**{current_question['question']}**")
    
    # Answer selection
    selected = st.radio(
        "Select your answer:",
        list(current_question['options'].keys()),
        format_func=lambda x: f"{x}. {current_question['options'][x]}",
        key=f"q_{st.session_state.current_idx}"
    )
    
    if selected:
        st.session_state.answers[st.session_state.current_idx] = selected
    
    # Navigation
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.session_state.current_idx > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_idx -= 1
                st.rerun()
    with col_next:
        if st.session_state.current_idx < len(st.session_state.questions) - 1:
            if st.button("Next ➡️"):
                st.session_state.current_idx += 1
                st.rerun()
        else:
            if st.button("✅ Submit Exam", type="primary"):
                st.session_state.exam_done = True
                st.session_state.exam_active = False
                st.rerun()
    
    # Question navigator
    st.markdown("---")
    st.markdown("### Quick Navigation")
    cols = st.columns(10)
    for i in range(len(st.session_state.questions)):
        col_idx = i % 10
        with cols[col_idx]:
            answered_class = "✅" if i in st.session_state.answers else "⬜"
            if st.button(f"{answered_class} {i+1}", key=f"nav_{i}"):
                st.session_state.current_idx = i
                st.rerun()

else:
    # Results page
    st.markdown("### 🎉 Exam Completed!")
    answered = len(st.session_state.answers)
    total = len(st.session_state.questions)
    percentage = (answered / total * 100) if total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Questions Answered", f"{answered}/{total}")
    col2.metric("Completion", f"{percentage:.1f}%")
    col3.metric("Time Taken", f"{st.session_state.duration} min")
    
    if st.button("🔄 Start New Exam"):
        st.session_state.questions = []
        st.session_state.current_idx = 0
        st.session_state.answers = {}
        st.session_state.start_time = None
        st.session_state.exam_active = False
        st.session_state.exam_done = False
        st.rerun()
