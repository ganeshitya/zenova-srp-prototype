import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- App Configuration ---
st.set_page_config(page_title="Zenova SRP", layout="wide", initial_sidebar_state="expanded")

# --- File Paths & Directory Setup ---
DATA_DIR = "data"
CHAT_FILE = os.path.join(DATA_DIR, "chat_history.csv")
FILES_FILE = os.path.join(DATA_DIR, "uploaded_files.csv")
PROJECTS_FILE = os.path.join(DATA_DIR, "project_tasks.csv")
ASSETS_FILE = os.path.join(DATA_DIR, "assets.csv")
AUDITS_FILE = os.path.join(DATA_DIR, "audit_points.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# --- Helper Functions for Data Handling ---
def initialize_csv(file_path, columns):
    if not os.path.exists(file_path):
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

def load_data(file_path, columns=None):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            return pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            if columns:
                return pd.DataFrame(columns=columns)
            return pd.DataFrame()
    elif columns:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame()

def append_data(file_path, new_entry_df):
    df = load_data(file_path, columns=new_entry_df.columns.tolist())
    df = pd.concat([df, new_entry_df], ignore_index=True)
    df.to_csv(file_path, index=False)

# --- Initialize CSV Files ---
initialize_csv(CHAT_FILE, ["role", "message", "timestamp"])
initialize_csv(FILES_FILE, ["filename", "type", "size", "uploader", "timestamp"])
initialize_csv(PROJECTS_FILE, ["task_id", "task_name", "status", "assigned_to", "due_date", "description"])
initialize_csv(ASSETS_FILE, ["asset_id", "asset_name", "location", "status", "eol_date", "calibration_date", "notes"])
initialize_csv(AUDITS_FILE, ["audit_id", "point_description", "status", "assignee", "due_date", "resolution"])

# --- Sidebar Login ---
st.sidebar.image("https://www.zenovagroup.com/wp-content/uploads/2023/10/logo.svg", width=200) # Placeholder for Zenova logo
st.sidebar.title("Zenova SRP Login")
user_roles = ["OEM", "Supplier A", "Supplier B", "Auditor"] # Expanded roles for better simulation
user_role = st.sidebar.selectbox("Login as", user_roles, key="user_role_select")
st.sidebar.success(f"Logged in as {user_role}")
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Zenova SRP** - #1 Supplier Resource Planning tool for OEM's.")

# --- Initialize Streamlit Session State (Global Scope) ---
# It's best practice to initialize session state variables at the beginning of the script
# to ensure they are available on all reruns.
if "chat_history" not in st.session_state:
    chat_df = load_data(CHAT_FILE, columns=["role", "message", "timestamp"])
    st.session_state.chat_history = chat_df.to_dict(orient="records")

# --- Main Application Tabs ---
tab_titles = [
    "💬 Chat",
    "📁 File Management",
    "📅 Project Management",
    "🛠️ Asset Management",
    "📋 Audit Management"
]
tabs = st.tabs(tab_titles)

# --- Chat Module ---
with tabs[0]:
    st.subheader("🔁 Inter-Company Communication Channel")
    st.markdown("Features: Inter-company communication with Privacy Protection, Encrypted message transfer. *Future: Group chats, email conversion.*")

    # Display chat messages (now using the globally initialized session_state)
    for msg_data in st.session_state.chat_history:
        role = str(msg_data.get("role", "Unknown"))
        message_content = str(msg_data.get("message", ""))
        with st.chat_message(name=role, avatar="🧑‍💻" if role == user_role else "🏢"):
            st.write(message_content)

    # Chat input
    prompt = st.chat_input("Type your message...")
    if prompt:
        new_message = {"role": user_role, "message": prompt, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        append_data(CHAT_FILE, pd.DataFrame([new_message]))
        # Update session state directly after appending to file for immediate display
        st.session_state.chat_history.append(new_message)
        st.rerun() # Rerun to display the new message and clear the input

# --- File Management Module ---
with tabs[1]:
    st.subheader("🔒 Secured File Management & Version Control")
    st.markdown("Features: Encrypted cloud file transfer, Preview (PDF/Office), Permissions, Sharing/Download history. *Future: Version control, Auto-grouping.*")

    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "xlsx", "txt", "png", "jpg"], key="file_uploader")

    if uploaded_file:
        file_details = {
            "filename": uploaded_file.name,
            "type": uploaded_file.type,
            "size": uploaded_file.size,
            "uploader": user_role,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        append_data(FILES_FILE, pd.DataFrame([file_details]))
        st.success(f"✅ '{uploaded_file.name}' uploaded successfully by {user_role}!")

        # Basic preview for some types
        if uploaded_file.type == "application/pdf":
            st.info("PDF Preview (first page will require a library like PyMuPDF or pdf2image for full preview)")
        elif "image" in uploaded_file.type:
            st.image(uploaded_file, caption=f"Preview of {uploaded_file.name}", use_column_width=True)
        else:
            st.write("Preview not available for this file type in this demo.")

    st.markdown("---")
    st.subheader("Uploaded Files History")
    files_df = load_data(FILES_FILE, columns=["filename", "type", "size", "uploader", "timestamp"])
    if not files_df.empty:
        st.dataframe(files_df, use_container_width=True)
    else:
        st.info("No files uploaded yet.")

# --- Project Management Module (Gantt) ---
with tabs[2]:
    st.subheader("📊 Project Management Tool with Gantt View")
    st.markdown("Features: Gantt view with milestones, Task dashboard (Open/WIP/Closed), Critical path notifications. *Future: Interactive Gantt, Email reminders.*")

    with st.expander("Add New Project Task", expanded=False):
        with st.form("new_task_form", clear_on_submit=True):
            task_id = f"TASK-{int(datetime.now().timestamp())}" # Simple unique ID
            task_name = st.text_input("Task Name")
            description = st.text_area("Task Description")
            status_options = ["Open", "Work In Progress", "Blocked", "Pending Review", "Closed"]
            status = st.selectbox("Status", status_options)
            assigned_to = st.selectbox("Assigned To", user_roles + ["Unassigned"])
            due_date = st.date_input("Due Date", min_value=datetime.today())
            submitted = st.form_submit_button("Add Task")

            if submitted and task_name:
                new_task = {
                    "task_id": task_id,
                    "task_name": task_name,
                    "status": status,
                    "assigned_to": assigned_to,
                    "due_date": due_date.strftime("%Y-%m-%d"),
                    "description": description
                }
                append_data(PROJECTS_FILE, pd.DataFrame([new_task]))
                st.success(f"Task '{task_name}' added successfully!")
                st.rerun()
            elif submitted:
                st.error("Task Name is required.")

    st.markdown("---")
    st.subheader("Current Project Tasks")
    projects_df = load_data(PROJECTS_FILE)
    if not projects_df.empty:
        st.dataframe(projects_df, use_container_width=True)
        st.info("💡 Tip: A full Gantt chart requires a visualization library like Plotly. This table shows task data.")
    else:
        st.info("No project tasks added yet.")

# --- Asset Management Module ---
with tabs[3]:
    st.subheader("🔧 Inter-Company Asset Management")
    st.markdown("Features: Log of assets, Manage EOL/Calibration, Assess inventory/scrap cost, Audit framework. *Future: Auto asset numbering, Cost analysis.*")

    with st.expander("Add New Asset", expanded=False):
        with st.form("new_asset_form", clear_on_submit=True):
            asset_id_val = st.text_input("Asset ID (e.g., ZNV-TOOL-001)", key="asset_id_input")
            asset_name = st.text_input("Asset Name/Description")
            location = st.selectbox("Location", ["OEM Site", "Supplier A Facility", "Supplier B Warehouse", "In Transit"])
            asset_status_options = ["In Use", "In Storage", "Under Maintenance", "Awaiting Calibration", "End of Life (EOL)", "Scrapped"]
            asset_status = st.selectbox("Status", asset_status_options)
            eol_date = st.date_input("End of Life (EOL) Date", value=None, key="eol_date_asset")
            calibration_date = st.date_input("Next Calibration Date", value=None, key="cal_date_asset")
            notes = st.text_area("Notes/Comments")
            asset_submitted = st.form_submit_button("Add Asset")

            if asset_submitted and asset_id_val and asset_name:
                new_asset = {
                    "asset_id": asset_id_val,
                    "asset_name": asset_name,
                    "location": location,
                    "status": asset_status,
                    "eol_date": eol_date.strftime("%Y-%m-%d") if eol_date else None,
                    "calibration_date": calibration_date.strftime("%Y-%m-%d") if calibration_date else None,
                    "notes": notes
                }
                append_data(ASSETS_FILE, pd.DataFrame([new_asset]))
                st.success(f"Asset '{asset_name}' ({asset_id_val}) added successfully!")
                st.rerun()
            elif asset_submitted:
                st.error("Asset ID and Asset Name are required.")

    st.markdown("---")
    st.subheader("Asset Inventory Log")
    assets_df = load_data(ASSETS_FILE)
    if not assets_df.empty:
        st.dataframe(assets_df, use_container_width=True)
    else:
        st.info("No assets logged yet.")

# --- Audit Management Module ---
with tabs[4]:
    st.subheader("🔍 Supplier Assessment Report & Actions Tracking")
    st.markdown("Features: Assessment management, Tracking open points with reminders, Third-party audit scores access, Deviation management. *Future: Reminder system, Score integration.*")

    with st.expander("Add New Audit Point / Finding", expanded=False):
        with st.form("new_audit_point_form", clear_on_submit=True):
            audit_id_val = f"AUDIT-{int(datetime.now().timestamp())}"
            point_description = st.text_area("Audit Point/Finding Description")
            audit_status_options = ["Open", "In Progress", "Resolved", "Pending Verification", "Closed", "Deviation Accepted"]
            audit_status = st.selectbox("Status", audit_status_options)
            assignee = st.selectbox("Assignee", user_roles + ["Cross-functional Team"])
            due_date_audit = st.date_input("Due Date for Resolution", min_value=datetime.today(), key="due_date_audit")
            resolution = st.text_area("Resolution / Corrective Action")
            audit_submitted = st.form_submit_button("Add Audit Point")

            if audit_submitted and point_description:
                new_audit_point = {
                    "audit_id": audit_id_val,
                    "point_description": point_description,
                    "status": audit_status,
                    "assignee": assignee,
                    "due_date": due_date_audit.strftime("%Y-%m-%d"),
                    "resolution": resolution
                }
                append_data(AUDITS_FILE, pd.DataFrame([new_audit_point]))
                st.success(f"Audit point '{audit_id_val}' added successfully!")
                st.rerun()
            elif audit_submitted:
                st.error("Audit Point Description is required.")

    st.markdown("---")
    st.subheader("Audit Records & Open Points")
    audits_df = load_data(AUDITS_FILE)
    if not audits_df.empty:
        st.dataframe(audits_df, use_container_width=True)
    else:
        st.info("No audit points recorded yet.")

st.sidebar.markdown("---")
st.sidebar.info("This is a demo application. Data is stored locally in CSV files in the 'data' directory.")
