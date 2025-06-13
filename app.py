import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# Configure Gemini API
genai.configure(api_key="AIzaSyBajGa89W5CJOGwLfYQUkSqw6B505KGRiA")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state
if 'df_users' not in st.session_state:
    st.session_state.df_users = pd.DataFrame(columns=['username', 'timestamp'])
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = None
if 'chapter_content' not in st.session_state:
    st.session_state.chapter_content = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'mcqs' not in st.session_state:
    st.session_state.mcqs = []
if 'subjective_questions' not in st.session_state:
    st.session_state.subjective_questions = []

# Page Config
st.set_page_config(page_title="EduBuddy AI", layout="wide", initial_sidebar_state="collapsed", page_icon="🧠")

# Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #ffffff;
            color: #1e293b;
        }
        .header-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin: 40px 0;
        }
        .header-logo {
            width: 80px;
            height: 80px;
            opacity: 0.8;
            transition: all 0.3s ease;
        }
        .header-logo:hover {
            opacity: 1;
            transform: scale(1.05);
        }
        .main-title {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #4f46e5 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin: 0;
            line-height: 1.2;
            letter-spacing: -0.5px;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #64748b;
            text-align: center;
            max-width: 700px;
            margin: 0 auto 40px;
            font-weight: 400;
        }
        .content-container {
            background-color: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            border: 1px solid #f1f5f9;
        }
        .footer {
            text-align: center;
            margin-top: 80px;
            padding: 40px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px 16px 0 0;
        }
        .footer a {
            color: white !important;
            text-decoration: none;
            margin: 0 15px;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)


