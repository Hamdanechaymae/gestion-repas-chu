import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* ===== GLOBAL ===== */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(59,130,246,0.16), transparent 35%),
            radial-gradient(circle at bottom right, rgba(14,165,233,0.14), transparent 35%),
            linear-gradient(135deg, #f7fbff, #edf4fb);
        color: #1f2937;
        font-family: "Segoe UI", sans-serif;
    }

    .block-container {
        padding-top: 1rem;
        max-width: 1200px;
    }

    /* ===== ANIMATIONS ===== */
    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(35px) scale(0.96);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @keyframes softGlow {
        0% { box-shadow: 0 14px 35px rgba(37,99,235,0.10); }
        50% { box-shadow: 0 22px 55px rgba(37,99,235,0.20); }
        100% { box-shadow: 0 14px 35px rgba(37,99,235,0.10); }
    }

    @keyframes shineMove {
        from { left: -90%; }
        to { left: 130%; }
    }

    /* ===== NAVBAR ===== */
    .navbar-box {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        padding: 16px 26px;
        border-radius: 24px;
        margin-bottom: 26px;
        border: 1px solid rgba(255,255,255,0.95);
        box-shadow: 0 14px 38px rgba(30,64,175,0.12);
        animation: fadeUp 0.7s ease-out;
        position: sticky;
        top: 0;
        z-index: 999;
    }

    .brand-title {
        font-size: 24px;
        font-weight: 900;
        color: #17315f;
        letter-spacing: -0.4px;
    }

    .brand-subtitle {
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
    }

    /* ===== HERO ===== */
    .hero {
        position: relative;
        overflow: hidden;
        padding: 56px;
        border-radius: 32px;
        margin-bottom: 34px;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.82), rgba(219,234,254,0.62)),
            radial-gradient(circle at top right, rgba(59,130,246,0.25), transparent 38%);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.95);
        box-shadow: 0 20px 50px rgba(30,64,175,0.14);
        animation: fadeUp 0.85s ease-out, softGlow 5s ease-in-out infinite;
    }

    .hero::after {
        content: "";
        position: absolute;
        top: -90px;
        right: -90px;
        width: 250px;
        height: 250px;
        background: rgba(59,130,246,0.18);
        border-radius: 50%;
        filter: blur(14px);
    }

    .hero::before {
        content: "";
        position: absolute;
        top: -75%;
        left: -90%;
        width: 70%;
        height: 250%;
        background: linear-gradient(
            120deg,
            transparent,
            rgba(255,255,255,0.45),
            transparent
        );
        transform: rotate(25deg);
        animation: shineMove 4.5s ease-in-out infinite;
    }

    .hero h1 {
        font-size: 46px;
        font-weight: 900;
        color: #0f172a;
        letter-spacing: -1px;
        position: relative;
        z-index: 2;
    }

    .hero p {
        font-size: 18px;
        color: #475569;
        line-height: 1.7;
        position: relative;
        z-index: 2;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(37,99,235,0.12);
        color: #1d4ed8;
        padding: 8px 15px;
        border-radius: 999px;
        font-weight: 800;
        margin-bottom: 18px;
        position: relative;
        z-index: 2;
    }

    /* ===== CARDS GLASS + LIGHT ===== */
    .custom-card {
        position: relative;
        overflow: hidden;
        background: rgba(255,255,255,0.76);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 28px;
        border-radius: 26px;
        border: 1px solid rgba(255,255,255,0.95);
        box-shadow: 0 16px 36px rgba(30,64,175,0.12);
        transition: transform 0.35s ease, box-shadow 0.35s ease, border 0.35s ease;
        animation: fadeUp 0.85s ease-out both;
    }

    .custom-card::before {
        content: "";
        position: absolute;
        top: -70%;
        left: -90%;
        width: 75%;
        height: 240%;
        background: linear-gradient(
            120deg,
            transparent,
            rgba(255,255,255,0.80),
            transparent
        );
        transform: rotate(25deg);
        transition: left 0.75s ease;
    }

    .custom-card:hover::before {
        left: 125%;
    }

    .custom-card:hover {
        transform: translateY(-15px) scale(1.04);
        box-shadow: 0 30px 60px rgba(37,99,235,0.25);
        border: 1px solid rgba(59,130,246,0.48);
    }

    .custom-card h3 {
        color: #17315f;
        font-weight: 900;
    }

    .custom-card p {
        color: #475569;
        font-weight: 500;
    }

    /* ===== LOGIN BOX ===== */
    .login-box {
        background: rgba(255,255,255,0.76);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        padding: 36px;
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.95);
        box-shadow: 0 20px 50px rgba(30,64,175,0.16);
        animation: fadeUp 0.8s ease-out;
    }

    /* ===== INPUTS / SELECT ===== */
    input,
    .stTextInput > div > div > input {
        border-radius: 16px !important;
        border: 1px solid #cbd5e1 !important;
        background: rgba(255,255,255,0.90) !important;
        transition: all 0.25s ease !important;
    }

    input:focus {
        border: 1px solid #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59,130,246,0.18) !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 16px !important;
        border: 1px solid #cbd5e1 !important;
        background: rgba(255,255,255,0.90) !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border-radius: 999px !important;
        padding: 0.68rem 1.45rem;
        border: none;
        font-weight: 900;
        letter-spacing: 0.4px;
        box-shadow: 0 10px 24px rgba(37,99,235,0.24);
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-5px) scale(1.06);
        box-shadow: 0 18px 34px rgba(37,99,235,0.38);
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
    }

    .stButton > button:active {
        transform: scale(0.96);
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-right: 1px solid rgba(226,232,240,0.95);
    }

    section[data-testid="stSidebar"] * {
        color: #1f2937;
    }

    /* ===== METRICS ===== */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.76);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.95);
        padding: 18px;
        border-radius: 22px;
        box-shadow: 0 14px 30px rgba(30,64,175,0.11);
        transition: 0.3s ease;
        animation: fadeUp 0.8s ease-out;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-7px) scale(1.02);
        box-shadow: 0 20px 42px rgba(37,99,235,0.20);
    }

    /* ===== TABLES ===== */
    [data-testid="stDataFrame"] {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 14px 34px rgba(30,64,175,0.10);
        animation: fadeUp 0.7s ease-out;
    }

    /* ===== RADIO ===== */
    div[role="radiogroup"] label {
        transition: 0.25s ease;
        border-radius: 12px;
        padding: 4px;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(59,130,246,0.10);
        transform: translateX(5px);
    }

    </style>
    """, unsafe_allow_html=True)