
import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.express as px
import numpy as np

# --- App Configuration ---
st.set_page_config(page_title="Zenova SRP", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Professional Look (Dark Mode, Google-inspired with horizontal tabs) ---
st.markdown("""
<style>
    /* Import Google Fonts - Roboto for general text */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    /* General Body and Text Styling for Dark Mode */
    body {
        font-family: 'Roboto', sans-serif;
        color: #E0E0E0; /* Light grey text for readability on dark background */
        background-color: #121212; /* Very dark grey background */
    }

    /* Streamlit Main Container Padding */
    .main .block-container {
        padding-top: 1rem; /* Reduced top padding for header */
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 2rem;
    }

    /* Sidebar Styling */
    .stSidebar {
        background-color: #1E1E1E; /* Darker grey for sidebar background */
        border-right: 1px solid #333333; /* Subtle darker border */
        padding-top: 1rem;
    }
    .stSidebar .stSelectbox > label {
        font-weight: 600;
        color: #A0A0A0; /* Lighter grey for labels */
    }
    .stSidebar .stImage {
        padding-bottom: 1rem;
        border-bottom: 1px solid #333333;
        margin-bottom: 1rem;
        display: block; /* Ensures proper centering/sizing */
        margin-left: auto;
        margin-right: auto;
    }
    .stSidebar .css-r6zgs0 { /* Target Streamlit's "Logged in as" success message */
        background-color: #004D40; /* Darker green for success */
        color: #80CBC4; /* Lighter green text */
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
    }

    /* Top Horizontal Tabs Styling */
    [data-testid="stTabs"] {
        background-color: #282828; /* Dark grey background for the tab bar */
        border-bottom: 1px solid #333333; /* Subtle line below tabs */
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.5); /* Stronger shadow for depth on dark */
        border-radius: 0 0 12px 12px;
        overflow: hidden;
    }

    [data-testid="stTab"] {
        font-weight: 500;
        font-size: 1.05em;
        padding: 0.75rem 1.25rem;
        margin: 0 0.25rem;
        border-radius: 8px;
        transition: background-color 0.2s, color 0.2s, box-shadow 0.2s;
        color: #A0A0A0; /* Default tab text color */
    }

    [data-testid="stTab"]:hover {
        background-color: #3A3A3A; /* Slightly lighter dark grey on hover */
        color: #E0E0E0; /* Lighter text on hover */
        box-shadow: 0 1px 4px rgba(0,0,0,0.3); /* Slight lift on hover */
    }

    [data-testid="stTab"][aria-selected="true"] {
        background-color: #003366; /* Darker blue for active tab */
        color: #90CAF9; /* Lighter blue for active tab text */
        font-weight: 600;
        box-shadow: 0 1px 4px rgba(0,0,0,0.3);
        border-bottom: 3px solid #1890FF; /* Primary blue underline for active tab */
        border-radius: 8px 8px 0 0;
        margin-bottom: -3px;
    }

    /* Headers and Subheaders */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Roboto', sans-serif;
        color: #FFFFFF; /* White for main headers */
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    h2 {
        border-bottom: 1px solid #333333; /* Darker line under main subheaders */
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    h3 {
        color: #A0A0A0; /* Lighter grey for sub-subheaders */
        margin-top: 1.25rem;
        margin-bottom: 0.75rem;
    }

    /* Markdown Text */
    p {
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    /* Info/Warning/Success Boxes */
    div.stAlert {
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #FFFFFF; /* White text for alerts */
    }
    div.stAlert.st-success {
        background-color: #28a745; /* Darker green */
        border-left: 5px solid #28a745;
    }
    div.stAlert.st-info {
        background-color: #1890FF; /* Primary blue */
        border-left: 5px solid #1890FF;
    }
    div.stAlert.st-warning {
        background-color: #ffc107; /* Darker yellow */
        border-left: 5px solid #ffc107;
    }
    div.stAlert.st-error {
        background-color: #dc3545; /* Darker red */
        border-left: 5px solid #dc3545;
    }

    /* Form Elements */
    .stTextInput > label, .stSelectbox > label, .stDateInput > label, .stNumberInput > label, .stSlider > label, .stTextArea > label, .stCheckbox > label {
        font-weight: 600;
        color: #A0A0A0; /* Lighter grey for form labels */
        margin-bottom: 0.5rem;
    }
    /* Input fields themselves need attention, but Streamlit often styles these internally.
       If specific input fields need background/text changes, individual targeting might be needed. */

    .stButton > button {
        background-color: #1890FF; /* Primary blue button */
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        border: none;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #096DD9; /* Darker blue on hover */
        color: white;
    }
    .stExpander {
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        background-color: #1E1E1E; /* Darker grey for expander */
        box-shadow: 0 2px 4px rgba(0,0,0,0.2); /* Subtle shadow for depth */
    }
    .stForm {
        padding: 1.5rem;
        border: 1px solid #333333;
        border-radius: 8px;
        background-color: #1E1E1E; /* Darker grey for forms */
    }

    /* Dataframes */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    /* Streamlit dataframes default to a dark mode friendly style when `plotly_dark` template is used,
       but specific cell colors might need manual overrides if default dark mode dataframe styling is not sufficient. */

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF; /* White for metric values */
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.1em;
        color: #A0A0A0; /* Lighter grey for metric labels */
    }
    [data-testid="stMetricDelta"] {
        font-size: 1.2em;
    }

    /* Card-like containers for sections */
    .stContainer {
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        background-color: #1E1E1E; /* Darker grey for cards */
        box-shadow: 0 4px 8px rgba(0,0,0,0.3); /* More pronounced shadow for cards on dark */
    }
    .stPlotlyChart {
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 0.5rem;
        background-color: #1E1E1E; /* Darker grey for chart backgrounds */
        box_shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .stCodeBlock {
        background-color: #2D2D2D; /* Darker grey for code blocks */
        border: 1px solid #333333;
        border-left: 5px solid #1890FF;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #E0E0E0; /* Light text for code */
    }

    /* Mailbox Specific Styling */
    .mailbox-container {
        display: flex;
        flex-direction: column;
        border: 1px solid #333333;
        border-radius: 12px;
        background-color: #1E1E1E;
        padding: 20px;
        min-height: 600px; /* Ensure enough height for content */
    }

    .message-card {
        background-color: #2D2D2D;
        border-left: 5px solid #1890FF;
        border-radius: 8px;
        padding: 15px 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        cursor: pointer;
        transition: background-color 0.2s, box-shadow 0.2s;
    }
    .message-card:hover {
        background-color: #3A3A3A;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .message-card.unread {
        border-left: 5px solid #FF4D4F; /* Red border for unread */
        font-weight: bold;
    }
    .message-card h5 {
        color: #FFFFFF;
        margin-bottom: 5px;
    }
    .message-card p {
        font-size: 0.9em;
        color: #B0B0B0;
        margin-bottom: 5px;
    }
    .message-card .message-meta {
        display: flex;
        justify-content: space-between;
        font-size: 0.8em;
        color: #888888;
        margin-top: 10px;
    }

    .message-detail-view {
        background-color: #282828;
        border: 1px solid #3A3A3A;
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
    }
    .message-detail-view h4 {
        color: #90CAF9;
        margin-bottom: 10px;
    }
    .message-detail-view .message-body {
        background-color: #1E1E1E;
        border-left: 3px solid #096DD9;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
        color: #E0E0E0;
        white-space: pre-wrap; /* Preserve whitespace and line breaks */
    }
    .reply-section {
        border-top: 1px solid #3A3A3A;
        padding-top: 20px;
        margin-top: 20px;
    }
    .reply-section .stTextArea textarea {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border: 1px solid #555555;
        border-radius: 8px;
    }
    .reply-list {
        margin-top: 20px;
        padding-left: 15px;
        border-left: 2px dashed #555555;
    }
    .single-reply {
        background-color: #3A3A3A;
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 10px;
        font-size: 0.9em;
        color: #E0E0E0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        white-space: pre-wrap;
    }
    .single-reply .reply-meta {
        font-size: 0.75em;
        color: #A0A0A0;
        margin-bottom: 5px;
        font-style: italic;
    }

    /* Search Bar Styling (only if used in specific tabs) */
    .search-bar-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1.5rem;
        background-color: #1E1E1E;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    .search-bar-container .stTextInput input {
        background-color: #2D2D2D;
        color: #E0E0E0;
        border: 1px solid #555555;
        border-radius: 6px;
        padding: 10px 15px;
    }
    .search-bar-container .stTextInput input:focus {
        border-color: #1890FF;
        box-shadow: 0 0 0 0.2rem rgba(24, 144, 255, 0.25);
    }

    /* Comment Section Styling */
    .comment-card {
        background-color: #2D2D2D;
        border-left: 4px solid #90CAF9; /* Light blue border */
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    .comment-card .comment-meta {
        font-size: 0.8em;
        color: #B0B0B0;
        margin-bottom: 5px;
    }
    .comment-card .comment-body {
        color: #E0E0E0;
        white-space: pre-wrap;
    }
    .reply-to-comment {
        margin-left: 20px;
        border-left: 2px dashed #555555;
        padding-left: 10px;
        margin-top: 10px;
    }

</style>
""", unsafe_allow_html=True)


# --- File Paths & Directory Setup ---
DATA_DIR = "data"
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, "notifications.csv")
FILES_FILE = os.path.join(DATA_DIR, "uploaded_files.csv")
PROJECTS_FILE = os.path.join(DATA_DIR, "project_tasks.csv")
ASSETS_FILE = os.path.join(DATA_DIR, "assets.csv")
AUDITS_FILE = os.path.join(DATA_DIR, "audit_points.csv")
EVENTS_FILE = os.path.join(DATA_DIR, "events.csv")
FILE_COMMENTS_FILE = os.path.join(DATA_DIR, "file_comments.csv") # NEW FILE COMMENTS
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

def update_data(file_path, df_to_save):
    """Overwrites the entire CSV file with the given DataFrame."""
    df_to_save.to_csv(file_path, index=False)

