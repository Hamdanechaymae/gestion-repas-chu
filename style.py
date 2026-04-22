import streamlit as st

def load_css():
    st.markdown("""
    <style>
    /* Fond général */
    .stApp {
        background-color: #f6f8fc;
    }

    /* Titres */
    h1, h2, h3 {
        color: #1f2937;
        font-weight: 700;
    }

    /* Texte */
    html, body, [class*="css"] {
        font-family: "Segoe UI", sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* Boutons */
    .stButton > button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1rem;
        font-weight: 600;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    /* Inputs */
    .stTextInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px !important;
    }

    /* Dataframe container */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
        background-color: white;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    /* Alerts */
    div[data-baseweb="notification"] {
        border-radius: 12px;
    }

    /* Custom card */
    .custom-card {
        background: white;
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    /* Small subtitle */
    .subtitle {
        color: #6b7280;
        font-size: 15px;
        margin-top: -8px;
        margin-bottom: 20px;
    }

    /* Section spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)