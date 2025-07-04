import streamlit as st
import openai
import os

# -------------------- Page Configuration --------------------
st.set_page_config(page_title="Mind2Market Group LLC Chat", page_icon="🤖", layout="centered")

# -------------------- Styling & Fonts --------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background-color: #f9f9f9;
    }

    .main-title {
        font-size: 2.2em;
        font-weight: 600;
        color: #202124;
        margin-top: 1em;
        text-align: center;
    }

    .message {
        padding: 1em;
        margin-bottom: 1em;
        border-radius: 12px;
        max-width: 90%;
        word-wrap: break-word;
    }

    .user {
        background-color: #dcfce7;
        align-self: flex-end;
        text-align: right;
    }

    .assistant {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        align-self: flex-start;
        text-align: left;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
    }

    .card {
        background-color: white;
        padding: 1.5em;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-top: 1.5em;
    }

    input:focus {
        border-color: #4285f4 !important;
        box-shadow: 0 0 0 0.2rem rgba(66, 133, 244, 0.25) !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- Logo & Title --------------------
st.image("Assets/logo.png", width=180)
st.markdown('<div class="main-title">What can I assist you with today?</div>', unsafe_allow_html=True)

# -------------------- Load Website Data --------------------
try:
    with open("mind2market_data.txt", "r", encoding="utf-8") as f:
        website_data = f.read()
except FileNotFoundError:
    st.error("❌ The file 'mind2market_data.txt' was not found in the app directory.")
    st.stop()

# -------------------- Load OpenAI API Key --------------------
api_key = None
try:
    api_key = st.secrets.get("OPENAI_API_KEY")
except Exception:
    pass

if not api_key:
    api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI API key not found. Please set it in `.streamlit/secrets.toml` or as an environment variable.")
    st.stop()

openai.api_key = api_key

# -------------------- Initialize Chat State --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- Display Chat History --------------------
for role, message in st.session_state.chat_history:
    st.markdown(
        f'<div class="message {role}">{message}</div>',
        unsafe_allow_html=True
    )

# -------------------- Chat Input Form --------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message", placeholder="Ask something about Mind2Market Group LLC...", label_visibility="collapsed")
    submit = st.form_submit_button("Send")

# -------------------- Chat Response --------------------
if submit and user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Thinking..."):
        prompt = f"""
You are a helpful and knowledgeable assistant for the Mind2Market Group LLC website.
Answer the user's question using the website content below. Be clear, concise, and helpful.

Website content:
\"\"\"
{website_data}
\"\"\"

User question: {user_input}
Answer:
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            answer = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            answer = f"❌ Error: {str(e)}"

    st.session_state.chat_history.append(("assistant", answer))
    st.rerun()