def show_cover_page():
    st.markdown("""
        <div class="header-container">
            <img src="https://cdn-icons-png.flaticon.com/512/2232/2232688.png" class="header-logo">
            <div>
                <h1 class="main-title">EduBuddy AI</h1>
                <p class="subtitle">Your intelligent learning companion that adapts to your study style</p>
            </div>
            <img src="https://cdn-icons-png.flaticon.com/512/2232/2232688.png" class="header-logo">
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📖 Smart Summaries"):
            st.session_state.current_tab = 'summary'
    with col2:
        if st.button("📝 Adaptive Testing"):
            st.session_state.current_tab = 'test'
    with col3:
        if st.button("💡 Doubt Resolution"):
            st.session_state.current_tab = 'doubt'


def show_summary_tab():
    with st.container():
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.header("📖 Chapter Summarizer", divider="blue")
        st.markdown("Paste your chapter content below to generate a concise, structured summary")
        
        chapter_text = st.text_area(
            "Chapter Content",
            height=300,
            placeholder="Paste your textbook chapter, lecture notes, or study materials here...",
            label_visibility="collapsed"
        )
        
        if st.button("Generate Summary", key="summarize_btn"):
            with st.spinner("Analyzing content and generating summary..."):
                try:
                    response = model.generate_content(
                        f"Create a comprehensive summary of this chapter with the following structure:\n\n"
                        f"1. Key Concepts (bullet points)\n"
                        f"2. Important Definitions\n"
                        f"3. Main Theories/Principles\n"
                        f"4. Practical Applications\n"
                        f"5. Summary Diagram Description\n\n"
                        f"Content:\n{chapter_text}"
                    )
                    summary = response.text
                    st.session_state.chapter_content = chapter_text
                    st.session_state.summary = summary
                    st.success("Here's your chapter summary:")
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)


def show_test_tab():
    with st.container():
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.header("📝 Knowledge Assessment", divider="blue")

        if not st.session_state.chapter_content:
            st.warning("Please generate a chapter summary first in the 'Chapter Summarizer' tab to create a test.")
        else:
            if not st.session_state.mcqs or not st.session_state.subjective_questions:
                with st.spinner("Creating personalized test questions..."):
                    try:
                        mcq_prompt = (
                            f"Generate 5 MCQs based on:\n{st.session_state.chapter_content}\n\n"
                            "Each should follow:\nQ1. Question\nA. Option\nB. Option\nC. Option\nD. Option\nAnswer: [A-D]"
                        )
                        mcq_response = model.generate_content(mcq_prompt)
                        raw_mcqs = mcq_response.text.strip().split("Q")[1:]
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
                        st.session_state.mcqs = parsed_mcqs[:5]

                        subj_prompt = (
                            f"Create 3 short answer questions based on:\n\n{st.session_state.chapter_content}"
                        )
                        subj_response = model.generate_content(subj_prompt)
                        st.session_state.subjective_questions = [q.strip() for q in subj_response.text.strip().split("\n") if q.strip()][:3]
                    except Exception as e:
                        st.error(f"Error generating test: {str(e)}")

            with st.form("test_form"):
                st.subheader("Multiple Choice Questions")
                user_answers = []

                for i, mcq in enumerate(st.session_state.mcqs):
                    st.markdown(f"*Q{i+1}.* {mcq['question']}")
                    user_choice = st.radio(
                        f"Choose answer for Q{i+1}",
                        options=mcq['options'],
                        key=f"mcq_{i}",
                        index=None,
                        label_visibility="collapsed"
                    )
                    user_answers.append((user_choice, mcq['answer']))
                    st.markdown("---")

                st.subheader("Short Answer Questions")
                subjective_responses = []

                for i, question in enumerate(st.session_state.subjective_questions):
                    st.markdown(f"*Q{i+6}.* {question}")
                    answer = st.text_area(f"Answer Q{i+6}", key=f"subj_{i}", height=120)
                    subjective_responses.append(answer)
                    st.markdown("---")

                submitted = st.form_submit_button("Submit Assessment")

            if submitted:
                st.subheader("Assessment Results")
                correct = 0
                for i, (user_choice, correct_answer) in enumerate(user_answers):
                    if user_choice is None:
                        st.markdown(f"❗ Q{i+1}: Unanswered | ✅ Correct: {correct_answer}")
                    elif user_choice.startswith(correct_answer):
                        correct += 1
                        st.success(f"✅ Q{i+1}: Correct!")
                    else:
                        st.error(f"❌ Q{i+1}: Incorrect | Correct Answer: {correct_answer}")

                st.progress(correct / len(st.session_state.mcqs), text=f"MCQ Score: {correct}/{len(st.session_state.mcqs)}")

                if any(subjective_responses):
                    st.subheader("Subjective Answers Evaluation")
                    for i, (q, resp) in enumerate(zip(st.session_state.subjective_questions, subjective_responses)):
                        if not resp:
                            st.warning(f"Q{i+6}: No answer given.")
                            continue
                        with st.spinner(f"Evaluating Q{i+6}..."):
                            try:
                                prompt = (
                                    f"Evaluate this answer to the question '{q}':\n\n"
                                    f"Student's Answer:\n{resp}\n\n"
                                    "Provide feedback with:\n- Strengths\n- Improvements\n- Score (1-5)\n- Model Answer"
                                )
                                feedback = model.generate_content(prompt).text
                                st.markdown(f"**Q{i+6}: {q}**")
                                st.markdown(f"**Your Answer:** {resp}")
                                st.markdown("**Evaluation:**")
                                st.markdown(feedback)
                            except Exception as e:
                                st.error(f"Error evaluating: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)


def show_doubt_tab():
    with st.container():
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.header("💭 Doubt Resolution", divider="blue")

        doubt = st.text_area(
            "Describe your doubt",
            height=150,
            placeholder="Explain what you're struggling to understand...",
            label_visibility="collapsed"
        )

        if st.button("Explain Concept", key="doubt_btn"):
            with st.spinner("Generating explanation..."):
                try:
                    prompt = (
                        f"Explain this concept:\n{doubt}\n\n"
                        "Structure:\n1. Definition\n2. Analogy\n3. Example\n4. Misconceptions\n5. Visual Aid Description"
                    )
                    response = model.generate_content(prompt).text
                    st.success("Explanation:")
                    st.markdown(response)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)


def main():
    if st.session_state.current_tab is None:
        show_cover_page()
    elif st.session_state.current_tab == 'summary':
        show_summary_tab()
    elif st.session_state.current_tab == 'test':
        show_test_tab()
    elif st.session_state.current_tab == 'doubt':
        show_doubt_tab()

    st.markdown("""
        <div class="footer">
            <p>©️ 2023 EduBuddy AI | Powered by Gemini AI</p>
            <div>
                <a href="#">Terms of Service</a>
                <a href="#">Privacy Policy</a>
                <a href="#">Contact Us</a>
            </div>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
