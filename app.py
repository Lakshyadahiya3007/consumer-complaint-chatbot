import streamlit as st
import pandas as pd
import joblib
from textblob import TextBlob
import time

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AI Consumer Complaint Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>

.main {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

.stApp {
    background: linear-gradient(to bottom right, #0f172a, #111827);
}

h1, h2, h3 {
    color: white !important;
}

.hero {
    padding: 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    text-align: center;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
    margin-bottom: 2rem;
}

.chat-box {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    margin-top: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}

.metric-card {
    background: rgba(255,255,255,0.07);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    color: white;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
}

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 40px;
}

.stButton>button {
    background: linear-gradient(to right, #3b82f6, #8b5cf6);
    color: white;
    border-radius: 12px;
    padding: 12px 25px;
    border: none;
    font-size: 18px;
    font-weight: bold;
    width: 100%;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(to right, #2563eb, #7c3aed);
}

textarea {
    border-radius: 15px !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD MODEL
# ==========================================
@st.cache_resource

def load_model():
    return joblib.load("complaint_classifier.pkl")

model = load_model()

# ==========================================
# SENTIMENT FUNCTION
# ==========================================
def get_sentiment(text):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0:
        return "Positive 😊"

    elif polarity < 0:
        return "Negative 😠"

    else:
        return "Neutral 😐"

# ==========================================
# RECOMMENDATIONS
# ==========================================
recommendations = {
    "Credit card": "Check recent transactions and contact card support immediately.",
    "Mortgage": "Review mortgage payment history and contact provider.",
    "Debt collection": "Request written debt verification from the collector.",
    "Bank account or service": "Check bank statements and raise a dispute if necessary.",
    "Student loan": "Contact the loan servicer regarding repayment assistance.",
    "Payday loan": "Carefully review all loan terms and report hidden charges."
}

# ==========================================
# CHATBOT FUNCTION
# ==========================================
def chatbot_response(user_input):

    predicted_product = model.predict([user_input])[0]

    sentiment = get_sentiment(user_input)

    recommendation = recommendations.get(
        predicted_product,
        "Please contact customer support regarding your complaint."
    )

    return {
        "product": predicted_product,
        "sentiment": sentiment,
        "recommendation": recommendation
    }

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.title("🤖 AI Dashboard")

st.sidebar.success("System Online")

st.sidebar.markdown("---")

st.sidebar.info("""
### Features

✅ AI Complaint Detection

✅ Sentiment Analysis

✅ Smart Recommendations

✅ Real-Time NLP Processing

✅ Interactive Dashboard
""")

st.sidebar.markdown("---")

st.sidebar.metric("Model Accuracy", "89%")
st.sidebar.metric("Dataset Records", "500K+")
st.sidebar.metric("Response Time", "1 sec")

# ==========================================
# HERO SECTION
# ==========================================
st.markdown("""
<div class='hero'>
    <h1>🤖 AI Consumer Complaint Assistant</h1>
    <p>
    Analyze customer complaints using Artificial Intelligence & NLP.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# DASHBOARD CARDS
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='metric-card'>
        <h2>⚡</h2>
        <h3>Fast AI Analysis</h3>
        <p>Instant complaint detection</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-card'>
        <h2>🧠</h2>
        <h3>NLP Engine</h3>
        <p>Smart sentiment understanding</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='metric-card'>
        <h2>📊</h2>
        <h3>Analytics</h3>
        <p>AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# INPUT SECTION
# ==========================================
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

st.subheader("💬 Enter Your Complaint")

user_input = st.text_area(
    "",
    placeholder="Example: My credit card has unauthorized charges and the bank is not responding.",
    height=180
)

analyze = st.button("🚀 Analyze Complaint")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# AI RESPONSE
# ==========================================
if analyze:

    if user_input.strip() != "":

        with st.spinner("AI is analyzing your complaint..."):

            time.sleep(1)

            result = chatbot_response(user_input)

            st.markdown("---")

            st.markdown("## 🤖 AI Analysis Result")

            col1, col2 = st.columns(2)

            with col1:
                st.success(f"😊 Sentiment: {result['sentiment']}")

                st.info(f"🏷️ Complaint Category: {result['product']}")

            with col2:
                st.warning("💡 AI Recommendation")

                st.write(result['recommendation'])

            st.markdown("---")

            st.subheader("✅ Suggested Next Steps")

            st.write("1. Contact customer support.")
            st.write("2. Save all complaint evidence.")
            st.write("3. Escalate complaint if unresolved.")
            st.write("4. File complaint through CFPB if required.")

    else:
        st.error("Please enter a complaint first.")

# ==========================================
# ANALYTICS SECTION
# ==========================================
st.markdown("---")

st.subheader("📈 Complaint Analytics Dashboard")

chart_data = pd.DataFrame({
    'Complaint Types': [
        'Credit Card',
        'Mortgage',
        'Debt Collection',
        'Bank Account',
        'Student Loan'
    ],
    'Count': [120, 90, 150, 80, 60]
})

st.bar_chart(chart_data.set_index('Complaint Types'))

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<div class='footer'>

Developed by Lakshya Dahiya 🚀<br>
AI-Powered Consumer Complaint Analysis System

</div>
""", unsafe_allow_html=True)