# --- Dynamic Search and Filter Function ---
def apply_search_and_filter(df, search_query_key, advance_search_key):
    st.markdown('<div class="search-bar-container">', unsafe_allow_html=True)
    search_query = st.text_input("Search...", key=search_query_key, placeholder="Type to search...", help="Search across all visible columns.")
    st.markdown('</div>', unsafe_allow_html=True)

    filtered_df = df.copy()

    if search_query:
        search_lower = search_query.lower()
        # Search across all string columns
        filtered_df = filtered_df[
            filtered_df.apply(lambda row: row.astype(str).str.lower().str.contains(search_lower).any(), axis=1)
        ]

    with st.expander("Advanced Search & Filters", expanded=False):
        if not filtered_df.empty:
            cols = filtered_df.columns.tolist()
            # Exclude ID columns from direct text filter, but allow them in options
            filterable_cols = [col for col in cols if filtered_df[col].dtype == 'object' or len(filtered_df[col].unique()) <= 20] # Text or low cardinality
            
            # Use unique keys for each expander's advanced search elements
            selected_column = st.selectbox("Filter by Column", [''] + filterable_cols, key=f"{advance_search_key}_col")

            if selected_column:
                unique_values = filtered_df[selected_column].dropna().unique().tolist()
                
                # Convert numbers to strings for consistent search/selection if mixed types
                unique_values = [str(val) for val in unique_values]
                unique_values.sort() # Sort alphabetically

                if filtered_df[selected_column].dtype == 'object' and len(unique_values) > 50: # For high cardinality text columns
                    filter_text_query = st.text_input(f"Enter search term for '{selected_column}'", key=f"{advance_search_key}_text_filter")
                    if filter_text_query:
                        filtered_df = filtered_df[filtered_df[selected_column].astype(str).str.contains(filter_text_query, case=False, na=False)]
                elif filtered_df[selected_column].dtype in ['int64', 'float64']: # For numeric columns
                    min_val, max_val = float(filtered_df[selected_column].min()), float(filtered_df[selected_column].max())
                    col_min, col_max = st.slider(f"Filter by range for '{selected_column}'", min_value=min_val, max_value=max_val, value=(min_val, max_val), key=f"{advance_search_key}_num_range")
                    filtered_df = filtered_df[(filtered_df[selected_column] >= col_min) & (filtered_df[selected_column] <= col_max)]
                else: # For low cardinality categorical or other types
                    selected_values = st.multiselect(f"Select values for '{selected_column}'", unique_values, key=f"{advance_search_key}_multiselect")
                    if selected_values:
                        # Convert column to string for consistent comparison with selected_values
                        filtered_df = filtered_df[filtered_df[selected_column].astype(str).isin(selected_values)]
        else:
            st.info("No data to apply advanced filters.")
    
    return filtered_df


# --- Initialize CSV Files ---
notification_columns = [
    "notification_id", "sender_role", "recipient_role", "subject", "message",
    "timestamp", "status", "parent_notification_id" # status: Sent, Read, Replied
]
initialize_csv(NOTIFICATIONS_FILE, notification_columns) # NEW
initialize_csv(FILES_FILE, ["filename", "type", "size", "uploader", "timestamp", "path"])

# --- MODIFIED: Added 'is_esg_project' for Sustainability Tracking ---
project_columns = ["task_id", "task_name", "status", "assigned_to", "due_date", "description", "input_pending", "is_esg_project"]
initialize_csv(PROJECTS_FILE, project_columns)

# --- MODIFIED: Added 'last_active_date' for AI Co-pilot (Idle Assets) ---
asset_columns = ["asset_id", "asset_name", "location", "status", "eol_date", "calibration_date", "notes", "supplier", "last_active_date"]
initialize_csv(ASSETS_FILE, asset_columns)

audit_columns = ["audit_id", "point_description", "status", "assignee", "due_date", "resolution", "input_pending"]
initialize_csv(AUDITS_FILE, audit_columns)
event_columns = [
    "event_id", "title", "description", "start_date", "end_date",
    "attendees", "created_by", "timestamp"
]
initialize_csv(EVENTS_FILE, event_columns)
file_comment_columns = [
    "comment_id", "file_name", "parent_comment_id", "author", "timestamp", "comment_text", "mentions" # mentions: list of roles
]
initialize_csv(FILE_COMMENTS_FILE, file_comment_columns) # NEW FILE COMMENTS

# --- MODIFIED: Added ESG-related columns for Sustainability Tracking & Gamification ---
supplier_columns = [
    "supplier_id", "supplier_name", "contact_person", "email", "phone",
    "agreement_status", "last_audit_score", "notes",
    "primary_product_category", "on_time_delivery_rate", "quality_reject_rate",
    "risk_level", "certification", "annual_spend_usd", "last_performance_review_date",
    "esg_compliance_score", "emissions_target_met" # NEW ESG Columns
]
initialize_csv(SUPPLIER_DUMMY_DATA_FILE, supplier_columns)


# --- Sidebar Login ---
st.sidebar.image("ZENOVASRPLOGO.png", width=200) # Updated logo path
st.sidebar.title("Zenova SRP") # More concise title
st.sidebar.markdown("### User Access")
user_roles = ["OEM", "Supplier A", "Supplier B", "Auditor"]
user_role = st.sidebar.selectbox("Login as", user_roles, key="user_role_select")
st.sidebar.success(f"Logged in as {user_role}")
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Zenova SRP** - Your #1 Partner for Strategic Supplier Resource Planning.")
st.sidebar.markdown("---")


# --- Main Application Header & Horizontal Tabs ---
st.header("Zenova SRP Portal") # Main application title at the top

tab_titles = [
    "📊 OEM Dashboard",
    "👥 Supplier Records",
    "🛠️ Asset Management",
    "📅 Project Management",
    "📋 Audit Management",
    "📁 File Management",
    "📧 Mailbox",
    "🗓️ Calendar"
]

# Create horizontal tabs
tabs = st.tabs(tab_titles)


# --- Initialize Streamlit Session State (Global Scope) ---
if "notifications_df" not in st.session_state:
    st.session_state.notifications_df = load_data(NOTIFICATIONS_FILE, columns=notification_columns)

if "mailbox_view" not in st.session_state:
    st.session_state.mailbox_view = "inbox" # Can be "inbox", "sent", "compose", "view_message"

if "selected_notification_id" not in st.session_state:
    st.session_state.selected_notification_id = None

if "events_df" not in st.session_state:
    st.session_state.events_df = load_data(EVENTS_FILE, columns=event_columns)

if "files_df" not in st.session_state:
    st.session_state.files_df = load_data(FILES_FILE, columns=["filename", "type", "size", "uploader", "timestamp", "path"])

if "file_comments_df" not in st.session_state:
    st.session_state.file_comments_df = load_data(FILE_COMMENTS_FILE, columns=file_comment_columns)
    # Ensure 'mentions' column is parsed as list
    if 'mentions' in st.session_state.file_comments_df.columns:
        st.session_state.file_comments_df['mentions'] = st.session_state.file_comments_df['mentions'].apply(lambda x: eval(x) if isinstance(x, str) else []).fillna('')


# --- Main Application Content based on Tab Selection ---

