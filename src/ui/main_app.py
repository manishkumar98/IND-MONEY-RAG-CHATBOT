import streamlit as st
import requests
import os
from PIL import Image

# Configuration
st.set_page_config(
    page_title="SBI MF Assistant | INDmoney Style",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# INDmoney Theme Colors
PRIMARY_COLOR = "#00d09c"  # Emerald Green
BG_COLOR = "#0e1117"
CARD_BG = "#1e222d"
TEXT_COLOR = "#ffffff"
SECONDARY_TEXT = "#8a94a6"

# Sidebar with Navigation
with st.sidebar:
    st.image("https://www.sbimf.com/Content/Images/logo.svg", width=200)
    st.markdown(f"""
    <div style='text-align: center; padding: 10px 0;'>
        <p style='color: {SECONDARY_TEXT};'>Official Factual Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("---")
    st.markdown("### Compliance")
    st.info("Facts-only answers using official sources. No investment advice.")
    st.warning("PII Protection active.")

# Custom CSS for Premium UI
st.markdown(f"""
    <style>
    /* Main Background */
    .stApp {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
    }}
    
    /* Header Container */
    .main-header {{
        text-align: center;
        padding-top: 50px;
        padding-bottom: 20px;
    }}
    
    /* Info Box */
    .info-box {{
        background-color: rgba(0, 208, 156, 0.1);
        border: 1px solid {PRIMARY_COLOR};
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
        color: {TEXT_COLOR};
        font-size: 0.9em;
    }}
    
    /* Chat Bubbles */
    .chat-bubble-user {{
        background-color: {CARD_BG};
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-right: 4px solid {PRIMARY_COLOR};
        display: flex;
        align-items: center;
    }}
    
    .chat-bubble-ai {{
        background-color: #2b313e;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid {PRIMARY_COLOR};
        display: flex;
        align-items: center;
    }}
    
    .icon {{
        font-size: 24px;
        margin-right: 15px;
    }}

    /* Buttons / Chips */
    .stButton > button {{
        background-color: rgba(255, 255, 255, 0.05);
        color: {TEXT_COLOR};
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.3s;
    }}
    
    .stButton > button:hover {{
        border-color: {PRIMARY_COLOR};
        color: {PRIMARY_COLOR};
        background-color: rgba(0, 208, 156, 0.05);
    }}
    
    /* Input Style */
    .stChatInputContainer textarea {{
        background-color: {CARD_BG} !important;
        border-radius: 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Main UI
st.markdown("<div class='main-header'>", unsafe_allow_html=True)
st.title(f"SBI Mutual Fund Assistant 💬")
st.markdown(f"<p style='color: {SECONDARY_TEXT};'>Ask anything about SBI Bluechip, Flexicap, Small Cap, and more.</p>", unsafe_allow_html=True)
st.markdown(f"<p style='color: {SECONDARY_TEXT}; font-size: 0.85em; font-style: italic;'>Facts-only. No investment advice.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Info Box (Similar to image)
st.markdown(f"""
<div class='info-box'>
    ℹ️ Welcome! I am your factual SBI Mutual Fund Assistant. I combine information from official SBI MF docs and INDmoney factsheets to give you the most accurate data.
</div>
""", unsafe_allow_html=True)

# Suggestion Chips
st.markdown("<p style='font-size: 0.9em; color: gray;'>Outline your query:</p>", unsafe_allow_html=True)
cols = st.columns(3)
suggestion = None
if cols[0].button("SBI Bluechip Expense Ratio", use_container_width=True):
    suggestion = "What is the expense ratio of SBI Bluechip Fund?"
if cols[1].button("ELSS Tax Saving Lock-in", use_container_width=True):
    suggestion = "What is the lock-in period of SBI Long Term Equity Fund?"
if cols[2].button("Small Cap Risk Level", use_container_width=True):
    suggestion = "What is the risk level of SBI Small Cap Fund?"

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class='chat-bubble-user'>
            <span class='icon'>👤</span>
            <div>{message['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='chat-bubble-ai'>
            <span class='icon'>🤖</span>
            <div>{message['content']}</div>
        </div>
        """, unsafe_allow_html=True)

# Input
user_query = st.chat_input("Your question...")
if suggestion:
    user_query = suggestion

if user_query:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.markdown(f"""
    <div class='chat-bubble-user'>
        <span class='icon'>👤</span>
        <div>{user_query}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call Backend
    BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
    with st.spinner("Analyzing data..."):
        try:
            response = requests.post(f"{BACKEND_URL}/ask", json={"query": user_query})
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.markdown(f"""
                <div class='chat-bubble-ai'>
                    <span class='icon'>🤖</span>
                    <div>{answer}</div>
                </div>
                """, unsafe_allow_html=True)
                st.rerun() # Refresh to show in correct order
            else:
                st.error("Error: Backend returned an error.")
        except Exception as e:
            st.error(f"Error: Could not connect to the backend at http://localhost:8000. {e}")
