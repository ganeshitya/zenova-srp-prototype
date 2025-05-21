import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.express as px
import numpy as np # For random choices in dummy data

# --- App Configuration ---
st.set_page_config(page_title="Zenova SRP", layout="wide", initial_sidebar_state="expanded")

# --- File Paths & Directory Setup ---
DATA_DIR = "data"
CHAT_FILE = os.path.join(DATA_DIR, "chat_history.csv")
FILES_FILE = os.path.join(DATA_DIR, "uploaded_files.csv")
PROJECTS_FILE = os.path.join(DATA_DIR, "project_tasks.csv")
ASSETS_FILE = os.path.join(DATA_DIR, "assets.csv")
AUDITS_FILE = os.path.join(DATA_DIR, "audit_points.csv")
SUPPLIER_RECORDS_DIR = os.path.join(DATA_DIR, "supplier_records")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SUPPLIER_RECORDS_DIR, exist_ok=True)

# --- Helper Functions for Data Handling ---
def initialize_csv(file_path, columns):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

def create_dummy_data(file_path, columns, data_type, user_roles):
    """Generates dummy data if the CSV is empty."""
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return # File already has data

    st.info(f"Creating dummy data for {os.path.basename(file_path)}...")

    if data_type == "chat":
        dummy_entries = [
            {"role": "OEM", "message": "Welcome to Zenova SRP!", "timestamp": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")},
            {"role": "Supplier A", "message": "Good morning OEM, checking in on the latest project updates.", "timestamp": (datetime.now() - timedelta(days=4, hours=2)).strftime("%Y-%m-%d %H:%M:%S")},
            {"role": "OEM", "message": "Project Alpha is progressing well. Task #TA-001 is awaiting your input.", "timestamp": (datetime.now() - timedelta(days=3, hours=5)).strftime("%Y-%m-%d %H:%M:%S")},
            {"role": "Supplier B", "message": "Asset AC-003 is due for calibration next week. Noted.", "timestamp": (datetime.now() - timedelta(days=2, hours=10)).strftime("%Y-%m-%d %H:%M:%S")},
            {"role": "Auditor", "message": "Initial audit for Q1 findings have been uploaded to file management.", "timestamp": (datetime.now() - timedelta(days=1, hours=1)).strftime("%Y-%m-%d %H:%M:%S")},
        ]
    elif data_type == "project":
        project_statuses = ["Open", "Work In Progress", "Blocked", "Pending Review", "Closed"]
        dummy_entries = []
        for i in range(1, 16):
            status = np.random.choice(project_statuses, p=[0.3, 0.4, 0.1, 0.1, 0.1])
            assigned_to = np.random.choice(user_roles + ["Unassigned"])
            due_date = (datetime.today() + timedelta(days=np.random.randint(-10, 30))).strftime("%Y-%m-%d")
            input_pending = "Yes" if np.random.rand() < 0.2 and status == "Open" else "No" # 20% chance of pending input for open tasks
            dummy_entries.append({
                "task_id": f"TA-{i:03d}",
                "task_name": f"Project Task {i}: " + np.random.choice(["Review designs", "Procure materials", "Assembly line setup", "Quality check", "Logistics coordination", "Documentation"]),
                "status": status,
                "assigned_to": assigned_to,
                "due_date": due_date,
                "description": f"Details for task {i}.",
                "input_pending": input_pending # New column
            })
    elif data_type == "asset":
        asset_statuses = ["In Use", "In Storage", "Under Maintenance", "Awaiting Calibration", "End of Life (EOL)", "Scrapped"]
        asset_locations = ["OEM Site", "Supplier A Facility", "Supplier B Warehouse", "In Transit"]
        suppliers = ["Supplier A", "Supplier B"] # Explicit suppliers for parts tracking
        dummy_entries = []
        for i in range(1, 21):
            supplier = np.random.choice(suppliers)
            eol_date = (datetime.today() + timedelta(days=np.random.randint(30, 365 * 3))).strftime("%Y-%m-%d") if np.random.rand() > 0.3 else None
            calibration_date = (datetime.today() + timedelta(days=np.random.randint(15, 180))).strftime("%Y-%m-%d") if np.random.rand() > 0.4 else None
            dummy_entries.append({
                "asset_id": f"AC-{i:03d}",
                "asset_name": np.random.choice(["CNC Machine", "3D Printer", "Assembly Robot", "Inspection Jig", "Material Handler", "Test Equipment"]),
                "location": np.random.choice(asset_locations),
                "status": np.random.choice(asset_statuses, p=[0.4, 0.2, 0.1, 0.1, 0.1, 0.1]),
                "eol_date": eol_date,
                "calibration_date": calibration_date,
                "notes": f"Asset {i} general notes.",
                "supplier": supplier # New column
            })
    elif data_type == "audit":
        audit_statuses = ["Open", "In Progress", "Resolved", "Pending Verification", "Closed", "Deviation Accepted"]
        assignees = user_roles + ["Cross-functional Team"]
        dummy_entries = []
        for i in range(1, 11):
            status = np.random.choice(audit_statuses, p=[0.3, 0.3, 0.2, 0.1, 0.05, 0.05])
            assignee = np.random.choice(assignees)
            due_date = (datetime.today() + timedelta(days=np.random.randint(-5, 45))).strftime("%Y-%m-%d")
            input_pending = "Yes" if np.random.rand() < 0.2 and status in ["Open", "In Progress"] else "No"
            dummy_entries.append({
                "audit_id": f"AD-{i:03d}",
                "point_description": f"Audit finding {i}: " + np.random.choice(["Non-compliance in safety protocol", "Documentation incomplete", "Calibration record missing", "Supplier quality deviation", "Environmental regulation breach"]),
                "status": status,
                "assignee": assignee,
                "due_date": due_date,
                "resolution": f"Resolution for finding {i}.",
                "input_pending": input_pending # New column
            })
    elif data_type == "files":
        dummy_entries = [
            {"filename": "Zenova_NDA_SupplierA.pdf", "type": "application/pdf", "size": 120000, "uploader": "OEM", "timestamp": (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S"), "path": os.path.join(SUPPLIER_RECORDS_DIR, "Zenova_NDA_SupplierA.pdf")},
            {"filename": "SupplierB_MSA_v2.docx", "type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "size": 85000, "uploader": "Supplier B", "timestamp": (datetime.now() - timedelta(days=18)).strftime("%Y-%m-%d %H:%M:%S"), "path": os.path.join(SUPPLIER_RECORDS_DIR, "SupplierB_MSA_v2.docx")},
            {"filename": "Q1_Audit_Summary_Report.xlsx", "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "size": 250000, "uploader": "Auditor", "timestamp": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S"), "path": os.path.join(DATA_DIR, "Q1_Audit_Summary_Report.xlsx")},
            {"filename": "Project_Alpha_Requirements.pdf", "type": "application/pdf", "size": 150000, "uploader": "OEM", "timestamp": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"), "path": os.path.join(DATA_DIR, "Project_Alpha_Requirements.pdf")},
            {"filename": "Asset_Calibration_Schedule.xlsx", "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "size": 90000, "uploader": "OEM", "timestamp": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"), "path": os.path.join(DATA_DIR, "Asset_Calibration_Schedule.xlsx")},
        ]
        # Create dummy files for demonstration (optional, as we just list them in CSV)
        for entry in dummy_entries:
            dummy_file_path = entry['path']
            os.makedirs(os.path.dirname(dummy_file_path), exist_ok=True)
            if not os.path.exists(dummy_file_path):
                with open(dummy_file_path, 'w') as f:
                    f.write(f"This is a dummy file for {entry['filename']}.")
                st.info(f"Created dummy file: {entry['filename']}")
    else:
        dummy_entries = [] # Fallback for unknown data_type

    if dummy_entries:
        pd.DataFrame(dummy_entries, columns=columns).to_csv(file_path, index=False)


def load_data(file_path, columns=None, data_type=None, user_roles=None):
    """Loads data, creating dummy data if the file is empty."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        create_dummy_data(file_path, columns, data_type, user_roles)

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            df = pd.read_csv(file_path)
            # Ensure columns are present, add if missing (e.g., new columns from updates)
            if columns:
                for col in columns:
                    if col not in df.columns:
                        df[col] = None # Add missing columns with None or default
            return df
        except pd.errors.EmptyDataError:
            if columns:
                return pd.DataFrame(columns=columns)
            return pd.DataFrame()
    elif columns:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame()

def append_data(file_path, new_entry_df):
    """Appends data to a CSV, ensuring all columns match."""
    # Load existing data to get correct column order
    df_existing = load_data(file_path, columns=new_entry_df.columns.tolist())
    # Ensure new_entry_df has all columns present in df_existing, filling missing with NaN
    # And ensure df_existing has all columns present in new_entry_df
    all_columns = list(set(df_existing.columns).union(set(new_entry_df.columns)))
    df_existing = df_existing.reindex(columns=all_columns)
    new_entry_df = new_entry_df.reindex(columns=all_columns)

    df = pd.concat([df_existing, new_entry_df], ignore_index=True)
    df.to_csv(file_path, index=False)

# --- Initialize CSV Files and Load Dummy Data ---
user_roles_list = ["OEM", "Supplier A", "Supplier B", "Auditor"] # Define here to pass to dummy data creator

initialize_csv(CHAT_FILE, ["role", "message", "timestamp"])
initialize_csv(FILES_FILE, ["filename", "type", "size", "uploader", "timestamp", "path"]) # Added 'path' for file storage
initialize_csv(PROJECTS_FILE, ["task_id", "task_name", "status", "assigned_to", "due_date", "description", "input_pending"]) # Added 'input_pending'
initialize_csv(ASSETS_FILE, ["asset_id", "asset_name", "location", "status", "eol_date", "calibration_date", "notes", "supplier"]) # Added 'supplier'
initialize_csv(AUDITS_FILE, ["audit_id", "point_description", "status", "assignee", "due_date", "resolution", "input_pending"]) # Added 'input_pending'

# Load dummy data into CSVs if they are empty
load_data(CHAT_FILE, columns=["role", "message", "timestamp"], data_type="chat", user_roles=user_roles_list)
load_data(FILES_FILE, columns=["filename", "type", "size", "uploader", "timestamp", "path"], data_type="files", user_roles=user_roles_list)
load_data(PROJECTS_FILE, columns=["task_id", "task_name", "status", "assigned_to", "due_date", "description", "input_pending"], data_type="project", user_roles=user_roles_list)
load_data(ASSETS_FILE, columns=["asset_id", "asset_name", "location", "status", "eol_date", "calibration_date", "notes", "supplier"], data_type="asset", user_roles=user_roles_list)
load_data(AUDITS_FILE, columns=["audit_id", "point_description", "status", "assignee", "due_date", "resolution", "input_pending"], data_type="audit", user_roles=user_roles_list)


# --- Sidebar Login ---
st.sidebar.image("https://www.zenovagroup.com/wp-content/uploads/2023/10/logo.svg", width=200) # Placeholder for Zenova logo
st.sidebar.title("Zenova SRP Login")
user_roles = ["OEM", "Supplier A", "Supplier B", "Auditor"] # Expanded roles for better simulation
user_role = st.sidebar.selectbox("Login as", user_roles, key="user_role_select")
st.sidebar.success(f"Logged in as {user_role}")
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Zenova SRP** - #1 Supplier Resource Planning tool for OEM's.")


# --- Initialize Streamlit Session State (Global Scope) ---
if "chat_history" not in st.session_state:
    chat_df = load_data(CHAT_FILE, columns=["role", "message", "timestamp"])
    st.session_state.chat_history = chat_df.to_dict(orient="records")

# --- Main Application Tabs ---
tab_titles = [
    "📊 OEM Dashboard", # New Dashboard Tab
    "💬 Chat",
    "📁 File Management",
    "📅 Project Management",
    "🛠️ Asset Management",
    "📋 Audit Management"
]
tabs = st.tabs(tab_titles)

# --- OEM Dashboard Module (NEW) ---
with tabs[0]:
    if user_role != "OEM":
        st.warning("You must be logged in as 'OEM' to view this dashboard.")
    else:
        st.subheader("📊 OEM Performance Dashboard")
        st.markdown("Monitor key performance indicators across suppliers and projects.")

        # Load all relevant data for the dashboard
        projects_df = load_data(PROJECTS_FILE, columns=["task_id", "task_name", "status", "assigned_to", "due_date", "input_pending"])
        assets_df = load_data(ASSETS_FILE, columns=["asset_id", "asset_name", "location", "status", "supplier"])
        audits_df = load_data(AUDITS_FILE, columns=["audit_id", "point_description", "status", "assignee", "due_date", "input_pending"])

        st.markdown("---")
        st.write("### Supplier Performance Metrics")
        if not assets_df.empty:
            st.write("#### Number of Parts/Assets with Each Supplier")
            parts_by_supplier = assets_df.groupby('supplier').size().reset_index(name='Number of Parts')
            fig_parts = px.bar(parts_by_supplier, x='supplier', y='Number of Parts',
                               title='Assets Managed by Each Supplier', color='supplier')
            st.plotly_chart(fig_parts, use_container_width=True)
        else:
            st.info("No asset data to show supplier parts breakdown.")

        st.markdown("---")
        st.write("### Operational Status Overview")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("#### Project Task Status")
            if not projects_df.empty:
                task_status_counts = projects_df['status'].value_counts().reset_index()
                task_status_counts.columns = ['Status', 'Count']
                fig_tasks = px.pie(task_status_counts, values='Count', names='Status',
                                   title='Project Task Distribution')
                st.plotly_chart(fig_tasks, use_container_width=True)
            else:
                st.info("No project task data.")

        with col2:
            st.write("#### Asset Status")
            if not assets_df.empty:
                asset_status_counts = assets_df['status'].value_counts().reset_index()
                asset_status_counts.columns = ['Status', 'Count']
                fig_assets = px.pie(asset_status_counts, values='Count', names='Status',
                                    title='Asset Status Distribution')
                st.plotly_chart(fig_assets, use_container_width=True)
            else:
                st.info("No asset data.")

        with col3:
            st.write("#### Audit Point Status")
            if not audits_df.empty:
                audit_status_counts = audits_df['status'].value_counts().reset_index()
                audit_status_counts.columns = ['Status', 'Count']
                fig_audits = px.pie(audit_status_counts, values='Count', names='Status',
                                    title='Audit Point Distribution')
                st.plotly_chart(fig_audits, use_container_width=True)
            else:
                st.info("No audit data.")

        st.markdown("---")
        st.write("### Performance Metrics")
        col4, col5 = st.columns(2)

        with col4:
            st.write("#### Average Time to Deliver (Remaining Days for Open/WIP Tasks)")
            if not projects_df.empty:
                # Convert due_date to datetime objects
                projects_df['due_date'] = pd.to_datetime(projects_df['due_date'])
                # Filter for open or work in progress tasks
                active_tasks = projects_df[projects_df['status'].isin(["Open", "Work In Progress", "Pending Review"])]
                if not active_tasks.empty:
                    # Calculate remaining days (only for future dates)
                    active_tasks['days_remaining'] = (active_tasks['due_date'] - datetime.today()).dt.days
                    positive_days_remaining = active_tasks[active_tasks['days_remaining'] >= 0]
                    if not positive_days_remaining.empty:
                        avg_days = positive_days_remaining['days_remaining'].mean()
                        st.metric(label="Avg. Days to Deliver (Active Tasks)", value=f"{avg_days:.1f} days")
                    else:
                        st.info("All active tasks are past their due date or have no due date.")
                else:
                    st.info("No active tasks to calculate average time to deliver.")
            else:
                st.info("No project data to calculate time to deliver.")

        with col5:
            st.write("#### Inputs Pending")
            total_pending_input = 0
            if not projects_df.empty:
                project_inputs_pending = projects_df[projects_df['input_pending'] == "Yes"].shape[0]
                total_pending_input += project_inputs_pending
                st.markdown(f"- **Project Tasks:** {project_inputs_pending} pending input")

            if not audits_df.empty:
                audit_inputs_pending = audits_df[audits_df['input_pending'] == "Yes"].shape[0]
                total_pending_input += audit_inputs_pending
                st.markdown(f"- **Audit Points:** {audit_inputs_pending} pending input")

            if projects_df.empty and audits_df.empty:
                st.info("No project or audit data to check for pending inputs.")
            elif total_pending_input == 0:
                st.success("🎉 No inputs are currently pending!")
            st.metric(label="Total Pending Inputs", value=f"{total_pending_input}")


# --- Chat Module ---
with tabs[1]:
    st.subheader("🔁 Inter-Company Communication Channel")
    st.markdown("Features: Inter-company communication with Privacy Protection, Encrypted message transfer. *Future: Group chats, email conversion.*")

    # Display chat messages
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
        st.session_state.chat_history.append(new_message) # Update session state directly
        st.rerun()

# --- File Management Module ---
with tabs[2]:
    st.subheader("🔒 Secured File Management & Version Control")
    st.markdown("Features: Encrypted cloud file transfer, Preview (PDF/Office), Permissions, Sharing/Download history. *Future: Version control, Auto-grouping.*")

    # Option to select upload folder
    upload_folder_options = {"General Files": DATA_DIR, "Supplier Records (NDA/MSA)": SUPPLIER_RECORDS_DIR}
    selected_upload_folder_name = st.selectbox("Select Upload Destination:", list(upload_folder_options.keys()))
    selected_upload_folder_path = upload_folder_options[selected_upload_folder_name]

    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "xlsx", "txt", "png", "jpg"], key="file_uploader")

    if uploaded_file:
        # Save the file to the chosen directory
        save_path = os.path.join(selected_upload_folder_path, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        file_details = {
            "filename": uploaded_file.name,
            "type": uploaded_file.type,
            "size": uploaded_file.size,
            "uploader": user_role,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "path": save_path # Store the full path
        }
        append_data(FILES_FILE, pd.DataFrame([file_details]))
        st.success(f"✅ '{uploaded_file.name}' uploaded successfully by {user_role} to '{selected_upload_folder_name}'!")

        # Basic preview for some types
        if uploaded_file.type == "application/pdf":
            st.info("PDF Preview (full preview would require a library like PyMuPDF or pdf2image)")
        elif "image" in uploaded_file.type:
            st.image(uploaded_file, caption=f"Preview of {uploaded_file.name}", use_column_width=True)
        else:
            st.write("Preview not available for this file type in this demo.")
        st.rerun() # Rerun to refresh the file list

    st.markdown("---")
    st.subheader("Uploaded Files History")
    files_df = load_data(FILES_FILE, columns=["filename", "type", "size", "uploader", "timestamp", "path"])
    if not files_df.empty:
        # Display only relevant columns for the table, but keep 'path' for download button
        display_df = files_df.drop(columns=['path'])
        st.dataframe(display_df, use_container_width=True)

        st.markdown("#### Download Files")
        selected_file_name_to_download = st.selectbox("Select a file to download:", files_df['filename'].tolist())
        if selected_file_name_to_download:
            file_to_download_path = files_df[files_df['filename'] == selected_file_name_to_download]['path'].iloc[0]
            if os.path.exists(file_to_download_path):
                with open(file_to_download_path, "rb") as file:
                    btn = st.download_button(
                        label=f"Download {selected_file_name_to_download}",
                        data=file,
                        file_name=selected_file_name_to_download,
                        mime=files_df[files_df['filename'] == selected_file_name_to_download]['type'].iloc[0]
                    )
            else:
                st.warning(f"File not found: {file_to_download_path}. It might be a dummy entry without a physical file.")
    else:
        st.info("No files uploaded yet.")

# --- Project Management Module (Gantt) ---
with tabs[3]:
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
            input_pending_status = st.checkbox("Requires Input?", value=False) # New input
            submitted = st.form_submit_button("Add Task")

            if submitted and task_name:
                new_task = {
                    "task_id": task_id,
                    "task_name": task_name,
                    "status": status,
                    "assigned_to": assigned_to,
                    "due_date": due_date.strftime("%Y-%m-%d"),
                    "description": description,
                    "input_pending": "Yes" if input_pending_status else "No" # Store as 'Yes'/'No'
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
with tabs[4]:
    st.subheader("🔧 Inter-Company Asset Management")
    st.markdown("Features: Log of assets, Manage EOL/Calibration, Assess inventory/scrap cost, Audit framework. *Future: Auto asset numbering, Cost analysis.*")

    with st.expander("Add New Asset", expanded=False):
        with st.form("new_asset_form", clear_on_submit=True):
            asset_id_val = st.text_input("Asset ID (e.g., ZNV-TOOL-001)", key="asset_id_input")
            asset_name = st.text_input("Asset Name/Description")
            location = st.selectbox("Location", ["OEM Site", "Supplier A Facility", "Supplier B Warehouse", "In Transit"])
            asset_status_options = ["In Use", "In Storage", "Under Maintenance", "Awaiting Calibration", "End of Life (EOL)", "Scrapped"]
            asset_status = st.selectbox("Status", asset_status_options)
            asset_supplier = st.selectbox("Supplier", user_roles_list) # New input for supplier
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
                    "notes": notes,
                    "supplier": asset_supplier # Store supplier
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
with tabs[5]: # Updated tab index
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
            input_pending_audit = st.checkbox("Requires Input from Stakeholders?", value=False) # New input
            audit_submitted = st.form_submit_button("Add Audit Point")

            if audit_submitted and point_description:
                new_audit_point = {
                    "audit_id": audit_id_val,
                    "point_description": point_description,
                    "status": audit_status,
                    "assignee": assignee,
                    "due_date": due_date_audit.strftime("%Y-%m-%d"),
                    "resolution": resolution,
                    "input_pending": "Yes" if input_pending_audit else "No" # Store as 'Yes'/'No'
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
