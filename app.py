import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.express as px
import numpy as np

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
SUPPLIER_DUMMY_DATA_FILE = os.path.join(DATA_DIR, "supplier_dummy_data.csv")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SUPPLIER_RECORDS_DIR, exist_ok=True)

# --- Helper Functions for Data Handling ---
def initialize_csv(file_path, columns):
    """Initializes a CSV file with headers if it doesn't exist or is empty."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

def load_data(file_path, columns=None):
    """Loads data from a CSV file. Returns an empty DataFrame if file is empty or not found."""
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
            # File exists but is empty
            if columns:
                return pd.DataFrame(columns=columns)
            return pd.DataFrame()
    else:
        # File does not exist or is empty (handled by initialize_csv)
        if columns:
            return pd.DataFrame(columns=columns)
        return pd.DataFrame()

def append_data(file_path, new_entry_df):
    """Appends data to a CSV, ensuring all columns match."""
    df_existing = load_data(file_path, columns=new_entry_df.columns.tolist())
    all_columns = list(set(df_existing.columns).union(set(new_entry_df.columns)))
    df_existing = df_existing.reindex(columns=all_columns)
    new_entry_df = new_entry_df.reindex(columns=all_columns)

    df = pd.concat([df_existing, new_entry_df], ignore_index=True)
    df.to_csv(file_path, index=False)

# --- Initialize CSV Files (without dummy data generation here) ---
user_roles_list = ["OEM", "Auditor"] # Removed Supplier A/B from generic roles as suppliers now come from supplier_dummy_data.csv

initialize_csv(CHAT_FILE, ["role", "message", "timestamp"])
initialize_csv(FILES_FILE, ["filename", "type", "size", "uploader", "timestamp", "path"])
initialize_csv(PROJECTS_FILE, ["task_id", "task_name", "status", "assigned_to", "due_date", "description", "input_pending"])
initialize_csv(ASSETS_FILE, ["asset_id", "asset_name", "location", "status", "eol_date", "calibration_date", "notes", "supplier"])
initialize_csv(AUDITS_FILE, ["audit_id", "point_description", "status", "assignee", "due_date", "resolution", "input_pending"])

# UPDATED SUPPLIER DUMMY DATA COLUMNS
supplier_columns = [
    "supplier_id", "supplier_name", "contact_person", "email", "phone",
    "agreement_status", "last_audit_score", "notes",
    "primary_product_category", "on_time_delivery_rate", "quality_reject_rate",
    "risk_level", "certification", "annual_spend_usd", "last_performance_review_date"
]
initialize_csv(SUPPLIER_DUMMY_DATA_FILE, supplier_columns)


# --- Sidebar Login ---
st.sidebar.image("https://www.zenovagroup.com/wp-content/uploads/2023/10/logo.svg", width=200)
st.sidebar.title("Zenova SRP Login")
user_roles = ["OEM", "Supplier A", "Supplier B", "Auditor"] # Keep for login
user_role = st.sidebar.selectbox("Login as", user_roles, key="user_role_select")
st.sidebar.success(f"Logged in as {user_role}")
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Zenova SRP** - #1 Supplier Resource Planning tool for OEM's.")


# --- Initialize Streamlit Session State (Global Scope) ---
chat_df = load_data(CHAT_FILE, columns=["role", "message", "timestamp"])
if "chat_history" not in st.session_state:
    st.session_state.chat_history = chat_df.to_dict(orient="records")


# --- Main Application Tabs ---
tab_titles = [
    "📊 OEM Dashboard",
    "💬 Chat",
    "📁 File Management",
    "📅 Project Management",
    "🛠️ Asset Management",
    "📋 Audit Management",
    "👥 Supplier Records"
]
tabs = st.tabs(tab_titles)

# --- OEM Dashboard Module ---
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
        supplier_df = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=supplier_columns)


        st.markdown("---")
        st.write("### Supplier Performance & Financial Overview")

        # Row for agreement status and audit score distribution
        col_sup1, col_sup2 = st.columns(2)

        with col_sup1:
            st.write("#### Supplier Agreement Status")
            if not supplier_df.empty and 'agreement_status' in supplier_df.columns:
                supplier_df['agreement_status'] = supplier_df['agreement_status'].fillna('Unknown').astype(str)
                status_counts = supplier_df['agreement_status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                fig_status = px.pie(status_counts, values='Count', names='Status',
                                    title='Distribution of Supplier Agreement Status')
                st.plotly_chart(fig_status, use_container_width=True)
            else:
                st.info("No supplier data to show agreement status.")

        with col_sup2:
            st.write("#### Last Audit Score Distribution")
            if not supplier_df.empty and 'last_audit_score' in supplier_df.columns:
                fig_audit_dist = px.histogram(supplier_df, x='last_audit_score', nbins=10,
                                             title='Distribution of Last Audit Scores',
                                             labels={'last_audit_score': 'Audit Score'})
                st.plotly_chart(fig_audit_dist, use_container_width=True)
            else:
                st.info("No supplier data to show audit score distribution.")

        st.markdown("---")
        col_performance1, col_performance2 = st.columns(2)
        with col_performance1:
            st.write("#### Average On-Time Delivery Rate (%)")
            if not supplier_df.empty and 'on_time_delivery_rate' in supplier_df.columns:
                avg_delivery = supplier_df['on_time_delivery_rate'].mean()
                st.metric(label="Average OTD Rate", value=f"{avg_delivery:.1f}%")
                fig_otd = px.box(supplier_df, y='on_time_delivery_rate', title='On-Time Delivery Rate Distribution')
                st.plotly_chart(fig_otd, use_container_width=True)
            else:
                st.info("No on-time delivery data available.")

        with col_performance2:
            st.write("#### Average Quality Reject Rate (%)")
            if not supplier_df.empty and 'quality_reject_rate' in supplier_df.columns:
                avg_reject = supplier_df['quality_reject_rate'].mean()
                st.metric(label="Average Reject Rate", value=f"{avg_reject:.2f}%")
                fig_reject = px.box(supplier_df, y='quality_reject_rate', title='Quality Reject Rate Distribution')
                st.plotly_chart(fig_reject, use_container_width=True)
            else:
                st.info("No quality reject rate data available.")

        st.markdown("---")
        col_risk_spend = st.columns(2)
        with col_risk_spend[0]:
            st.write("#### Supplier Risk Level Distribution")
            if not supplier_df.empty and 'risk_level' in supplier_df.columns:
                risk_counts = supplier_df['risk_level'].value_counts().reset_index()
                risk_counts.columns = ['Risk Level', 'Count']
                fig_risk = px.pie(risk_counts, values='Count', names='Risk Level',
                                  title='Distribution of Supplier Risk Levels',
                                  color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'})
                st.plotly_chart(fig_risk, use_container_width=True)
            else:
                st.info("No supplier risk level data.")

        with col_risk_spend[1]:
            st.write("#### Annual Spend by Primary Product Category")
            if not supplier_df.empty and 'annual_spend_usd' in supplier_df.columns and 'primary_product_category' in supplier_df.columns:
                spend_by_category = supplier_df.groupby('primary_product_category')['annual_spend_usd'].sum().reset_index()
                spend_by_category = spend_by_category.sort_values(by='annual_spend_usd', ascending=False)
                fig_spend = px.bar(spend_by_category, x='primary_product_category', y='annual_spend_usd',
                                   title='Total Annual Spend by Product Category (USD)',
                                   labels={'primary_product_category': 'Product Category', 'annual_spend_usd': 'Annual Spend (USD)'})
                st.plotly_chart(fig_spend, use_container_width=True)
            else:
                st.info("No annual spend or product category data.")

        st.markdown("---")
        st.write("#### Top 10 Suppliers by Annual Spend")
        if not supplier_df.empty and 'annual_spend_usd' in supplier_df.columns:
            top_spend_suppliers = supplier_df.sort_values(by='annual_spend_usd', ascending=False).head(10)
            st.dataframe(top_spend_suppliers[['supplier_name', 'annual_spend_usd', 'primary_product_category']], use_container_width=True)
        else:
            st.info("No supplier spend data to show top suppliers.")

        st.markdown("---")
        col_audit1, col_audit2 = st.columns(2)
        with col_audit1:
            st.write("#### Top 10 Suppliers by Audit Score")
            if not supplier_df.empty and 'last_audit_score' in supplier_df.columns:
                top_suppliers = supplier_df.sort_values(by='last_audit_score', ascending=False).head(10)
                st.dataframe(top_suppliers[['supplier_name', 'last_audit_score']], use_container_width=True)
            else:
                st.info("No supplier data to show top suppliers.")

        with col_audit2:
            st.write("#### Bottom 10 Suppliers by Audit Score")
            if not supplier_df.empty and 'last_audit_score' in supplier_df.columns:
                bottom_suppliers = supplier_df.sort_values(by='last_audit_score', ascending=True).head(10)
                st.dataframe(bottom_suppliers[['supplier_name', 'last_audit_score']], use_container_width=True)
            else:
                st.info("No supplier data to show bottom suppliers.")

        st.markdown("---")
        st.write("#### Suppliers with Agreements Due for Renewal or Overdue Performance Reviews")
        if not supplier_df.empty:
            pending_renewal = supplier_df[supplier_df['agreement_status'] == 'Pending Renewal']
            st.dataframe(pending_renewal[['supplier_name', 'contact_person', 'email', 'agreement_status']], use_container_width=True)

            st.write("##### Suppliers with Overdue Performance Reviews (Past 1 Year)")
            supplier_df['last_performance_review_date'] = pd.to_datetime(supplier_df['last_performance_review_date'], errors='coerce')
            overdue_reviews = supplier_df[
                (supplier_df['last_performance_review_date'].notna()) &
                (supplier_df['last_performance_review_date'] < (datetime.today() - timedelta(days=365)))
            ]
            if not overdue_reviews.empty:
                st.dataframe(overdue_reviews[['supplier_name', 'contact_person', 'email', 'last_performance_review_date']], use_container_width=True)
            else:
                st.info("No suppliers with overdue performance reviews.")

            if pending_renewal.empty and overdue_reviews.empty:
                 st.info("No suppliers currently pending renewal or with overdue performance reviews.")
        else:
            st.info("No supplier data to check for pending renewals or overdue reviews.")


        st.markdown("---")
        if not assets_df.empty:
            st.write("#### Number of Parts/Assets with Each Supplier")
            assets_df['supplier'] = assets_df['supplier'].fillna('Unassigned').astype(str)
            parts_by_supplier = assets_df.groupby('supplier').size().reset_index(name='Number of Parts')
            fig_parts = px.bar(parts_by_supplier, x='supplier', y='Number of Parts',
                               title='Assets Managed by Each Supplier', color='supplier')
            st.plotly_chart(fig_parts, use_container_width=True)
        else:
            st.info("No asset data to show supplier parts breakdown. Add assets in 'Asset Management' tab.")

        st.markdown("---")
        st.write("### Operational Status Overview")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("#### Project Task Status")
            if not projects_df.empty:
                projects_df['status'] = projects_df['status'].fillna('Unknown').astype(str)
                task_status_counts = projects_df['status'].value_counts().reset_index()
                task_status_counts.columns = ['Status', 'Count']
                fig_tasks = px.pie(task_status_counts, values='Count', names='Status',
                                   title='Project Task Distribution')
                st.plotly_chart(fig_tasks, use_container_width=True)
            else:
                st.info("No project task data. Add tasks in 'Project Management' tab.")

        with col2:
            st.write("#### Asset Status")
            if not assets_df.empty:
                assets_df['status'] = assets_df['status'].fillna('Unknown').astype(str)
                asset_status_counts = assets_df['status'].value_counts().reset_index()
                asset_status_counts.columns = ['Status', 'Count']
                fig_assets = px.pie(asset_status_counts, values='Count', names='Status',
                                    title='Asset Status Distribution')
                st.plotly_chart(fig_assets, use_container_width=True)
            else:
                st.info("No asset data. Add assets in 'Asset Management' tab.")

        with col3:
            st.write("#### Audit Point Status")
            if not audits_df.empty:
                audits_df['status'] = audits_df['status'].fillna('Unknown').astype(str)
                audit_status_counts = audits_df['status'].value_counts().reset_index()
                audit_status_counts.columns = ['Status', 'Count']
                fig_audits = px.pie(audit_status_counts, values='Count', names='Status',
                                    title='Audit Point Distribution')
                st.plotly_chart(fig_audits, use_container_width=True)
            else:
                st.info("No audit data. Add audit points in 'Audit Management' tab.")

        st.markdown("---")
        st.write("### Performance Metrics")
        col4, col5 = st.columns(2)

        with col4:
            st.write("#### Average Time to Deliver (Remaining Days for Open/WIP Tasks)")
            if not projects_df.empty:
                projects_df['due_date'] = pd.to_datetime(projects_df['due_date'], errors='coerce')
                active_tasks = projects_df[
                    projects_df['status'].isin(["Open", "Work In Progress", "Pending Review"]) &
                    projects_df['due_date'].notna()
                ].copy()

                if not active_tasks.empty:
                    active_tasks['days_remaining'] = (active_tasks['due_date'] - datetime.today()).dt.days
                    positive_days_remaining = active_tasks[active_tasks['days_remaining'] >= 0]
                    if not positive_days_remaining.empty:
                        avg_days = positive_days_remaining['days_remaining'].mean()
                        st.metric(label="Avg. Days to Deliver (Active Tasks)", value=f"{avg_days:.1f} days")
                    else:
                        st.info("All active tasks are past their due date or have no future due date.")
                else:
                    st.info("No active tasks to calculate average time to deliver.")
            else:
                st.info("No project data to calculate time to deliver.")

        with col5:
            st.write("#### Inputs Pending")
            total_pending_input = 0
            if not projects_df.empty:
                projects_df['input_pending'] = projects_df['input_pending'].fillna('No').astype(str)
                project_inputs_pending = projects_df[projects_df['input_pending'] == "Yes"].shape[0]
                total_pending_input += project_inputs_pending
                st.markdown(f"- **Project Tasks:** {project_inputs_pending} pending input")

            if not audits_df.empty:
                audits_df['input_pending'] = audits_df['input_pending'].fillna('No').astype(str)
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

    for msg_data in st.session_state.chat_history:
        role = str(msg_data.get("role", "Unknown"))
        message_content = str(msg_data.get("message", ""))
        with st.chat_message(name=role, avatar="🧑‍💻" if role == user_role else "🏢"):
            st.write(message_content)

    prompt = st.chat_input("Type your message...")
    if prompt:
        new_message = {"role": user_role, "message": prompt, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        append_data(CHAT_FILE, pd.DataFrame([new_message]))
        st.session_state.chat_history.append(new_message)
        st.rerun()

# --- File Management Module ---
with tabs[2]:
    st.subheader("🔒 Secured File Management & Version Control")
    st.markdown("Features: Encrypted cloud file transfer, Preview (PDF/Office), Permissions, Sharing/Download history. *Future: Version control, Auto-grouping.*")

    upload_folder_options = {"General Files": DATA_DIR, "Supplier Records (NDA/MSA)": SUPPLIER_RECORDS_DIR}
    selected_upload_folder_name = st.selectbox("Select Upload Destination:", list(upload_folder_options.keys()))
    selected_upload_folder_path = upload_folder_options[selected_upload_folder_name]

    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "xlsx", "txt", "png", "jpg"], key="file_uploader")

    if uploaded_file:
        save_path = os.path.join(selected_upload_folder_path, uploaded_file.name)

        try:
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        except TypeError as e:
            st.error(f"Error saving file: {e}. 'save_path' might not be a valid string. Check console for DEBUG messages.")
            st.stop()

        file_details = {
            "filename": uploaded_file.name,
            "type": uploaded_file.type,
            "size": uploaded_file.size,
            "uploader": user_role,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "path": save_path
        }
        append_data(FILES_FILE, pd.DataFrame([file_details]))
        st.success(f"✅ '{uploaded_file.name}' uploaded successfully by {user_role} to '{selected_upload_folder_name}'!")
        if uploaded_file.type == "application/pdf":
            st.info("PDF Preview (full preview would require a library like PyMuPDF or pdf2image)")
        elif "image" in uploaded_file.type:
            st.image(uploaded_file, caption=f"Preview of {uploaded_file.name}", use_column_width=True)
        else:
            st.write("Preview not available for this file type in this demo.")
        st.rerun()

    st.markdown("---")
    st.subheader("Uploaded Files History")
    files_df = load_data(FILES_FILE, columns=["filename", "type", "size", "uploader", "timestamp", "path"])
    if not files_df.empty:
        files_df['path'] = files_df['path'].fillna('').astype(str)
        display_df = files_df.drop(columns=['path'])
        st.dataframe(display_df, use_container_width=True)

        st.markdown("#### Download Files")
        selected_file_name_to_download = st.selectbox("Select a file to download:", files_df['filename'].tolist(), key="download_file_select")
        if selected_file_name_to_download:
            file_to_download_path_series = files_df[files_df['filename'] == selected_file_name_to_download]['path']
            file_to_download_path = file_to_download_path_series.iloc[0] if not file_to_download_path_series.empty else ''

            if not isinstance(file_to_download_path, str):
                st.error(f"Internal error: Download path is not a string. Type: {type(file_to_download_path)}, Value: {file_to_download_path}")
                file_to_download_path = ''

            if file_to_download_path and os.path.exists(file_to_download_path):
                with open(file_to_download_path, "rb") as file:
                    btn = st.download_button(
                        label=f"Download {selected_file_name_to_download}",
                        data=file,
                        file_name=selected_file_name_to_download,
                        mime=files_df[files_df['filename'] == selected_file_name_to_download]['type'].iloc[0]
                    )
            else:
                st.warning(f"File '{selected_file_name_to_download}' not found at path: {file_to_download_path}. It might be a dummy entry without a physical file, or the path is incorrect.")
    else:
        st.info("No files uploaded yet.")

# --- Project Management Module (Gantt) ---
with tabs[3]:
    st.subheader("📊 Project Management Tool with Gantt View")
    st.markdown("Features: Gantt view with milestones, Task dashboard (Open/WIP/Closed), Critical path notifications. *Future: Interactive Gantt, Email reminders.*")

    with st.expander("Add New Project Task", expanded=False):
        with st.form("new_task_form", clear_on_submit=True):
            task_id = f"TASK-{int(datetime.now().timestamp())}"
            task_name = st.text_input("Task Name")
            description = st.text_area("Task Description")
            status_options = ["Open", "Work In Progress", "Blocked", "Pending Review", "Closed"]
            status = st.selectbox("Status", status_options)
            assigned_to = st.selectbox("Assigned To", user_roles + ["Unassigned"])
            due_date = st.date_input("Due Date", min_value=datetime.today())
            input_pending_status = st.checkbox("Requires Input?", value=False)
            submitted = st.form_submit_button("Add Task")

            if submitted and task_name:
                new_task = {
                    "task_id": task_id,
                    "task_name": task_name,
                    "status": status,
                    "assigned_to": assigned_to,
                    "due_date": due_date.strftime("%Y-%m-%d"),
                    "description": description,
                    "input_pending": "Yes" if input_pending_status else "No"
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
        st.info("No project tasks added yet. Add tasks using the 'Add New Project Task' expander above.")

# --- Asset Management Module ---
with tabs[4]:
    st.subheader("🔧 Inter-Company Asset Management")
    st.markdown("Features: Log of assets, Manage EOL/Calibration, Assess inventory/scrap cost, Audit framework. *Future: Auto asset numbering, Cost analysis.*")

    # Load supplier data for the dropdown
    supplier_df_for_selection = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=["supplier_name"])
    supplier_names_for_dropdown = supplier_df_for_selection['supplier_name'].tolist()
    if not supplier_names_for_dropdown:
        supplier_names_for_dropdown = ["N/A (No suppliers found)"] # Fallback if supplier file is empty

    with st.expander("Add New Asset", expanded=False):
        with st.form("new_asset_form", clear_on_submit=True):
            asset_id_val = st.text_input("Asset ID (e.g., ZNV-TOOL-001)", key="asset_id_input")
            asset_name = st.text_input("Asset Name/Description")
            location = st.selectbox("Location", ["OEM Site", "Supplier A Facility", "Supplier B Warehouse", "In Transit"])
            asset_status_options = ["In Use", "In Storage", "Under Maintenance", "Awaiting Calibration", "End of Life (EOL)", "Scrapped"]
            asset_status = st.selectbox("Status", asset_status_options)
            # Use actual supplier names for asset assignment
            asset_supplier = st.selectbox("Supplier", supplier_names_for_dropdown)
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
                    "supplier": asset_supplier
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
        st.info("No assets logged yet. Add assets using the 'Add New Asset' expander above.")

# --- Audit Management Module ---
with tabs[5]:
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
            input_pending_audit = st.checkbox("Requires Input from Stakeholders?", value=False)
            audit_submitted = st.form_submit_button("Add Audit Point")

            if audit_submitted and point_description:
                new_audit_point = {
                    "audit_id": audit_id_val,
                    "point_description": point_description,
                    "status": audit_status,
                    "assignee": assignee,
                    "due_date": due_date_audit.strftime("%Y-%m-%d"),
                    "resolution": resolution,
                    "input_pending": "Yes" if input_pending_audit else "No"
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
        st.info("No audit points recorded yet. Add audit points using the 'Add New Audit Point / Finding' expander above.")

# --- Supplier Records Module ---
with tabs[6]:
    st.subheader("👥 Supplier Records")
    st.markdown("View and manage detailed information about your suppliers.")

    supplier_df = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=supplier_columns)

    if not supplier_df.empty:
        st.dataframe(supplier_df, use_container_width=True)
    else:
        st.info("No supplier records available. Ensure 'supplier_dummy_data.csv' is in your 'data/' folder.")

    st.markdown("---")
    st.write("### Add New Supplier Record")
    with st.expander("Add New Supplier", expanded=False):
        with st.form("new_supplier_form", clear_on_submit=True):
            new_supplier_id = st.text_input("Supplier ID (e.g., SUP-006)")
            new_supplier_name = st.text_input("Supplier Name")
            new_contact_person = st.text_input("Contact Person")
            new_email = st.text_input("Email")
            new_phone = st.text_input("Phone")
            new_agreement_status = st.selectbox("Agreement Status", ["Active", "Pending Renewal", "Terminated", "On Hold"])
            new_last_audit_score = st.number_input("Last Audit Score", min_value=0, max_value=100, value=80, key="new_last_audit_score")
            new_notes = st.text_area("Notes")

            st.markdown("---")
            st.write("#### Additional Details:")
            new_primary_product_category = st.text_input("Primary Product Category (e.g., Raw Materials, Electronics)")
            new_on_time_delivery_rate = st.slider("On-Time Delivery Rate (%)", min_value=0.0, max_value=100.0, value=95.0, step=0.1)
            new_quality_reject_rate = st.slider("Quality Reject Rate (%)", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
            new_risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])
            new_certification = st.text_input("Certifications (comma-separated, e.g., ISO 9001, IATF 16949)")
            new_annual_spend_usd = st.number_input("Annual Spend (USD)", min_value=0, value=100000, step=10000)
            new_last_performance_review_date = st.date_input("Last Performance Review Date", value=None, key="new_last_performance_review_date")

            supplier_submitted = st.form_submit_button("Add Supplier")

            if supplier_submitted and new_supplier_id and new_supplier_name:
                new_supplier_entry = {
                    "supplier_id": new_supplier_id,
                    "supplier_name": new_supplier_name,
                    "contact_person": new_contact_person,
                    "email": new_email,
                    "phone": new_phone,
                    "agreement_status": new_agreement_status,
                    "last_audit_score": new_last_audit_score,
                    "notes": new_notes,
                    "primary_product_category": new_primary_product_category,
                    "on_time_delivery_rate": new_on_time_delivery_rate,
                    "quality_reject_rate": new_quality_reject_rate,
                    "risk_level": new_risk_level,
                    "certification": new_certification,
                    "annual_spend_usd": new_annual_spend_usd,
                    "last_performance_review_date": new_last_performance_review_date.strftime("%Y-%m-%d") if new_last_performance_review_date else None
                }
                append_data(SUPPLIER_DUMMY_DATA_FILE, pd.DataFrame([new_supplier_entry]))
                st.success(f"Supplier '{new_supplier_name}' ({new_supplier_id}) added successfully!")
                st.rerun()
            elif supplier_submitted:
                st.error("Supplier ID and Supplier Name are required.")


st.sidebar.markdown("---")
st.sidebar.info("This is a demo application. Data is stored locally in CSV files in the 'data' directory.")
