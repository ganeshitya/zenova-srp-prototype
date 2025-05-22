import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.express as px
import numpy as np
from faker import Faker # NEW: Import Faker for dummy data generation
import random # NEW: Import random for dummy data generation

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
# ORIGINAL: FILES_FILE = os.path.join(DATA_DIR, "uploaded_files.csv") # Renaming to prevent conflict
PROJECTS_FILE = os.path.join(DATA_DIR, "project_tasks.csv")
ASSETS_FILE = os.path.join(DATA_DIR, "assets.csv")
AUDITS_FILE = os.path.join(DATA_DIR, "audit_points.csv")
EVENTS_FILE = os.path.join(DATA_DIR, "events.csv")
FILE_COMMENTS_FILE = os.path.join(DATA_DIR, "file_comments.csv") # NEW FILE COMMENTS
SUPPLIER_RECORDS_DIR = os.path.join(DATA_DIR, "supplier_records")
SUPPLIER_DUMMY_DATA_FILE = os.path.join(DATA_DIR, "supplier_dummy_data.csv")

# NEW: File paths for Supplier World data
SUPPLIER_ENRICHED_DATA_FILE = os.path.join(DATA_DIR, "supplier_enriched_data.csv")
SUPPLIER_ASSETS_FILE = os.path.join(DATA_DIR, "supplier_assets.csv")
SUPPLIER_PROJECTS_FILE = os.path.join(DATA_DIR, "supplier_projects.csv")
SUPPLIER_FILES_FILE = os.path.join(DATA_DIR, "supplier_files.csv")

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

# --- NEW: Data Generation Functions for Supplier World ---
# Initialize Faker once globally for data generation
fake = Faker('en_US')

@st.cache_data
def generate_enriched_supplier_data(num_suppliers=100):
    """Generates a DataFrame of enriched supplier data."""
    data = []
    product_categories = [
        "Raw Materials", "Electronic Components", "Machined Parts", "Assemblies",
        "Sub-assemblies", "Fabricated Metals", "Tools & Dies", "Automation Equipment",
        "Quality Services", "Plastic Components", "Engineering Services", "Prototypes",
        "Optical Components", "Maintenance Supplies", "Technology Services", "Fasteners"
    ]
    cities = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
        "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
        "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis",
        "Seattle", "Denver", "Washington D.C.", "Boston", "El Paso", "Detroit",
        "Nashville", "Portland", "Memphis", "Oklahoma City", "Las Vegas", "Louisville",
        "Baltimore", "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento",
        "Mesa", "Kansas City", "Atlanta", "Colorado Springs", "Miami", "Raleigh",
        "Omaha", "Long Beach", "Virginia Beach", "Oakland", "Minneapolis", "Tulsa",
        "Arlington", "New Orleans", "Wichita", "Cleveland", "Tampa", "Orlando",
        "Anaheim", "Honolulu", "Lexington", "St. Louis", "Cincinnati", "Pittsburgh",
        "Durham", "Greensboro", "Richmond", "Boise", "Spokane", "Lincoln", "Madison"
    ]
    agreement_statuses = ["Active", "Active", "Active", "Pending Renewal", "On Hold", "Terminated"]
    risk_levels = ["Low", "Low", "Low", "Medium", "Medium", "High"]
    certifications = ["ISO 9001", "AS9100", "ISO 14001", "ISO 27001", "ISO 17025", "N/A"]
    payment_terms_options = ["Net 30", "Net 60", "Net 90", "Prepayment"]
    account_managers = ["Alex Johnson", "Sarah Lee", "David Chen", "Emily White", "Mark Green", "Susan Black"]

    for i in range(1, num_suppliers + 1):
        supplier_id = f"SUP-{i:03d}"
        annual_spend = random.randint(100000, 1500000)
        risk_level = random.choice(risk_levels)

        agreement_status = random.choice(agreement_statuses)
        if agreement_status == 'Terminated':
            last_audit_score = random.randint(50, 70)
            on_time_delivery_rate = round(random.uniform(70.0, 90.0), 1)
            quality_reject_rate = round(random.uniform(1.0, 3.0), 1)
            risk_level = "High"
        elif agreement_status == 'On Hold':
            last_audit_score = random.randint(60, 75)
            on_time_delivery_rate = round(random.uniform(80.0, 92.0), 1)
            quality_reject_rate = round(random.uniform(0.8, 2.0), 1)
            if risk_level == "Low": risk_level = "Medium"
        else: # Active or Pending Renewal
            last_audit_score = random.randint(75, 95)
            on_time_delivery_rate = round(random.uniform(90.0, 99.5), 1)
            quality_reject_rate = round(random.uniform(0.0, 1.0), 2)
            if last_audit_score < 80: risk_level = "Medium"

        if on_time_delivery_rate < 90 or quality_reject_rate > 1.0:
            if risk_level == "Low": risk_level = "Medium"
        if on_time_delivery_rate < 85 or quality_reject_rate > 1.5:
            risk_level = "High"

        supplier_tier = "Tier 3 - Approved"
        if annual_spend >= 700000 and last_audit_score >= 85 and risk_level == "Low":
            supplier_tier = "Tier 1 - Strategic"
        elif annual_spend >= 400000 and last_audit_score >= 80 and risk_level in ["Low", "Medium"]:
            supplier_tier = "Tier 2 - Preferred"
        elif agreement_status in ["Terminated", "On Hold"] or risk_level == "High" or last_audit_score < 75:
             supplier_tier = "Tier 4 - Watchlist"


        contact_person = fake.name()
        supplier_name = fake.company()
        email = f"{contact_person.replace(' ', '.').lower()}@{supplier_name.replace(' ', '').lower()}.com"
        phone = fake.phone_number()
        notes = fake.sentence()
        primary_product_category = random.choice(product_categories)
        certification = random.choice(certifications) if random.random() > 0.1 else "N/A"
        if agreement_status == 'Terminated' or agreement_status == 'On Hold':
            certification = "N/A"

        last_performance_review_date = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
        supplier_city = random.choice(cities)
        supplier_country = "USA"
        payment_terms = random.choice(payment_terms_options)
        contract_start_date = fake.date_between(start_date='-4y', end_date='-1y').strftime('%Y-%m-%d')
        csd_dt = datetime.strptime(contract_start_date, '%Y-%m-%d')
        contract_end_date = (csd_dt + timedelta(days=random.randint(365, 1095))).strftime('%Y-%m-%d')
        if agreement_status == 'Pending Renewal':
            contract_end_date = fake.date_between(start_date='today', end_date='+6m').strftime('%Y-%m-%d')
        elif agreement_status == 'Terminated':
            contract_end_date = fake.date_between(start_date='-2y', end_date='-6m').strftime('%Y-%m-%d')

        esg_score = random.randint(50, 95)
        account_manager = random.choice(account_managers)
        onboarding_date = (csd_dt - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d')
        emissions_target_met = random.choice([True, False]) # For ESG compliance

        data.append([
            supplier_id, supplier_name, contact_person, email, phone, agreement_status,
            last_audit_score, notes, primary_product_category, on_time_delivery_rate,
            quality_reject_rate, risk_level, certification, annual_spend,
            last_performance_review_date, supplier_city, supplier_country, payment_terms,
            contract_start_date, contract_end_date, supplier_tier, esg_score,
            account_manager, onboarding_date, emissions_target_met
        ])

    df = pd.DataFrame(data, columns=[
        'supplier_id', 'supplier_name', 'contact_person', 'email', 'phone', 'agreement_status',
        'last_audit_score', 'notes', 'primary_product_category', 'on_time_delivery_rate',
        'quality_reject_rate', 'risk_level', 'certification', 'annual_spend_usd',
        'last_performance_review_date', 'supplier_city', 'supplier_country', 'payment_terms',
        'contract_start_date', 'contract_end_date', 'supplier_tier', 'ESG_score',
        'account_manager', 'onboarding_date', 'emissions_target_met'
    ])

    df['phone'] = df['phone'].apply(lambda x: ''.join(filter(str.isdigit, x)))
    df['phone'] = df['phone'].apply(lambda x: f"+1 ({x[1:4]}) {x[4:7]}-{x[7:]}" if len(x) >= 10 else x)

    return df

@st.cache_data
def generate_supplier_assets(supplier_ids):
    """Generates a DataFrame of supplier assets."""
    data = []
    asset_types = ["Tooling", "Equipment", "Software License", "Vehicle", "Fixture", "Mold"]
    statuses = ["In Use", "In Storage", "Under Maintenance", "Retired", "Loaned"]
    locations = ["Supplier Plant A", "Supplier Plant B", "Supplier Plant C", "Client Site X"]

    asset_id_counter = 1
    for s_id in supplier_ids:
        num_assets = random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1], k=1)[0]
        for _ in range(num_assets):
            asset_id = f"SUP_AST-{asset_id_counter:04d}" # Differentiate from general assets
            asset_name = fake.catch_phrase() + " " + random.choice(["Machine", "Tool", "System", "License"])
            asset_type = random.choice(asset_types)
            description = fake.sentence()
            acquisition_date = fake.date_between(start_date='-5y', end_date='-6m').strftime('%Y-%m-%d')
            status = random.choice(statuses)
            location = random.choice(locations)
            notes = fake.optional(fake.sentence, 0.7)

            data.append([
                asset_id, s_id, asset_name, asset_type, description,
                acquisition_date, status, location, notes
            ])
            asset_id_counter += 1
    return pd.DataFrame(data, columns=[
        'asset_id', 'supplier_id', 'asset_name', 'asset_type', 'description',
        'acquisition_date', 'status', 'location', 'notes'
    ])

