import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Zenova SRP", layout="wide")
if st.session_state.get("just_sent"):
    st.session_state["just_sent"] = False
    st.experimental_rerun()


CHAT_FILE = "data/chat_history.csv"
os.makedirs("data", exist_ok=True)

# Load chat history or create it
if not os.path.exists(CHAT_FILE):
    df = pd.DataFrame(columns=["role", "message", "timestamp"])
    df.to_csv(CHAT_FILE, index=False)

def load_chat():
    return pd.read_csv(CHAT_FILE)

def append_message(role, message):
    df = load_chat()
    new_row = pd.DataFrame([[role, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CHAT_FILE, index=False)

# Sidebar Login
st.sidebar.title("Zenova SRP Login")
user_role = st.sidebar.selectbox("Login as", ["OEM", "Supplier"])

st.sidebar.success(f"Logged in as {user_role}")

# Tabs
tabs = st.tabs(["Chat", "File Upload", "Project Timeline", "Assets", "Audits"])

with tabs[0]:
    st.subheader("🔁 OEM ↔ Supplier Chat")

    chat_df = load_chat()
    for i, row in chat_df.iterrows():
        if row["role"] == user_role:
            st.markdown(f"<div style='text-align:right; color:blue'><strong>{row['role']}:</strong> {row['message']} <br><small>{row['timestamp']}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; color:green'><strong>{row['role']}:</strong> {row['message']} <br><small>{row['timestamp']}</small></div>", unsafe_allow_html=True)

    message = st.text_input("Type your message")
    if st.button("Send"):
        if message.strip():
            append_message(user_role, message)
            st.session_state["just_sent"] = True
            st.experimental_set_query_params(refresh=True)


with tabs[1]:
    st.subheader("📁 File Upload & Preview")
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "xlsx"])
    if uploaded_file:
        file_details = {"filename": uploaded_file.name, "type": uploaded_file.type, "size": uploaded_file.size}
        st.write(file_details)
        st.success(f"{uploaded_file.name} uploaded successfully!")

with tabs[2]:
    st.subheader("📅 Project Timeline (Gantt Placeholder)")
    st.info("Gantt charts and task tracking will be visualized here.")

with tabs[3]:
    st.subheader("🛠 Asset Management")
    st.info("Track assets, EOL, and calibration data.")

with tabs[4]:
    st.subheader("📋 Supplier Assessment & Audits")
    st.info("Audit records, deviations, and third-party scores.")
