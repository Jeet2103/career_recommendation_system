import streamlit as st
from main_flow import run_pipeline
from logger_config.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# ----------------- Streamlit Page Configuration -----------------
st.set_page_config(
    page_title="Career Path Recommender",
    layout="centered",
    page_icon="🎓"
)

# ----------------- Dark Mode Styling -----------------
st.markdown("""
<style>
/* Page Background Image */
body {
    background-image: url("https://i.pinimg.com/736x/d1/f5/fc/d1f5fceea6d7c8325296cef44f6adcf1.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    opacity: 0.95;
}

/* Text Styling */
h1 {
    text-align: center;
    color: white;
}
.desc {
    text-align: center;
    font-size: 16px;
    color: #cccccc;
    margin-bottom: 30px;
}
.stTextArea textarea {
    background-color: #1e1e1e;
    color: white;
    font-size: 16px;
}

/* Recommendation Box Styling */
.recommend-box {
    background-color: rgba(44, 44, 44, 0.95);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border-left: 6px solid #1e90ff;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
</style>

<h1>🎓 Career Path Recommender</h1>
<div class='desc'>Powered by AI · Describe your interests to discover the perfect career paths</div>
""", unsafe_allow_html=True)

# ----------------- Input Text Area -----------------
user_input = st.text_area("✏️ Enter your interests (e.g., 'I love sketching and programming'):", height=150)

# ----------------- Process Button -----------------
if st.button("🚀 Get Career Recommendations"):
    if user_input.strip():
        logger.info("User submitted input: %s", user_input)

        with st.spinner("Analyzing your interests and generating personalized recommendations..."):
            output = run_pipeline(user_input)

        # ----------------- Check for fallback -----------------
        if output.startswith("Clarification Needed:"):
            question = output.replace("Clarification Needed:", "").strip()
            st.warning(f"🧐 {question}")
        else:
            st.markdown("### 🎯 Your Recommended Career Paths")

            # Split results into career+explanation blocks
            for block in output.strip().split("Career Path:")[1:]:
                lines = block.strip().split("\n")
                career = lines[0].strip()
                explanation = "\n".join(lines[1:]).replace("Explanation:", "").strip()

                st.markdown(f"""
                <div class='recommend-box'>
                    <strong>👔 {career}</strong><br/>
                    <div style="font-size: 15px; margin-top: 5px;">{explanation}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please describe your interests before clicking the button.")