@st.cache_data
def generate_supplier_projects(supplier_ids):
    """Generates a DataFrame of supplier projects."""
    data = []
    project_types = ["New Product Development", "Process Improvement", "Cost Reduction",
                     "Quality Enhancement", "Technology Integration", "Supply Chain Optimization",
                     "ESG Compliance Initiative", "Waste Reduction Program"] # Added ESG types
    statuses = ["Planned", "In Progress", "Completed", "On Hold", "Cancelled"]
    project_managers = ["Emily White", "Mark Green", "Susan Black", "Robert Blue", "Olivia Grey"]

    project_id_counter = 1
    for s_id in supplier_ids:
        num_projects = random.choices([0, 1, 2], weights=[0.3, 0.5, 0.2], k=1)[0]
        for _ in range(num_projects):
            project_id = f"SUP_PRJ-{project_id_counter:04d}" # Differentiate from general projects
            project_name = fake.bs().title() + " Project"
            project_type = random.choice(project_types)
            start_date = fake.date_between(start_date='-1y', end_date='-1m').strftime('%Y-%m-%d')
            end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
            status = random.choice(statuses)
            budget_usd = round(random.uniform(20000, 1000000), -3)

            if status == 'Completed':
                end_date = fake.date_between(start_date='-1y', end_date='-1m').strftime('%Y-%m-%d')
                start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=random.randint(30, 300))).strftime('%Y-%m-%d')
            elif status == 'Planned':
                start_date = fake.date_between(start_date='+1m', end_date='+6m').strftime('%Y-%m-%d')
                end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=random.randint(60, 365))).strftime('%Y-%m-%d')
            
            # Check if it's an ESG related project
            is_esg_project = True if "ESG" in project_type or "Reduction" in project_type else False

            description = fake.paragraph(nb_sentences=2)
            project_manager = random.choice(project_managers)

            data.append([
                project_id, s_id, project_name, project_type, start_date, end_date,
                status, budget_usd, description, project_manager, is_esg_project # Added is_esg_project
            ])
            project_id_counter += 1
    return pd.DataFrame(data, columns=[
        'project_id', 'supplier_id', 'project_name', 'project_type', 'start_date',
        'end_date', 'status', 'budget_usd', 'description', 'project_manager', 'is_esg_project'
    ])

