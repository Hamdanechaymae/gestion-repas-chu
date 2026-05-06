import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --bg: #f7f9fc;
            --surface: #ffffff;
            --surface-alt: #f9fbfd;
            --border: #dce3ea;
            --border-strong: #c8d2dc;
            --text: #1f2937;
            --muted: #667085;
            --primary: #0f6cbd;
            --primary-hover: #0b5aa0;
            --success: #1f845a;
            --warning: #b54708;
            --danger: #b42318;
            --shadow-sm: 0 1px 2px rgba(16, 24, 40, 0.04);
            --shadow-md: 0 8px 24px rgba(16, 24, 40, 0.06);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, h4 {
            color: var(--text);
            letter-spacing: 0;
        }

        p, label, span, div {
            color: var(--text);
        }

        small {
            color: var(--muted);
        }

        .navbar-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 0.9rem 1.1rem;
            margin-bottom: 1.25rem;
            box-shadow: var(--shadow-sm);
        }

        .brand-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text);
            line-height: 1.2;
            margin-top: 0.15rem;
        }

        .brand-subtitle {
            font-size: 0.88rem;
            color: var(--muted);
            margin-top: 0.15rem;
        }

        .hero {
            background: linear-gradient(180deg, #ffffff 0%, #f9fbfd 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1.6rem 1.6rem 1.4rem 1.6rem;
            margin-bottom: 1.25rem;
            box-shadow: var(--shadow-sm);
        }

        .hero h1 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.55rem;
        }

        .hero p {
            font-size: 0.98rem;
            color: var(--muted);
            max-width: 900px;
            line-height: 1.65;
            margin-bottom: 0;
        }

        .hero-badge {
            display: inline-block;
            background: #eaf3fb;
            color: var(--primary);
            border: 1px solid #cfe3f6;
            border-radius: 999px;
            padding: 0.22rem 0.7rem;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }

        .custom-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.1rem 1rem;
            min-height: 150px;
            box-shadow: var(--shadow-sm);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .custom-card:hover {
            border-color: var(--border-strong);
            box-shadow: var(--shadow-md);
        }

        .custom-card h3 {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .custom-card p {
            font-size: 0.92rem;
            color: var(--muted);
            line-height: 1.55;
            margin-bottom: 0;
        }

        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stDateInput input,
        .stNumberInput input {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-sm) !important;
            color: var(--text) !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea textarea:focus,
        .stDateInput input:focus,
        .stNumberInput input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(15, 108, 189, 0.12) !important;
        }

        div[data-baseweb="select"] > div {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-sm) !important;
            min-height: 42px;
        }

        .stButton > button {
            background: var(--primary);
            color: #ffffff;
            border: 1px solid var(--primary);
            border-radius: var(--radius-sm) !important;
            padding: 0.6rem 1rem;
            font-weight: 600;
            box-shadow: none;
            transition: background 0.2s ease, border-color 0.2s ease;
        }

        .stButton > button:hover {
            background: var(--primary-hover);
            border-color: var(--primary-hover);
            color: #ffffff;
        }

        .stButton > button:focus {
            box-shadow: 0 0 0 3px rgba(15, 108, 189, 0.15) !important;
        }

        section[data-testid="stSidebar"] {
            background: #f3f6f9;
            border-right: 1px solid var(--border);
        }

        section[data-testid="stSidebar"] * {
            color: var(--text);
        }

        section[data-testid="stSidebar"] .stRadio > div {
            gap: 0.35rem;
        }

        div[role="radiogroup"] label {
            background: transparent;
            border: 1px solid transparent;
            border-radius: var(--radius-sm);
            padding: 0.45rem 0.5rem;
            transition: background 0.15s ease, border-color 0.15s ease;
        }

        div[role="radiogroup"] label:hover {
            background: #eaf3fb;
            border-color: #cfe3f6;
        }

        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 0.9rem 1rem;
            box-shadow: var(--shadow-sm);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: var(--text);
            font-weight: 700;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
            background: var(--surface);
        }

        [data-testid="stAlert"] {
            border-radius: var(--radius-sm);
            border: 1px solid var(--border);
        }

        hr {
            border: none;
            border-top: 1px solid var(--border);
            margin: 1.2rem 0;
        }

        .login-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1.4rem;
            box-shadow: var(--shadow-sm);
        }

        button[data-baseweb="tab"] {
            border-radius: var(--radius-sm) !important;
        }

        @media (max-width: 768px) {
            .hero {
                padding: 1.2rem;
            }

            .hero h1 {
                font-size: 1.55rem;
            }

            .custom-card {
                min-height: auto;
            }

            .block-container {
                padding-top: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )