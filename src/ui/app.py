import streamlit as st
import requests
import json

st.set_page_config(page_title="INDMoney MF Assistant", layout="centered")

# Custom CSS for INDMoney-like aesthetic
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #1a1c23;
        color: white;
        border-radius: 10px;
    }
    .stButton > button {
        border-radius: 20px;
        background-color: #00d09c;
        color: black;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💸 SBI Mutual Fund Assistant")
st.info("Welcome to the SBI Mutual Fund Assistant. I can help you with factual information about our core schemes.")
st.warning("Facts-only. No investment advice.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Suggestion chips (Example Questions)
st.markdown("### Suggested Questions")
cols = st.columns(3)
selected_query = None
if cols[0].button("SBI Bluechip Expense Ratio"):
    selected_query = "What is the expense ratio of SBI Bluechip Fund?"
elif cols[1].button("ELSS Lock-in period"):
    selected_query = "What is the lock-in period for SBI Long Term Equity (ELSS)?"
elif cols[2].button("Small Cap Risk"):
    selected_query = "What is the risk category of SBI Small Cap Fund?"

user_input = st.chat_input("Ask about SBI Mutual Funds...")
if selected_query:
    user_input = selected_query

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call FastAPI backend
    try:
        response = requests.post("http://localhost:8000/ask", json={"query": user_input})
        data = response.json()
        
        answer = data["answer"]
        sources = "\n\n**Sources:**\n" + "\n".join([f"- {s}" for s in data["sources"]])
        timestamp = f"\n\n*Last updated from sources: {data['last_updated']}*"
        
        full_response = answer + sources + timestamp
        
        with st.chat_message("assistant"):
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
