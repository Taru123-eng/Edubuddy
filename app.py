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
        .correct {color: green; font-weight: bold;}
        .incorrect {color: red; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.title("📚 EduBuddy - AI Learning Assistant")
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
    st.header("📖 Chapter Summarizer")
    chapter_text = st.text_area("Paste your chapter or notes here", height=300)
    if st.button("Summarize Chapter"):
        with st.spinner("Summarizing..."):
            try:
                response = model.generate_content(f"Summarize this chapter:\n\n{chapter_text}")
                summary = response.text
                st.session_state.chapter_content = chapter_text
                st.session_state.summary = summary
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
        if not st.session_state.mcqs or not st.session_state.subjective_questions:
            with st.spinner("Generating test questions..."):
                try:
                    # Generate MCQs
                    mcq_prompt = (
                        f"Generate 5 multiple-choice questions (MCQs) based on the following chapter content:\n\n"
                        f"{st.session_state.chapter_content}\n\n"
                        "Each question should have 4 options labeled A to D, and specify the correct answer. "
                        "Format:\n"
                        "Q1. What is ...?\nA. ...\nB. ...\nC. ...\nD. ...\nAnswer: B"
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
                    st.session_state.mcqs = parsed_mcqs

                    # Generate Subjective Questions
                    subj_prompt = (
                        f"Generate 3 short answer questions based on the following chapter content:\n\n"
                        f"{st.session_state.chapter_content}\n\n"
                        "Format each question as:\n"
                        "Q1. Explain the concept of...\n"
                        "Q2. Describe the process of...\n"
                        "Q3. Compare and contrast..."
                    )
                    subj_response = model.generate_content(subj_prompt)
                    raw_subj = subj_response.text.strip().split("Q")[1:]
                    parsed_subj = []
                    for q in raw_subj:
                        question_text = q.strip()
                        parsed_subj.append(question_text)
                    st.session_state.subjective_questions = parsed_subj[:3]  # Take first 3 questions
                    
                except Exception as e:
                    st.error(f"Error generating test: {e}")

        # Display test
        score = 0
        user_answers = []
        subjective_responses = []

        with st.form("test_form"):
            st.subheader("Multiple Choice Questions")
            for i, mcq in enumerate(st.session_state.mcqs):
                st.write(f"*Q{i+1}. {mcq['question']}*")
                user_choice = st.radio(
                    f"Choose an option for Q{i+1}", 
                    options=mcq['options'], 
                    key=f"mcq{i+1}",
                    index=None
                )
                user_answers.append((user_choice, mcq['answer']))
                st.markdown("---")

            st.subheader("Short Answer Questions")
            for i, question in enumerate(st.session_state.subjective_questions):
                st.write(f"*Q{i+6}. {question}*")
                answer = st.text_area(f"Your answer for Q{i+6}", key=f"subj{i+1}")
                subjective_responses.append(answer)
                st.markdown("---")

            submitted = st.form_submit_button("Submit Test")

        if submitted:
            # Evaluate MCQs
            correct = 0
            detailed_feedback = []
            
            st.subheader("Test Results")
            st.markdown("### Multiple Choice Questions Evaluation:")
            
            for i, (user_choice, correct_answer) in enumerate(user_answers):
                if user_choice is None:
                    feedback = f"Q{i+1}: You didn't select any option. Correct answer is {correct_answer}."
                    detailed_feedback.append(feedback)
                    st.markdown(f"❌ Q{i+1}: You didn't select any option. <span class='correct'>Correct answer is {correct_answer}.</span>", unsafe_allow_html=True)
                elif user_choice.startswith(correct_answer):
                    correct += 1
                    feedback = f"Q{i+1}: Correct! Your answer: {user_choice}"
                    detailed_feedback.append(feedback)
                    st.markdown(f"✅ Q{i+1}: <span class='correct'>Correct! Your answer: {user_choice}</span>", unsafe_allow_html=True)
                else:
                    feedback = f"Q{i+1}: Incorrect. Your answer: {user_choice}. Correct answer is {correct_answer}."
                    detailed_feedback.append(feedback)
                    st.markdown(f"❌ Q{i+1}: <span class='incorrect'>Your answer: {user_choice}</span>. <span class='correct'>Correct answer is {correct_answer}.</span>", unsafe_allow_html=True)

            st.success(f"📊 You scored {correct}/5 on multiple choice questions")

            # Evaluate Subjective Questions
            st.markdown("### Short Answer Questions Evaluation:")
            subjective_feedback = []
            
            for i, (question, response) in enumerate(zip(st.session_state.subjective_questions, subjective_responses)):
                if not response:
                    st.warning(f"Q{i+6}: You didn't answer this question.")
                    subjective_feedback.append(f"Q{i+6}: No answer provided.")
                    continue
                
                with st.spinner(f"Evaluating Q{i+6}..."):
                    eval_prompt = (
                        f"Evaluate this answer to the question '{question}':\n\n"
                        f"Student's Answer:\n{response}\n\n"
                        "Provide feedback in this format:\n"
                        "Strengths: [what's good]\n"
                        "Areas for Improvement: [what could be better]\n"
                        "Score: [1-5]\n"
                        "Model Answer: [ideal answer]"
                    )
                    try:
                        eval_response = model.generate_content(eval_prompt)
                        feedback = eval_response.text
                        subjective_feedback.append(f"Q{i+6}:\n{feedback}")
                        
                        st.markdown(f"#### Q{i+6}: {question}")
                        st.markdown(f"**Your Answer:** {response}")
                        st.markdown(f"**Evaluation:**")
                        st.markdown(feedback)
                        st.markdown("---")
                    except Exception as e:
                        st.error(f"Error evaluating answer: {e}")

            st.session_state.subjective_feedback = subjective_feedback

            # Overall performance remark
            if correct == 5 and all(subjective_responses):
                remark = "🌟 Outstanding performance! You've mastered this material."
            elif correct >= 3 and any(subjective_responses):
                remark = "👍 Good job! You understand most concepts but could review some areas."
            else:
                remark = "📖 Keep practicing! Review the material and try again."

            st.info(f"Overall Performance: {remark}")

            # Generate dynamic resources based on content
            with st.spinner("Generating personalized learning resources..."):
                try:
                    resource_prompt = (
                        f"Based on this chapter summary:\n\n{st.session_state.summary}\n\n"
                        "Suggest 3-5 specific online learning resources (with URLs) that would help the student "
                        "better understand this material. Include videos, articles, and interactive exercises. "
                        "Format each as: [Resource Type] [Title](URL) - Brief description"
                    )
                    resource_response = model.generate_content(resource_prompt)
                    st.markdown("### 📚 Personalized Learning Resources:")
                    st.markdown(resource_response.text)
                except Exception as e:
                    st.error(f"Error generating resources: {e}")

# --- Doubt Solver ---
with tabs[2]:
    st.header("💭 Doubt Solver")
    doubt = st.text_area("Write your doubt or what you're confused about")
    if st.button("Solve My Doubt"):
        with st.spinner("Solving your doubt..."):
            try:
                response = model.generate_content(
                    f"Explain this doubt in a simple and clear way: {doubt}\n\n"
                    "Provide examples if possible and suggest analogies to help understand better. "
                    "Break down complex concepts into smaller steps."
                )
                st.success("Explanation:")
                st.markdown(response.text)
                
                # Follow-up questions
                follow_up_prompt = (
                    f"Based on this doubt: '{doubt}' and your explanation, "
                    "suggest 2-3 follow-up questions the student might have, "
                    "and provide brief answers to each."
                )
                follow_up_response = model.generate_content(follow_up_prompt)
                st.markdown("### 🤔 You Might Also Wonder:")
                st.markdown(follow_up_response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
