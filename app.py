import streamlit as st

st.set_page_config(page_title="Zenova SRP", layout="wide")

# Sidebar Login
st.sidebar.title("Zenova SRP Login")
user_role = st.sidebar.selectbox("Login as", ["OEM", "Supplier"])

st.sidebar.success(f"Logged in as {user_role}")

# Tabs
tabs = st.tabs(["Chat", "File Upload", "Project Timeline", "Assets", "Audits"])

with tabs[0]:
    st.subheader("🔁 Inter-company Chat")
    st.info("This is where encrypted messaging and chat features will go.")
    message = st.text_input("Type a message")
    if message:
        st.write(f"**{user_role}** says: {message}")

with tabs[1]:
    st.subheader("📁 File Upload & Preview")
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "xlsx"])
    if uploaded_file:
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
