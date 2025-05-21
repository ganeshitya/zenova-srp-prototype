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

    /* Search Bar Styling */
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
</style>
""", unsafe_allow_html=True)


# --- File Paths & Directory Setup ---
DATA_DIR = "data"
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, "notifications.csv")
FILES_FILE = os.path.join(DATA_DIR, "uploaded_files.csv")
PROJECTS_FILE = os.path.join(DATA_DIR, "project_tasks.csv")
ASSETS_FILE = os.path.join(DATA_DIR, "assets.csv")
AUDITS_FILE = os.path.join(DATA_DIR, "audit_points.csv")
EVENTS_FILE = os.path.join(DATA_DIR, "events.csv") # NEW CALENDAR EVENTS FILE
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
project_columns = ["task_id", "task_name", "status", "assigned_to", "due_date", "description", "input_pending"]
initialize_csv(PROJECTS_FILE, project_columns)
asset_columns = ["asset_id", "asset_name", "location", "status", "eol_date", "calibration_date", "notes", "supplier"]
initialize_csv(ASSETS_FILE, asset_columns)
audit_columns = ["audit_id", "point_description", "status", "assignee", "due_date", "resolution", "input_pending"]
initialize_csv(AUDITS_FILE, audit_columns)
event_columns = [
    "event_id", "title", "description", "start_date", "end_date",
    "attendees", "created_by", "timestamp"
]
initialize_csv(EVENTS_FILE, event_columns) # NEW
supplier_columns = [
    "supplier_id", "supplier_name", "contact_person", "email", "phone",
    "agreement_status", "last_audit_score", "notes",
    "primary_product_category", "on_time_delivery_rate", "quality_reject_rate",
    "risk_level", "certification", "annual_spend_usd", "last_performance_review_date"
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
    "🗓️ Calendar" # NEW CALENDAR TAB
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

        # Apply search and filter to supplier_df (example, adjust for other DFs if needed)
        st.markdown("---")
        st.subheader("Supplier Performance & Financial Overview")
        st.markdown("You can search and filter the supplier data below.")
        filtered_supplier_df = apply_search_and_filter(supplier_df, "oem_dashboard_search", "oem_dashboard_advance_search")

        if not filtered_supplier_df.empty:
            st.dataframe(filtered_supplier_df, use_container_width=True, hide_index=True)
        else:
            st.info("No supplier data matching your search/filter criteria.")


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
                        (supplier_df['last_performance_review_date'].notna()) &
                        (supplier_df['last_performance_review_date'] < (datetime.today() - timedelta(days=365)))
                    ]
                    if not overdue_reviews.empty:
                        st.dataframe(overdue_reviews[['supplier_name', 'contact_person', 'email', 'last_performance_review_date']],
                                     use_container_width=True, hide_index=True)
                    else:
                        st.success("✅ All supplier performance reviews are up-to-date (within the last year).")
                else:
                    st.info("No supplier data to check for overdue reviews.")


        st.markdown("---")
        st.subheader("Operational Status Overview")

        with st.container():
            col_ops1, col_ops2, col_ops3 = st.columns(3)

            with col_ops1:
                st.markdown("##### 🚀 Project Task Status")
                if not projects_df.empty:
                    projects_df['status'] = projects_df['status'].fillna('Unknown').astype(str)
                    task_status_counts = projects_df['status'].value_counts().reset_index()
                    task_status_counts.columns = ['Status', 'Count']
                    fig_tasks = px.pie(task_status_counts, values='Count', names='Status',
                                       title='Project Task Distribution', hole=0.3,
                                       template='plotly_dark') # Set dark theme for Plotly
                    fig_tasks.update_traces(textposition='inside', textinfo='percent+label')
                    fig_tasks.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20), height=250)
                    st.plotly_chart(fig_tasks, use_container_width=True)
                else:
                    st.info("No project task data. Add tasks in '📅 Project Management'.")

            with col_ops2:
                st.markdown("##### 📦 Asset Status")
                if not assets_df.empty:
                    assets_df['status'] = assets_df['status'].fillna('Unknown').astype(str)
                    asset_status_counts = assets_df['status'].value_counts().reset_index()
                    asset_status_counts.columns = ['Status', 'Count']
                    fig_assets = px.pie(asset_status_counts, values='Count', names='Status',
                                        title='Asset Status Distribution', hole=0.3,
                                        template='plotly_dark') # Set dark theme for Plotly
                    fig_assets.update_traces(textposition='inside', textinfo='percent+label')
                    fig_assets.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20), height=250)
                    st.plotly_chart(fig_assets, use_container_width=True)
                else:
                    st.info("No asset data. Add assets in '🛠️ Asset Management'.")

            with col_ops3:
                st.markdown("##### ✅ Audit Point Status")
                if not audits_df.empty:
                    audits_df['status'] = audits_df['status'].fillna('Unknown').astype(str)
                    audit_status_counts = audits_df['status'].value_counts().reset_index()
                    audit_status_counts.columns = ['Status', 'Count']
                    fig_audits = px.pie(audit_status_counts, values='Count', names='Status',
                                        title='Audit Point Distribution', hole=0.3,
                                        template='plotly_dark') # Set dark theme for Plotly
                    fig_audits.update_traces(textposition='inside', textinfo='percent+label')
                    fig_audits.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20), height=250)
                    st.plotly_chart(fig_audits, use_container_width=True)
                else:
                    st.info("No audit data. Add audit points in '📋 Audit Management'.")

        st.markdown("---")
        with st.container():
            st.markdown("#### ⏱️ Key Performance Metrics")
            col_metrics1, col_metrics2 = st.columns(2)

            with col_metrics1:
                st.markdown("##### Avg. Project Delivery Time")
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
                            st.metric(label="Days to Deliver (Active Tasks)", value=f"{avg_days:.1f} days")
                        else:
                            st.info("All active tasks are past their due date or have no future due date.")
                    else:
                        st.info("No active tasks to calculate average time to deliver.")
                else:
                    st.info("No project data to calculate time to deliver.")

            with col_metrics2:
                st.markdown("##### 📥 Inputs Pending")
                total_pending_input = 0
                if not projects_df.empty:
                    projects_df['input_pending'] = projects_df['input_pending'].fillna('No').astype(str)
                    project_inputs_pending = projects_df[projects_df['input_pending'] == "Yes"].shape[0]
                    total_pending_input += project_inputs_pending
                    st.markdown(f"- **Project Tasks:** `{project_inputs_pending}` pending input")

                if not audits_df.empty:
                    audits_df['input_pending'] = audits_df['input_pending'].fillna('No').astype(str)
                    audit_inputs_pending = audits_df[audits_df['input_pending'] == "Yes"].shape[0]
                    total_pending_input += audit_inputs_pending
                    st.markdown(f"- **Audit Points:** `{audit_inputs_pending}` pending input")

                if projects_df.empty and audits_df.empty:
                    st.info("No project or audit data to check for pending inputs.")
                elif total_pending_input == 0:
                    st.success("🎉 No inputs are currently pending!")
                st.metric(label="Total Pending Inputs", value=f"{total_pending_input}")

        st.markdown("---")
        with st.container():
            st.markdown("#### 🔗 Supplier-Associated Assets")
            if not assets_df.empty:
                assets_df['supplier'] = assets_df['supplier'].fillna('Unassigned').astype(str)
                parts_by_supplier = assets_df.groupby('supplier').size().reset_index(name='Number of Assets')
                fig_parts = px.bar(parts_by_supplier, x='supplier', y='Number of Assets',
                                   title='Assets Managed by Each Supplier', color='supplier',
                                   color_discrete_sequence=px.colors.qualitative.Bold,
                                   template='plotly_dark') # Set dark theme for Plotly
                fig_parts.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=300)
                st.plotly_chart(fig_parts, use_container_width=True)
            else:
                st.info("No asset data to show supplier parts breakdown. Add assets in '🛠️ Asset Management'.")


# --- Supplier Records Module ---
with tabs[1]: # Corresponding to "👥 Supplier Records"
    st.subheader("Supplier Records")
    st.markdown("View and manage detailed information about your valued suppliers. This comprehensive database enables efficient supplier relationship management.")

    supplier_df = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=supplier_columns)
    
    st.markdown("---")
    st.subheader("Current Supplier Database")
    # Apply search and filter to supplier_df
    filtered_supplier_df = apply_search_and_filter(supplier_df, "supplier_records_search", "supplier_records_advance_search")

    if not filtered_supplier_df.empty:
        st.dataframe(filtered_supplier_df, use_container_width=True, hide_index=True)
    else:
        st.info("No supplier records available or no records matching your search/filter criteria. Please add new suppliers below.")

    st.markdown("---")
    with st.container():
        st.subheader("Add New Supplier Record")
        with st.expander("Click to add a new supplier", expanded=False):
            with st.form("new_supplier_form", clear_on_submit=True):
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    new_supplier_id = st.text_input("Supplier ID (e.g., SUP-006)", placeholder="e.g., SUP-001")
                with col_s2:
                    new_supplier_name = st.text_input("Supplier Name", placeholder="e.g., Global Parts Inc.")
                with col_s3:
                    new_contact_person = st.text_input("Contact Person", placeholder="e.g., Alice Smith")

                col_s4, col_s5, col_s6 = st.columns(3)
                with col_s4:
                    new_email = st.text_input("Email", placeholder="e.g., info@supplier.com")
                with col_s5:
                    new_phone = st.text_input("Phone", placeholder="+1-555-123-4567")
                with col_s6:
                    new_agreement_status = st.selectbox("Agreement Status", ["Active", "Pending Renewal", "Terminated", "On Hold"])

                new_last_audit_score = st.number_input("Last Audit Score (0-100)", min_value=0, max_value=100, value=80, key="new_last_audit_score")
                new_notes = st.text_area("Notes", placeholder="Any important notes about this supplier...")

                st.markdown("#### Additional Supplier Details:")
                col_s7, col_s8, col_s9 = st.columns(3)
                with col_s7:
                    new_primary_product_category = st.text_input("Primary Product Category", placeholder="e.g., Raw Materials, Electronic Components")
                with col_s8:
                    new_on_time_delivery_rate = st.slider("On-Time Delivery Rate (%)", min_value=0.0, max_value=100.0, value=95.0, step=0.1)
                with col_s9:
                    new_quality_reject_rate = st.slider("Quality Reject Rate (%)", min_value=0.0, max_value=10.0, value=0.5, step=0.1)

                col_s10, col_s11 = st.columns(2)
                with col_s10:
                    new_risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])
                with col_s11:
                    new_certification = st.text_input("Certifications (comma-separated)", placeholder="e.g., ISO 9001, IATF 16949")

                col_s12, col_s13 = st.columns(2)
                with col_s12:
                    new_annual_spend_usd = st.number_input("Annual Spend (USD)", min_value=0, value=100000, step=10000, format="%d")
                with col_s13:
                    new_last_performance_review_date = st.date_input("Last Performance Review Date", value=None, key="new_last_performance_review_date")

                supplier_submitted = st.form_submit_button("➕ Add Supplier Record")

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
                    st.success(f"✅ Supplier '{new_supplier_name}' ({new_supplier_id}) added successfully!")
                    st.rerun()
                elif supplier_submitted:
                    st.error("❗ Supplier ID and Supplier Name are required fields.")

# --- Asset Management Module ---
with tabs[2]: # Corresponding to "🛠️ Asset Management"
    st.subheader("Inter-Company Asset Management")
    st.markdown("Track and manage all critical assets across your OEM and supplier facilities, ensuring proper utilization and maintenance.")

    # Load supplier data for the dropdown
    supplier_df_for_selection = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=["supplier_name"])
    supplier_names_for_dropdown = supplier_df_for_selection['supplier_name'].tolist()
    if not supplier_names_for_dropdown:
        supplier_names_for_dropdown = ["N/A (No suppliers found)"] # Fallback if supplier file is empty

    st.markdown("---")
    st.subheader("Asset Inventory Log")
    assets_df = load_data(ASSETS_FILE, columns=asset_columns)
    
    # Apply search and filter to assets_df
    filtered_assets_df = apply_search_and_filter(assets_df, "asset_management_search", "asset_management_advance_search")

    if not filtered_assets_df.empty:
        st.dataframe(filtered_assets_df, use_container_width=True, hide_index=True)
    else:
        st.info("No assets logged yet or no assets matching your search/filter criteria. Add assets using the 'Add New Asset' expander below.")

    st.markdown("---")
    with st.container():
        st.subheader("Add New Asset")
        with st.expander("Click to log a new asset", expanded=False):
            with st.form("new_asset_form", clear_on_submit=True):
                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    asset_id_val = st.text_input("Asset ID (e.g., ZNV-TOOL-001)", placeholder="e.g., ZNV-TOOL-001")
                with col_a2:
                    asset_name = st.text_input("Asset Name/Description", placeholder="e.g., CNC Milling Machine, Robotic Arm")

                location = st.selectbox("Current Location", ["OEM Site", "Supplier A Facility", "Supplier B Warehouse", "In Transit"])
                asset_status_options = ["In Use", "In Storage", "Under Maintenance", "Awaiting Calibration", "End of Life (EOL)", "Scrapped"]
                asset_status = st.selectbox("Asset Status", asset_status_options)
                asset_supplier = st.selectbox("Associated Supplier", supplier_names_for_dropdown, help="Select the supplier currently using or managing this asset.")

                col_a3, col_a4 = st.columns(2)
                with col_a3:
                    eol_date = st.date_input("Estimated End of Life (EOL) Date", value=None, key="eol_date_asset")
                with col_a4:
                    calibration_date = st.date_input("Next Calibration Date", value=None, key="cal_date_asset")

                notes = st.text_area("Notes/Comments about the asset", placeholder="e.g., Last serviced on XYZ date, requires special lubricant.")
                asset_submitted = st.form_submit_button("➕ Add Asset")

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
                    st.success(f"✅ Asset '{asset_name}' ({asset_id_val}) added successfully!")
                    st.rerun()
                elif asset_submitted:
                    st.error("❗ Asset ID and Asset Name are required.")


# --- Project Management Module (Gantt) ---
with tabs[3]: # Corresponding to "📅 Project Management"
    st.subheader("Project Management Tool")
    st.markdown("Streamline and track all collaborative projects and tasks with your suppliers. Monitor progress, deadlines, and critical path items.")

    st.markdown("---")
    st.subheader("Current Project Tasks")
    projects_df = load_data(PROJECTS_FILE, columns=project_columns)

    # Apply search and filter to projects_df
    filtered_projects_df = apply_search_and_filter(projects_df, "project_management_search", "project_management_advance_search")

    if not filtered_projects_df.empty:
        st.dataframe(filtered_projects_df, use_container_width=True, hide_index=True)
        st.info("💡 Tip: For a full Gantt chart visualization, a dedicated library like Plotly's Timeline chart could be integrated.")
    else:
        st.info("No project tasks added yet or no tasks matching your search/filter criteria. Add tasks using the 'Add New Project Task' section below.")


    st.markdown("---")
    with st.container():
        st.subheader("Add New Project Task")
        with st.expander("Click to create a new task", expanded=False):
            with st.form("new_task_form", clear_on_submit=True):
                task_id = f"TASK-{int(datetime.now().timestamp())}"
                task_name = st.text_input("Task Name", placeholder="e.g., Develop new component prototype")
                description = st.text_area("Task Description", placeholder="Detailed description of the task and its objectives.")
                col_p1, col_p2, col_p3 = st.columns(3)
                with col_p1:
                    status_options = ["Open", "Work In Progress", "Blocked", "Pending Review", "Closed"]
                    status = st.selectbox("Status", status_options)
                with col_p2:
                    assigned_to = st.selectbox("Assigned To", user_roles + ["Unassigned", "Cross-functional Team"])
                with col_p3:
                    due_date = st.date_input("Due Date", min_value=datetime.today())

                input_pending_status = st.checkbox("Requires Input from Stakeholders?", value=False, help="Check if this task requires input or approval from other parties.")
                submitted = st.form_submit_button("➕ Add Task")

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
                    st.success(f"✅ Task '{task_name}' added successfully!")
                    st.rerun()
                elif submitted:
                    st.error("❗ Task Name is required.")


# --- Audit Management Module ---
with tabs[4]: # Corresponding to "📋 Audit Management"
    st.subheader("Supplier Assessment & Actions Tracking")
    st.markdown("Efficiently manage supplier audit findings, track corrective actions, and maintain a robust assessment history.")

    st.markdown("---")
    st.subheader("Audit Records & Open Points")
    audits_df = load_data(AUDITS_FILE, columns=audit_columns)
    
    # Apply search and filter to audits_df
    filtered_audits_df = apply_search_and_filter(audits_df, "audit_management_search", "audit_management_advance_search")

    if not filtered_audits_df.empty:
        st.dataframe(filtered_audits_df, use_container_width=True, hide_index=True)
    else:
        st.info("No audit points recorded yet or no audit points matching your search/filter criteria. Add audit points using the 'Add New Audit Point / Finding' section below.")


    st.markdown("---")
    with st.container():
        st.subheader("Add New Audit Point / Finding")
        with st.expander("Click to log a new audit point", expanded=False):
            with st.form("new_audit_point_form", clear_on_submit=True):
                audit_id_val = f"AUDIT-{int(datetime.now().timestamp())}"
                point_description = st.text_area("Audit Point/Finding Description", placeholder="e.g., Non-conformance in raw material batch #12345.")
                col_au1, col_au2, col_au3 = st.columns(3)
                with col_au1:
                    audit_status_options = ["Open", "In Progress", "Resolved", "Pending Verification", "Closed", "Deviation Accepted"]
                    audit_status = st.selectbox("Status", audit_status_options)
                with col_au2:
                    assignee = st.selectbox("Assignee", user_roles + ["Cross-functional Team"])
                with col_au3:
                    due_date_audit = st.date_input("Due Date for Resolution", min_value=datetime.today(), key="due_date_audit")

                resolution = st.text_area("Resolution / Corrective Action (if available)", placeholder="Describe actions taken to resolve the finding.")
                input_pending_audit = st.checkbox("Requires Input from Stakeholders?", value=False, help="Check if this audit point needs input or collaboration from others.")
                audit_submitted = st.form_submit_button("➕ Add Audit Point")

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
                    st.success(f"✅ Audit point '{audit_id_val}' added successfully!")
                    st.rerun()
                elif audit_submitted:
                    st.error("❗ Audit Point Description is required.")


# --- File Management Module ---
with tabs[5]: # Corresponding to "📁 File Management"
    st.subheader("Secured File Management & Version Control")
    st.markdown("Securely upload, store, and manage all critical documents with your suppliers. Ensure data integrity and controlled access.")

    st.markdown("---")
    st.subheader("Uploaded Files History")
    files_df = load_data(FILES_FILE, columns=["filename", "type", "size", "uploader", "timestamp", "path"])
    
    # Apply search and filter to files_df
    filtered_files_df = apply_search_and_filter(files_df, "file_management_search", "file_management_advance_search")

    if not filtered_files_df.empty:
        display_df = filtered_files_df.drop(columns=['path']) # Hide path from display table
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("##### Download Files")
        selected_file_name_to_download = st.selectbox("Select a file to download:", filtered_files_df['filename'].tolist(), key="download_file_select")
        if selected_file_name_to_download:
            file_to_download_path_series = filtered_files_df[filtered_files_df['filename'] == selected_file_name_to_download]['path']
            file_to_download_path = file_to_download_path_series.iloc[0] if not file_to_download_path_series.empty else ''

            if file_to_download_path and os.path.exists(file_to_download_path):
                with open(file_to_download_path, "rb") as file:
                    st.download_button(
                        label=f"⬇️ Download {selected_file_name_to_download}",
                        data=file,
                        file_name=selected_file_name_to_download,
                        mime=files_df[files_df['filename'] == selected_file_name_to_download]['type'].iloc[0],
                        key=f"download_btn_{selected_file_name_to_download}"
                    )
            else:
                st.warning(f"❗ File '{selected_file_name_to_download}' not found at path: {file_to_download_path}. It might be a dummy entry without a physical file, or the path is incorrect.")
    else:
        st.info("No files uploaded yet or no files matching your search/filter criteria. Use the section below to upload your documents.")


    st.markdown("---")
    with st.container():
        st.subheader("Upload New File")
        upload_folder_options = {"General Files": DATA_DIR, "Supplier Records (NDA/MSA)": SUPPLIER_RECORDS_DIR}
        selected_upload_folder_name = st.selectbox("Select Upload Destination Folder:", list(upload_folder_options.keys()))
        selected_upload_folder_path = upload_folder_options[selected_upload_folder_name]

        uploaded_file = st.file_uploader("Upload a document or image", type=["pdf", "docx", "xlsx", "txt", "png", "jpg", "jpeg"], key="file_uploader")

        if uploaded_file:
            save_path = os.path.join(selected_upload_folder_path, uploaded_file.name)
            try:
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

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

                # Basic Preview
                if uploaded_file.type == "application/pdf":
                    st.info("📄 PDF Preview (full preview would require a backend service or specialized library).")
                elif "image" in uploaded_file.type:
                    st.image(uploaded_file, caption=f"Preview of {uploaded_file.name}", use_column_width=True)
                else:
                    st.info("🔍 Preview not available for this file type in this demo.")
                st.rerun()

            except Exception as e:
                st.error(f"❗ Error saving file: {e}")

# --- Mailbox Module (NEW) ---
with tabs[6]: # Corresponding to "📧 Mailbox"
    st.subheader("Inter-Company Mailbox")
    st.markdown("Send notifications, receive messages, and manage communication with other entities within the Zenova SRP ecosystem.")

    st.markdown('<div class="mailbox-container">', unsafe_allow_html=True)

    # Mailbox Navigation Tabs
    mailbox_tabs = st.tabs(["📥 Inbox", "📤 Sent", "✍️ Compose Notification"])

    with mailbox_tabs[0]: # Inbox Tab
        st.markdown("### Your Received Notifications")
        
        # Apply search and filter to inbox messages
        inbox_messages_raw = st.session_state.notifications_df[
            (st.session_state.notifications_df['recipient_role'] == user_role) &
            (st.session_state.notifications_df['parent_notification_id'].isna()) # Only show top-level messages
        ].sort_values(by="timestamp", ascending=False)
        
        filtered_inbox_messages = apply_search_and_filter(inbox_messages_raw, "inbox_search", "inbox_advance_search")


        if filtered_inbox_messages.empty:
            st.info("Your inbox is empty or no messages matching your search/filter criteria.")
        else:
            st.markdown('<div style="max-height: 400px; overflow-y: auto;">', unsafe_allow_html=True) # Scrollable area for messages
            for idx, row in filtered_inbox_messages.iterrows():
                notification_id = row['notification_id']
                sender = row['sender_role']
                subject = row['subject']
                timestamp = row['timestamp']
                status = row['status']

                # Determine if the message is unread for the current user
                is_unread = (status != "Read" and status != "Replied" and row['recipient_role'] == user_role)

                card_class = "message-card unread" if is_unread else "message-card"
                
                # Use st.form_submit_button to make the entire card clickable
                with st.container():
                    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                    col_msg1, col_msg2 = st.columns([0.7, 0.3])
                    with col_msg1:
                        st.markdown(f"<h5>Subject: {subject}</h5>", unsafe_allow_html=True)
                        st.markdown(f"<p>From: {sender}</p>", unsafe_allow_html=True)
                    with col_msg2:
                        st.markdown(f"<div class='message-meta'><span>Status: {status}</span><span>{timestamp}</span></div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Create a hidden button to trigger the view when the div is clicked
                    # This is a common workaround for making custom clickable elements in Streamlit
                    if st.button("View", key=f"view_inbox_{notification_id}", use_container_width=True):
                        st.session_state.selected_notification_id = notification_id
                        st.session_state.mailbox_view = "view_message"
                        # Mark as read
                        if st.session_state.notifications_df.loc[idx, 'status'] == "Sent": # Only mark as read if it was just "Sent" (not already Replied)
                            st.session_state.notifications_df.loc[idx, 'status'] = "Read"
                            update_data(NOTIFICATIONS_FILE, st.session_state.notifications_df)
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True) # End scrollable area


    with mailbox_tabs[1]: # Sent Tab
        st.markdown("### Your Sent Notifications")

        # Filter messages where current user is the sender (top-level messages or replies)
        sent_messages_raw = st.session_state.notifications_df[
            st.session_state.notifications_df['sender_role'] == user_role
        ].sort_values(by="timestamp", ascending=False)

        # Filter out replies if the original message is also shown for the sender
        # For simplicity, let's just show all sent messages including replies for now
        # If needed, we can implement more complex threading logic
        filtered_sent_messages = apply_search_and_filter(sent_messages_raw, "sent_mailbox_search", "sent_mailbox_advance_search")

        if filtered_sent_messages.empty:
            st.info("You haven't sent any notifications yet or no messages matching your search/filter criteria.")
        else:
            st.markdown('<div style="max-height: 400px; overflow-y: auto;">', unsafe_allow_html=True) # Scrollable area for messages
            for idx, row in filtered_sent_messages.iterrows():
                notification_id = row['notification_id']
                recipient = row['recipient_role']
                subject = row['subject']
                timestamp = row['timestamp']
                status = row['status'] # Status from sender's perspective (e.g., "Sent", "Read", "Replied")
                parent_id = row['parent_notification_id']

                # Don't show replies as separate top-level items in sent list if the original is also listed
                if pd.notna(parent_id):
                    continue

                card_class = "message-card"
                
                with st.container():
                    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                    col_msg1, col_msg2 = st.columns([0.7, 0.3])
                    with col_msg1:
                        st.markdown(f"<h5>Subject: {subject}</h5>", unsafe_allow_html=True)
                        st.markdown(f"<p>To: {recipient}</p>", unsafe_allow_html=True)
                    with col_msg2:
                        st.markdown(f"<div class='message-meta'><span>Status: {status}</span><span>{timestamp}</span></div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    if st.button("View", key=f"view_sent_{notification_id}", use_container_width=True):
                        st.session_state.selected_notification_id = notification_id
                        st.session_state.mailbox_view = "view_message"
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True) # End scrollable area


    with mailbox_tabs[2]: # Compose Tab
        st.markdown("### Compose New Notification")

        # Define possible recipients based on user role
        available_recipients = []
        if user_role == "OEM":
            supplier_df_compose = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=["supplier_name"])
            available_recipients.extend(supplier_df_compose['supplier_name'].tolist())
            available_recipients.append("Auditor")
        elif user_role.startswith("Supplier") or user_role == "Auditor":
            available_recipients.append("OEM")

        if not available_recipients:
            st.warning("No available recipients for your role.")
        else:
            with st.form("compose_notification_form", clear_on_submit=True):
                recipient = st.selectbox("Recipient", available_recipients)
                subject = st.text_input("Subject")
                message_content = st.text_area("Message", height=200)

                send_button = st.form_submit_button("✉️ Send Notification")

                if send_button:
                    if recipient and subject and message_content:
                        new_notification_id = f"MSG-{int(datetime.now().timestamp())}-{np.random.randint(1000, 9999)}"
                        new_notification = {
                            "notification_id": new_notification_id,
                            "sender_role": user_role,
                            "recipient_role": recipient,
                            "subject": subject,
                            "message": message_content,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "Sent",
                            "parent_notification_id": None
                        }
                        append_data(NOTIFICATIONS_FILE, pd.DataFrame([new_notification]))
                        st.session_state.notifications_df = load_data(NOTIFICATIONS_FILE, columns=notification_columns) # Refresh dataframe
                        st.success(f"✅ Notification sent to {recipient}!")
                        st.session_state.mailbox_view = "sent" # Redirect to sent messages after sending
                        st.rerun()
                    else:
                        st.error("❗ Please fill in all fields (Recipient, Subject, Message).")

    # Display single message view
    if st.session_state.mailbox_view == "view_message" and st.session_state.selected_notification_id:
        selected_msg_id = st.session_state.selected_notification_id
        
        # Find the main message
        message_row = st.session_state.notifications_df[
            st.session_state.notifications_df['notification_id'] == selected_msg_id
        ]
        
        if not message_row.empty:
            message = message_row.iloc[0]
            
            # Get replies to this message (where parent_notification_id matches)
            replies_df = st.session_state.notifications_df[
                st.session_state.notifications_df['parent_notification_id'] == selected_msg_id
            ].sort_values(by="timestamp", ascending=True)

            st.markdown('<div class="message-detail-view">', unsafe_allow_html=True)
            st.button("↩️ Back to Inbox", on_click=lambda: (setattr(st.session_state, 'mailbox_view', 'inbox'), setattr(st.session_state, 'selected_notification_id', None)))

            st.markdown(f"#### Subject: {message['subject']}")
            st.markdown(f"<p><strong>From:</strong> {message['sender_role']} <strong>To:</strong> {message['recipient_role']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Sent:</strong> {message['timestamp']}</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='message-body'>{message['message']}</div>", unsafe_allow_html=True)

            # Display replies
            if not replies_df.empty:
                st.markdown("---")
                st.markdown("#### Replies:")
                st.markdown('<div class="reply-list">', unsafe_allow_html=True)
                for _, reply_row in replies_df.iterrows():
                    st.markdown(f"""
                        <div class="single-reply">
                            <div class="reply-meta">
                                From: {reply_row['sender_role']} | To: {reply_row['recipient_role']} | Sent: {reply_row['timestamp']}
                            </div>
                            <div>{reply_row['message']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Reply functionality (only if current user is the recipient of the main message)
            if message['recipient_role'] == user_role:
                st.markdown("---")
                st.markdown("#### Reply to this Notification")
                with st.form("reply_notification_form", clear_on_submit=True, key=f"reply_form_{selected_msg_id}"):
                    reply_message_content = st.text_area("Your Reply", height=100)
                    send_reply_button = st.form_submit_button("⬆️ Send Reply")

                    if send_reply_button:
                        if reply_message_content:
                            reply_id = f"REPLY-{int(datetime.now().timestamp())}-{np.random.randint(1000, 9999)}"
                            new_reply = {
                                "notification_id": reply_id,
                                "sender_role": user_role,
                                "recipient_role": message['sender_role'], # Reply goes back to the original sender
                                "subject": f"Re: {message['subject']}", # Subject auto-prefixed with Re:
                                "message": reply_message_content,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "status": "Sent",
                                "parent_notification_id": selected_msg_id # Link to the original message
                            }
                            append_data(NOTIFICATIONS_FILE, pd.DataFrame([new_reply]))
                            st.session_state.notifications_df = load_data(NOTIFICATIONS_FILE, columns=notification_columns) # Refresh dataframe

                            # Update status of the original message to "Replied"
                            original_msg_idx = st.session_state.notifications_df[
                                st.session_state.notifications_df['notification_id'] == selected_msg_id
                            ].index
                            if not original_msg_idx.empty:
                                st.session_state.notifications_df.loc[original_msg_idx[0], 'status'] = "Replied"
                                update_data(NOTIFICATIONS_FILE, st.session_state.notifications_df)

                            st.success("✅ Reply sent!")
                            st.rerun()
                        else:
                            st.error("Please type a reply message.")
            st.markdown('</div>', unsafe_allow_html=True) # End message-detail-view
        else:
            st.warning("Notification not found.")
            if st.button("Back to Inbox", key="back_to_inbox_not_found"):
                st.session_state.mailbox_view = "inbox"
                st.session_state.selected_notification_id = None
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True) # End mailbox-container

