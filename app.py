import os
import streamlit as st

from style import load_css
from auth import verifier_connexion
from modules.admin import admin_page
from modules.service import service_page
from modules.cuisine import cuisine_page
from database import init_db, get_services


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
    for key in list(st.session_state.keys()):
        if key != "page":
            del st.session_state[key]
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
            <div class="brand-subtitle">Gestion hospitaliere des bons de repas</div>
            """,
            unsafe_allow_html=True
        )

    with col1:
        if st.button("Accueil", key="nav_home", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    with col2:
        if st.button("A propos", key="nav_about", use_container_width=True):
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
            <div class="hero-badge">Application metier</div>
            <h1>Gestion fiable des bons de repas hospitaliers</h1>
            <p>
                CHU Repas centralise la saisie, le suivi et la consultation des bons de repas
                entre les services hospitaliers, les chambres et la cuisine. L'objectif est de
                reduire les erreurs manuelles, ameliorer la coordination et faciliter le suivi quotidien.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Acces par role")
    col1, col2, col3 = st.columns(3)

    role_cards = [
        (
            "Administration",
            "Gestion des services, chambres, regimes, utilisateurs et suivi global des donnees."
        ),
        (
            "Service hospitalier",
            "Saisie des bons, consultation des enregistrements et mise a jour des demandes."
        ),
        (
            "Cuisine",
            "Consultation des volumes a preparer, suivi des statuts et synthese par service."
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

    st.subheader("Fonctionnalites principales")
    col4, col5, col6, col7 = st.columns(4)

    feature_cards = [
        ("Services", "Organisation des unites hospitalieres et rattachement des chambres."),
        ("Chambres", "Suivi structure des chambres par service."),
        ("Bons de repas", "Creation, modification et consultation des bons enregistres."),
        ("Preparation cuisine", "Visualisation des totaux a produire et des statuts de traitement."),
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
        "Cette application est concue pour un usage operationnel quotidien : lisibilite, tracabilite et simplicite d'execution."
    )


def page_about():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">A propos</div>
            <h1>Une application concue pour le suivi hospitalier des repas</h1>
            <p>
                CHU Repas est une application web dediee a la gestion des bons de repas
                dans un environnement hospitalier. Elle facilite la coordination entre les services,
                les chambres et la cuisine centrale, tout en ameliorant la fiabilite des informations saisies.
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
                    et ameliorer le suivi quotidien des demandes par service hospitalier.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="custom-card">
                <h3>Valeur metier</h3>
                <p>
                    Fournir un outil simple, lisible et fiable pour suivre les repas,
                    centraliser les donnees et fluidifier la communication avec la cuisine.
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
                <h3>Fonctionnalites couvertes</h3>
                <p>
                    Gestion des services, chambres, utilisateurs, saisie des bons,
                    consultation des demandes et suivi des volumes a preparer.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="custom-card">
                <h3>Benefices attendus</h3>
                <p>
                    Meilleure tracabilite, organisation plus claire et reduction des risques
                    d'oubli ou d'incoherence dans la transmission des repas.
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
                Pour toute demande liee a l'application ou a la gestion des bons de repas,
                vous pouvez contacter le CHU d'Oujda.
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
                <h3>Etablissement</h3>
                <p>CHU Oujda</p>
                <h3>Email</h3>
                <p>contact@chuoujda.ma</p>
                <h3>Telephone</h3>
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
            <div class="hero-badge">Acces securise</div>
            <h1>Connexion</h1>
            <p>
                Accedez a votre espace selon votre role pour gerer ou consulter les operations
                liees aux bons de repas.
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
        role = st.selectbox("Role", ["admin", "service", "cuisine"])

        if st.button("Se connecter", key="btn_login", use_container_width=True):
            user = verifier_connexion(email, password)

            if user and user[3] == role:
                st.session_state["user"] = {
                    "id": user[0],
                    "nom": user[1],
                    "email": user[2],
                    "role": user[3]
                }
                
                if role == "service":
                    st.session_state["choisir_service"] = True
                    st.rerun()
                else:
                    st.rerun()
            else:
                st.error("Email, mot de passe ou role incorrect.")

        st.markdown("</div>", unsafe_allow_html=True)


def choisir_service_page():
    """Page pour qu'un agent service choisisse son service hospitalier"""
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">Selection du service</div>
            <h1>Choisissez votre service</h1>
            <p>Selectionnez le service hospitalier pour lequel vous travaillez.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        services = get_services()
        if services:
            services_dict = {s[1]: s[0] for s in services}
            service_choisi = st.selectbox("Service hospitalier", list(services_dict.keys()))
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Valider", type="primary", use_container_width=True):
                    st.session_state["id_service"] = services_dict[service_choisi]
                    st.session_state["user_service"] = service_choisi
                    st.session_state["choisir_service"] = False
                    st.rerun()
            with col_b:
                if st.button("Retour", use_container_width=True):
                    st.session_state["user"] = None
                    st.session_state["choisir_service"] = False
                    st.session_state["page"] = "login"
                    st.rerun()
        else:
            st.error("Aucun service n'est configure. Contactez l'administrateur.")
            if st.button("Retour"):
                st.session_state["user"] = None
                st.session_state["choisir_service"] = False
                st.session_state["page"] = "home"
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)


def dashboard():
    user = st.session_state["user"]

    st.sidebar.success(f"Connecte : {user['nom']}")
    st.sidebar.write(f"Role : {user['role']}")
    
    if user["role"] == "service" and "user_service" in st.session_state:
        st.sidebar.write(f"Service : {st.session_state['user_service']}")

    if st.sidebar.button("Deconnexion", key="btn_logout"):
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
    if st.session_state["user"]["role"] == "service" and st.session_state.get("choisir_service", False):
        choisir_service_page()
    else:
        dashboard()