# --- OEM Dashboard Module ---
with tabs[0]: # Corresponding to "📊 OEM Dashboard"
    st.subheader("OEM Performance Dashboard")
    st.markdown("A comprehensive overview of key performance indicators across your supplier network and internal operations.")

    if user_role != "OEM":
        st.warning("🔒 You must be logged in as 'OEM' to view this dashboard.")
    else:
        # Load all relevant data for the dashboard
        projects_df = load_data(PROJECTS_FILE, columns=project_columns)
        assets_df = load_data(ASSETS_FILE, columns=asset_columns)
        audits_df = load_data(AUDITS_FILE, columns=audit_columns)
        supplier_df = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=supplier_columns)

        st.markdown("---")
        st.subheader("💡 AI Co-pilot Insights")
        st.markdown("Automated recommendations to highlight critical areas and suggest actions.")
        current_date = datetime.now()

        col_ai1, col_ai2 = st.columns(2)

        with col_ai1:
            # --- AI Co-pilot Recommendation 1: Idle Assets ---
            if not assets_df.empty and 'last_active_date' in assets_df.columns:
                try:
                    assets_df['last_active_date'] = pd.to_datetime(assets_df['last_active_date'], errors='coerce')
                    idle_threshold_days = 60 # Example threshold
                    idle_assets = assets_df[
                        (assets_df['status'] == 'Operational') & # Only operational assets can be idle
                        (current_date - assets_df['last_active_date']).dt.days > idle_threshold_days
                    ]
                    if not idle_assets.empty:
                        st.warning(f"**Action Required:** {len(idle_assets)} assets are idle for over {idle_threshold_days} days. Review their utilization.")
                        with st.expander("View Idle Assets"):
                            st.dataframe(idle_assets[['asset_name', 'location', 'status', 'last_active_date']], use_container_width=True, hide_index=True)
                    else:
                        st.info(f"No operational assets have been idle for over {idle_threshold_days} days.")
                except Exception as e:
                    st.error(f"Error checking idle assets: {e}")
            else:
                st.info("To enable idle asset tracking, ensure 'last_active_date' column is available and populated in Asset Management.")
            
            st.markdown("---") # Separator for better layout
            # --- AI Co-pilot Recommendation 2: Overdue Projects/Tasks ---
            if not projects_df.empty and 'due_date' in projects_df.columns:
                try:
                    projects_df['due_date'] = pd.to_datetime(projects_df['due_date'], errors='coerce')
                    overdue_tasks = projects_df[
                        (projects_df['status'] != 'Completed') &
                        (projects_df['due_date'] < current_date)
                    ]
                    if not overdue_tasks.empty:
                        st.error(f"**Urgent:** {len(overdue_tasks)} projects/tasks are overdue. Prioritize immediate action.")
                        with st.expander("View Overdue Tasks"):
                            st.dataframe(overdue_tasks[['task_name', 'assigned_to', 'due_date', 'status']], use_container_width=True, hide_index=True)
                    else:
                        st.success("All active projects/tasks are currently on track.")
                except Exception as e:
                    st.error(f"Error checking overdue projects: {e}")

        with col_ai2:
            # --- AI Co-pilot Recommendation 3: Low Performing Suppliers (e.g., Quality Reject Rate) ---
            if not supplier_df.empty and 'quality_reject_rate' in supplier_df.columns:
                try:
                    reject_threshold = 1.5 # Example threshold: more than 1.5% reject rate
                    low_quality_suppliers = supplier_df[supplier_df['quality_reject_rate'] > reject_threshold]
                    if not low_quality_suppliers.empty:
                        st.warning(f"**Review Needed:** {len(low_quality_suppliers)} suppliers have a Quality Reject Rate exceeding {reject_threshold}%.")
                        with st.expander("View Suppliers with High Reject Rates"):
                            st.dataframe(low_quality_suppliers[['supplier_name', 'quality_reject_rate', 'last_performance_review_date']], use_container_width=True, hide_index=True)
                    else:
                        st.success(f"All suppliers currently meet the quality reject rate target of {reject_threshold}%.")
                except Exception as e:
                    st.error(f"Error checking low performing suppliers: {e}")

            st.markdown("---") # Separator for better layout
            # --- AI Co-pilot Recommendation 4: Audits Due Soon or Overdue ---
            if not audits_df.empty and 'due_date' in audits_df.columns:
                try:
                    audits_df['due_date'] = pd.to_datetime(audits_df['due_date'], errors='coerce')
                    upcoming_audits = audits_df[
                        (audits_df['status'] != 'Completed') &
                        (audits_df['due_date'] >= current_date) &
                        (audits_df['due_date'] <= current_date + timedelta(days=30))
                    ]
                    overdue_audits = audits_df[
                        (audits_df['status'] != 'Completed') &
                        (audits_df['due_date'] < current_date)
                    ]

                    if not overdue_audits.empty:
                        st.error(f"**Urgent:** {len(overdue_audits)} audits are overdue. Ensure immediate follow-up.")
                        with st.expander("View Overdue Audits"):
                            st.dataframe(overdue_audits[['point_description', 'assignee', 'due_date', 'status']], use_container_width=True, hide_index=True)

                    if not upcoming_audits.empty:
                        st.info(f"**Heads Up:** {len(upcoming_audits)} audits are due in the next 30 days. Plan accordingly.")
                        with st.expander("View Upcoming Audits"):
                            st.dataframe(upcoming_audits[['point_description', 'assignee', 'due_date', 'status']], use_container_width=True, hide_index=True)
                    else:
                        st.success("No audits are currently overdue or due in the next 30 days.")
                except Exception as e:
                    st.error(f"Error checking audits: {e}")

        # --- Sustainability Tracking (ESG KPIs) ---
        st.markdown("---")
        st.subheader("🌍 Sustainability & ESG Monitoring")
        st.markdown("Tracking your environmental, social, and governance (ESG) performance.")

        col_esg1, col_esg2 = st.columns(2)

        with col_esg1:
            # ESG Project Delays
            if not projects_df.empty and 'is_esg_project' in projects_df.columns:
                try:
                    # Ensure due_date is datetime and is_esg_project is boolean
                    projects_df['due_date'] = pd.to_datetime(projects_df['due_date'], errors='coerce')
                    projects_df['is_esg_project'] = projects_df['is_esg_project'].astype(bool)

                    esg_project_delays = projects_df[
                        (projects_df['is_esg_project'] == True) &
                        (projects_df['status'] != 'Completed') &
                        (projects_df['due_date'] < current_date)
                    ]
                    if not esg_project_delays.empty:
                        st.error(f"**Sustainability Alert:** {len(esg_project_delays)} ESG-related projects are overdue, potentially impacting sustainability KPIs.")
                        with st.expander("View Delayed ESG Projects"):
                            st.dataframe(esg_project_delays[['task_name', 'assigned_to', 'due_date', 'description']], use_container_width=True, hide_index=True)
                    else:
                        st.success("All ESG-related projects are currently on track.")
                except Exception as e:
                    st.error(f"Error checking ESG project delays: {e}")
            else:
                st.info("No ESG project data available. Mark projects as 'ESG-related' in Project Management.")

        with col_esg2:
            # Supplier ESG Compliance (requires new columns in supplier_dummy_data.csv)
            if not supplier_df.empty and 'esg_compliance_score' in supplier_df.columns:
                try:
                    low_esg_score_threshold = 70 # Example threshold
                    non_compliant_suppliers = supplier_df[supplier_df['esg_compliance_score'] < low_esg_score_threshold]
                    if not non_compliant_suppliers.empty:
                        st.warning(f"**Sustainability Watch:** {len(non_compliant_suppliers)} suppliers have an ESG compliance score below {low_esg_score_threshold}.")
                        with st.expander("View Suppliers with Low ESG Scores"):
                            st.dataframe(non_compliant_suppliers[['supplier_name', 'esg_compliance_score', 'certification']], use_container_width=True, hide_index=True)
                    else:
                        st.success(f"All suppliers currently meet the ESG compliance score target of {low_esg_score_threshold}.")

                    # Example: Suppliers not meeting emissions target
                    if 'emissions_target_met' in supplier_df.columns:
                        not_met_emissions = supplier_df[supplier_df['emissions_target_met'] == False]
                        if not not_met_emissions.empty:
                            st.warning(f"**Environmental Focus:** {len(not_met_emissions)} suppliers have not met their emissions reduction targets.")
                            with st.expander("View Suppliers Not Meeting Emissions Targets"):
                                st.dataframe(not_met_emissions[['supplier_name', 'emissions_target_met']], use_container_width=True, hide_index=True)
                        else:
                            st.success("All suppliers are meeting their emissions reduction targets.")

                except Exception as e:
                    st.error(f"Error checking supplier ESG compliance: {e}")
            else:
                st.info("No supplier ESG data available. Add 'esg_compliance_score' and 'emissions_target_met' to supplier records.")

        # --- Gamification - Badges for Suppliers ---
        st.markdown("---")
        st.subheader("🏅 Supplier Recognition & Gamification")
        st.markdown("Recognize and reward your suppliers for outstanding performance.")

        if not supplier_df.empty:
            gamified_suppliers = supplier_df.copy()

            # Define badge criteria and apply
            # Badge 1: On-Time Delivery Champion
            otd_threshold = 98.0
            gamified_suppliers['OTD Champion 🏆'] = gamified_suppliers['on_time_delivery_rate'] >= otd_threshold

            # Badge 2: Zero Quality Deviations
            reject_threshold = 0.1 # Very low reject rate for 'zero'
            gamified_suppliers['Quality Star ⭐'] = gamified_suppliers['quality_reject_rate'] <= reject_threshold

            # Badge 3: Perfect Audit Score (assuming 100 is perfect)
            perfect_audit_score = 100
            gamified_suppliers['Audit Excellence 💯'] = gamified_suppliers['last_audit_score'] == perfect_audit_score

            # Badge 4: Low Risk Partner
            gamified_suppliers['Low Risk Partner ✅'] = gamified_suppliers['risk_level'] == 'Low'

            st.markdown("### Supplier Badges Overview")
            col_badges1, col_badges2, col_badges3, col_badges4 = st.columns(4)
            with col_badges1:
                st.metric("OTD Champions", f"{gamified_suppliers['OTD Champion 🏆'].sum()} / {len(gamified_suppliers)}", help=f"Suppliers with On-Time Delivery Rate >= {otd_threshold}%")
            with col_badges2:
                st.metric("Quality Stars", f"{gamified_suppliers['Quality Star ⭐'].sum()} / {len(gamified_suppliers)}", help=f"Suppliers with Quality Reject Rate <= {reject_threshold}%")
            with col_badges3:
                st.metric("Audit Excellence", f"{gamified_suppliers['Audit Excellence 💯'].sum()} / {len(gamified_suppliers)}", help=f"Suppliers with Last Audit Score of {perfect_audit_score}")
            with col_badges4:
                st.metric("Low Risk Partners", f"{gamified_suppliers['Low Risk Partner ✅'].sum()} / {len(gamified_suppliers)}", help=f"Suppliers categorized as 'Low' risk")


            st.markdown("### Detailed Supplier Badge Status")
            # Select columns to display for gamification summary
            badge_display_cols = ['supplier_name', 'on_time_delivery_rate', 'quality_reject_rate', 'last_audit_score', 'risk_level',
                                  'OTD Champion 🏆', 'Quality Star ⭐', 'Audit Excellence 💯', 'Low Risk Partner ✅']

            st.dataframe(gamified_suppliers[badge_display_cols], use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("#### Send a Recognition!")
            selected_supplier_name = st.selectbox("Select a supplier to recognize:", [''] + supplier_df['supplier_name'].tolist(), key="recognize_supplier_select")
            if selected_supplier_name:
                recognition_message = st.text_area(f"Enter recognition message for {selected_supplier_name}:", key="recognition_message_text")
                if st.button("Send Recognition Message", key="send_recognition_btn"):
                    if recognition_message:
                        notification_id = "NOTIF" + str(len(st.session_state.notifications_df) + 1).zfill(4)
                        new_notification = pd.DataFrame([{
                            "notification_id": notification_id,
                            "sender_role": user_role,
                            "recipient_role": selected_supplier_name, # Assuming recipient_role can be a specific supplier
                            "subject": f"Recognition for Excellence - {selected_supplier_name}",
                            "message": recognition_message,
                            "timestamp": datetime.now().isoformat(),
                            "status": "Sent",
                            "parent_notification_id": None
                        }])
                        append_data(NOTIFICATIONS_FILE, new_notification)
                        st.session_state.notifications_df = load_data(NOTIFICATIONS_FILE, columns=notification_columns) # Reload
                        st.success(f"Recognition message sent to {selected_supplier_name}!")
                        # Clear message area after sending (requires a small workaround for st.text_area)
                        # st.session_state.recognition_message_text = "" # This might not clear immediately
                    else:
                        st.warning("Please enter a recognition message.")
        else:
            st.info("No supplier data available to apply gamification.")

        st.markdown("---")
        st.subheader("Supplier Performance & Financial Overview")
        # Removed search bar here
        if not supplier_df.empty:
            st.dataframe(supplier_df, use_container_width=True, hide_index=True)
        else:
            st.info("No supplier data available. Please add new suppliers in '👥 Supplier Records'.")


        with st.container():
            col_sup1, col_sup2 = st.columns(2)

            with col_sup1:
                st.markdown("#### 🤝 Supplier Agreement Status")
                if not supplier_df.empty and 'agreement_status' in supplier_df.columns:
                    supplier_df['agreement_status'] = supplier_df['agreement_status'].fillna('Unknown').astype(str)
                    status_counts = supplier_df['agreement_status'].value_counts().reset_index()
                    status_counts.columns = ['Status', 'Count']
                    fig_status = px.pie(status_counts, values='Count', names='Status',
                                         title='Distribution of Supplier Agreement Status', hole=0.3,
                                         template='plotly_dark') # Set dark theme for Plotly
                    fig_status.update_traces(textposition='inside', textinfo='percent+label')
                    fig_status.update_layout(showlegend=True, margin=dict(l=20, r=20, t=30, b=20), height=300)
                    st.plotly_chart(fig_status, use_container_width=True)
                else:
                    st.info("No supplier data to show agreement status.")

            with col_sup2:
                st.markdown("#### 💯 Last Audit Score Distribution")
                if not supplier_df.empty and 'last_audit_score' in supplier_df.columns:
                    fig_audit_dist = px.histogram(supplier_df, x='last_audit_score', nbins=10,
                                                  title='Distribution of Last Audit Scores',
                                                  labels={'last_audit_score': 'Audit Score'},
                                                  color_discrete_sequence=['#1890FF'],
                                                  template='plotly_dark') # Set dark theme for Plotly
                    fig_audit_dist.update_layout(bargap=0.1, margin=dict(l=20, r=20, t=30, b=20), height=300)
                    st.plotly_chart(fig_audit_dist, use_container_width=True)
                else:
                    st.info("No supplier data to show audit score distribution.")

        st.markdown("---")
        with st.container():
            col_performance1, col_performance2 = st.columns(2)
            with col_performance1:
                st.markdown("#### 🚚 Average On-Time Delivery Rate")
                if not supplier_df.empty and 'on_time_delivery_rate' in supplier_df.columns:
                    avg_delivery = supplier_df['on_time_delivery_rate'].mean()
                    st.metric(label="Overall OTD Rate", value=f"{avg_delivery:.1f}%", delta="Excellent!" if avg_delivery >= 95 else "Needs Improvement" if avg_delivery < 90 else None)
                    fig_otd = px.box(supplier_df, y='on_time_delivery_rate', title='On-Time Delivery Rate Distribution',
                                     color_discrete_sequence=['#52C41A'],
                                     template='plotly_dark') # Set dark theme for Plotly
                    fig_otd.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=250)
                    st.plotly_chart(fig_otd, use_container_width=True)
                else:
                    st.info("No on-time delivery data available.")

            with col_performance2:
                st.markdown("#### 🔍 Average Quality Reject Rate")
                if not supplier_df.empty and 'quality_reject_rate' in supplier_df.columns:
                    avg_reject = supplier_df['quality_reject_rate'].mean()
                    st.metric(label="Overall Reject Rate", value=f"{avg_reject:.2f}%", delta="Low" if avg_reject < 0.5 else "High" if avg_reject > 1.0 else None, delta_color="inverse")
                    fig_reject = px.box(supplier_df, y='quality_reject_rate', title='Quality Reject Rate Distribution',
                                         color_discrete_sequence=['#FF4D4F'],
                                         template='plotly_dark') # Set dark theme for Plotly
                    fig_reject.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=250)
                    st.plotly_chart(fig_reject, use_container_width=True)
                else:
                    st.info("No quality reject rate data available.")

        st.markdown("---")
        with st.container():
            col_risk_spend = st.columns(2)
            with col_risk_spend[0]:
                st.markdown("#### 🚨 Supplier Risk Level Distribution")
                if not supplier_df.empty and 'risk_level' in supplier_df.columns:
                    risk_counts = supplier_df['risk_level'].value_counts().reset_index()
                    risk_counts.columns = ['Risk Level', 'Count']
                    # Ensure consistent order for risk levels
                    risk_order = ["Low", "Medium", "High"]
                    risk_counts['Risk Level'] = pd.Categorical(risk_counts['Risk Level'], categories=risk_order, ordered=True)
                    risk_counts = risk_counts.sort_values('Risk Level')

                    fig_risk = px.pie(risk_counts, values='Count', names='Risk Level',
                                      title='Distribution of Supplier Risk Levels', hole=0.3,
                                      color='Risk Level',
                                      color_discrete_map={'Low': '#52C41A', 'Medium': '#FAAD14', 'High': '#FF4D4F'},
                                      template='plotly_dark') # Set dark theme for Plotly
                    fig_risk.update_traces(textposition='inside', textinfo='percent+label')
                    fig_risk.update_layout(showlegend=True, margin=dict(l=20, r=20, t=30, b=20), height=300)
                    st.plotly_chart(fig_risk, use_container_width=True)
                else:
                    st.info("No supplier risk level data.")

            with col_risk_spend[1]:
                st.markdown("#### 💰 Annual Spend by Primary Product Category")
                if not supplier_df.empty and 'annual_spend_usd' in supplier_df.columns and 'primary_product_category' in supplier_df.columns:
                    spend_by_category = supplier_df.groupby('primary_product_category')['annual_spend_usd'].sum().reset_index()
                    spend_by_category = spend_by_category.sort_values(by='annual_spend_usd', ascending=False)
                    fig_spend = px.bar(spend_by_category, x='primary_product_category', y='annual_spend_usd',
                                       title='Total Annual Spend by Product Category (USD)',
                                       labels={'primary_product_category': 'Product Category', 'annual_spend_usd': 'Annual Spend (USD)'},
                                       color_discrete_sequence=px.colors.qualitative.Plotly,
                                       template='plotly_dark') # Set dark theme for Plotly
                    fig_spend.update_layout(xaxis_title_text='Product Category', yaxis_title_text='Annual Spend (USD)',
                                            margin=dict(l=20, r=20, t=30, b=20), height=300)
                    st.plotly_chart(fig_spend, use_container_width=True)
                else:
                    st.info("No annual spend or product category data.")

        st.markdown("---")
        with st.container():
            st.markdown("#### 📈 Key Supplier Rankings")
            col_rank1, col_rank2 = st.columns(2)
            with col_rank1:
                st.markdown("##### Top 10 Suppliers by Annual Spend")
                if not supplier_df.empty and 'annual_spend_usd' in supplier_df.columns:
                    top_spend_suppliers = supplier_df.sort_values(by='annual_spend_usd', ascending=False).head(10)
                    st.dataframe(top_spend_suppliers[['supplier_name', 'annual_spend_usd', 'primary_product_category']],
                                 use_container_width=True, hide_index=True)
                else:
                    st.info("No supplier spend data to show top suppliers.")

            with col_rank2:
                st.markdown("##### Top 10 Suppliers by Audit Score")
                if not supplier_df.empty and 'last_audit_score' in supplier_df.columns:
                    top_suppliers = supplier_df.sort_values(by='last_audit_score', ascending=False).head(10)
                    st.dataframe(top_suppliers[['supplier_name', 'last_audit_score', 'agreement_status']],
                                 use_container_width=True, hide_index=True)
                else:
                    st.info("No supplier data to show top suppliers.")

        st.markdown("---")
        with st.container():
            st.markdown("#### ⚠️ Critical Supplier Alerts")
            col_alerts1, col_alerts2 = st.columns(2)
            with col_alerts1:
                st.markdown("##### Agreements Due for Renewal")
                if not supplier_df.empty:
                    pending_renewal = supplier_df[supplier_df['agreement_status'] == 'Pending Renewal']
                    if not pending_renewal.empty:
                        st.dataframe(pending_renewal[['supplier_name', 'contact_person', 'email', 'agreement_status']],
                                     use_container_width=True, hide_index=True)
                    else:
                        st.success("🎉 No supplier agreements are pending renewal.")
                else:
                    st.info("No supplier data to check for pending renewals.")

            with col_alerts2:
                st.markdown("##### Overdue Performance Reviews (> 1 Year)")
                if not supplier_df.empty:
                    supplier_df['last_performance_review_date'] = pd.to_datetime(supplier_df['last_performance_review_date'], errors='coerce')
                    overdue_reviews = supplier_df[
                        (current_date - supplier_df['last_performance_review_date']).dt.days > 365
                    ]
                    if not overdue_reviews.empty:
                        st.warning(f"**Action Required:** {len(overdue_reviews)} supplier performance reviews are overdue.")
                        st.dataframe(overdue_reviews[['supplier_name', 'contact_person', 'last_performance_review_date']],
                                     use_container_width=True, hide_index=True)
                    else:
                        st.success("All supplier performance reviews are up-to-date.")
                else:
                    st.info("No supplier data to check for overdue performance reviews.")