@st.cache_data
def generate_supplier_files(supplier_ids):
    """Generates a DataFrame of supplier files."""
    data = []
    file_types = ["PDF", "DOCX", "XLSX", "CAD", "JPG", "PNG", "Legal Document",
                  "Audit Report", "Performance Report", "Contract", "Specification"]
    uploaded_by_options = ["Admin", "John Doe", "Legal Dept", "Engineering Team", "Procurement"]

    file_id_counter = 1
    for s_id in supplier_ids:
        num_files = random.choices([0, 1, 2, 3, 4], weights=[0.2, 0.3, 0.2, 0.2, 0.1], k=1)[0]
        for _ in range(num_files):
            file_id = f"SUP_FIL-{file_id_counter:04d}" # Differentiate from general files
            file_type = random.choice(file_types)
            file_name = fake.word().title() + " " + file_type + " " + fake.numerify(text='###')

            if file_type == "Audit Report": file_name = f"{fake.company()} Audit Report {fake.year()}"
            elif file_type == "Performance Report": file_name = f"{fake.company()} Q{random.randint(1,4)} {fake.year()} Perf."
            elif file_type == "Contract": file_name = f"{fake.company()} Master Agreement {fake.year()}"
            elif file_type == "Specification": file_name = f"Component X Spec v{random.randint(1,5)}.{random.randint(0,9)}"
            elif file_type == "Legal Document": file_name = f"{fake.company()} NDA {fake.year()}"

            upload_date = fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
            uploaded_by = random.choice(uploaded_by_options)
            description = fake.sentence(nb_words=6)
            document_link = f"https://yourcompany.com/documents/{s_id}/{file_name.replace(' ', '_').lower()}"

            data.append([
                file_id, s_id, file_name, file_type, upload_date,
                uploaded_by, description, document_link
            ])
            file_id_counter += 1
    return pd.DataFrame(data, columns=[
        'file_id', 'supplier_id', 'file_name', 'file_type', 'upload_date',
        'uploaded_by', 'description', 'document_link'
    ])

# --- NEW: Function to ensure Supplier World CSVs exist and load them ---
@st.cache_resource
def load_supplier_world_data():
    """
    Checks if Supplier World CSVs exist, generates them if not, then loads all dataframes.
    Uses st.cache_resource to avoid re-running on every page interaction.
    """
    csv_files = {
        'suppliers': SUPPLIER_ENRICHED_DATA_FILE,
        'assets': SUPPLIER_ASSETS_FILE,
        'projects': SUPPLIER_PROJECTS_FILE,
        'files': SUPPLIER_FILES_FILE
    }

    # Check if all CSVs exist. If not, generate them.
    all_exist = True
    for key, filename in csv_files.items():
        if not os.path.exists(filename):
            all_exist = False
            break

    if not all_exist:
        st.info("Generating dummy data CSVs for the first time for Supplier World... This may take a moment.")
        df_suppliers_gen = generate_enriched_supplier_data(num_suppliers=50) # Reduced count for faster generation
        df_suppliers_gen.to_csv(csv_files['suppliers'], index=False)

        all_supplier_ids = df_suppliers_gen['supplier_id'].tolist()

        df_assets_gen = generate_supplier_assets(all_supplier_ids)
        df_assets_gen.to_csv(csv_files['assets'], index=False)

        # Updated columns for projects, ensure new col is present
        project_cols = ["project_id", "supplier_id", "project_name", "project_type", "start_date",
                        "end_date", "status", "budget_usd", "description", "project_manager", "is_esg_project"]
        df_projects_gen = generate_supplier_projects(all_supplier_ids)
        df_projects_gen.to_csv(csv_files['projects'], index=False)

        df_files_gen = generate_supplier_files(all_supplier_ids)
        df_files_gen.to_csv(csv_files['files'], index=False)
        st.success("Dummy data for Supplier World generated and saved to CSV files!")
        # Reload the generated data
        return pd.read_csv(csv_files['suppliers']), pd.read_csv(csv_files['assets']), \
               pd.read_csv(csv_files['projects']), pd.read_csv(csv_files['files'])
    else:
        # Load existing data
        # Ensure project columns include 'is_esg_project' when loading
        df_projects_loaded = load_data(csv_files['projects'], columns=["project_id", "supplier_id", "project_name", "project_type", "start_date",
                        "end_date", "status", "budget_usd", "description", "project_manager", "is_esg_project"])
        
        return pd.read_csv(csv_files['suppliers']), pd.read_csv(csv_files['assets']), \
               df_projects_loaded, pd.read_csv(csv_files['files'])


# --- Initialize CSV Files (Your existing setup) ---
notification_columns = [
    "notification_id", "sender_role", "recipient_role", "subject", "message",
    "timestamp", "status", "parent_notification_id" # status: Sent, Read, Replied
]
initialize_csv(NOTIFICATIONS_FILE, notification_columns) # NEW
# Renamed from FILES_FILE to avoid conflict with supplier_files.csv
initialize_csv(os.path.join(DATA_DIR, "uploaded_docs.csv"), ["filename", "type", "size", "uploader", "timestamp", "path"]) 

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
# This file is for the 'Supplier Records' tab and will be separate from the 'Supplier World' data
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
    "👥 Supplier Records", # Your existing supplier records tab
    "🌎 Supplier World", # NEW: Supplier World tab
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

# Renamed to avoid conflict with supplier files for "Supplier World"
if "uploaded_docs_df" not in st.session_state:
    st.session_state.uploaded_docs_df = load_data(os.path.join(DATA_DIR, "uploaded_docs.csv"), 
                                                   columns=["filename", "type", "size", "uploader", "timestamp", "path"])


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
        # Load all relevant data for the dashboard (your existing data)
        projects_df = load_data(PROJECTS_FILE, columns=project_columns)
        assets_df = load_data(ASSETS_FILE, columns=asset_columns)
        audits_df = load_data(AUDITS_FILE, columns=audit_columns)
        supplier_df = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=supplier_columns) # Your existing supplier data

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
                st.info("To track supplier ESG compliance, ensure 'esg_compliance_score' and 'emissions_target_met' columns are available and populated in Supplier Records.")

