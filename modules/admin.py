import streamlit as st
import pandas as pd
from database import (
    ajouter_service,
    get_services,
    supprimer_service,
    ajouter_regime,
    get_regimes,
    supprimer_regime,
    ajouter_utilisateur,
    get_utilisateurs,
    supprimer_utilisateur,
    get_stats_admin
)


def gestion_services():
    st.title("🏥 Gestion des services")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("➕ Ajouter un service")
        nom_service = st.text_input("Nom du service", placeholder="Ex : Pédiatrie")

        if st.button("Ajouter le service", key="add_service"):
            if nom_service.strip():
                try:
                    ajouter_service(nom_service.strip())
                    st.success("Service ajouté avec succès.")
                    st.rerun()
                except Exception:
                    st.error("Ce service existe déjà ou une erreur est survenue.")
            else:
                st.warning("Veuillez saisir le nom du service.")

    with col2:
        st.subheader("📋 Liste des services")
        services = get_services()

        if services:
            df = pd.DataFrame(services, columns=["ID", "Nom du service"])
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("🗑️ Supprimer un service")
            service_options = {service[1]: service[0] for service in services}
            service_choisi = st.selectbox(
                "Choisir un service à supprimer",
                list(service_options.keys())
            )

            if st.button("Supprimer le service", key="delete_service"):
                supprimer_service(service_options[service_choisi])
                st.warning("Service supprimé.")
                st.rerun()
        else:
            st.info("Aucun service enregistré.")


def gestion_regimes():
    st.title("🥗 Gestion des régimes")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("➕ Ajouter un régime")
        nom_regime = st.text_input("Nom du régime", placeholder="Ex : Normal")

        if st.button("Ajouter le régime", key="add_regime"):
            if nom_regime.strip():
                try:
                    ajouter_regime(nom_regime.strip())
                    st.success("Régime ajouté avec succès.")
                    st.rerun()
                except Exception:
                    st.error("Ce régime existe déjà ou une erreur est survenue.")
            else:
                st.warning("Veuillez saisir le nom du régime.")

    with col2:
        st.subheader("📋 Liste des régimes")
        regimes = get_regimes()

        if regimes:
            df = pd.DataFrame(regimes, columns=["ID", "Nom du régime"])
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("🗑️ Supprimer un régime")
            regime_options = {regime[1]: regime[0] for regime in regimes}
            regime_choisi = st.selectbox(
                "Choisir un régime à supprimer",
                list(regime_options.keys())
            )

            if st.button("Supprimer le régime", key="delete_regime"):
                supprimer_regime(regime_options[regime_choisi])
                st.warning("Régime supprimé.")
                st.rerun()
        else:
            st.info("Aucun régime enregistré.")


def gestion_utilisateurs():
    st.title("👥 Gestion des utilisateurs")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("➕ Ajouter un utilisateur")

        nom = st.text_input("Nom complet", placeholder="Ex : Agent Service")
        email = st.text_input("Email", placeholder="Ex : service@chu.ma")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        role = st.selectbox("Rôle", ["admin", "service", "cuisine"])

        if st.button("Ajouter l'utilisateur", key="add_user"):
            if nom.strip() and email.strip() and mot_de_passe.strip():
                try:
                    ajouter_utilisateur(
                        nom.strip(),
                        email.strip(),
                        mot_de_passe.strip(),
                        role
                    )
                    st.success("Utilisateur ajouté avec succès.")
                    st.rerun()
                except Exception:
                    st.error("Cet email existe déjà ou une erreur est survenue.")
            else:
                st.warning("Veuillez remplir tous les champs.")

    with col2:
        st.subheader("📋 Liste des utilisateurs")

        users = get_utilisateurs()

        if users:
            df = pd.DataFrame(users, columns=["ID", "Nom", "Email", "Rôle"])
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("🗑️ Supprimer un utilisateur")

            user_options = {
                f"{user[1]} - {user[2]} ({user[3]})": user[0]
                for user in users
            }

            user_choisi = st.selectbox(
                "Choisir un utilisateur à supprimer",
                list(user_options.keys())
            )

            if st.button("Supprimer l'utilisateur", key="delete_user"):
                supprimer_utilisateur(user_options[user_choisi])
                st.warning("Utilisateur supprimé.")
                st.rerun()
        else:
            st.info("Aucun utilisateur enregistré.")


def statistiques_admin():
    st.title("📊 Statistiques Administrateur")

    (
        total_services,
        total_regimes,
        total_users,
        total_bons,
        total_normal,
        total_diabetique
    ) = get_stats_admin()

    total_repas = total_normal + total_diabetique

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("🏥 Services", total_services)
    col2.metric("🥗 Régimes", total_regimes)
    col3.metric("👥 Utilisateurs", total_users)

    col4.metric("📄 Bons", total_bons)
    col5.metric("🍽️ Repas normaux", total_normal)
    col6.metric("📊 Total repas", total_repas)

    st.divider()

    st.markdown("""
    <div class="custom-card">
        <h3>Résumé global</h3>
        <p>
            Cette page permet à l’administrateur d’avoir une vision globale
            sur les services, les régimes, les utilisateurs et les bons de repas.
        </p>
    </div>
    """, unsafe_allow_html=True)


def dashboard_admin():
    st.title("👨‍💼 Dashboard Administrateur")

    (
        total_services,
        total_regimes,
        total_users,
        total_bons,
        total_normal,
        total_diabetique
    ) = get_stats_admin()

    total_repas = total_normal + total_diabetique

    st.markdown("""
    <div class="custom-card">
        <h3>Bienvenue dans l’espace administrateur</h3>
        <p>
            Cet espace permet de gérer les services, les régimes,
            les utilisateurs et de suivre l’activité globale de l’application.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏥 Services", total_services)
    col2.metric("🥗 Régimes", total_regimes)
    col3.metric("👥 Utilisateurs", total_users)
    col4.metric("📄 Bons", total_bons)

    st.divider()

    col5, col6, col7 = st.columns(3)
    col5.metric("🍽️ Normal", total_normal)
    col6.metric("🥗 Diabétique", total_diabetique)
    col7.metric("📊 Total repas", total_repas)


def admin_page():
    menu = st.sidebar.radio(
        "Fonctionnalités Admin",
        ["Dashboard", "Services", "Régimes", "Utilisateurs", "Statistiques"],
        key="menu_admin"
    )

    if menu == "Dashboard":
        dashboard_admin()

    elif menu == "Services":
        gestion_services()

    elif menu == "Régimes":
        gestion_regimes()

    elif menu == "Utilisateurs":
        gestion_utilisateurs()

    elif menu == "Statistiques":
        statistiques_admin()