# --- Supplier Records Module ---
with tabs[1]: # Corresponding to "👥 Supplier Records"
    st.subheader("Manage Supplier Information")
    st.markdown("Maintain a comprehensive database of all your OEM suppliers.")

    supplier_df = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=supplier_columns)

    if user_role not in ["OEM"]:
        st.warning("🔒 You must be logged in as 'OEM' to manage supplier records.")
    else:
        st.markdown("### Add New Supplier")
        with st.form("new_supplier_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                new_supplier_name = st.text_input("Supplier Name", key="new_sup_name")
                new_contact_person = st.text_input("Contact Person", key="new_sup_contact")
                new_email = st.text_input("Email", key="new_sup_email")
            with col2:
                new_phone = st.text_input("Phone", key="new_sup_phone")
                new_agreement_status = st.selectbox("Agreement Status", ["Active", "Pending Renewal", "Expired", "Under Review"], key="new_sup_agreement")
                new_product_category = st.text_input("Primary Product Category", help="e.g., Electronics, Raw Materials, Assembly", key="new_sup_prod_cat")
            with col3:
                new_last_audit_score = st.number_input("Last Audit Score (0-100)", min_value=0, max_value=100, value=75, key="new_sup_audit_score")
                new_on_time_delivery = st.number_input("On-Time Delivery Rate (%)", min_value=0.0, max_value=100.0, value=95.0, key="new_sup_otd")
                new_quality_reject = st.number_input("Quality Reject Rate (%)", min_value=0.0, max_value=100.0, value=0.5, format="%.2f", key="new_sup_reject")
            
            # --- NEW: ESG Fields for Supplier ---
            col_esg_sup1, col_esg_sup2 = st.columns(2)
            with col_esg_sup1:
                new_esg_score = st.number_input("ESG Compliance Score (0-100)", min_value=0, max_value=100, value=70, key="new_sup_esg_score")
            with col_esg_sup2:
                new_emissions_target_met = st.checkbox("Met Emissions Reduction Target?", value=False, key="new_sup_emissions_met")

            new_risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"], key="new_sup_risk")
            new_certification = st.text_input("Certifications (e.g., ISO 9001)", key="new_sup_cert")
            new_annual_spend = st.number_input("Annual Spend (USD)", min_value=0, value=100000, key="new_sup_annual_spend")
            new_notes = st.text_area("Notes", key="new_sup_notes")
            new_last_performance_review_date = st.date_input("Last Performance Review Date", value=datetime.today() - timedelta(days=90), key="new_sup_perf_date")

            submit_supplier = st.form_submit_button("Add Supplier")

            if submit_supplier:
                if new_supplier_name and new_contact_person and new_email:
                    supplier_id = "SUP" + str(len(supplier_df) + 1).zfill(4)
                    new_entry = pd.DataFrame([{
                        "supplier_id": supplier_id,
                        "supplier_name": new_supplier_name,
                        "contact_person": new_contact_person,
                        "email": new_email,
                        "phone": new_phone,
                        "agreement_status": new_agreement_status,
                        "last_audit_score": new_last_audit_score,
                        "notes": new_notes,
                        "primary_product_category": new_product_category,
                        "on_time_delivery_rate": new_on_time_delivery,
                        "quality_reject_rate": new_quality_reject,
                        "risk_level": new_risk_level,
                        "certification": new_certification,
                        "annual_spend_usd": new_annual_spend,
                        "last_performance_review_date": new_last_performance_review_date.isoformat(),
                        "esg_compliance_score": new_esg_score, # NEW
                        "emissions_target_met": new_emissions_target_met # NEW
                    }])
                    append_data(SUPPLIER_DUMMY_DATA_FILE, new_entry)
                    st.success(f"Supplier '{new_supplier_name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields: Supplier Name, Contact Person, Email.")

        st.markdown("### Existing Suppliers")
        
        # Apply search and filter to supplier data
        display_supplier_df = apply_search_and_filter(supplier_df, "supplier_search", "supplier_advanced_search")

        if not display_supplier_df.empty:
            st.dataframe(display_supplier_df, use_container_width=True, hide_index=True)

            selected_supplier_id = st.selectbox("Select Supplier ID to Edit/Delete", [''] + display_supplier_df['supplier_id'].tolist(), key="select_supplier_edit_del")

            if selected_supplier_id:
                selected_supplier = supplier_df[supplier_df['supplier_id'] == selected_supplier_id].iloc[0]
                st.markdown(f"#### Edit Supplier: {selected_supplier['supplier_name']}")
                with st.form("edit_supplier_form"):
                    col1_edit, col2_edit, col3_edit = st.columns(3)
                    with col1_edit:
                        edit_supplier_name = st.text_input("Supplier Name", value=selected_supplier['supplier_name'], key="edit_sup_name")
                        edit_contact_person = st.text_input("Contact Person", value=selected_supplier['contact_person'], key="edit_sup_contact")
                        edit_email = st.text_input("Email", value=selected_supplier['email'], key="edit_sup_email")
                    with col2_edit:
                        edit_phone = st.text_input("Phone", value=selected_supplier['phone'], key="edit_sup_phone")
                        edit_agreement_status = st.selectbox("Agreement Status", ["Active", "Pending Renewal", "Expired", "Under Review"], index=["Active", "Pending Renewal", "Expired", "Under Review"].index(selected_supplier['agreement_status']), key="edit_sup_agreement")
                        edit_product_category = st.text_input("Primary Product Category", value=selected_supplier['primary_product_category'], key="edit_sup_prod_cat")
                    with col3_edit:
                        edit_last_audit_score = st.number_input("Last Audit Score (0-100)", min_value=0, max_value=100, value=int(selected_supplier['last_audit_score']), key="edit_sup_audit_score")
                        edit_on_time_delivery = st.number_input("On-Time Delivery Rate (%)", min_value=0.0, max_value=100.0, value=float(selected_supplier['on_time_delivery_rate']), format="%.2f", key="edit_sup_otd")
                        edit_quality_reject = st.number_input("Quality Reject Rate (%)", min_value=0.0, max_value=100.0, value=float(selected_supplier['quality_reject_rate']), format="%.2f", key="edit_sup_reject")
                    
                    # --- NEW: ESG Fields for Supplier Editing ---
                    col_esg_sup1_edit, col_esg_sup2_edit = st.columns(2)
                    with col_esg_sup1_edit:
                        edit_esg_score = st.number_input("ESG Compliance Score (0-100)", min_value=0, max_value=100, value=int(selected_supplier['esg_compliance_score']), key="edit_sup_esg_score")
                    with col_esg_sup2_edit:
                        edit_emissions_target_met = st.checkbox("Met Emissions Reduction Target?", value=bool(selected_supplier['emissions_target_met']), key="edit_sup_emissions_met")

                    edit_risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(selected_supplier['risk_level']), key="edit_sup_risk")
                    edit_certification = st.text_input("Certifications (e.g., ISO 9001)", value=selected_supplier['certification'], key="edit_sup_cert")
                    edit_annual_spend = st.number_input("Annual Spend (USD)", min_value=0, value=int(selected_supplier['annual_spend_usd']), key="edit_sup_annual_spend")
                    edit_notes = st.text_area("Notes", value=selected_supplier['notes'], key="edit_sup_notes")
                    
                    # Handle potential NaT for date input
                    try:
                        default_date = datetime.strptime(str(selected_supplier['last_performance_review_date']), '%Y-%m-%d').date()
                    except (ValueError, TypeError):
                        default_date = datetime.today().date()
                    edit_last_performance_review_date = st.date_input("Last Performance Review Date", value=default_date, key="edit_sup_perf_date")

                    update_supplier_btn = st.form_submit_button("Update Supplier")
                    delete_supplier_btn = st.form_submit_button("Delete Supplier")

                    if update_supplier_btn:
                        idx = supplier_df[supplier_df['supplier_id'] == selected_supplier_id].index[0]
                        supplier_df.loc[idx] = {
                            "supplier_id": selected_supplier_id,
                            "supplier_name": edit_supplier_name,
                            "contact_person": edit_contact_person,
                            "email": edit_email,
                            "phone": edit_phone,
                            "agreement_status": edit_agreement_status,
                            "last_audit_score": edit_last_audit_score,
                            "notes": edit_notes,
                            "primary_product_category": edit_product_category,
                            "on_time_delivery_rate": edit_on_time_delivery,
                            "quality_reject_rate": edit_quality_reject,
                            "risk_level": edit_risk_level,
                            "certification": edit_certification,
                            "annual_spend_usd": edit_annual_spend,
                            "last_performance_review_date": edit_last_performance_review_date.isoformat(),
                            "esg_compliance_score": edit_esg_score, # NEW
                            "emissions_target_met": edit_emissions_target_met # NEW
                        }
                        update_data(SUPPLIER_DUMMY_DATA_FILE, supplier_df)
                        st.success(f"Supplier '{edit_supplier_name}' updated successfully!")
                        st.rerun()
                    
                    if delete_supplier_btn:
                        supplier_df = supplier_df[supplier_df['supplier_id'] != selected_supplier_id]
                        update_data(SUPPLIER_DUMMY_DATA_FILE, supplier_df)
                        st.warning(f"Supplier '{selected_supplier['supplier_name']}' deleted.")
                        st.rerun()
        else:
            st.info("No suppliers added yet.")


