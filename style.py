import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* Cacher la barre Streamlit */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background: linear-gradient(135deg, #f5f9ff, #eef7ff);
        font-family: "Segoe UI", sans-serif;
        color: #172033;
    }

    .block-container {
        padding-top: 1rem;
        max-width: 1200px;
    }

    /* Navbar */
    .navbar-box {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 18px 28px;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 35px;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 900;
        color: #0f3b73;
        margin-top: 8px;
    }

    .brand-subtitle {
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
    }

    /* Boutons navbar */
    .stButton > button {
        background: transparent;
        color: #0f3b73;
        border: none;
        border-radius: 999px;
        font-weight: 700;
        padding: 0.55rem 1.1rem;
        box-shadow: none;
    }

    .stButton > button:hover {
        background: #dbeafe;
        color: #0f3b73;
    }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #ffffff 0%, #eaf4ff 55%, #e8f8f2 100%);
        padding: 60px 50px;
        border-radius: 30px;
        box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 30px;
    }

    .hero-badge {
        display: inline-block;
        background: #dbeafe;
        color: #1d4ed8;
        padding: 8px 15px;
        border-radius: 999px;
        font-weight: 800;
        margin-bottom: 18px;
    }

    .hero h1 {
        font-size: 48px;
        line-height: 1.12;
        color: #0f172a;
        font-weight: 900;
        margin-bottom: 18px;
    }

    .hero p {
        font-size: 18px;
        color: #475569;
        line-height: 1.7;
        max-width: 850px;
    }

    .custom-card {
        background: white;
        padding: 28px;
        border-radius: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
        margin-bottom: 20px;
        min-height: 155px;
    }

    .custom-card h3 {
        color: #0f3b73;
        margin-bottom: 10px;
    }

    .section-title {
        font-size: 32px;
        font-weight: 900;
        color: #0f172a;
        margin: 35px 0 18px 0;
    }

    .login-box {
        background: white;
        padding: 35px;
        border-radius: 26px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
        border: 1px solid #e2e8f0;
    }

    input {
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
    }

    section[data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e2e8f0;
    }

    </style>
    """, unsafe_allow_html=True)