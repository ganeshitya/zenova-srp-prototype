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
        background-color: #1E1E1E; /* Darker grey background for the tab bar */
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
        background-color: #2D2D2D; /* Slightly lighter dark grey on hover */
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
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
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

    /* Chat messages */
    .chat-message-container {
        display: flex;
        align-items: flex-start;
        word-break: break-word;
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 15px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        color: #E0E0E0; /* Light text for chat messages */
    }
    .chat-message-user {
        background-color: #003366; /* Dark blue for user messages */
        margin-left: auto;
        margin-right: 0;
        border-top-right-radius: 2px;
    }
    .chat-message-other {
        background-color: #2D2D2D; /* Slightly lighter dark grey for others */
        margin-left: 0;
        margin-right: auto;
        border-top-left-radius: 2px;
    }
    .chat-avatar {
        font-size: 1.5em;
        margin-right: 10px;
    }
    .chat-role {
        color: #90CAF9; /* Lighter blue for role */
        font-weight: strong;
    }
    .chat-timestamp {
        color: #A0A0A0; /* Lighter grey for timestamp */
        font-size: 0.8em;
    }
</style>
""", unsafe_allow_html=True)


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

# --- Initialize CSV Files ---
initialize_csv(CHAT_FILE, ["role", "message", "timestamp"])
initialize_csv(FILES_FILE, ["filename", "type", "size", "uploader", "timestamp", "path"])
initialize_csv(PROJECTS_FILE, ["task_id", "task_name", "status", "assigned_to", "due_date", "description", "input_pending"])
initialize_csv(ASSETS_FILE, ["asset_id", "asset_name", "location", "status", "eol_date", "calibration_date", "notes", "supplier"])
initialize_csv(AUDITS_FILE, ["audit_id", "point_description", "status", "assignee", "due_date", "resolution", "input_pending"])

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
    "💬 Chat"
]

# Create horizontal tabs
tabs = st.tabs(tab_titles)


# --- Initialize Streamlit Session State (Global Scope) ---
chat_df = load_data(CHAT_FILE, columns=["role", "message", "timestamp"])
if "chat_history" not in st.session_state:
    st.session_state.chat_history = chat_df.to_dict(orient="records")


# --- Main Application Content based on Tab Selection ---

# --- OEM Dashboard Module ---
with tabs[0]: # Corresponding to "📊 OEM Dashboard"
    st.subheader("OEM Performance Dashboard")
    st.markdown("A comprehensive overview of key performance indicators across your supplier network and internal operations.")

    if user_role != "OEM":
        st.warning("🔒 You must be logged in as 'OEM' to view this dashboard.")
    else:
        # Load all relevant data for the dashboard
        projects_df = load_data(PROJECTS_FILE, columns=["task_id", "task_name", "status", "assigned_to", "due_date", "input_pending"])
        assets_df = load_data(ASSETS_FILE, columns=["asset_id", "asset_name", "location", "status", "supplier"])
        audits_df = load_data(AUDITS_FILE, columns=["audit_id", "point_description", "status", "assignee", "due_date", "input_pending"])
        supplier_df = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=supplier_columns)

        st.markdown("---")
        st.subheader("Supplier Performance & Financial Overview")

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

    with st.container():
        st.subheader("Current Supplier Database")
        if not supplier_df.empty:
            st.dataframe(supplier_df, use_container_width=True, hide_index=True)
        else:
            st.info("No supplier records available. Please add new suppliers below.")

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

    st.markdown("---")
    with st.container():
        st.subheader("Asset Inventory Log")
        assets_df = load_data(ASSETS_FILE)
        if not assets_df.empty:
            st.dataframe(assets_df, use_container_width=True, hide_index=True)
        else:
            st.info("No assets logged yet. Add assets using the 'Add New Asset' expander above.")


# --- Project Management Module (Gantt) ---
with tabs[3]: # Corresponding to "📅 Project Management"
    st.subheader("Project Management Tool")
    st.markdown("Streamline and track all collaborative projects and tasks with your suppliers. Monitor progress, deadlines, and critical path items.")

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

    st.markdown("---")
    with st.container():
        st.subheader("Current Project Tasks")
        projects_df = load_data(PROJECTS_FILE)
        if not projects_df.empty:
            st.dataframe(projects_df, use_container_width=True, hide_index=True)
            st.info("💡 Tip: For a full Gantt chart visualization, a dedicated library like Plotly's Timeline chart could be integrated.")
        else:
            st.info("No project tasks added yet. Add tasks using the 'Add New Project Task' section above.")


# --- Audit Management Module ---
with tabs[4]: # Corresponding to "📋 Audit Management"
    st.subheader("Supplier Assessment & Actions Tracking")
    st.markdown("Efficiently manage supplier audit findings, track corrective actions, and maintain a robust assessment history.")

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

    st.markdown("---")
    with st.container():
        st.subheader("Audit Records & Open Points")
        audits_df = load_data(AUDITS_FILE)
        if not audits_df.empty:
            st.dataframe(audits_df, use_container_width=True, hide_index=True)
        else:
            st.info("No audit points recorded yet. Add audit points using the 'Add New Audit Point / Finding' section above.")


# --- File Management Module ---
with tabs[5]: # Corresponding to "📁 File Management"
    st.subheader("Secured File Management & Version Control")
    st.markdown("Securely upload, store, and manage all critical documents with your suppliers. Ensure data integrity and controlled access.")

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

    st.markdown("---")
    with st.container():
        st.subheader("Uploaded Files History")
        files_df = load_data(FILES_FILE, columns=["filename", "type", "size", "uploader", "timestamp", "path"])
        if not files_df.empty:
            files_df['path'] = files_df['path'].fillna('').astype(str) # Ensure 'path' is string
            display_df = files_df.drop(columns=['path']) # Hide path from display table
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            st.markdown("##### Download Files")
            selected_file_name_to_download = st.selectbox("Select a file to download:", files_df['filename'].tolist(), key="download_file_select")
            if selected_file_name_to_download:
                file_to_download_path_series = files_df[files_df['filename'] == selected_file_name_to_download]['path']
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
            st.info("No files uploaded yet. Use the section above to upload your documents.")

# --- Chat Module ---
with tabs[6]: # Corresponding to "💬 Chat"
    st.subheader("Inter-Company Communication Channel")
    st.markdown("Engage in real-time, secured communication with your suppliers and internal teams. Facilitate quick queries and collaborative discussions.")

    with st.container():
        st.subheader("Chat History")
        for msg_data in st.session_state.chat_history:
            role = str(msg_data.get("role", "Unknown"))
            message_content = str(msg_data.get("message", ""))
            timestamp = str(msg_data.get("timestamp", ""))

            # Determine if the message is from the current user for styling
            is_user_message = (role == user_role)
            
            # Custom message display with CSS classes
            st.markdown(f"""
            <div class="chat-message-container {'chat-message-user' if is_user_message else 'chat-message-other'}" style="max-width: 70%;">
                <span class="chat-avatar">{"🧑‍💻" if is_user_message else "🏢" if role in ["OEM", "Auditor"] else "👤"}</span>
                <div>
                    <strong class="chat-role">{role}</strong> <small class="chat-timestamp">({timestamp})</small><br>
                    {message_content}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Send New Message")
    prompt = st.chat_input("Type your message here...", key="chat_input_box")
    if prompt:
        new_message = {"role": user_role, "message": prompt, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        append_data(CHAT_FILE, pd.DataFrame([new_message]))
        st.session_state.chat_history.append(new_message)
        st.rerun()

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown(f"© {datetime.now().year} Zenova SRP. All rights reserved.")
st.sidebar.markdown("Powered by Streamlit")
