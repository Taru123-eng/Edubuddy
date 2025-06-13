import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# Configure Gemini API
genai.configure(api_key="AIzaSyBajGa89W5CJOGwLfYQUkSqw6B505KGRiA")  # Replace with your API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state
if 'df_users' not in st.session_state:
    st.session_state.df_users = pd.DataFrame(columns=['username', 'timestamp'])
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "home"
if 'username' not in st.session_state:
    st.session_state.username = None
if 'chapter_content' not in st.session_state:
    st.session_state.chapter_content = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'mcqs' not in st.session_state:
    st.session_state.mcqs = []
if 'subjective_questions' not in st.session_state:
    st.session_state.subjective_questions = []

# Page Configuration
st.set_page_config(
    page_title="EduBuddy AI",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🧠"
)

# Custom CSS
st.markdown("""
    <style>
        /* Main styles */
        .main {
            background-color: #f8fafc;
        }
        
        /* Header */
        .header {
            text-align: center;
            padding: 2rem 0;
        }
        
        .title {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(90deg, #4f46e5 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #64748b;
            max-width: 700px;
            margin: 0 auto 2rem;
        }
        
        /* Feature cards */
        .feature-container {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 2rem auto;
            max-width: 1200px;
        }
        
        .feature-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
            flex: 1;
            text-align: center;
            cursor: pointer;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0,0,0,0.1);
            border-color: #4f46e5;
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: #4f46e5;
        }
        
        .feature-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .feature-desc {
            color: #64748b;
            line-height: 1.6;
        }
        
        /* Content containers */
        .content-box {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
            margin-bottom: 2rem;
            max-width: 1000px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Username input */
        .username-form {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 100;
            border: 1px solid #e2e8f0;
        }
        
        /* Back button */
        .back-btn {
            margin-bottom: 1rem;
        }
        
        /* Text areas */
        .stTextArea>div>div>textarea {
            border-radius: 12px;
            padding: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Home Page
def show_home():
    st.markdown("""
        <div class="header">
            <h1 class="title">EduBuddy AI</h1>
            <p class="subtitle">Your intelligent learning companion powered by Gemini AI</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="feature-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📖 Smart Summaries", key="summary_btn", use_container_width=True):
            st.session_state.current_tab = "summary"
            st.experimental_rerun()
    with col2:
        if st.button("📝 Adaptive Testing", key="test_btn", use_container_width=True):
            st.session_state.current_tab = "test"
            st.experimental_rerun()
    with col3:
        if st.button("💡 Doubt Solver", key="doubt_btn", use_container_width=True):
            st.session_state.current_tab = "doubt"
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Chapter Summarizer
def show_summary():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    if st.button("← Back to Home", key="back_summary", use_container_width=True):
        st.session_state.current_tab = "home"
        st.experimental_rerun()
    
    st.header("📖 Chapter Summarizer")
    
    chapter_text = st.text_area(
        "Paste your chapter content here:",
        height=300,
        placeholder="Textbook chapter, lecture notes, or study materials..."
    )
    
    if st.button("Generate Summary", type="primary"):
        if chapter_text:
            with st.spinner("Creating your summary..."):
                try:
                    response = model.generate_content(
                        f"Create a comprehensive summary with key points for:\n\n{chapter_text}"
                    )
                    st.session_state.chapter_content = chapter_text
                    st.session_state.summary = response.text
                    st.success("Summary generated successfully!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter some text to summarize")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Knowledge Assessment
def show_test():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    if st.button("← Back to Home", key="back_test", use_container_width=True):
        st.session_state.current_tab = "home"
        st.experimental_rerun()
    
    st.header("📝 Knowledge Assessment")
    
    if not st.session_state.chapter_content:
        st.warning("Please generate a chapter summary first")
    else:
        if st.button("Generate Test Questions"):
            with st.spinner("Creating assessment..."):
                try:
                    # Generate MCQs
                    mcq_response = model.generate_content(
                        f"Create 5 MCQs based on:\n\n{st.session_state.chapter_content}\n\n"
                        "Format each as: Q1. [Question] A) [Option] B) [Option] C) [Option] D) [Option] Answer: [Letter]"
                    )
                    st.session_state.mcqs = mcq_response.text
                    
                    # Generate subjective questions
                    subj_response = model.generate_content(
                        f"Create 3 short answer questions based on:\n\n{st.session_state.chapter_content}"
                    )
                    st.session_state.subjective_questions = subj_response.text
                    
                    st.success("Test questions generated!")
                    st.markdown("### Multiple Choice Questions")
                    st.markdown(st.session_state.mcqs)
                    st.markdown("### Short Answer Questions")
                    st.markdown(st.session_state.subjective_questions)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Doubt Solver
def show_doubt():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    if st.button("← Back to Home", key="back_doubt", use_container_width=True):
        st.session_state.current_tab = "home"
        st.experimental_rerun()
    
    st.header("💡 Doubt Solver")
    
    doubt = st.text_area(
        "Explain what you're confused about:",
        height=150,
        placeholder="I don't understand how photosynthesis works..."
    )
    
    if st.button("Get Explanation", type="primary"):
        if doubt:
            with st.spinner("Generating explanation..."):
                try:
                    response = model.generate_content(
                        f"Explain this in simple terms with examples:\n{doubt}\n\n"
                        "Include: 1) Definition 2) Analogy 3) Examples 4) Common mistakes"
                    )
                    st.success("Here's your explanation:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please describe your doubt")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Username Input
def username_form():
    with st.form("username_form", clear_on_submit=True):
        st.markdown('<div class="username-form">', unsafe_allow_html=True)
        username = st.text_input("Enter your username to continue:")
        submitted = st.form_submit_button("Submit")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submitted and username:
            st.session_state.username = username
            new_entry = {
                'username': username,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            st.session_state.df_users = pd.concat([
                st.session_state.df_users,
                pd.DataFrame([new_entry])
            ], ignore_index=True)
            st.session_state.df_users.to_csv('user_data.csv', index=False)
            st.success("Username saved!")

# Main App
def main():
    if st.session_state.current_tab == "home":
        show_home()
    elif st.session_state.current_tab == "summary":
        show_summary()
    elif st.session_state.current_tab == "test":
        show_test()
    elif st.session_state.current_tab == "doubt":
        show_doubt()
    
    # Show username input when not on home page
    if st.session_state.current_tab != "home" and not st.session_state.username:
        username_form()

if __name__ == "__main__":
    main()