# --- Asset Management Module ---
with tabs[2]: # Corresponding to "🛠️ Asset Management"
    st.subheader("Asset Management")
    st.markdown("Track and manage physical assets used by OEM and suppliers.")

    assets_df = load_data(ASSETS_FILE, columns=asset_columns)
    
    if user_role not in ["OEM", "Supplier A", "Supplier B"]:
        st.warning("🔒 You must be logged in as 'OEM' or a 'Supplier' to manage assets.")
    else:
        st.markdown("### Add New Asset")
        with st.form("new_asset_form"):
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                new_asset_name = st.text_input("Asset Name", key="new_asset_name")
                new_location = st.text_input("Location", key="new_asset_location")
                new_status = st.selectbox("Status", ["Operational", "Under Maintenance", "Retired", "Idle"], key="new_asset_status")
                new_supplier = st.text_input("Associated Supplier (Optional)", help="e.g., Supplier A, Supplier B, or OEM", key="new_asset_supplier")
            with col_a2:
                new_eol_date = st.date_input("End of Life Date", value=datetime.today() + timedelta(days=365*5), key="new_asset_eol")
                new_calibration_date = st.date_input("Last Calibration Date", value=datetime.today(), key="new_asset_calibration")
                # --- NEW: last_active_date for AI Co-pilot ---
                new_last_active_date = st.date_input("Last Active Date", value=datetime.today(), help="When was this asset last actively used?", key="new_asset_last_active")
                new_notes = st.text_area("Notes", key="new_asset_notes")

            submit_asset = st.form_submit_button("Add Asset")

            if submit_asset:
                if new_asset_name and new_location:
                    asset_id = "AST" + str(len(assets_df) + 1).zfill(4)
                    new_entry = pd.DataFrame([{
                        "asset_id": asset_id,
                        "asset_name": new_asset_name,
                        "location": new_location,
                        "status": new_status,
                        "eol_date": new_eol_date.isoformat(),
                        "calibration_date": new_calibration_date.isoformat(),
                        "notes": new_notes,
                        "supplier": new_supplier,
                        "last_active_date": new_last_active_date.isoformat() # NEW
                    }])
                    append_data(ASSETS_FILE, new_entry)
                    st.success(f"Asset '{new_asset_name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in Asset Name and Location.")
        
        st.markdown("### Existing Assets")
        
        # Filter assets for non-OEM users
        if user_role == "OEM":
            display_assets_df = assets_df
        elif user_role in ["Supplier A", "Supplier B"]:
            display_assets_df = assets_df[assets_df['supplier'] == user_role]
            if display_assets_df.empty:
                st.info(f"No assets found for {user_role}.")
        else: # For Auditor, etc. just show all but no edit/delete
            display_assets_df = assets_df

        # Apply search and filter to asset data
        display_assets_df = apply_search_and_filter(display_assets_df, "asset_search", "asset_advanced_search")

        if not display_assets_df.empty:
            st.dataframe(display_assets_df, use_container_width=True, hide_index=True)

            if user_role in ["OEM", "Supplier A", "Supplier B"]: # Only allow editing/deleting for OEM or the specific supplier
                selected_asset_id = st.selectbox("Select Asset ID to Edit/Delete", [''] + display_assets_df['asset_id'].tolist(), key="select_asset_edit_del")

                if selected_asset_id:
                    selected_asset = assets_df[assets_df['asset_id'] == selected_asset_id].iloc[0]
                    
                    # Check if the asset belongs to the logged-in supplier, if applicable
                    if user_role != "OEM" and selected_asset['supplier'] != user_role:
                        st.warning(f"You ({user_role}) do not have permission to edit this asset as it belongs to {selected_asset['supplier']}.")
                    else:
                        st.markdown(f"#### Edit Asset: {selected_asset['asset_name']}")
                        with st.form("edit_asset_form"):
                            col_e1, col_e2 = st.columns(2)
                            with col_e1:
                                edit_asset_name = st.text_input("Asset Name", value=selected_asset['asset_name'], key="edit_asset_name")
                                edit_location = st.text_input("Location", value=selected_asset['location'], key="edit_asset_location")
                                edit_status = st.selectbox("Status", ["Operational", "Under Maintenance", "Retired", "Idle"], index=["Operational", "Under Maintenance", "Retired", "Idle"].index(selected_asset['status']), key="edit_asset_status")
                                edit_supplier = st.text_input("Associated Supplier (Optional)", value=selected_asset['supplier'], key="edit_asset_supplier")
                            with col_e2:
                                try:
                                    default_eol = datetime.strptime(str(selected_asset['eol_date']), '%Y-%m-%d').date()
                                except (ValueError, TypeError):
                                    default_eol = datetime.today().date()
                                edit_eol_date = st.date_input("End of Life Date", value=default_eol, key="edit_asset_eol")
                                
                                try:
                                    default_cal = datetime.strptime(str(selected_asset['calibration_date']), '%Y-%m-%d').date()
                                except (ValueError, TypeError):
                                    default_cal = datetime.today().date()
                                edit_calibration_date = st.date_input("Last Calibration Date", value=default_cal, key="edit_asset_calibration")
                                
                                # --- NEW: last_active_date for editing ---
                                try:
                                    default_active = datetime.strptime(str(selected_asset['last_active_date']), '%Y-%m-%d').date()
                                except (ValueError, TypeError):
                                    default_active = datetime.today().date()
                                edit_last_active_date = st.date_input("Last Active Date", value=default_active, key="edit_asset_last_active")

                                edit_notes = st.text_area("Notes", value=selected_asset['notes'], key="edit_asset_notes")

                            update_asset_btn = st.form_submit_button("Update Asset")
                            delete_asset_btn = st.form_submit_button("Delete Asset")

                            if update_asset_btn:
                                idx = assets_df[assets_df['asset_id'] == selected_asset_id].index[0]
                                assets_df.loc[idx] = {
                                    "asset_id": selected_asset_id,
                                    "asset_name": edit_asset_name,
                                    "location": edit_location,
                                    "status": edit_status,
                                    "eol_date": edit_eol_date.isoformat(),
                                    "calibration_date": edit_calibration_date.isoformat(),
                                    "notes": edit_notes,
                                    "supplier": edit_supplier,
                                    "last_active_date": edit_last_active_date.isoformat() # NEW
                                }
                                update_data(ASSETS_FILE, assets_df)
                                st.success(f"Asset '{edit_asset_name}' updated successfully!")
                                st.rerun()
                            
                            if delete_asset_btn:
                                assets_df = assets_df[assets_df['asset_id'] != selected_asset_id]
                                update_data(ASSETS_FILE, assets_df)
                                st.warning(f"Asset '{selected_asset['asset_name']}' deleted.")
                                st.rerun()
            else:
                st.info("Select an asset above to see details or edit/delete options.")
        else:
            if user_role in ["Supplier A", "Supplier B"]:
                st.info(f"No assets currently managed by {user_role}.")
            else:
                st.info("No assets added yet.")


