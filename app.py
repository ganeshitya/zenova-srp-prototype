import streamlit as st
import pandas as pd
import os
from datetime import datetime

# App config
st.set_page_config(page_title="Zenova SRP", layout="wide")

# Paths
CHAT_FILE = "data/chat_history.csv"
os.makedirs("data", exist_ok=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load chat history or create file if not present
def load_chat():
    if os.path.exists(CHAT_FILE):
        return pd.read_csv(CHAT_FILE)
    else:
        df = pd.DataFrame(columns=["role", "message", "timestamp"])
        df.to_csv(CHAT_FILE, index=False)
        return df

# Append message to CSV
def append_message(role, message):
    df = load_chat()
    new_row = pd.DataFrame([[role, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                           columns=["role", "message", "timestamp"])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CHAT_FILE, index=False)

# Sidebar login
st.sidebar.title("Zenova SRP Login")
user_role = st.sidebar.selectbox("Login as", ["OEM", "Supplier"])
st.sidebar.success(f"Logged in as {user_role}")

# Main tabs
tabs = st.tabs(["Chat", "File Upload", "Project Timeline", "Assets", "Audits"])

# ---- CHAT MODULE ----
with tabs[0]:
    st.subheader("🔁 OEM ↔ Supplier Chat")
    
    chat_df = load_chat()
    for i, row in chat_df.iterrows():
        align = "right" if row["role"] == user_role else "left"
        color = "blue" if row["role"] == user_role else "green"
        st.markdown(
            f"<div style='text-align:{align}; color:{color}; margin-bottom:10px;'><strong>{row['role']}:</strong> {row['message']} <br><small>{row['timestamp']}</small></div>",
            unsafe_allow_html=True,
        )

    message = st.text_input("Type your message", key="chat_input")

    if st.button("Send"):
        if message.strip():
            append_message(user_role, message)
            st.session_state.chat_input = ""  # Clear input
            st.experimental_set_query_params(updated=datetime.now().timestamp())  # Trigger refresh

# ---- FILE UPLOAD ----
with tabs[1]:
    st.subheader("📁 File Upload & Preview")
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "xlsx"])
    if uploaded_file:
        file_details = {
            "filename": uploaded_file.name,
            "type": uploaded_file.type,
            "size": uploaded_file.size
        }
        st.write(file_details)
        st.success(f"{uploaded_file.name} uploaded successfully!")

# ---- PROJECT TIMELINE ----
with tabs[2]:
    st.subheader("📅 Project Timeline (Gantt Placeholder)")
    st.info("Gantt charts and task tracking will be visualized here.")

# ---- ASSET MANAGEMENT ----
with tabs[3]:
    st.subheader("🛠 Asset Management")
    st.info("Track assets, EOL, and calibration data.")

# ---- AUDITS ----
with tabs[4]:
    st.subheader("📋 Supplier Assessment & Audits")
    st.info("Audit records, deviations, and third-party scores.")
