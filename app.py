import os
import streamlit as st
from style import load_css
from auth import verifier_connexion

from modules.admin import admin_page
from modules.service import service_page
from modules.cuisine import cuisine_page

st.set_page_config(
    page_title="CHU Repas",
    page_icon="🏥",
    layout="wide"
)

load_css()

if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "home"


def logout():
    st.session_state["user"] = None
    st.session_state["page"] = "home"
    st.rerun()


def navbar():
    st.markdown('<div class="navbar-box">', unsafe_allow_html=True)

    nav_logo, nav_brand, nav1, nav2, nav3, nav4 = st.columns([0.7, 3, 1, 1, 1, 1.3])

    with nav_logo:
        logo_path = os.path.join(os.path.dirname(__file__), "logo_chu.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=60)
        else:
            st.markdown("<h2>🏥</h2>", unsafe_allow_html=True)

    with nav_brand:
        st.markdown("""
        <div class="brand-title">CHU Repas</div>
        <div class="brand-subtitle">Gestion hospitalière des bons de repas</div>
        """, unsafe_allow_html=True)

    with nav1:
        if st.button("Accueil", key="btn_accueil"):
            st.session_state["page"] = "home"

    with nav2:
        if st.button("À propos", key="btn_about"):
            st.session_state["page"] = "about"

    with nav3:
        if st.button("Contact", key="btn_contact"):
            st.session_state["page"] = "contact"

    with nav4:
        if st.button("Connexion", key="btn_login"):
            st.session_state["page"] = "login"

    st.markdown('</div>', unsafe_allow_html=True)


def page_accueil():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Solution numérique pour le CHU Oujda</div>
        <h1>Modernisation de la gestion des bons de repas hospitaliers</h1>
        <p>
            Une application web professionnelle conçue pour organiser les services,
            les régimes, les utilisateurs et les bons de repas afin d’améliorer
            le suivi, la précision et la coordination avec la cuisine hospitalière.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3>🏥 Services</h3>
            <p>Organisation des services hospitaliers.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3>🥗 Régimes</h3>
            <p>Gestion des régimes alimentaires.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="custom-card">
            <h3>📝 Bons</h3>
            <p>Création et suivi des bons de repas.</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="custom-card">
            <h3>📊 Totaux</h3>
            <p>Affichage des totaux pour la cuisine.</p>
        </div>
        """, unsafe_allow_html=True)


def page_about():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">À propos</div>
        <h1>Une application pensée pour le contexte hospitalier</h1>
        <p>
            Cette application facilite la gestion quotidienne des bons de repas
            au sein du CHU Oujda. Elle permet à chaque utilisateur d’accéder
            aux fonctionnalités adaptées à son rôle.
        </p>
    </div>
    """, unsafe_allow_html=True)


def page_contact():
    st.markdown("""
    <div class="custom-card">
        <h1>Contact</h1>
        <p><b>Établissement :</b> CHU Oujda</p>
        <p><b>Encadrante :</b> Madame Khadija Himri</p>
        <p><b>Réalisé par :</b> Chaymae Hamdane et Wiame Jaouher</p>
        <p><b>Projet :</b> Gestion des bons de repas hospitaliers</p>
    </div>
    """, unsafe_allow_html=True)


def page_login():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Accès sécurisé</div>
        <h1>Connexion à l’espace utilisateur</h1>
        <p>
            Chaque utilisateur accède uniquement aux fonctionnalités correspondant
            à son rôle.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])

    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        role_choisi = st.selectbox("Rôle", ["admin", "service", "cuisine"])

        if st.button("Se connecter", key="btn_se_connecter"):
            user = verifier_connexion(email, password)

            if user and user[3] == role_choisi:
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


def dashboard():
    user = st.session_state["user"]

    st.sidebar.success(f"Connecté : {user['nom']}")
    st.sidebar.write(f"Rôle : {user['role']}")

    if st.sidebar.button("Déconnexion", key="btn_deconnexion"):
        logout()

    if user["role"] == "admin":
        admin_page()

    elif user["role"] == "service":
        service_page()

    elif user["role"] == "cuisine":
        cuisine_page()


if st.session_state["user"] is None:
    navbar()

    if st.session_state["page"] == "home":
        page_accueil()
    elif st.session_state["page"] == "about":
        page_about()
    elif st.session_state["page"] == "contact":
        page_contact()
    elif st.session_state["page"] == "login":
        page_login()
else:
    dashboard()