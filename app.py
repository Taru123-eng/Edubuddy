import streamlit as st
import google.generativeai as genai

# Set your Gemini API key directly here
genai.configure(api_key="AIzaSyBajGa89W5CJOGwLfYQUkSqw6B505KGRiA")  # <-- Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="📚 EduBuddy - AI Learning Assistant", layout="centered")

# UI Styling
st.markdown("""
    <style>
        .main {background-color: #f4f6f8;}
        h1, h2, h3 {color: #333;}
        .stButton>button {background-color: #4CAF50; color: white;}
        .stRadio>label {background-color: #9AC5F4; padding: 10px; border-radius: 5px;}
        .stRadio input:checked+label {background-color: #068DA9; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("📚 EduBuddy - AI Learning Assistant")
tabs = st.tabs(["📖 Chapter Summarizer", "📝 Take a Test", "💭 Doubt Solver"])

# Session state to store chapter summary and test
if "chapter_content" not in st.session_state:
    st.session_state.chapter_content = ""
if "mcqs" not in st.session_state:
    st.session_state.mcqs = []
if "subjective_questions" not in st.session_state:
    st.session_state.subjective_questions = []

# --- Chapter Summarizer ---
with tabs[0]:
    st.header("📖 Chapter Summarizer")
    chapter_text = st.text_area("Paste your chapter or notes here", height=300)
    if st.button("Summarize Chapter"):
        with st.spinner("Summarizing..."):
            try:
                response = model.generate_content(f"Summarize this chapter:\n\n{chapter_text}")
                summary = response.text
                st.session_state.chapter_content = chapter_text
                st.success("Summary:")
                st.markdown(summary)
            except Exception as e:
                st.error(f"Error: {e}")

# --- Take a Test ---
with tabs[1]:
    st.header("📝 Test on Chapter Content")

    if not st.session_state.chapter_content:
        st.warning("Please paste and summarize a chapter first in the 'Chapter Summarizer' tab.")
    else:
        if not st.session_state.mcqs:
            with st.spinner("Generating test questions..."):
                try:
                    prompt = (
                        f"Generate 5 multiple-choice questions (MCQs) based on the following chapter content:\n\n"
                        f"{st.session_state.chapter_content}\n\n"
                        "Each question should have 4 options labeled A to D, and specify the correct answer. "
                        "Format:\n"
                        "Q1. What is ...?\nA. ...\nB. ...\nC. ...\nD. ...\nAnswer: B"
                    )
                    response = model.generate_content(prompt)
                    raw_mcqs = response.text.strip().split("Q")[1:]
                    parsed_mcqs = []
                    for q in raw_mcqs:
                        lines = q.strip().split("\n")
                        if len(lines) < 6:
                            continue
                        question_text = lines[0].strip()
                        options = [line.strip() for line in lines[1:5]]
                        answer = lines[5].split("Answer:")[-1].strip()
                        parsed_mcqs.append({
                            "question": question_text,
                            "options": options,
                            "answer": answer
                        })
                    st.session_state.mcqs = parsed_mcqs
                except Exception as e:
                    st.error(f"Error generating test: {e}")

        # Display test
        score = 0
        user_answers = []

        with st.form("test_form"):
            for i, mcq in enumerate(st.session_state.mcqs):
                st.write(f"*Q{i+1}. {mcq['question']}*")
                user_choice = st.radio(
                    f"Choose an option for Q{i+1}", 
                    options=mcq['options'], 
                    key=f"q{i+1}"
                )
                user_answers.append((user_choice, mcq['answer']))
                st.markdown("---")

            submitted = st.form_submit_button("Submit Test")

        if submitted:
            correct = 0
            for user, correct_answer in user_answers:
                if user.startswith(correct_answer):
                    correct += 1
            st.success(f"✅ You scored {correct}/5")

            if correct == 5:
                remark = "🌟 Excellent work!"
            elif correct >= 3:
                remark = "👍 Good job! Review the chapter for better understanding."
            else:
                remark = "📖 Needs improvement. Go through the chapter again."

            st.info(remark)

            # Provide resource links
            resources = [
                "📘 [Khan Academy - Science Courses](https://www.khanacademy.org/science)",
                "📚 [Coursera - Biology Courses](https://www.coursera.org/browse/health/biology)",
                "🧪 [YouTube - CrashCourse Biology](https://www.youtube.com/playlist?list=PL8dPuuaLjXtM5ZlQXyXgQZ6WzvF6c5c3u)"
            ]
            st.markdown("### 📚 Recommended Resources:")
            for resource in resources:
                st.markdown(f"- {resource}")

# --- Doubt Solver ---
with tabs[2]:
    st.header("💭 Doubt Solver")
    doubt = st.text_area("Write your doubt or what you're confused about")
    if st.button("Solve My Doubt"):
        with st.spinner("Solving your doubt..."):
            try:
                response = model.generate_content(f"Explain this doubt in a simple and clear way: {doubt}")
                st.success("Explanation:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
