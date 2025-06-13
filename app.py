import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# Configure Gemini API
genai.configure(api_key="AIzaSyBajGa89W5CJOGwLfYQUkSqw6B505KGRiA")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state and data storage
if 'df_users' not in st.session_state:
    st.session_state.df_users = pd.DataFrame(columns=['username', 'timestamp'])
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = None

# Page Configuration
st.set_page_config(
    page_title="EduBuddy AI",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🧠"
)

# Custom CSS for premium styling
st.markdown("""
    <style>
        /* Main styles */
        .main {
            background-color: #ffffff;
            color: #1e293b;
        }
        
        /* Premium header */
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
        
        /* Feature cards */
        .feature-card {
            background-color: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            border: 1px solid #f1f5f9;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
            border-color: #4f46e5;
        }
        
        .feature-card.selected {
            border: 2px solid #4f46e5;
            background-color: #f8fafc;
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: #4f46e5;
        }
        
        .feature-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: #1e293b;
        }
        
        .feature-desc {
            color: #64748b;
            line-height: 1.6;
        }
        
        /* Content containers */
        .content-container {
            background-color: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            border: 1px solid #f1f5f9;
        }
        
        /* Gradient footer */
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
        
        /* Username input */
        .username-input {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            z-index: 100;
            border: 1px solid #e2e8f0;
        }
    </style>
""", unsafe_allow_html=True)

# Function to handle tab selection
def select_tab(tab_name):
    st.session_state.current_tab = tab_name

# Cover Page - Only shown when no tab is selected
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
        st.markdown(f"""
            <div class="feature-card" onclick="selectTab('summary')">
                <div class="feature-icon">📖</div>
                <h3 class="feature-title">Smart Summaries</h3>
                <p class="feature-desc">Transform lengthy chapters into concise, digestible summaries with key concepts highlighted.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="feature-card" onclick="selectTab('test')">
                <div class="feature-icon">📝</div>
                <h3 class="feature-title">Adaptive Testing</h3>
                <p class="feature-desc">Personalized quizzes that identify knowledge gaps and reinforce learning.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="feature-card" onclick="selectTab('doubt')">
                <div class="feature-icon">💡</div>
                <h3 class="feature-title">Doubt Resolution</h3>
                <p class="feature-desc">Instant explanations with analogies and examples for any concept you're stuck on.</p>
            </div>
        """, unsafe_allow_html=True)

    # Add JavaScript for tab selection
    st.markdown("""
        <script>
            function selectTab(tabName) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: tabName
                }, '*');
            }
        </script>
    """, unsafe_allow_html=True)

# Chapter Summarizer Tab
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

# Knowledge Assessment Tab
def show_test_tab():
    with st.container():
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.header("📝 Knowledge Assessment", divider="blue")
        
        if not st.session_state.chapter_content:
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
                        st.session_state.mcqs = parsed_mcqs[:5]

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
                    st.markdown(f"**Q{i+1}.** {mcq['question']}")
                    user_choice = st.radio(
                        f"Select your answer for Q{i+1}",
                        options=mcq['options'],
                        key=f"mcq_{i}",
                        index=None,
                        label_visibility="collapsed"
                    )
                    user_answers.append((user_choice, mcq['answer']))
                    st.markdown("---")
                
                st.subheader("Short Answer Questions", divider="gray")
                subjective_responses = []
                
                for i, question in enumerate(st.session_state.subjective_questions):
                    st.markdown(f"**Q{i+6}.** {question}")
                    answer = st.text_area(
                        f"Your response for Q{i+6}",
                        key=f"subj_{i}",
                        height=120,
                        placeholder="Type your answer here...",
                        label_visibility="collapsed"
                    )
                    subjective_responses.append(answer)
                    st.markdown("---")
                
                submitted = st.form_submit_button("Submit Assessment", type="primary")

            if submitted:
                # Evaluate MCQs
                correct = 0
                detailed_feedback = []
                
                st.subheader("Assessment Results", divider="blue")
                st.markdown("### Multiple Choice Evaluation")
                
                for i, (user_choice, correct_answer) in enumerate(user_answers):
                    if user_choice is None:
                        st.markdown(f"**Q{i+1}:** <span class='warning'>Unanswered</span>. <span class='correct'>Correct answer: {correct_answer}</span>", unsafe_allow_html=True)
                    elif user_choice.startswith(correct_answer):
                        correct += 1
                        st.markdown(f"✅ **Q{i+1}:** <span class='correct'>Correct! Your answer: {user_choice.split('.')[0]}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"❌ **Q{i+1}:** <span class='incorrect'>Your answer: {user_choice.split('.')[0]}</span>. <span class='correct'>Correct answer: {correct_answer}</span>", unsafe_allow_html=True)
                    st.markdown("---")

                # Progress bar for MCQs
                mcq_score = correct / len(st.session_state.mcqs)
                st.progress(mcq_score, text=f"Multiple Choice Score: {correct}/{len(st.session_state.mcqs)}")
                
                # Evaluate Subjective Questions
                if any(subjective_responses):
                    st.markdown("### Short Answer Evaluation")
                    subjective_feedback = []
                    
                    for i, (question, response) in enumerate(zip(st.session_state.subjective_questions, subjective_responses)):
                        if not response:
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
                                
                                st.markdown(f"#### Q{i+6}: {question}")
                                st.markdown(f"**Your Answer:**\n{response}")
                                st.markdown("---")
                                st.markdown(f"**Evaluation:**\n{feedback}")
                                st.markdown("---")
                            except Exception as e:
                                st.error(f"Error evaluating answer: {str(e)}")

                    st.session_state.subjective_feedback = subjective_feedback

                # Performance Summary
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
                        
                        st.markdown("### 📚 Recommended Learning Resources")
                        st.markdown(resource_response.text)
                    except Exception as e:
                        st.error(f"Error generating resources: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

# Doubt Solver Tab
def show_doubt_tab():
    with st.container():
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.header("💭 Doubt Resolution", divider="blue")
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
                        
                        st.markdown("### 🤔 Related Concepts to Explore")
                        st.markdown(follow_up_response.text)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

# Username Input (Fixed at bottom right)
def show_username_input():
    with st.container():
        st.markdown("""
            <div class="username-input">
                <form onsubmit="captureUsername(event)">
                    <input type="text" id="username" placeholder="Enter your username" required>
                    <button type="submit">Save</button>
                </form>
            </div>
            <script>
                function captureUsername(event) {
                    event.preventDefault();
                    const username = document.getElementById('username').value;
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue',
                        value: username
                    }, '*');
                }
            </script>
        """, unsafe_allow_html=True)

# Main App Logic
def main():
    # Handle tab selection
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = None
    
    # Check for username submission
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    # Show appropriate content based on current tab
    if st.session_state.current_tab is None:
        show_cover_page()
    elif st.session_state.current_tab == 'summary':
        show_summary_tab()
    elif st.session_state.current_tab == 'test':
        show_test_tab()
    elif st.session_state.current_tab == 'doubt':
        show_doubt_tab()
    
    # Always show username input (except on cover page)
    if st.session_state.current_tab is not None:
        show_username_input()
    
    # Gradient Footer
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
    
    # Handle username submission
    if st.session_state.get('username_submitted'):
        new_user = {
            'username': st.session_state.username_submitted,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        st.session_state.df_users = pd.concat([
            st.session_state.df_users,
            pd.DataFrame([new_user])
        ], ignore_index=True)
        
        # Save to CSV (in a real app, you'd use a database)
        st.session_state.df_users.to_csv('user_data.csv', index=False)
        st.session_state.username_submitted = None
        st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    main()
