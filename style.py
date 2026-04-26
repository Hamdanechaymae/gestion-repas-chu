import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* Cacher les éléments Streamlit */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Fond général */
    .stApp {
        background: linear-gradient(135deg, #f5f9ff, #eef7ff);
        font-family: "Segoe UI", sans-serif;
        color: #172033;
    }

    .block-container {
        padding-top: 1rem;
        max-width: 1200px;
    }

    /* NAVBAR */
    .navbar-box {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(10px); /* ✅ corrigé */
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

    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border-radius: 999px;
        font-weight: 700;
        padding: 0.6rem 1.3rem;
        border: none;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        transform: scale(1.05);
    }

    /* HERO */
    .hero {
        background: linear-gradient(135deg, #ffffff 0%, #eaf4ff 55%, #e8f8f2 100%);
        padding: 60px 50px;
        border-radius: 30px;
        box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 30px;
    }

    .hero h1 {
        font-size: 42px;
        line-height: 1.2;
        color: #0f172a;
        font-weight: 900;
    }

    .hero p {
        font-size: 18px;
        color: #475569;
        line-height: 1.6;
    }

    /* CARDS */
    .custom-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
        margin-bottom: 20px;
    }

    .custom-card h3 {
        color: #0f3b73;
    }

    /* TITRES */
    .section-title {
        font-size: 28px;
        font-weight: 900;
        color: #0f172a;
        margin: 30px 0 15px;
    }

    /* LOGIN */
    .login-box {
        background: white;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
        border: 1px solid #e2e8f0;
    }

    /* INPUTS */
    input {
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e2e8f0;
    }

    </style>
    """, unsafe_allow_html=True)