# --- Supplier Records Module (Your existing one) ---
with tabs[1]: # Corresponding to "👥 Supplier Records"
    st.subheader("Manage Supplier Records")
    if user_role not in ["OEM", "Auditor"]:
        st.warning("🔒 You must be logged in as 'OEM' or 'Auditor' to view Supplier Records.")
    else:
        supplier_df = load_data(SUPPLIER_DUMMY_DATA_FILE, columns=supplier_columns)

        st.markdown("---")
        st.subheader("All Suppliers")
        
        # Apply search and filter to supplier records
        filtered_suppliers_df = apply_search_and_filter(supplier_df, "supplier_records_search", "supplier_records_adv_search")

        if not filtered_suppliers_df.empty:
            st.dataframe(filtered_suppliers_df, use_container_width=True, hide_index=True)
        else:
            st.info("No suppliers found matching your criteria.")

        st.markdown("---")
        st.subheader("Add New Supplier")
        with st.form("add_supplier_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_supplier_name = st.text_input("Supplier Name*", max_chars=100)
                new_contact_person = st.text_input("Contact Person")
                new_email = st.text_input("Email")
                new_phone = st.text_input("Phone")
                new_agreement_status = st.selectbox("Agreement Status", ["Active", "Pending Renewal", "On Hold", "Terminated"])
                new_last_audit_score = st.number_input("Last Audit Score", min_value=0, max_value=100, value=75)
            with col2:
                new_primary_product_category = st.text_input("Primary Product Category")
                new_on_time_delivery_rate = st.slider("On-Time Delivery Rate (%)", 0.0, 100.0, 95.0, 0.1)
                new_quality_reject_rate = st.slider("Quality Reject Rate (%)", 0.0, 10.0, 0.5, 0.01)
                new_risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])
                new_certification = st.text_input("Certification (e.g., ISO 9001)")
                new_annual_spend_usd = st.number_input("Annual Spend (USD)", min_value=0, value=500000, step=10000)
                new_esg_compliance_score = st.number_input("ESG Compliance Score", min_value=0, max_value=100, value=80, key="new_esg_score")
                new_emissions_target_met = st.checkbox("Emissions Target Met", value=True, key="new_emissions_met")

            new_notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("Add Supplier")

            if submitted:
                if new_supplier_name:
                    new_supplier_id = f"SUP-{len(supplier_df) + 1:03d}" if not supplier_df.empty else "SUP-001"
                    new_entry = pd.DataFrame([{
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
                        "last_performance_review_date": datetime.now().strftime('%Y-%m-%d'),
                        "esg_compliance_score": new_esg_compliance_score,
                        "emissions_target_met": new_emissions_target_met
                    }])
                    append_data(SUPPLIER_DUMMY_DATA_FILE, new_entry)
                    st.success(f"Supplier '{new_supplier_name}' added successfully!")
                    st.experimental_rerun() # Rerun to refresh the dataframe
                else:
                    st.error("Supplier Name is required.")

# --- NEW: Supplier World Module ---
with tabs[2]: # Corresponding to "🌎 Supplier World"
    st.subheader("Supplier World: Deep Dive into Supplier Data")

    # Load all dataframes for Supplier World (cached)
    df_suppliers_sw, df_assets_sw, df_projects_sw, df_files_sw = load_supplier_world_data()

    if user_role not in ["OEM", "Auditor"]:
        st.warning("🔒 You must be logged in as 'OEM' or 'Auditor' to view Supplier World.")
    else:
        # --- Sidebar for Supplier Selection (for Supplier World) ---
        # Get unique supplier names and IDs from the loaded data for this module
        supplier_names_ids_sw = df_suppliers_sw[['supplier_name', 'supplier_id']].apply(lambda x: f"{x['supplier_name']} ({x['supplier_id']})", axis=1).tolist()
        
        # Add an empty option to the selection
        display_options_sw = ["-- Select a Supplier --"] + supplier_names_ids_sw
        
        # Use a distinct key for this selectbox to avoid conflicts with other selectboxes
        selected_supplier_display_sw = st.sidebar.selectbox("Choose a Supplier for Supplier World:", display_options_sw, key="supplier_world_selection")

        selected_supplier_id_sw = None
        if selected_supplier_display_sw != "-- Select a Supplier --":
            selected_supplier_id_sw = selected_supplier_display_sw.split('(')[-1][:-1]

        if selected_supplier_id_sw:
            st.markdown(f"## 🌐 Supplier World: {selected_supplier_display_sw.split('(')[0].strip()}")
            st.markdown("---")

            # Filter data for the selected supplier
            current_supplier_info_sw = df_suppliers_sw[df_suppliers_sw['supplier_id'] == selected_supplier_id_sw].iloc[0]
            current_supplier_assets_sw = df_assets_sw[df_assets_sw['supplier_id'] == selected_supplier_id_sw]
            current_supplier_projects_sw = df_projects_sw[df_projects_sw['supplier_id'] == selected_supplier_id_sw]
            current_supplier_files_sw = df_files_sw[df_files_sw['supplier_id'] == selected_supplier_id_sw]

            # --- Display Supplier Overview ---
            st.subheader("📊 Supplier Overview")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Agreement Status", current_supplier_info_sw['agreement_status'])
                st.metric("Supplier Tier", current_supplier_info_sw['supplier_tier'])
            with col2:
                st.metric("Last Audit Score", current_supplier_info_sw['last_audit_score'])
                st.metric("Annual Spend (USD)", f"${current_supplier_info_sw['annual_spend_usd']:,}")
            with col3:
                st.metric("On-Time Delivery Rate", f"{current_supplier_info_sw['on_time_delivery_rate']}%")
                st.metric("Quality Reject Rate", f"{current_supplier_info_sw['quality_reject_rate']}%")
            with col4:
                st.metric("Risk Level", current_supplier_info_sw['risk_level'])
                st.metric("ESG Score", current_supplier_info_sw['ESG_score'])

            st.write(f"**Contact Person:** {current_supplier_info_sw['contact_person']}")
            st.write(f"**Email:** {current_supplier_info_sw['email']}")
            st.write(f"**Phone:** {current_supplier_info_sw['phone']}")
            st.write(f"**Primary Product Category:** {current_supplier_info_sw['primary_product_category']}")
            st.write(f"**Certification:** {current_supplier_info_sw['certification']}")
            st.write(f"**Payment Terms:** {current_supplier_info_sw['payment_terms']}")
            st.write(f"**Contract Dates:** {current_supplier_info_sw['contract_start_date']} to {current_supplier_info_sw['contract_end_date']}")
            st.write(f"**Account Manager:** {current_supplier_info_sw['account_manager']}")
            st.write(f"**Onboarding Date:** {current_supplier_info_sw['onboarding_date']}")
            st.info(f"**Notes:** {current_supplier_info_sw['notes']}")


            # --- Tabs for Asset, Project, File Management (within Supplier World) ---
            tab1_sw, tab2_sw, tab3_sw = st.tabs(["🗄️ Assets", "🗓️ Projects", "📁 Files"])

            with tab1_sw:
                st.subheader(f"Assets for {current_supplier_info_sw['supplier_name']}")
                # Apply search and filter within this tab for assets
                filtered_assets_sw = apply_search_and_filter(current_supplier_assets_sw, "supplier_world_assets_search", "supplier_world_assets_adv_search")
                if not filtered_assets_sw.empty:
                    st.dataframe(filtered_assets_sw, use_container_width=True, hide_index=True)
                else:
                    st.info("No assets found for this supplier.")

            with tab2_sw:
                st.subheader(f"Projects for {current_supplier_info_sw['supplier_name']}")
                # Apply search and filter within this tab for projects
                filtered_projects_sw = apply_search_and_filter(current_supplier_projects_sw, "supplier_world_projects_search", "supplier_world_projects_adv_search")
                if not filtered_projects_sw.empty:
                    st.dataframe(filtered_projects_sw, use_container_width=True, hide_index=True)
                else:
                    st.info("No projects found for this supplier.")

            with tab3_sw:
                st.subheader(f"Files for {current_supplier_info_sw['supplier_name']}")
                # Apply search and filter within this tab for files
                filtered_files_sw = apply_search_and_filter(current_supplier_files_sw, "supplier_world_files_search", "supplier_world_files_adv_search")
                if not filtered_files_sw.empty:
                    st.dataframe(filtered_files_sw, use_container_width=True, hide_index=True)
                else:
                    st.info("No files found for this supplier.")
        else:
            st.info("Please select a supplier from the sidebar to view their 'Supplier World' details.")


