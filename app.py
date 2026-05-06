import os
import streamlit as st

from style import load_css
from auth import verifier_connexion
from modules.admin import admin_page
from modules.service import service_page
from modules.cuisine import cuisine_page
from database import init_db


st.set_page_config(
    page_title="CHU Repas",
    page_icon="🍽️",
    layout="wide"
)

init_db()
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

    col_logo, col_brand, col1, col2, col3, col4 = st.columns([0.7, 2.2, 1, 1, 1, 1])

    with col_logo:
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "chu.jpg")
        if os.path.exists(logo_path):
            st.image(logo_path, width=56)

    with col_brand:
        st.markdown(
            """
            <div class="brand-title">CHU Repas</div>
            <div class="brand-subtitle">Gestion hospitalière des bons de repas</div>
            """,
            unsafe_allow_html=True
        )

    with col1:
        if st.button("Accueil", key="nav_home", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    with col2:
        if st.button("À propos", key="nav_about", use_container_width=True):
            st.session_state["page"] = "about"
            st.rerun()

    with col3:
        if st.button("Contact", key="nav_contact", use_container_width=True):
            st.session_state["page"] = "contact"
            st.rerun()

    with col4:
        if st.button("Connexion", key="nav_login", use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def page_accueil():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">Application métier</div>
            <h1>Gestion fiable des bons de repas hospitaliers</h1>
            <p>
                CHU Repas centralise la saisie, le suivi et la consultation des bons de repas
                entre les services hospitaliers, les chambres et la cuisine. L’objectif est de
                réduire les erreurs manuelles, améliorer la coordination et faciliter le suivi quotidien.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Accès par rôle")
    col1, col2, col3 = st.columns(3)

    role_cards = [
        (
            "Administration",
            "Gestion des services, chambres, régimes, utilisateurs et suivi global des données."
        ),
        (
            "Service hospitalier",
            "Saisie des bons, consultation des enregistrements et mise à jour des demandes."
        ),
        (
            "Cuisine",
            "Consultation des volumes à préparer, suivi des statuts et synthèse par service."
        ),
    ]

    for col, (title, desc) in zip([col1, col2, col3], role_cards):
        with col:
            st.markdown(
                f"""
                <div class="custom-card">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    st.subheader("Fonctionnalités principales")
    col4, col5, col6, col7 = st.columns(4)

    feature_cards = [
        ("Services", "Organisation des unités hospitalières et rattachement des chambres."),
        ("Chambres", "Suivi structuré des chambres par service."),
        ("Bons de repas", "Création, modification et consultation des bons enregistrés."),
        ("Préparation cuisine", "Visualisation des totaux à produire et des statuts de traitement."),
    ]

    for col, (title, desc) in zip([col4, col5, col6, col7], feature_cards):
        with col:
            st.markdown(
                f"""
                <div class="custom-card">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    st.info(
        "Cette application est conçue pour un usage opérationnel quotidien : lisibilité, traçabilité et simplicité d’exécution."
    )


def page_about():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">À propos</div>
            <h1>Une application conçue pour le suivi hospitalier des repas</h1>
            <p>
                CHU Repas est une application web dédiée à la gestion des bons de repas
                dans un environnement hospitalier. Elle facilite la coordination entre les services,
                les chambres et la cuisine centrale, tout en améliorant la fiabilité des informations saisies.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="custom-card">
                <h3>Objectif</h3>
                <p>
                    Structurer la gestion des bons de repas, limiter les erreurs manuelles
                    et améliorer le suivi quotidien des demandes par service hospitalier.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="custom-card">
                <h3>Valeur métier</h3>
                <p>
                    Fournir un outil simple, lisible et fiable pour suivre les repas,
                    centraliser les données et fluidifier la communication avec la cuisine.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            """
            <div class="custom-card">
                <h3>Fonctionnalités couvertes</h3>
                <p>
                    Gestion des services, chambres, utilisateurs, saisie des bons,
                    consultation des demandes et suivi des volumes à préparer.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="custom-card">
                <h3>Bénéfices attendus</h3>
                <p>
                    Meilleure traçabilité, organisation plus claire et réduction des risques
                    d’oubli ou d’incohérence dans la transmission des repas.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


def page_contact():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">Contact</div>
            <h1>Informations de contact</h1>
            <p>
                Pour toute demande liée à l’application ou à la gestion des bons de repas,
                vous pouvez contacter le CHU d’Oujda.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="custom-card">
                <h3>Établissement</h3>
                <p>CHU Oujda</p>
                <h3>Email</h3>
                <p>contact@chuoujda.ma</p>
                <h3>Téléphone</h3>
                <p>+212 5 36 53 91 00</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="custom-card">
                <h3>Projet</h3>
                <p>Application de gestion des bons de repas hospitaliers</p>
                <h3>Usage</h3>
                <p>Suivi des services, chambres, bons de repas et coordination avec la cuisine.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def page_login():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">Accès sécurisé</div>
            <h1>Connexion</h1>
            <p>
                Accédez à votre espace selon votre rôle pour gérer ou consulter les opérations
                liées aux bons de repas.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        role = st.selectbox("Rôle", ["admin", "service", "cuisine"])

        if st.button("Se connecter", key="btn_login", use_container_width=True):
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

        st.markdown("</div>", unsafe_allow_html=True)


def dashboard():
    user = st.session_state["user"]

    st.sidebar.success(f"Connecté : {user['nom']}")
    st.sidebar.write(f"Rôle : {user['role']}")

    if st.sidebar.button("Déconnexion", key="btn_logout"):
        logout()

    if user["role"] == "admin":
        admin_page()
    elif user["role"] == "service":
        service_page()
    elif user["role"] == "cuisine":
        cuisine_page()


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