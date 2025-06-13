import streamlit as st
import google.generativeai as genai

# Set your Gemini API key directly here
genai.configure(api_key="AIzaSyBajGa89W5CJOGwLfYQUkSqw6B505KGRiA")
model = genai.GenerativeModel("gemini-1.5-flash")

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
        
        .cta-button {
            display: flex;
            justify-content: center;
            margin: 40px 0 60px;
        }
        
        /* Premium tabs */
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
            gap: 10px;
            margin-bottom: 30px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 30px;
            border-radius: 12px !important;
            background-color: transparent !important;
            font-weight: 500;
            font-size: 1rem;
            transition: all 0.3s ease !important;
            border: 1px solid #e2e8f0 !important;
            color: #64748b !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #4f46e5 !important;
            color: white !important;
            border-color: #4f46e5 !important;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #4f46e5;
            color: white;
            border-radius: 12px;
            padding: 14px 28px;
            font-weight: 500;
            font-size: 1rem;
            transition: all 0.3s ease;
            border: none;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
        }
        
        .stButton>button:hover {
            background-color: #4338ca;
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
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
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
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
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 80px;
            padding: 30px 0;
            color: #94a3b8;
            font-size: 0.9rem;
            border-top: 1px solid #f1f5f9;
        }
    </style>
""", unsafe_allow_html=True)

# Premium Header Section
st.markdown("""
    <div class="header-container">
        <img src="https://cdn-icons-png.flaticon.com/512/2232/2232688.png" class="header-logo">
        <div>
            <h1 class="main-title">EduBuddy AI</h1>
            <p class="subtitle">Your intelligent learning companion that adapts to your study style, powered by Gemini AI</p>
        </div>
        <img src="https://cdn-icons-png.flaticon.com/512/2232/2232688.png" class="header-logo">
    </div>
""", unsafe_allow_html=True)

# Centered CTA Button
st.markdown("""
    <div class="cta-button">
        <button>Get Started →</button>
    </div>
""", unsafe_allow_html=True)

# Feature Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📖</div>
            <h3 class="feature-title">Smart Summaries</h3>
            <p class="feature-desc">Transform lengthy chapters into concise, digestible summaries with key concepts highlighted.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3 class="feature-title">Adaptive Testing</h3>
            <p class="feature-desc">Personalized quizzes that identify knowledge gaps and reinforce learning.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <h3 class="feature-title">Doubt Resolution</h3>
            <p class="feature-desc">Instant explanations with analogies and examples for any concept you're stuck on.</p>
        </div>
    """, unsafe_allow_html=True)

# Main tabs - kept from your original code but with premium styling
tabs = st.tabs(["   📖 Chapter Summarizer   ", "   📝 Take a Test   ", "   💭 Doubt Solver   "])

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

# [REST OF YOUR ORIGINAL CODE FOR THE TABS CONTENT REMAINS THE SAME]
# Include all your existing tab content here exactly as you had it

# Premium Footer
st.markdown("""
    <div class="footer">
        ©️ 2023 EduBuddy AI | Powered by Gemini AI | Terms of Service | Privacy Policy
    </div>
""", unsafe_allow_html=True)