# --- Asset Management Module (Your existing one) ---
with tabs[3]: # Corresponding to "🛠️ Asset Management"
    st.subheader("Manage Assets")
    if user_role not in ["OEM", "Supplier A", "Supplier B"]:
        st.warning("🔒 You must be logged in as 'OEM' or a 'Supplier' to manage assets.")
    else:
        assets_df = load_data(ASSETS_FILE, columns=asset_columns)

        st.markdown("---")
        st.subheader("All Assets")
        
        # Apply search and filter
        filtered_assets_df = apply_search_and_filter(assets_df, "asset_management_search", "asset_management_adv_search")

        if not filtered_assets_df.empty:
            st.dataframe(filtered_assets_df, use_container_width=True, hide_index=True)
        else:
            st.info("No assets found matching your criteria.")

        st.markdown("---")
        st.subheader("Add New Asset")
        with st.form("add_asset_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_asset_name = st.text_input("Asset Name*", max_chars=100)
                new_location = st.text_input("Location")
                new_status = st.selectbox("Status", ["Operational", "Under Maintenance", "Retired", "Loaned"])
                new_supplier = st.text_input("Supplier (e.g., Supplier A)", help="Input the name of the supplier associated with this asset.")
            with col2:
                new_eol_date = st.date_input("End of Life Date", value=datetime.now() + timedelta(days=365*5))
                new_calibration_date = st.date_input("Last Calibration Date", value=datetime.now())
                new_last_active_date = st.date_input("Last Active Date", value=datetime.now(), help="Date when the asset was last actively used or checked.")
            new_notes_asset = st.text_area("Notes")
            
            submitted_asset = st.form_submit_button("Add Asset")

            if submitted_asset:
                if new_asset_name and new_supplier:
                    new_asset_id = f"AST-{len(assets_df) + 1:04d}" if not assets_df.empty else "AST-0001"
                    new_entry = pd.DataFrame([{
                        "asset_id": new_asset_id,
                        "asset_name": new_asset_name,
                        "location": new_location,
                        "status": new_status,
                        "eol_date": new_eol_date.strftime('%Y-%m-%d'),
                        "calibration_date": new_calibration_date.strftime('%Y-%m-%d'),
                        "notes": new_notes_asset,
                        "supplier": new_supplier,
                        "last_active_date": new_last_active_date.strftime('%Y-%m-%d')
                    }])
                    append_data(ASSETS_FILE, new_entry)
                    st.success(f"Asset '{new_asset_name}' added successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Asset Name and Supplier are required.")

# --- Project Management Module (Your existing one) ---
with tabs[4]: # Corresponding to "📅 Project Management"
    st.subheader("Manage Projects & Tasks")
    if user_role not in ["OEM", "Supplier A", "Supplier B"]:
        st.warning("🔒 You must be logged in as 'OEM' or a 'Supplier' to manage projects.")
    else:
        projects_df = load_data(PROJECTS_FILE, columns=project_columns)

        st.markdown("---")
        st.subheader("All Projects/Tasks")

        # Apply search and filter
        filtered_projects_df = apply_search_and_filter(projects_df, "project_management_search", "project_management_adv_search")

        if not filtered_projects_df.empty:
            st.dataframe(filtered_projects_df, use_container_width=True, hide_index=True)
        else:
            st.info("No projects/tasks found matching your criteria.")

        st.markdown("---")
        st.subheader("Add New Project/Task")
        with st.form("add_project_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_task_name = st.text_input("Project/Task Name*", max_chars=150)
                new_assigned_to = st.text_input("Assigned To (User/Team)")
                new_due_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=30))
            with col2:
                new_status_project = st.selectbox("Status", ["Planned", "In Progress", "Completed", "On Hold", "Cancelled"])
                new_input_pending = st.checkbox("Input Pending", value=False)
                new_is_esg_project = st.checkbox("Is ESG-related Project?", value=False, help="Check if this project contributes to sustainability or ESG goals.")
            new_description = st.text_area("Description")
            
            submitted_project = st.form_submit_button("Add Project/Task")

            if submitted_project:
                if new_task_name and new_assigned_to:
                    new_task_id = f"PRJ-{len(projects_df) + 1:04d}" if not projects_df.empty else "PRJ-0001"
                    new_entry = pd.DataFrame([{
                        "task_id": new_task_id,
                        "task_name": new_task_name,
                        "status": new_status_project,
                        "assigned_to": new_assigned_to,
                        "due_date": new_due_date.strftime('%Y-%m-%d'),
                        "description": new_description,
                        "input_pending": new_input_pending,
                        "is_esg_project": new_is_esg_project # Save the boolean
                    }])
                    append_data(PROJECTS_FILE, new_entry)
                    st.success(f"Project/Task '{new_task_name}' added successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Project/Task Name and Assigned To are required.")


