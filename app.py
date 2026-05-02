import os
import streamlit as st
from style import load_css
from auth import verifier_connexion

from modules.admin import admin_page
from modules.service import service_page
from modules.cuisine import cuisine_page
from database import init_db


# ================= CONFIG =================
st.set_page_config(
    page_title="CHU Repas",
    page_icon="🏥",
    layout="wide"
)

# INIT DB
init_db()

# CSS
load_css()


# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "home"


# ================= LOGOUT =================
def logout():
    st.session_state["user"] = None
    st.session_state["page"] = "home"
    st.rerun()


# ================= NAVBAR =================
def navbar():
    st.markdown('<div class="navbar-box">', unsafe_allow_html=True)

    col_logo, col_brand, col1, col2, col3, col4 = st.columns([0.7, 2, 1, 1, 1, 1])

    with col_logo:
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "chu.jpg")

        if os.path.exists(logo_path):
            st.image(logo_path, width=60)
        else:
            st.markdown("<h2>🏥</h2>", unsafe_allow_html=True)

    with col_brand:
        st.markdown("""
        <div class="brand-title">CHU Repas</div>
        <div class="brand-subtitle">Gestion hospitalière des bons de repas</div>
        """, unsafe_allow_html=True)

    with col1:
        if st.button("Accueil", key="nav_home"):
            st.session_state["page"] = "home"
            st.rerun()

    with col2:
        if st.button("À propos", key="nav_about"):
            st.session_state["page"] = "about"
            st.rerun()

    with col3:
        if st.button("Contact", key="nav_contact"):
            st.session_state["page"] = "contact"
            st.rerun()

    with col4:
        if st.button("Connexion", key="nav_login"):
            st.session_state["page"] = "login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ================= ACCUEIL =================
def page_accueil():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">🚀 Application intelligente</div>
        <h1>CHU Repas</h1>
        <p>
            Plateforme moderne de gestion des bons de repas hospitaliers.<br>
            Rapide • Fiable • Professionnelle
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    cards = [
        ("🏥 Services", "Organisation des services hospitaliers."),
        ("🥗 Régimes", "Gestion des régimes alimentaires."),
        ("📝 Bons", "Création et suivi des bons de repas."),
        ("📊 Totaux", "Analyse des repas pour la cuisine.")
    ]

    for col, (title, desc) in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(f"""
            <div class="custom-card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)


# ================= ABOUT =================
def page_about():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">À propos</div>
        <h1>Application de gestion hospitalière</h1>
        <p>
            CHU Repas est une application web conçue pour faciliter la gestion
            des bons de repas au sein d’un établissement hospitalier.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ================= CONTACT =================
def page_contact():
    st.markdown("""
    <div class="custom-card">
        <h1>Contact</h1>
        <p><b>CHU :</b> Oujda</p>
        <p><b>Encadrante :</b> Mme Khadija Himri</p>
        <p><b>Réalisé par :</b> Chaymae Hamdane & Wiame Jaouher</p>
        <p><b>Projet :</b> Gestion des bons de repas hospitaliers</p>
    </div>
    """, unsafe_allow_html=True)


# ================= LOGIN =================
def page_login():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Accès sécurisé</div>
        <h1>Connexion</h1>
        <p>Accédez à votre espace selon votre rôle.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])

    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        role = st.selectbox("Rôle", ["admin", "service", "cuisine"])

        if st.button("Se connecter", key="btn_login"):
            user = verifier_connexion(email, password)

            if user and user[3] == role:
                st.session_state["user"] = {
                    "id": user[0],
                    "nom": user[1],
                    "email": user[2],
                    "role": user[3]
                }
                st.rerun()
            else:
                st.error("Email, mot de passe ou rôle incorrect.")

        st.markdown('</div>', unsafe_allow_html=True)


# ================= DASHBOARD =================
def dashboard():
    user = st.session_state["user"]

    st.sidebar.success(f"👤 Connecté : {user['nom']}")
    st.sidebar.write(f"Rôle : {user['role']}")

    if st.sidebar.button("🚪 Déconnexion", key="btn_logout"):
        logout()

    if user["role"] == "admin":
        admin_page()

    elif user["role"] == "service":
        service_page()

    elif user["role"] == "cuisine":
        cuisine_page()


# ================= ROUTING =================
if st.session_state["user"] is None:
    navbar()

    page = st.session_state["page"]

    if page == "home":
        page_accueil()

    elif page == "about":
        page_about()

    elif page == "contact":
        page_contact()

    elif page == "login":
        page_login()

else:
    dashboard()