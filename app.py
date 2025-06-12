import streamlit as st
import google.generativeai as genai
from streamlit_extras.stylable_container import stylable_container

# Set your Gemini API key directly here
genai.configure(api_key="AIzaSyBajGa89W5CJOGwLfYQUkSqw6B505KGRiA")  # <-- Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Page Configuration
st.set_page_config(
    page_title="📚 EduBuddy - AI Learning Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
        /* Main styles */
        .main {
            background-color: #f8fafc;
            color: #1e293b;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #1e293b;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #4f46e5;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
            transition: all 0.3s ease;
            border: none;
        }
        
        .stButton>button:hover {
            background-color: #4338ca;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Text areas */
        .stTextArea>div>div>textarea {
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #e2e8f0;
        }
        
        /* Radio buttons */
        .stRadio>div {
            gap: 8px;
        }
        
        .stRadio>div>label {
            background-color: #f1f5f9;
            border-radius: 8px;
            padding: 12px 16px;
            border: 1px solid #e2e8f0;
            transition: all 0.2s ease;
        }
        
        .stRadio>div>label:hover {
            background-color: #e2e8f0;
        }
        
        .stRadio input:checked+label {
            background-color: #4f46e5 !important;
            color: white !important;
            border-color: #4f46e5 !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            padding: 0 16px;
            border-radius: 8px !important;
            background-color: #f1f5f9 !important;
            transition: all 0.3s ease !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #4f46e5 !important;
            color: white !important;
        }
        
        /* Cards */
        .card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 16px;
            border: 1px solid #e2e8f0;
        }
        
        /* Colors */
        .correct {
            color: #10b981;
            font-weight: 600;
        }
        
        .incorrect {
            color: #ef4444;
            font-weight: 600;
        }
        
        .warning {
            color: #f59e0b;
            font-weight: 600;
        }
        
        /* Progress bar */
        .stProgress>div>div>div>div {
            background-color: #4f46e5 !important;
        }
        
        /* Spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #c7d2fe;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a5b4fc;
        }
    </style>
""", unsafe_allow_html=True)

# App Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=80)
with col2:
    st.title("EduBuddy")
    st.caption("Your AI-powered learning companion for smarter studying")

# Main tabs
tabs = st.tabs(["📖 Chapter Summarizer", "📝 Take a Test", "💭 Doubt Solver"])

# Session state to store chapter summary and test
if "chapter_content" not in st.session_state:
    st.session_state.chapter_content = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "mcqs" not in st.session_state:
    st.session_state.mcqs = []
if "subjective_questions" not in st.session_state:
    st.session_state.subjective_questions = []
if "subjective_answers" not in st.session_state:
    st.session_state.subjective_answers = []
if "subjective_feedback" not in st.session_state:
    st.session_state.subjective_feedback = []

# --- Chapter Summarizer ---
with tabs[0]:
    with stylable_container(
        key="summary_container",
        css_styles="""
            {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 16px;
                border: 1px solid #e2e8f0;
            }
        """
    ):
        st.header("Chapter Summarizer", divider="blue")
        st.markdown("Paste your chapter content below to generate a concise summary")
        
        chapter_text = st.text_area(
            "Chapter Content",
            height=300,
            placeholder="Paste your textbook chapter, lecture notes, or study materials here...",
            label_visibility="collapsed"
        )
        
        if st.button("Generate Summary", key="summarize_btn"):
            with st.spinner("Analyzing content and generating summary..."):
                try:
                    response = model.generate_content(f"Summarize this chapter in a structured format with key concepts:\n\n{chapter_text}")
                    summary = response.text
                    st.session_state.chapter_content = chapter_text
                    st.session_state.summary = summary
                    
                    with stylable_container(
                        key="summary_output",
                        css_styles="""
                            {
                                background-color: #f8fafc;
                                border-radius: 8px;
                                padding: 16px;
                                border-left: 4px solid #4f46e5;
                            }
                        """
                    ):
                        st.success("Here's your chapter summary:")
                        st.markdown(summary)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# --- Take a Test ---
with tabs[1]:
    with stylable_container(
        key="test_container",
        css_styles="""
            {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 16px;
                border: 1px solid #e2e8f0;
            }
        """
    ):
        st.header("Knowledge Assessment", divider="blue")
        
        if not st.session_state.chapter_content:
            with stylable_container(
                key="warning_box",
                css_styles="""
                    {
                        background-color: #fffbeb;
                        border-radius: 8px;
                        padding: 16px;
                        border-left: 4px solid #f59e0b;
                    }
                """
            ):
                st.warning("Please generate a chapter summary first in the 'Chapter Summarizer' tab to create a test.")
        else:
            if not st.session_state.mcqs or not st.session_state.subjective_questions:
                with st.spinner("Creating personalized test questions based on your content..."):
                    try:
                        # Generate MCQs
                        mcq_prompt = (
                            f"Generate 5 high-quality multiple-choice questions (MCQs) based on:\n\n"
                            f"{st.session_state.chapter_content}\n\n"
                            "Format each with:\n"
                            "Q1. [Question]\nA. [Option]\nB. [Option]\nC. [Option]\nD. [Option]\nAnswer: [Letter]"
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
                        st.session_state.mcqs = parsed_mcqs[:5]  # Ensure we only take 5

                        # Generate Subjective Questions
                        subj_prompt = (
                            f"Create 3 thought-provoking short answer questions based on:\n\n"
                            f"{st.session_state.chapter_content}\n\n"
                            "Format each as:\n"
                            "Q1. [Open-ended question requiring analysis]"
                        )
                        subj_response = model.generate_content(subj_prompt)
                        raw_subj = subj_response.text.strip().split("Q")[1:]
                        parsed_subj = []
                        for q in raw_subj:
                            question_text = q.strip()
                            parsed_subj.append(question_text)
                        st.session_state.subjective_questions = parsed_subj[:3]
                        
                    except Exception as e:
                        st.error(f"Error generating test: {str(e)}")

            # Test Form
            with st.form("test_form"):
                st.subheader("Multiple Choice Questions", divider="gray")
                user_answers = []
                
                for i, mcq in enumerate(st.session_state.mcqs):
                    with stylable_container(
                        key=f"mcq_{i}",
                        css_styles="""
                            {
                                background-color: #f8fafc;
                                border-radius: 8px;
                                padding: 16px;
                                margin-bottom: 12px;
                            }
                        """
                    ):
                        st.markdown(f"**Q{i+1}.** {mcq['question']}")
                        user_choice = st.radio(
                            f"Select your answer for Q{i+1}",
                            options=mcq['options'],
                            key=f"mcq_{i}",
                            index=None,
                            label_visibility="collapsed"
                        )
                        user_answers.append((user_choice, mcq['answer']))
                
                st.subheader("Short Answer Questions", divider="gray")
                subjective_responses = []
                
                for i, question in enumerate(st.session_state.subjective_questions):
                    with stylable_container(
                        key=f"subj_{i}",
                        css_styles="""
                            {
                                background-color: #f8fafc;
                                border-radius: 8px;
                                padding: 16px;
                                margin-bottom: 12px;
                            }
                        """
                    ):
                        st.markdown(f"**Q{i+6}.** {question}")
                        answer = st.text_area(
                            f"Your response for Q{i+6}",
                            key=f"subj_{i}",
                            height=120,
                            placeholder="Type your answer here...",
                            label_visibility="collapsed"
                        )
                        subjective_responses.append(answer)
                
                submitted = st.form_submit_button("Submit Assessment", type="primary")

            if submitted:
                # Evaluate MCQs
                correct = 0
                detailed_feedback = []
                
                st.subheader("Assessment Results", divider="blue")
                st.markdown("### Multiple Choice Evaluation")
                
                for i, (user_choice, correct_answer) in enumerate(user_answers):
                    with stylable_container(
                        key=f"result_{i}",
                        css_styles="""
                            {
                                background-color: white;
                                border-radius: 8px;
                                padding: 12px;
                                margin-bottom: 8px;
                                border: 1px solid #e2e8f0;
                            }
                        """
                    ):
                        if user_choice is None:
                            st.markdown(f"**Q{i+1}:** <span class='warning'>Unanswered</span>. <span class='correct'>Correct answer: {correct_answer}</span>", unsafe_allow_html=True)
                        elif user_choice.startswith(correct_answer):
                            correct += 1
                            st.markdown(f"✅ **Q{i+1}:** <span class='correct'>Correct! Your answer: {user_choice.split('.')[0]}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"❌ **Q{i+1}:** <span class='incorrect'>Your answer: {user_choice.split('.')[0]}</span>. <span class='correct'>Correct answer: {correct_answer}</span>", unsafe_allow_html=True)

                # Progress bar for MCQs
                mcq_score = correct / len(st.session_state.mcqs)
                st.progress(mcq_score, text=f"Multiple Choice Score: {correct}/{len(st.session_state.mcqs)}")
                
                # Evaluate Subjective Questions
                if any(subjective_responses):
                    st.markdown("### Short Answer Evaluation")
                    subjective_feedback = []
                    
                    for i, (question, response) in enumerate(zip(st.session_state.subjective_questions, subjective_responses)):
                        if not response:
                            with stylable_container(
                                key=f"empty_{i}",
                                css_styles="""
                                    {
                                        background-color: #fffbeb;
                                        border-radius: 8px;
                                        padding: 16px;
                                        margin-bottom: 12px;
                                    }
                                """
                            ):
                                st.warning(f"**Q{i+6}:** You didn't answer this question.")
                                subjective_feedback.append(f"Q{i+6}: No answer provided.")
                            continue
                        
                        with st.spinner(f"Evaluating your response to Q{i+6}..."):
                            try:
                                eval_prompt = (
                                    f"Evaluate this answer to the question '{question}':\n\n"
                                    f"Student's Answer:\n{response}\n\n"
                                    "Provide detailed feedback in this structure:\n"
                                    "**Strengths:** [what's good]\n\n"
                                    "**Areas for Improvement:** [what could be better]\n\n"
                                    "**Score:** [1-5 with 5 being excellent]\n\n"
                                    "**Model Answer:** [comprehensive ideal answer]"
                                )
                                eval_response = model.generate_content(eval_prompt)
                                feedback = eval_response.text
                                subjective_feedback.append(f"Q{i+6}:\n{feedback}")
                                
                                with stylable_container(
                                    key=f"eval_{i}",
                                    css_styles="""
                                        {
                                            background-color: #f0fdf4;
                                            border-radius: 8px;
                                            padding: 16px;
                                            margin-bottom: 16px;
                                            border-left: 4px solid #10b981;
                                        }
                                    """
                                ):
                                    st.markdown(f"#### Q{i+6}: {question}")
                                    st.markdown(f"**Your Answer:**\n{response}")
                                    st.markdown("---")
                                    st.markdown(f"**Evaluation:**\n{feedback}")
                            except Exception as e:
                                st.error(f"Error evaluating answer: {str(e)}")

                    st.session_state.subjective_feedback = subjective_feedback

                # Performance Summary
                with stylable_container(
                    key="performance_summary",
                    css_styles="""
                        {
                            background-color: #eff6ff;
                            border-radius: 8px;
                            padding: 20px;
                            margin-top: 16px;
                            border-left: 4px solid #4f46e5;
                        }
                    """
                ):
                    st.markdown("### Performance Summary")
                    
                    if correct == len(st.session_state.mcqs) and all(subjective_responses):
                        st.success("🌟 Outstanding! You've demonstrated excellent understanding of the material.")
                    elif correct >= len(st.session_state.mcqs) * 0.7 and any(subjective_responses):
                        st.info("👍 Good work! You understand most concepts but could review some areas.")
                    else:
                        st.warning("📖 Keep practicing! Review the material and try again for better results.")
                    
                    # Generate dynamic resources
                    with st.spinner("Compiling personalized learning resources..."):
                        try:
                            resource_prompt = (
                                f"Based on this chapter summary:\n\n{st.session_state.summary}\n\n"
                                "and these test results, suggest specific resources to improve understanding. "
                                "Include 1 video, 1 interactive resource, and 1 reading material. "
                                "Format as markdown bullet points with titles and URLs."
                            )
                            resource_response = model.generate_content(resource_prompt)
                            
                            with stylable_container(
                                key="resources_box",
                                css_styles="""
                                    {
                                        background-color: white;
                                        border-radius: 8px;
                                        padding: 16px;
                                        margin-top: 16px;
                                        border: 1px solid #e2e8f0;
                                    }
                                """
                            ):
                                st.markdown("### 📚 Recommended Learning Resources")
                                st.markdown(resource_response.text)
                        except Exception as e:
                            st.error(f"Error generating resources: {str(e)}")

# --- Doubt Solver ---
with tabs[2]:
    with stylable_container(
        key="doubt_container",
        css_styles="""
            {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 16px;
                border: 1px solid #e2e8f0;
            }
        """
    ):
        st.header("Doubt Resolution", divider="blue")
        st.markdown("Stuck on a concept? Get detailed explanations and examples")
        
        doubt = st.text_area(
            "Describe your doubt or confusion",
            height=150,
            placeholder="Explain what you're struggling to understand...",
            label_visibility="collapsed"
        )
        
        if st.button("Explain Concept", key="doubt_btn"):
            with st.spinner("Analyzing your doubt and preparing explanation..."):
                try:
                    response = model.generate_content(
                        f"Explain this concept/doubt in simple terms with examples:\n{doubt}\n\n"
                        "Structure your response with:\n"
                        "1. Clear definition\n"
                        "2. Real-world analogy\n"
                        "3. Practical examples\n"
                        "4. Common misconceptions\n"
                        "5. Visual representation suggestion"
                    )
                    
                    with stylable_container(
                        key="explanation_box",
                        css_styles="""
                            {
                                background-color: #f8fafc;
                                border-radius: 8px;
                                padding: 20px;
                                border-left: 4px solid #4f46e5;
                            }
                        """
                    ):
                        st.success("Here's your detailed explanation:")
                        st.markdown(response.text)
                    
                    # Follow-up questions
                    with st.spinner("Preparing related concepts to explore..."):
                        follow_up_prompt = (
                            f"Based on this doubt: '{doubt}' and the explanation given, "
                            "suggest 3 follow-up questions the learner might have, "
                            "with brief answers to each."
                        )
                        follow_up_response = model.generate_content(follow_up_prompt)
                        
                        with stylable_container(
                            key="followup_box",
                            css_styles="""
                                {
                                    background-color: #f0fdf4;
                                    border-radius: 8px;
                                    padding: 16px;
                                    margin-top: 16px;
                                }
                            """
                        ):
                            st.markdown("### 🤔 Related Concepts to Explore")
                            st.markdown(follow_up_response.text)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