# --- Audit Management Module (Your existing one) ---
with tabs[5]: # Corresponding to "📋 Audit Management"
    st.subheader("Manage Audit Points")
    if user_role not in ["OEM", "Auditor"]:
        st.warning("🔒 You must be logged in as 'OEM' or 'Auditor' to manage audits.")
    else:
        audits_df = load_data(AUDITS_FILE, columns=audit_columns)

        st.markdown("---")
        st.subheader("All Audit Points")

        # Apply search and filter
        filtered_audits_df = apply_search_and_filter(audits_df, "audit_management_search", "audit_management_adv_search")

        if not filtered_audits_df.empty:
            st.dataframe(filtered_audits_df, use_container_width=True, hide_index=True)
        else:
            st.info("No audit points found matching your criteria.")

        st.markdown("---")
        st.subheader("Add New Audit Point")
        with st.form("add_audit_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_point_description = st.text_input("Audit Point Description*", max_chars=200)
                new_assignee = st.text_input("Assignee (User/Team)")
            with col2:
                new_due_date_audit = st.date_input("Due Date for Resolution", value=datetime.now() + timedelta(days=30))
                new_status_audit = st.selectbox("Status", ["Open", "In Progress", "Closed", "Pending Validation"])
            new_resolution = st.text_area("Resolution (if applicable)")
            new_input_pending_audit = st.checkbox("Input Pending from Supplier", value=False)
            
            submitted_audit = st.form_submit_button("Add Audit Point")

            if submitted_audit:
                if new_point_description and new_assignee:
                    new_audit_id = f"AUD-{len(audits_df) + 1:04d}" if not audits_df.empty else "AUD-0001"
                    new_entry = pd.DataFrame([{
                        "audit_id": new_audit_id,
                        "point_description": new_point_description,
                        "status": new_status_audit,
                        "assignee": new_assignee,
                        "due_date": new_due_date_audit.strftime('%Y-%m-%d'),
                        "resolution": new_resolution,
                        "input_pending": new_input_pending_audit
                    }])
                    append_data(AUDITS_FILE, new_entry)
                    st.success(f"Audit point '{new_point_description}' added successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Audit Point Description and Assignee are required.")


# --- File Management Module (Your existing one) ---
with tabs[6]: # Corresponding to "📁 File Management"
    st.subheader("Manage Documents")
    
    # Renamed the session state and file path to avoid conflict with supplier_files in Supplier World
    files_df_general = st.session_state.uploaded_docs_df 
    file_comments_df = st.session_state.file_comments_df

    st.markdown("---")
    st.subheader("Upload New File")
    uploaded_file = st.file_uploader("Choose a file to upload", type=["pdf", "docx", "xlsx", "jpg", "png", "cad"])

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        
        # Save file to disk
        file_path = os.path.join(SUPPLIER_RECORDS_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Add to DataFrame
        new_file_entry = pd.DataFrame([{
            "filename": uploaded_file.name,
            "type": uploaded_file.type,
            "size": uploaded_file.size,
            "uploader": user_role, # Assuming current logged-in user is uploader
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "path": file_path
        }])
        append_data(os.path.join(DATA_DIR, "uploaded_docs.csv"), new_file_entry) # Save to the correct file
        st.session_state.uploaded_docs_df = load_data(os.path.join(DATA_DIR, "uploaded_docs.csv"), 
                                                       columns=["filename", "type", "size", "uploader", "timestamp", "path"]) # Refresh session state
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        st.experimental_rerun()

    st.markdown("---")
    st.subheader("Uploaded Files")

    # Apply search and filter for general files
    filtered_files_general_df = apply_search_and_filter(files_df_general, "general_files_search", "general_files_adv_search")

    if not filtered_files_general_df.empty:
        st.dataframe(filtered_files_general_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("File Comments & Discussions")

        selected_file_name_for_comments = st.selectbox(
            "Select a file to view/add comments:",
            ["-- Select a File --"] + filtered_files_general_df['filename'].tolist(),
            key="select_file_for_comments"
        )

        if selected_file_name_for_comments != "-- Select a File --":
            current_file_comments = file_comments_df[file_comments_df['file_name'] == selected_file_name_for_comments]

            st.markdown(f"#### Comments for '{selected_file_name_for_comments}'")

            # Display existing comments
            if not current_file_comments.empty:
                # Sort comments for display (e.g., by timestamp, main comments first)
                main_comments = current_file_comments[current_file_comments['parent_comment_id'].isnull()].sort_values('timestamp', ascending=True)
                replies = current_file_comments[current_file_comments['parent_comment_id'].notnull()]

                for idx, comment in main_comments.iterrows():
                    st.markdown(f"""
                    <div class="comment-card">
                        <div class="comment-meta">
                            <strong>{comment['author']}</strong> ({comment['timestamp']})
                            {f" @Mentions: {', '.join(comment['mentions'])}" if comment['mentions'] else ''}
                        </div>
                        <div class="comment-body">
                            {comment['comment_text']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display replies to this main comment
                    current_replies = replies[replies['parent_comment_id'] == comment['comment_id']].sort_values('timestamp', ascending=True)
                    if not current_replies.empty:
                        st.markdown('<div class="reply-to-comment">', unsafe_allow_html=True)
                        for r_idx, reply in current_replies.iterrows():
                            st.markdown(f"""
                            <div class="single-reply">
                                <div class="reply-meta">
                                    <strong>{reply['author']}</strong> ({reply['timestamp']})
                                    {f" @Mentions: {', '.join(reply['mentions'])}" if reply['mentions'] else ''}
                                </div>
                                <div>{reply['comment_text']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No comments yet for this file.")

            # Add new comment/reply form
            st.markdown("---")
            st.markdown("#### Add New Comment or Reply")
            with st.form(f"add_comment_form_{selected_file_name_for_comments}"):
                comment_text = st.text_area("Your Comment/Reply", height=100)
                
                # Option to reply to an existing comment
                parent_comments_options = [""] + main_comments['comment_id'].tolist() if not main_comments.empty else [""]
                parent_comment_id = st.selectbox("Reply to (optional):", parent_comments_options, format_func=lambda x: f"Comment ID: {x}" if x else "New Top-Level Comment")

                # Mentions functionality
                available_roles = ["OEM", "Supplier A", "Supplier B", "Auditor"]
                mentions = st.multiselect("Mention Users/Roles (optional):", available_roles)
                
                submit_comment = st.form_submit_button("Post Comment")

                if submit_comment:
                    if comment_text:
                        new_comment_id = f"COM-{len(file_comments_df) + 1:04d}" if not file_comments_df.empty else "COM-0001"
                        new_comment_entry = pd.DataFrame([{
                            "comment_id": new_comment_id,
                            "file_name": selected_file_name_for_comments,
                            "parent_comment_id": parent_comment_id if parent_comment_id else None,
                            "author": user_role,
                            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "comment_text": comment_text,
                            "mentions": mentions # Store as list
                        }])
                        
                        # Convert list to string for CSV saving
                        new_comment_entry['mentions'] = new_comment_entry['mentions'].apply(str) 

                        append_data(FILE_COMMENTS_FILE, new_comment_entry)
                        st.success("Comment posted successfully!")
                        st.session_state.file_comments_df = load_data(FILE_COMMENTS_FILE, columns=file_comment_columns) # Refresh session state
                        
                        # Re-parse 'mentions' column after reloading
                        if 'mentions' in st.session_state.file_comments_df.columns:
                            st.session_state.file_comments_df['mentions'] = st.session_state.file_comments_df['mentions'].apply(lambda x: eval(x) if isinstance(x, str) else [])
                        
                        st.experimental_rerun()
                    else:
                        st.error("Comment text cannot be empty.")
    else:
        st.info("No files uploaded yet.")


# --- Mailbox Module (Your existing one) ---
with tabs[7]: # Corresponding to "📧 Mailbox"
    st.subheader("Your Mailbox")

    st.markdown('<div class="mailbox-container">', unsafe_allow_html=True)

    # Filter notifications for the current user's role
    current_user_notifications = st.session_state.notifications_df[
        (st.session_state.notifications_df['recipient_role'] == user_role) |
        (st.session_state.notifications_df['sender_role'] == user_role)
    ].sort_values(by='timestamp', ascending=False).reset_index(drop=True)

    # Initialize current_user_notifications if it's empty to prevent errors
    if current_user_notifications.empty:
        st.info("Your mailbox is empty. Send a message to get started!")
        current_user_notifications = pd.DataFrame(columns=notification_columns) # Ensure it's a DataFrame

    # Mailbox Navigation Buttons
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
        inbox_messages = current_user_notifications[
            (current_user_notifications['recipient_role'] == user_role) & 
            (current_user_notifications['parent_notification_id'].isnull()) # Only show top-level messages in inbox
        ].sort_values(by='timestamp', ascending=False)
        
        if inbox_messages.empty:
            st.info("No messages in your inbox.")
        else:
            for idx, msg in inbox_messages.iterrows():
                unread_class = "unread" if msg['status'] == "Sent" else ""
                if st.markdown(f"""
                <div class="message-card {unread_class}" id="msg_{msg['notification_id']}">
                    <h5>{msg['subject']}</h5>
                    <p>From: {msg['sender_role']}</p>
                    <div class="message-meta">
                        <span>Status: {msg['status']}</span>
                        <span>{msg['timestamp']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True):
                    # Set the session state to view this message
                    st.session_state.mailbox_view = "view_message"
                    st.session_state.selected_notification_id = msg['notification_id']
                    st.experimental_rerun() # Rerun to switch view

    elif st.session_state.mailbox_view == "sent":
        st.markdown("### Sent Messages")
        sent_messages = current_user_notifications[
            (current_user_notifications['sender_role'] == user_role) &
            (current_user_notifications['parent_notification_id'].isnull())
        ].sort_values(by='timestamp', ascending=False)

        if sent_messages.empty:
            st.info("No sent messages.")
        else:
            for idx, msg in sent_messages.iterrows():
                if st.markdown(f"""
                <div class="message-card" id="msg_{msg['notification_id']}">
                    <h5>{msg['subject']}</h5>
                    <p>To: {msg['recipient_role']}</p>
                    <div class="message-meta">
                        <span>Status: {msg['status']}</span>
                        <span>{msg['timestamp']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True):
                    st.session_state.mailbox_view = "view_message"
                    st.session_state.selected_notification_id = msg['notification_id']
                    st.experimental_rerun()

    elif st.session_state.mailbox_view == "compose":
        st.markdown("### Compose New Message")
        with st.form("compose_message_form"):
            recipient = st.selectbox("Recipient Role", [r for r in user_roles if r != user_role])
            subject = st.text_input("Subject")
            message = st.text_area("Message", height=200)
            
            send_button = st.form_submit_button("Send Message")

            if send_button:
                if recipient and subject and message:
                    new_notification_id = f"NOT-{len(st.session_state.notifications_df) + 1:04d}" if not st.session_state.notifications_df.empty else "NOT-0001"
                    new_entry = pd.DataFrame([{
                        "notification_id": new_notification_id,
                        "sender_role": user_role,
                        "recipient_role": recipient,
                        "subject": subject,
                        "message": message,
                        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "status": "Sent",
                        "parent_notification_id": None
                    }])
                    append_data(NOTIFICATIONS_FILE, new_entry)
                    st.session_state.notifications_df = load_data(NOTIFICATIONS_FILE, columns=notification_columns)
                    st.success("Message sent successfully!")
                    st.session_state.mailbox_view = "sent" # Go to sent items after sending
                    st.experimental_rerun()
                else:
                    st.error("Please fill in all fields (Recipient, Subject, Message).")

    elif st.session_state.mailbox_view == "view_message":
        selected_id = st.session_state.selected_notification_id
        if selected_id:
            message_details = st.session_state.notifications_df[st.session_state.notifications_df['notification_id'] == selected_id].iloc[0]

            st.markdown(f'<div class="message-detail-view">', unsafe_allow_html=True)
            st.markdown(f"#### Subject: {message_details['subject']}")
            st.markdown(f"**From:** {message_details['sender_role']} &nbsp; **To:** {message_details['recipient_role']}")
            st.markdown(f"**Date:** {message_details['timestamp']}")
            st.markdown(f'<div class="message-body">{message_details["message"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Mark as Read if it was an inbox message and status is 'Sent'
            if message_details['recipient_role'] == user_role and message_details['status'] == "Sent":
                idx_to_update = st.session_state.notifications_df[st.session_state.notifications_df['notification_id'] == selected_id].index
                if not idx_to_update.empty:
                    st.session_state.notifications_df.loc[idx_to_update, 'status'] = "Read"
                    update_data(NOTIFICATIONS_FILE, st.session_state.notifications_df)
                    st.experimental_rerun() # Rerun to update status in inbox list

            # Display replies (if any)
            st.markdown("---")
            st.markdown("#### Conversation History")
            replies_df = st.session_state.notifications_df[
                (st.session_state.notifications_df['parent_notification_id'] == selected_id) |
                (st.session_state.notifications_df['notification_id'] == selected_id) # Include the original message
            ].sort_values(by='timestamp', ascending=True)

            if not replies_df.empty:
                st.markdown('<div class="reply-list">', unsafe_allow_html=True)
                for idx, reply in replies_df.iterrows():
                    sender_label = "You" if reply['sender_role'] == user_role else reply['sender_role']
                    st.markdown(f"""
                    <div class="single-reply">
                        <div class="reply-meta">
                            <strong>{sender_label}</strong> ({reply['timestamp']})
                        </div>
                        <div>{reply['message']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)


            # Reply section
            st.markdown('<div class="reply-section">', unsafe_allow_html=True)
            st.markdown("#### Reply")
            with st.form("reply_message_form"):
                reply_message = st.text_area("Your Reply", height=150)
                send_reply_button = st.form_submit_button("Send Reply")

                if send_reply_button:
                    if reply_message:
                        new_reply_id = f"NOT-{len(st.session_state.notifications_df) + 1:04d}"
                        new_reply_entry = pd.DataFrame([{
                            "notification_id": new_reply_id,
                            "sender_role": user_role,
                            "recipient_role": message_details['sender_role'], # Reply to the original sender
                            "subject": f"Re: {message_details['subject']}",
                            "message": reply_message,
                            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "status": "Sent",
                            "parent_notification_id": selected_id
                        }])
                        append_data(NOTIFICATIONS_FILE, new_reply_entry)
                        st.session_state.notifications_df = load_data(NOTIFICATIONS_FILE, columns=notification_columns) # Refresh
                        st.success("Reply sent!")
                        st.experimental_rerun()
                    else:
                        st.error("Reply message cannot be empty.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("No message selected.")
    st.markdown('</div>', unsafe_allow_html=True)


# --- Calendar Module (Your existing one) ---
with tabs[8]: # Corresponding to "🗓️ Calendar"
    st.subheader("Event Calendar")
    events_df = st.session_state.events_df

    st.markdown("---")
    st.subheader("Upcoming Events")
    
    current_date = datetime.now()
    # Filter for future events
    events_df['start_date'] = pd.to_datetime(events_df['start_date'])
    upcoming_events = events_df[events_df['start_date'] >= current_date].sort_values(by='start_date')

    if not upcoming_events.empty:
        for idx, event in upcoming_events.iterrows():
            st.markdown(f"""
            <div class="stContainer">
                <h5 style="color:#90CAF9;">{event['title']}</h5>
                <p><strong>Date:</strong> {event['start_date'].strftime('%Y-%m-%d')} - {event['end_date'].strftime('%Y-%m-%d')}</p>
                <p><strong>Attendees:</strong> {event['attendees']}</p>
                <p>{event['description']}</p>
                <small><em>Created by {event['created_by']} on {event['timestamp']}</em></small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No upcoming events scheduled.")

    st.markdown("---")
    st.subheader("Add New Event")
    with st.form("add_event_form"):
        new_event_title = st.text_input("Event Title*", max_chars=150)
        new_event_description = st.text_area("Description")
        col_event_dates = st.columns(2)
        with col_event_dates[0]:
            new_event_start_date = st.date_input("Start Date", value=datetime.now())
        with col_event_dates[1]:
            new_event_end_date = st.date_input("End Date", value=datetime.now() + timedelta(days=1))
        new_event_attendees = st.text_input("Attendees (comma-separated roles/names, e.g., OEM, Supplier A, John Doe)")
        
        add_event_button = st.form_submit_button("Add Event")

        if add_event_button:
            if new_event_title:
                new_event_id = f"EVT-{len(events_df) + 1:04d}" if not events_df.empty else "EVT-0001"
                new_entry = pd.DataFrame([{
                    "event_id": new_event_id,
                    "title": new_event_title,
                    "description": new_event_description,
                    "start_date": new_event_start_date.strftime('%Y-%m-%d'),
                    "end_date": new_event_end_date.strftime('%Y-%m-%d'),
                    "attendees": new_event_attendees,
                    "created_by": user_role,
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }])
                append_data(EVENTS_FILE, new_entry)
                st.session_state.events_df = load_data(EVENTS_FILE, columns=event_columns)
                st.success(f"Event '{new_event_title}' added successfully!")
                st.experimental_rerun()
            else:
                st.error("Event Title is required.")