# --- Project Management Module ---
with tabs[3]: # Corresponding to "📅 Project Management"
    st.subheader("Project & Task Management")
    st.markdown("Oversee internal projects and tasks, assigning them to relevant personnel.")

    projects_df = load_data(PROJECTS_FILE, columns=project_columns)

    if user_role not in ["OEM", "Supplier A", "Supplier B"]: # Allowing suppliers to see their own projects
        st.warning("🔒 You must be logged in as 'OEM' or a 'Supplier' to manage projects.")
    else:
        st.markdown("### Create New Project/Task")
        with st.form("new_project_form"):
            new_task_name = st.text_input("Task Name", key="new_task_name")
            new_description = st.text_area("Description", key="new_task_description")
            new_status = st.selectbox("Status", ["Not Started", "In Progress", "Completed", "On Hold", "Input Pending"], key="new_task_status")
            new_assigned_to = st.text_input("Assigned To (Name/Role)", key="new_task_assignee")
            new_due_date = st.date_input("Due Date", value=datetime.today() + timedelta(days=7), key="new_task_due_date")
            new_input_pending = st.checkbox("Input Pending from Supplier?", value=False, key="new_task_input_pending")
            # --- NEW: is_esg_project for Sustainability Tracking ---
            new_is_esg_project = st.checkbox("Is this an ESG-related project?", value=False, help="Check if this project contributes to Environmental, Social, or Governance goals.", key="new_task_esg_project")


            submit_project = st.form_submit_button("Add Project/Task")

            if submit_project:
                if new_task_name and new_assigned_to:
                    task_id = "TASK" + str(len(projects_df) + 1).zfill(4)
                    new_entry = pd.DataFrame([{
                        "task_id": task_id,
                        "task_name": new_task_name,
                        "status": new_status,
                        "assigned_to": new_assigned_to,
                        "due_date": new_due_date.isoformat(),
                        "description": new_description,
                        "input_pending": new_input_pending,
                        "is_esg_project": new_is_esg_project # NEW
                    }])
                    append_data(PROJECTS_FILE, new_entry)
                    st.success(f"Project/Task '{new_task_name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in Task Name and Assigned To.")

        st.markdown("### Existing Projects/Tasks")
        
        # Filter projects for non-OEM users
        if user_role == "OEM":
            display_projects_df = projects_df
        elif user_role in ["Supplier A", "Supplier B"]:
            display_projects_df = projects_df[projects_df['assigned_to'] == user_role]
            if display_projects_df.empty:
                st.info(f"No projects/tasks assigned to {user_role}.")
        else: # For Auditor, etc. just show all but no edit/delete
            display_projects_df = projects_df

        # Apply search and filter to project data
        display_projects_df = apply_search_and_filter(display_projects_df, "project_search", "project_advanced_search")

        if not display_projects_df.empty:
            st.dataframe(display_projects_df, use_container_width=True, hide_index=True)

            if user_role in ["OEM", "Supplier A", "Supplier B"]: # Only allow editing/deleting for OEM or the specific supplier
                selected_task_id = st.selectbox("Select Task ID to Edit/Delete", [''] + display_projects_df['task_id'].tolist(), key="select_task_edit_del")

                if selected_task_id:
                    selected_task = projects_df[projects_df['task_id'] == selected_task_id].iloc[0]

                    # Check if the task is assigned to the logged-in supplier, if applicable
                    if user_role != "OEM" and selected_task['assigned_to'] != user_role:
                        st.warning(f"You ({user_role}) do not have permission to edit this task as it is assigned to {selected_task['assigned_to']}.")
                    else:
                        st.markdown(f"#### Edit Project/Task: {selected_task['task_name']}")
                        with st.form("edit_project_form"):
                            edit_task_name = st.text_input("Task Name", value=selected_task['task_name'], key="edit_task_name")
                            edit_description = st.text_area("Description", value=selected_task['description'], key="edit_task_description")
                            edit_status = st.selectbox("Status", ["Not Started", "In Progress", "Completed", "On Hold", "Input Pending"], index=["Not Started", "In Progress", "Completed", "On Hold", "Input Pending"].index(selected_task['status']), key="edit_task_status")
                            edit_assigned_to = st.text_input("Assigned To (Name/Role)", value=selected_task['assigned_to'], key="edit_task_assignee")
                            
                            try:
                                default_due = datetime.strptime(str(selected_task['due_date']), '%Y-%m-%d').date()
                            except (ValueError, TypeError):
                                default_due = datetime.today().date()
                            edit_due_date = st.date_input("Due Date", value=default_due, key="edit_task_due_date")
                            edit_input_pending = st.checkbox("Input Pending from Supplier?", value=bool(selected_task['input_pending']), key="edit_task_input_pending")
                            # --- NEW: is_esg_project for editing ---
                            edit_is_esg_project = st.checkbox("Is this an ESG-related project?", value=bool(selected_task['is_esg_project']), key="edit_task_esg_project")


                            update_project_btn = st.form_submit_button("Update Project/Task")
                            delete_project_btn = st.form_submit_button("Delete Project/Task")

                            if update_project_btn:
                                idx = projects_df[projects_df['task_id'] == selected_task_id].index[0]
                                projects_df.loc[idx] = {
                                    "task_id": selected_task_id,
                                    "task_name": edit_task_name,
                                    "status": edit_status,
                                    "assigned_to": edit_assigned_to,
                                    "due_date": edit_due_date.isoformat(),
                                    "description": edit_description,
                                    "input_pending": edit_input_pending,
                                    "is_esg_project": edit_is_esg_project # NEW
                                }
                                update_data(PROJECTS_FILE, projects_df)
                                st.success(f"Project/Task '{edit_task_name}' updated successfully!")
                                st.rerun()
                            
                            if delete_project_btn:
                                projects_df = projects_df[projects_df['task_id'] != selected_task_id]
                                update_data(PROJECTS_FILE, projects_df)
                                st.warning(f"Project/Task '{selected_task['task_name']}' deleted.")
                                st.rerun()
            else:
                st.info("Select a project/task above to see details or edit/delete options.")
        else:
            if user_role in ["Supplier A", "Supplier B"]:
                st.info(f"No projects/tasks currently assigned to {user_role}.")
            else:
                st.info("No projects/tasks added yet.")


# --- Audit Management Module ---
with tabs[4]: # Corresponding to "📋 Audit Management"
    st.subheader("Audit Management")
    st.markdown("Manage audit points, track their status, and assign resolutions.")

    audits_df = load_data(AUDITS_FILE, columns=audit_columns)

    if user_role not in ["OEM", "Auditor"]:
        st.warning("🔒 You must be logged in as 'OEM' or 'Auditor' to manage audits.")
    else:
        st.markdown("### Add New Audit Point")
        with st.form("new_audit_form"):
            new_point_description = st.text_area("Audit Point Description", key="new_audit_desc")
            new_status = st.selectbox("Status", ["Open", "In Progress", "Closed", "Requires Supplier Input"], key="new_audit_status")
            new_assignee = st.text_input("Assignee (Name/Role)", key="new_audit_assignee")
            new_due_date = st.date_input("Due Date", value=datetime.today() + timedelta(days=14), key="new_audit_due_date")
            new_resolution = st.text_area("Resolution Notes (Optional)", key="new_audit_res")
            new_input_pending_audit = st.checkbox("Input Pending from Supplier?", value=False, key="new_audit_input_pending")

            submit_audit = st.form_submit_button("Add Audit Point")

            if submit_audit:
                if new_point_description and new_assignee:
                    audit_id = "AUDIT" + str(len(audits_df) + 1).zfill(4)
                    new_entry = pd.DataFrame([{
                        "audit_id": audit_id,
                        "point_description": new_point_description,
                        "status": new_status,
                        "assignee": new_assignee,
                        "due_date": new_due_date.isoformat(),
                        "resolution": new_resolution,
                        "input_pending": new_input_pending_audit
                    }])
                    append_data(AUDITS_FILE, new_entry)
                    st.success(f"Audit point added successfully: '{new_point_description[:30]}...'")
                    st.rerun()
                else:
                    st.error("Please fill in Audit Point Description and Assignee.")
        
        st.markdown("### Existing Audit Points")
        
        # Filter audits for non-OEM/Auditor roles (e.g., Suppliers can see audits assigned to them)
        if user_role == "OEM" or user_role == "Auditor":
            display_audits_df = audits_df
        elif user_role in ["Supplier A", "Supplier B"]:
            display_audits_df = audits_df[audits_df['assignee'] == user_role]
            if display_audits_df.empty:
                st.info(f"No audit points assigned to {user_role}.")
        else: # For other roles, just show all but no edit/delete
            display_audits_df = audits_df

        # Apply search and filter to audit data
        display_audits_df = apply_search_and_filter(display_audits_df, "audit_search", "audit_advanced_search")

        if not display_audits_df.empty:
            st.dataframe(display_audits_df, use_container_width=True, hide_index=True)

            if user_role == "OEM" or user_role == "Auditor": # Only allow editing/deleting for OEM and Auditor
                selected_audit_id = st.selectbox("Select Audit ID to Edit/Delete", [''] + display_audits_df['audit_id'].tolist(), key="select_audit_edit_del")

                if selected_audit_id:
                    selected_audit = audits_df[audits_df['audit_id'] == selected_audit_id].iloc[0]
                    st.markdown(f"#### Edit Audit Point: {selected_audit['point_description'][:50]}...")
                    with st.form("edit_audit_form"):
                        edit_point_description = st.text_area("Audit Point Description", value=selected_audit['point_description'], key="edit_audit_desc")
                        edit_status = st.selectbox("Status", ["Open", "In Progress", "Closed", "Requires Supplier Input"], index=["Open", "In Progress", "Closed", "Requires Supplier Input"].index(selected_audit['status']), key="edit_audit_status")
                        edit_assignee = st.text_input("Assignee (Name/Role)", value=selected_audit['assignee'], key="edit_audit_assignee")
                        
                        try:
                            default_audit_due = datetime.strptime(str(selected_audit['due_date']), '%Y-%m-%d').date()
                        except (ValueError, TypeError):
                            default_audit_due = datetime.today().date()
                        edit_due_date = st.date_input("Due Date", value=default_audit_due, key="edit_audit_due_date")
                        edit_resolution = st.text_area("Resolution Notes", value=selected_audit['resolution'], key="edit_audit_res")
                        edit_input_pending_audit = st.checkbox("Input Pending from Supplier?", value=bool(selected_audit['input_pending']), key="edit_audit_input_pending")

                        update_audit_btn = st.form_submit_button("Update Audit Point")
                        delete_audit_btn = st.form_submit_button("Delete Audit Point")

                        if update_audit_btn:
                            idx = audits_df[audits_df['audit_id'] == selected_audit_id].index[0]
                            audits_df.loc[idx] = {
                                "audit_id": selected_audit_id,
                                "point_description": edit_point_description,
                                "status": edit_status,
                                "assignee": edit_assignee,
                                "due_date": edit_due_date.isoformat(),
                                "resolution": edit_resolution,
                                "input_pending": edit_input_pending_audit
                            }
                            update_data(AUDITS_FILE, audits_df)
                            st.success(f"Audit point '{edit_point_description[:30]}...' updated successfully!")
                            st.rerun()
                        
                        if delete_audit_btn:
                            audits_df = audits_df[audits_df['audit_id'] != selected_audit_id]
                            update_data(AUDITS_FILE, audits_df)
                            st.warning(f"Audit point '{selected_audit['point_description'][:30]}...' deleted.")
                            st.rerun()
            else:
                st.info("Select an audit point above to see details.")
        else:
            if user_role in ["Supplier A", "Supplier B"]:
                st.info(f"No audit points currently assigned to {user_role}.")
            else:
                st.info("No audit points added yet.")


# --- File Management Module ---
with tabs[5]: # Corresponding to "📁 File Management"
    st.subheader("File Management")
    st.markdown("Upload, download, and manage important documents.")

    files_df = st.session_state.files_df # Use session state for files_df
    file_comments_df = st.session_state.file_comments_df # Use session state for comments_df

    if user_role not in ["OEM", "Supplier A", "Supplier B", "Auditor"]:
        st.warning("🔒 You must be logged in as 'OEM', 'Supplier', or 'Auditor' to access File Management.")
    else:
        st.markdown("### Upload New File")
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "doc", "docx", "txt", "csv", "xlsx", "png", "jpg", "jpeg"])

        if uploaded_file is not None:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
            
            # Create a unique filename to prevent overwrites
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
            save_path = os.path.join(DATA_DIR, "uploaded_files", unique_filename) # Store in a subfolder

            # Ensure the subfolder exists
            os.makedirs(os.path.join(DATA_DIR, "uploaded_files"), exist_ok=True)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            file_id = "FILE" + str(len(files_df) + 1).zfill(4) # Add file_id for better management if needed
            new_file_entry = pd.DataFrame([{
                "filename": uploaded_file.name,
                "type": uploaded_file.type,
                "size": uploaded_file.size,
                "uploader": user_role,
                "timestamp": datetime.now().isoformat(),
                "path": save_path
            }])
            append_data(FILES_FILE, new_file_entry)
            st.session_state.files_df = load_data(FILES_FILE, columns=["filename", "type", "size", "uploader", "timestamp", "path"]) # Reload
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            st.rerun()

        st.markdown("### Existing Files")

        # Display files relevant to the user role
        if user_role == "OEM" or user_role == "Auditor":
            display_files_df = files_df
        else: # Suppliers can only see files they uploaded
            display_files_df = files_df[files_df['uploader'] == user_role]
            if display_files_df.empty:
                st.info(f"No files uploaded by {user_role}.")

        display_files_df = apply_search_and_filter(display_files_df, "file_search", "file_advanced_search")

        if not display_files_df.empty:
            st.dataframe(display_files_df, use_container_width=True, hide_index=True)

            selected_file_name = st.selectbox("Select a file to view comments or download", [''] + display_files_df['filename'].tolist(), key="select_file_for_action")

            if selected_file_name:
                selected_file_row = display_files_df[display_files_df['filename'] == selected_file_name].iloc[0]
                
                st.markdown(f"#### Actions for: {selected_file_name}")
                col_file_actions1, col_file_actions2 = st.columns(2)
                
                with col_file_actions1:
                    try:
                        with open(selected_file_row['path'], "rb") as f:
                            st.download_button(
                                label=f"Download {selected_file_name}",
                                data=f,
                                file_name=selected_file_name,
                                mime=selected_file_row['type']
                            )
                    except FileNotFoundError:
                        st.error("File not found on server. It might have been moved or deleted.")
                
                with col_file_actions2:
                    if st.button(f"Delete {selected_file_name}", key="delete_file_btn"):
                        # Ensure actual file is deleted
                        try:
                            os.remove(selected_file_row['path'])
                            files_df = files_df[files_df['filename'] != selected_file_name]
                            update_data(FILES_FILE, files_df)
                            st.session_state.files_df = files_df # Update session state
                            # Also delete associated comments
                            st.session_state.file_comments_df = st.session_state.file_comments_df[st.session_state.file_comments_df['file_name'] != selected_file_name]
                            update_data(FILE_COMMENTS_FILE, st.session_state.file_comments_df)
                            st.warning(f"File '{selected_file_name}' and its comments deleted.")
                            st.rerun()
                        except FileNotFoundError:
                            st.warning(f"File '{selected_file_name}' not found on disk, removing from record only.")
                            files_df = files_df[files_df['filename'] != selected_file_name]
                            update_data(FILES_FILE, files_df)
                            st.session_state.files_df = files_df
                            st.session_state.file_comments_df = st.session_state.file_comments_df[st.session_state.file_comments_df['file_name'] != selected_file_name]
                            update_data(FILE_COMMENTS_FILE, st.session_state.file_comments_df)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting file: {e}")

                st.markdown(f"---")
                st.markdown(f"#### Comments for {selected_file_name}")

                current_file_comments = file_comments_df[file_comments_df['file_name'] == selected_file_name]

                if not current_file_comments.empty:
                    # Display top-level comments first
                    top_level_comments = current_file_comments[current_file_comments['parent_comment_id'].isna()]
                    
                    for idx, comment in top_level_comments.iterrows():
                        st.markdown(f"""
                            <div class="comment-card">
                                <div class="comment-meta">
                                    <strong>{comment['author']}</strong> commented on {pd.to_datetime(comment['timestamp']).strftime('%Y-%m-%d %H:%M')}
                                </div>
                                <div class="comment-body">{comment['comment_text']}</div>
                                {'<div class="comment-meta">Mentions: ' + ', '.join(eval(comment['mentions'])) + '</div>' if comment['mentions'] and eval(comment['mentions']) else ''}
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Display replies to this comment
                        replies = current_file_comments[current_file_comments['parent_comment_id'] == comment['comment_id']]
                        if not replies.empty:
                            st.markdown('<div class="reply-to-comment">', unsafe_allow_html=True)
                            st.markdown("##### Replies:")
                            for ridx, reply in replies.iterrows():
                                st.markdown(f"""
                                    <div class="comment-card">
                                        <div class="comment-meta">
                                            <strong>{reply['author']}</strong> replied on {pd.to_datetime(reply['timestamp']).strftime('%Y-%m-%d %H:%M')}
                                        </div>
                                        <div class="comment-body">{reply['comment_text']}</div>
                                        {'<div class="comment-meta">Mentions: ' + ', '.join(eval(reply['mentions'])) + '</div>' if reply['mentions'] and eval(reply['mentions']) else ''}
                                    </div>
                                """, unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No comments for this file yet.")
                
                st.markdown("---")
                st.markdown("#### Add a New Comment")
                with st.form(key=f"add_comment_to_{selected_file_name}"):
                    comment_text = st.text_area("Your Comment", key=f"comment_text_{selected_file_name}")
                    
                    # Allow mentioning roles or specific suppliers/OEM
                    all_mentionable_roles = user_roles + supplier_df['supplier_name'].tolist() + ['OEM']
                    selected_mentions = st.multiselect("Mention (Optional)", all_mentionable_roles, key=f"mentions_{selected_file_name}")

                    add_comment_btn = st.form_submit_button("Post Comment")

                    if add_comment_btn:
                        if comment_text:
                            comment_id = "COMM" + str(len(file_comments_df) + 1).zfill(4)
                            new_comment = pd.DataFrame([{
                                "comment_id": comment_id,
                                "file_name": selected_file_name,
                                "parent_comment_id": None, # Top-level comment
                                "author": user_role,
                                "timestamp": datetime.now().isoformat(),
                                "comment_text": comment_text,
                                "mentions": str(selected_mentions) # Store as string representation of list
                            }])
                            append_data(FILE_COMMENTS_FILE, new_comment)
                            st.session_state.file_comments_df = load_data(FILE_COMMENTS_FILE, columns=file_comment_columns) # Reload
                            st.session_state.file_comments_df['mentions'] = st.session_state.file_comments_df['mentions'].apply(lambda x: eval(x) if isinstance(x, str) else [])
                            st.success("Comment added!")
                            st.rerun()
                        else:
                            st.warning("Comment cannot be empty.")
        else:
            st.info("No files uploaded yet.")


# --- Mailbox Module ---
with tabs[6]: # Corresponding to "📧 Mailbox"
    st.subheader("Mailbox")
    st.markdown("Communicate securely with OEM, suppliers, and auditors.")

    notifications_df = st.session_state.notifications_df

    st.markdown('<div class="mailbox-container">', unsafe_allow_html=True)

    # Mailbox Navigation
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    with col_nav1:
        if st.button("Inbox", key="inbox_btn"):
            st.session_state.mailbox_view = "inbox"
            st.session_state.selected_notification_id = None
    with col_nav2:
        if st.button("Sent", key="sent_btn"):
            st.session_state.mailbox_view = "sent"
            st.session_state.selected_notification_id = None
    with col_nav3:
        if st.button("Compose", key="compose_btn"):
            st.session_state.mailbox_view = "compose"
            st.session_state.selected_notification_id = None

    st.markdown("---")

    if st.session_state.mailbox_view == "inbox":
        st.markdown("### Inbox")
        # Filter messages received by the current user_role or specific supplier name
        if user_role in ["OEM", "Auditor"]: # OEMs and Auditors receive messages addressed to their role
            my_inbox = notifications_df[(notifications_df['recipient_role'] == user_role) | (notifications_df['recipient_role'].isin(user_roles) & (notifications_df['sender_role'] != user_role))]
        else: # Suppliers receive messages specifically addressed to their name
            my_inbox = notifications_df[notifications_df['recipient_role'] == user_role]
        
        # Filter out replies for initial view (only show top-level messages)
        my_inbox = my_inbox[my_inbox['parent_notification_id'].isna()].sort_values(by="timestamp", ascending=False)

        if not my_inbox.empty:
            for idx, message in my_inbox.iterrows():
                is_unread = (message['status'] != 'Read')
                card_class = "message-card unread" if is_unread else "message-card"
                
                # Display clickable message card
                st.markdown(f"""
                    <div class="{card_class}" onclick="
                        const el = document.getElementById('notification_{message['notification_id']}');
                        if (el) el.click();
                    ">
                        <h5>Subject: {message['subject']}</h5>
                        <p>From: {message['sender_role']}</p>
                        <div class="message-meta">
                            <span>{pd.to_datetime(message['timestamp']).strftime('%Y-%m-%d %H:%M')}</span>
                            <span>Status: {message['status']}</span>
                        </div>
                        <button id="notification_{message['notification_id']}" style="display:none;"></button>
                    </div>
                """, unsafe_allow_html=True)
                
                # Hidden button to trigger Streamlit state change on click
                if st.button(f"view_msg_{message['notification_id']}", key=f"view_msg_btn_{message['notification_id']}", help="Click to view message details", use_container_width=False):
                    st.session_state.selected_notification_id = message['notification_id']
                    st.session_state.mailbox_view = "view_message"
                    st.rerun()
        else:
            st.info("Your inbox is empty.")

    elif st.session_state.mailbox_view == "sent":
        st.markdown("### Sent Messages")
        my_sent_messages = notifications_df[notifications_df['sender_role'] == user_role].sort_values(by="timestamp", ascending=False)
        # Filter out replies for initial view (only show top-level messages)
        my_sent_messages = my_sent_messages[my_sent_messages['parent_notification_id'].isna()]

        if not my_sent_messages.empty:
            for idx, message in my_sent_messages.iterrows():
                st.markdown(f"""
                    <div class="message-card" onclick="
                        const el = document.getElementById('notification_{message['notification_id']}');
                        if (el) el.click();
                    ">
                        <h5>Subject: {message['subject']}</h5>
                        <p>To: {message['recipient_role']}</p>
                        <div class="message-meta">
                            <span>{pd.to_datetime(message['timestamp']).strftime('%Y-%m-%d %H:%M')}</span>
                            <span>Status: {message['status']}</span>
                        </div>
                        <button id="notification_{message['notification_id']}" style="display:none;"></button>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"view_sent_msg_{message['notification_id']}", key=f"view_sent_msg_btn_{message['notification_id']}", help="Click to view message details", use_container_width=False):
                    st.session_state.selected_notification_id = message['notification_id']
                    st.session_state.mailbox_view = "view_message"
                    st.rerun()
        else:
            st.info("You haven't sent any messages yet.")

    elif st.session_state.mailbox_view == "compose":
        st.markdown("### Compose New Message")
        with st.form("new_message_form"):
            recipient_options = [r for r in user_roles if r != user_role] + supplier_df['supplier_name'].tolist() # Allow sending to roles or specific suppliers
            new_recipient = st.selectbox("Recipient", [''] + sorted(list(set(recipient_options))), key="new_msg_recipient")
            new_subject = st.text_input("Subject", key="new_msg_subject")
            new_message_body = st.text_area("Message", height=200, key="new_msg_body")
            
            send_message_btn = st.form_submit_button("Send Message")

            if send_message_btn:
                if new_recipient and new_subject and new_message_body:
                    notification_id = "NOTIF" + str(len(notifications_df) + 1).zfill(4)
                    new_entry = pd.DataFrame([{
                        "notification_id": notification_id,
                        "sender_role": user_role,
                        "recipient_role": new_recipient,
                        "subject": new_subject,
                        "message": new_message_body,
                        "timestamp": datetime.now().isoformat(),
                        "status": "Sent",
                        "parent_notification_id": None
                    }])
                    append_data(NOTIFICATIONS_FILE, new_entry)
                    st.session_state.notifications_df = load_data(NOTIFICATIONS_FILE, columns=notification_columns) # Reload
                    st.success("Message sent successfully!")
                    st.session_state.mailbox_view = "sent" # Go to sent items after sending
                    st.rerun()
                else:
                    st.error("Please fill in Recipient, Subject, and Message.")

    elif st.session_state.mailbox_view == "view_message":
        if st.session_state.selected_notification_id:
            selected_message = notifications_df[notifications_df['notification_id'] == st.session_state.selected_notification_id].iloc[0]

            # Mark as read if it's an inbox message
            if selected_message['recipient_role'] == user_role and selected_message['status'] != 'Read':
                idx = notifications_df[notifications_df['notification_id'] == st.session_state.selected_notification_id].index[0]
                notifications_df.loc[idx, 'status'] = 'Read'
                update_data(NOTIFICATIONS_FILE, notifications_df)
                st.session_state.notifications_df = notifications_df # Update session state

            st.markdown(f"""
                <div class="message-detail-view">
                    <h4>Subject: {selected_message['subject']}</h4>
                    <p><strong>From:</strong> {selected_message['sender_role']}</p>
                    <p><strong>To:</strong> {selected_message['recipient_role']}</p>
                    <p><strong>Date:</strong> {pd.to_datetime(selected_message['timestamp']).strftime('%Y-%m-%d %H:%M')}</p>
                    <p><strong>Status:</strong> {selected_message['status']}</p>
                    <div class="message-body">{selected_message['message']}</div>
                </div>
            """, unsafe_allow_html=True)

            # Display replies (if any)
            st.markdown("<div class='reply-list'>", unsafe_allow_html=True)
            replies_to_message = notifications_df[
                notifications_df['parent_notification_id'] == st.session_state.selected_notification_id
            ].sort_values(by='timestamp', ascending=True)

            if not replies_to_message.empty:
                st.markdown("<h5>Conversation History:</h5>")
                for _, reply in replies_to_message.iterrows():
                    st.markdown(f"""
                        <div class="single-reply">
                            <div class="reply-meta">From: {reply['sender_role']} on {pd.to_datetime(reply['timestamp']).strftime('%Y-%m-%d %H:%M')}</div>
                            <div>{reply['message']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Reply section (only if recipient or sender matches current user)
            if user_role == selected_message['recipient_role'] or user_role == selected_message['sender_role']:
                st.markdown("<div class='reply-section'>", unsafe_allow_html=True)
                with st.form("reply_message_form", clear_on_submit=True):
                    reply_text = st.text_area("Reply to this message:", height=100, key="reply_text_area")
                    
                    if st.form_submit_button("Send Reply"):
                        if reply_text:
                            reply_id = "NOTIF" + str(len(notifications_df) + 1).zfill(4)
                            reply_entry = pd.DataFrame([{
                                "notification_id": reply_id,
                                "sender_role": user_role,
                                "recipient_role": selected_message['sender_role'] if user_role == selected_message['recipient_role'] else selected_message['recipient_role'], # Reply to sender if you are recipient, else to recipient
                                "subject": f"Re: {selected_message['subject']}",
                                "message": reply_text,
                                "timestamp": datetime.now().isoformat(),
                                "status": "Sent",
                                "parent_notification_id": selected_message['notification_id']
                            }])
                            append_data(NOTIFICATIONS_FILE, reply_entry)
                            st.session_state.notifications_df = load_data(NOTIFICATIONS_FILE, columns=notification_columns) # Reload
                            
                            # Update original message status to 'Replied' if current user is the recipient
                            if user_role == selected_message['recipient_role']:
                                idx = notifications_df[notifications_df['notification_id'] == selected_message['notification_id']].index[0]
                                notifications_df.loc[idx, 'status'] = 'Replied'
                                update_data(NOTIFICATIONS_FILE, notifications_df)
                                st.session_state.notifications_df = notifications_df # Update session state

                            st.success("Reply sent!")
                            st.rerun() # Rerun to show new reply and update status
                        else:
                            st.warning("Reply cannot be empty.")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("You can only reply to messages you sent or received.")
        else:
            st.warning("No message selected.")

    st.markdown('</div>', unsafe_allow_html=True)


# --- Calendar Module ---
with tabs[7]: # Corresponding to "🗓️ Calendar"
    st.subheader("Event Calendar")
    st.markdown("View upcoming events, meetings, and deadlines.")

    events_df = st.session_state.events_df

    if user_role not in ["OEM", "Supplier A", "Supplier B", "Auditor"]:
        st.warning("🔒 You must be logged in as 'OEM', 'Supplier', or 'Auditor' to view the Calendar.")
    else:
        st.markdown("### Create New Event")
        with st.form("new_event_form"):
            new_event_title = st.text_input("Event Title", key="new_event_title")
            new_event_description = st.text_area("Description", key="new_event_desc")
            
            col_event_date1, col_event_date2 = st.columns(2)
            with col_event_date1:
                new_event_start_date = st.date_input("Start Date", value=datetime.today(), key="new_event_start_date")
            with col_event_date2:
                new_event_end_date = st.date_input("End Date", value=datetime.today() + timedelta(hours=1), key="new_event_end_date") # Default to same day

            # Attendees can be roles or specific supplier names
            all_attendee_options = user_roles + supplier_df['supplier_name'].tolist()
            new_event_attendees = st.multiselect("Attendees (Roles or Specific Suppliers)", sorted(list(set(all_attendee_options))), key="new_event_attendees")

            submit_event = st.form_submit_button("Add Event")

            if submit_event:
                if new_event_title and new_event_start_date and new_event_end_date:
                    event_id = "EVENT" + str(len(events_df) + 1).zfill(4)
                    new_entry = pd.DataFrame([{
                        "event_id": event_id,
                        "title": new_event_title,
                        "description": new_event_description,
                        "start_date": new_event_start_date.isoformat(),
                        "end_date": new_event_end_date.isoformat(),
                        "attendees": str(new_event_attendees), # Store list as string
                        "created_by": user_role,
                        "timestamp": datetime.now().isoformat()
                    }])
                    append_data(EVENTS_FILE, new_entry)
                    st.session_state.events_df = load_data(EVENTS_FILE, columns=event_columns) # Reload
                    # Ensure 'attendees' column is parsed as list when reloaded
                    st.session_state.events_df['attendees'] = st.session_state.events_df['attendees'].apply(lambda x: eval(x) if isinstance(x, str) else [])
                    st.success(f"Event '{new_event_title}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in Event Title, Start Date, and End Date.")

        st.markdown("### Upcoming Events")

        if not events_df.empty:
            # Convert date columns to datetime objects
            events_df['start_date'] = pd.to_datetime(events_df['start_date'], errors='coerce')
            events_df['end_date'] = pd.to_datetime(events_df['end_date'], errors='coerce')
            
            # Filter events for current user
            # User is an attendee if their role is in the 'attendees' list or their specific supplier name is in it
            user_specific_events = events_df[
                events_df['attendees'].apply(lambda x: user_role in x if isinstance(x, list) else False)
            ].copy() # Use .copy() to avoid SettingWithCopyWarning

            # Filter for upcoming events
            upcoming_events = user_specific_events[user_specific_events['end_date'] >= datetime.now()].sort_values(by='start_date', ascending=True)

            if not upcoming_events.empty:
                for idx, event in upcoming_events.iterrows():
                    st.markdown(f"""
                        <div class="message-card">
                            <h5>🗓️ {event['title']}</h5>
                            <p><strong>Description:</strong> {event['description']}</p>
                            <p><strong>Dates:</strong> {event['start_date'].strftime('%Y-%m-%d')} to {event['end_date'].strftime('%Y-%m-%d')}</p>
                            <p><strong>Attendees:</strong> {', '.join(event['attendees'])}</p>
                            <p><strong>Created By:</strong> {event['created_by']}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"No upcoming events found for {user_role}.")
        else:
            st.info("No events added yet.")