# --- Calendar Module (NEW) ---
with tabs[7]: # Corresponding to "🗓️ Calendar"
    st.subheader("Inter-Company Calendar")
    st.markdown("Coordinate events, meetings, and deadlines across all relevant stakeholders. All synchronized events are visible to all involved parties.")

    st.markdown("---")
    st.subheader("Upcoming Events")

    events_df = st.session_state.events_df.copy()

    # Filter events based on who is attending
    if not events_df.empty:
        # Convert 'attendees' column to list of strings for easier checking
        events_df['attendees'] = events_df['attendees'].apply(lambda x: eval(x) if isinstance(x, str) else x)
        
        # Filter for events where current user is an attendee or creator
        # Also filter for events that are in the future or ongoing
        filtered_events = events_df[
            (events_df['attendees'].apply(lambda x: user_role in x if isinstance(x, list) else False)) |
            (events_df['created_by'] == user_role)
        ].copy()

        # Convert date columns to datetime objects for proper sorting and comparison
        filtered_events['start_date'] = pd.to_datetime(filtered_events['start_date'], errors='coerce')
        filtered_events['end_date'] = pd.to_datetime(filtered_events['end_date'], errors='coerce')

        # Filter for events that are in the future or ongoing
        today = datetime.now().normalize()
        filtered_events = filtered_events[(filtered_events['end_date'] >= today) | (filtered_events['start_date'] >= today)]

        filtered_events = filtered_events.sort_values(by="start_date", ascending=True)
        
        # Apply search and filter to events_df
        display_events_df = apply_search_and_filter(filtered_events, "calendar_search", "calendar_advance_search")

        if not display_events_df.empty:
            # Format dates for display
            display_events_df['start_date'] = display_events_df['start_date'].dt.strftime("%Y-%m-%d")
            display_events_df['end_date'] = display_events_df['end_date'].dt.strftime("%Y-%m-%d")
            st.dataframe(display_events_df[['title', 'description', 'start_date', 'end_date', 'attendees', 'created_by']], use_container_width=True, hide_index=True)
        else:
            st.info("No upcoming events or no events matching your search/filter criteria. Add new events below.")
    else:
        st.info("No events scheduled yet. Add new events below.")


    st.markdown("---")
    with st.container():
        st.subheader("Schedule New Event")
        with st.expander("Click to schedule a new event", expanded=False):
            with st.form("new_event_form", clear_on_submit=True):
                event_id = f"EVT-{int(datetime.now().timestamp())}-{np.random.randint(1000, 9999)}"
                event_title = st.text_input("Event Title", placeholder="e.g., Q3 Supplier Review Meeting")
                event_description = st.text_area("Event Description", placeholder="Detailed agenda or notes for the event.")

                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    event_start_date = st.date_input("Start Date", value=datetime.today(), key="event_start_date")
                with col_e2:
                    event_end_date = st.date_input("End Date", value=datetime.today() + timedelta(days=1), key="event_end_date")
                
                # Attendees selection (multiselect from all user roles)
                all_possible_attendees = user_roles # Already defined globally
                selected_attendees = st.multiselect("Attendees", all_possible_attendees, default=[user_role])

                schedule_button = st.form_submit_button("➕ Schedule Event")

                if schedule_button:
                    if event_title and event_start_date and event_end_date and selected_attendees:
                        if event_start_date > event_end_date:
                            st.error("❗ Start date cannot be after end date.")
                        else:
                            new_event = {
                                "event_id": event_id,
                                "title": event_title,
                                "description": event_description,
                                "start_date": event_start_date.strftime("%Y-%m-%d"),
                                "end_date": event_end_date.strftime("%Y-%m-%d"),
                                "attendees": str(selected_attendees), # Store as string representation of list
                                "created_by": user_role,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            append_data(EVENTS_FILE, pd.DataFrame([new_event]))
                            st.session_state.events_df = load_data(EVENTS_FILE, columns=event_columns) # Refresh dataframe
                            st.success(f"✅ Event '{event_title}' scheduled successfully!")
                            st.rerun()
                    else:
                        st.error("❗ Please fill in all required fields (Title, Start Date, End Date, Attendees).")


# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown(f"© {datetime.now().year} Zenova SRP. All rights reserved.")
st.sidebar.markdown("Powered by Streamlit")
