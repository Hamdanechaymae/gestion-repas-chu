import streamlit as st

def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --bg: #F1F5F9;
            --surface: #FFFFFF;
            --border: #CBD5E1;
            --text-main: #0F172A;
            --text-muted: #475569;
            --primary: #0F4C81;
            --primary-dark: #0A3A62;
            --primary-light: #DBEAFE;
            --primary-50: #EFF6FF;
            --success: #047857;
            --warning: #B45309;
            --danger: #B91C1C;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.03);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.04);
            --radius-sm: 4px;
            --radius-md: 6px;
            --radius-lg: 8px;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            font-size: 14px;
        }

        .navbar-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 0.6rem 1.25rem;
            margin-bottom: 1.25rem;
            box-shadow: var(--shadow-sm);
            display: flex;
            align-items: center;
        }

        .brand-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--primary-dark);
            letter-spacing: -0.01em;
        }

        .brand-subtitle {
            font-size: 0.7rem;
            color: var(--text-muted);
            font-weight: 500;
            letter-spacing: 0.04em;
        }

        .hero {
            background: var(--primary);
            border-radius: var(--radius-lg);
            padding: 1.75rem 1.5rem;
            margin-bottom: 1.25rem;
            color: white;
        }

        .hero h1 {
            color: #FFFFFF !important;
            font-size: 1.35rem;
            font-weight: 600;
            margin-bottom: 0.35rem;
        }

        .hero p {
            color: rgba(255,255,255,0.8) !important;
            font-size: 0.85rem;
            line-height: 1.5;
        }

        .hero-badge {
            display: inline-block;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.18);
            color: #FFFFFF;
            border-radius: 3px;
            padding: 0.15rem 0.6rem;
            font-size: 0.65rem;
            font-weight: 600;
            margin-bottom: 0.6rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .section-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 0.15rem;
        }
        
        .section-subtitle {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
        }

        .custom-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.25rem;
            height: 100%;
            box-shadow: var(--shadow-sm);
        }

        .custom-card h3 {
            color: var(--primary-dark);
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
        }
        
        .custom-card p {
            color: var(--text-muted);
            font-size: 0.8rem;
            line-height: 1.5;
            margin: 0;
        }

        .login-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
        }

        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 0.75rem 1rem !important;
            box-shadow: var(--shadow-sm) !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.65rem !important;
            font-weight: 600 !important;
            color: var(--text-muted) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            color: var(--text-main) !important;
        }

        .stButton > button {
            background: var(--primary);
            color: #FFFFFF;
            border: none;
            border-radius: var(--radius-sm);
            padding: 0.45rem 1rem;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            transition: background 0.15s ease;
            box-shadow: var(--shadow-sm);
        }

        .stButton > button:hover {
            background: var(--primary-dark);
        }

        .stButton > button[kind="secondary"] {
            background: var(--surface);
            color: var(--text-main);
            border: 1px solid var(--border);
        }
        
        .stButton > button[kind="secondary"]:hover {
            border-color: var(--primary);
            color: var(--primary-dark);
            background: var(--primary-50);
        }

        .stTextInput input, 
        .stSelectbox > div,
        .stNumberInput input {
            border-radius: var(--radius-sm) !important;
            border: 1px solid var(--border) !important;
            font-size: 0.8rem !important;
        }

        .stTextInput input:focus, 
        .stSelectbox > div:focus-within,
        .stNumberInput input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(15, 76, 129, 0.1) !important;
        }

        [data-testid="stSidebar"] {
            background: #FAFBFC;
            border-right: 1px solid var(--border);
        }
        
        [data-testid="stSidebar"] .stRadio > div {
            gap: 0.1rem;
        }
        
        [data-testid="stSidebar"] .stRadio label {
            padding: 0.4rem 0.6rem;
            border-radius: var(--radius-sm);
            font-size: 0.8rem;
        }
        
        [data-testid="stSidebar"] .stRadio label:hover {
            background: #EFF6FF;
        }

        [data-testid="stTable"] {
            border-radius: var(--radius-sm) !important;
            overflow: hidden !important;
            border: 1px solid var(--border) !important;
            font-size: 0.8rem !important;
        }
        
        [data-testid="stTable"] th {
            background: #F1F5F9 !important;
            font-weight: 600 !important;
            color: #475569 !important;
            font-size: 0.68rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
            padding: 0.45rem 0.75rem !important;
        }
        
        [data-testid="stTable"] td {
            padding: 0.4rem 0.75rem !important;
            border-bottom: 1px solid #E2E8F0 !important;
        }

        .streamlit-expanderHeader {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-sm) !important;
            font-weight: 500 !important;
            font-size: 0.82rem !important;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: var(--primary) !important;
            background: #EFF6FF !important;
        }

        .stAlert {
            border-radius: var(--radius-sm) !important;
            font-size: 0.8rem !important;
        }

        hr {
            border-color: var(--border) !important;
            margin: 1rem 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )