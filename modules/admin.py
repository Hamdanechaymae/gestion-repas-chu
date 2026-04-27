import streamlit as st
import pandas as pd
from database import (
    ajouter_service, get_services, supprimer_service, get_services_dict,
    ajouter_regime, get_regimes, supprimer_regime,
    ajouter_utilisateur, get_utilisateurs, supprimer_utilisateur,
    ajouter_chambre, get_chambres, supprimer_chambre,
    get_stats_admin
)


def gestion_services():
    st.title("🏥 Gestion des services")

    nom_service = st.text_input("Nom du service", placeholder="Ex : Pédiatrie")

    if st.button("Ajouter le service", key="add_service"):
        if nom_service.strip():
            try:
                ajouter_service(nom_service.strip())
                st.success("Service ajouté avec succès.")
                st.rerun()
            except Exception:
                st.error("Ce service existe déjà.")
        else:
            st.warning("Veuillez saisir le nom du service.")

    services = get_services()

    if services:
        df = pd.DataFrame(services, columns=["ID", "Nom du service"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        service_options = {service[1]: service[0] for service in services}
        service_choisi = st.selectbox("Choisir un service à supprimer", list(service_options.keys()))

        if st.button("Supprimer le service", key="delete_service"):
            supprimer_service(service_options[service_choisi])
            st.warning("Service supprimé.")
            st.rerun()
    else:
        st.info("Aucun service enregistré.")


def gestion_regimes():
    st.title("🥗 Gestion des régimes")

    nom_regime = st.text_input("Nom du régime", placeholder="Ex : Normal")

    if st.button("Ajouter le régime", key="add_regime"):
        if nom_regime.strip():
            try:
                ajouter_regime(nom_regime.strip())
                st.success("Régime ajouté avec succès.")
                st.rerun()
            except Exception:
                st.error("Ce régime existe déjà.")
        else:
            st.warning("Veuillez saisir le nom du régime.")

    regimes = get_regimes()

    if regimes:
        df = pd.DataFrame(regimes, columns=["ID", "Nom du régime"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        regime_options = {regime[1]: regime[0] for regime in regimes}
        regime_choisi = st.selectbox("Choisir un régime à supprimer", list(regime_options.keys()))

        if st.button("Supprimer le régime", key="delete_regime"):
            supprimer_regime(regime_options[regime_choisi])
            st.warning("Régime supprimé.")
            st.rerun()
    else:
        st.info("Aucun régime enregistré.")


def gestion_chambres():
    st.title("🛏️ Gestion des chambres")

    services = get_services_dict()

    if not services:
        st.warning("Ajoute d’abord un service avant d’ajouter des chambres.")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("➕ Ajouter une chambre")

        numero_chambre = st.text_input("Numéro de chambre", placeholder="Ex : 101")
        service_nom = st.selectbox("Service", list(services.keys()), key="service_chambre")

        if st.button("Ajouter la chambre", key="add_chambre"):
            if numero_chambre.strip():
                try:
                    ajouter_chambre(numero_chambre.strip(), services[service_nom])
                    st.success("Chambre ajoutée avec succès.")
                    st.rerun()
                except Exception:
                    st.error("Erreur lors de l’ajout de la chambre.")
            else:
                st.warning("Veuillez saisir le numéro de chambre.")

    with col2:
        st.subheader("📋 Liste des chambres")

        chambres = get_chambres()

        if chambres:
            df = pd.DataFrame(chambres, columns=["ID", "Numéro chambre", "Service"])
            st.dataframe(df, use_container_width=True, hide_index=True)

            chambre_options = {
                f"Chambre {chambre[1]} - {chambre[2]}": chambre[0]
                for chambre in chambres
            }

            chambre_choisie = st.selectbox(
                "Choisir une chambre à supprimer",
                list(chambre_options.keys())
            )

            if st.button("Supprimer la chambre", key="delete_chambre"):
                supprimer_chambre(chambre_options[chambre_choisie])
                st.warning("Chambre supprimée.")
                st.rerun()
        else:
            st.info("Aucune chambre enregistrée.")


def gestion_utilisateurs():
    st.title("👥 Gestion des utilisateurs")

    nom = st.text_input("Nom complet")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")
    role = st.selectbox("Rôle", ["admin", "service", "cuisine"])

    if st.button("Ajouter l'utilisateur", key="add_user"):
        if nom.strip() and email.strip() and mot_de_passe.strip():
            try:
                ajouter_utilisateur(nom.strip(), email.strip(), mot_de_passe.strip(), role)
                st.success("Utilisateur ajouté avec succès.")
                st.rerun()
            except Exception:
                st.error("Cet email existe déjà.")
        else:
            st.warning("Veuillez remplir tous les champs.")

    users = get_utilisateurs()

    if users:
        df = pd.DataFrame(users, columns=["ID", "Nom", "Email", "Rôle"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        user_options = {
            f"{user[1]} - {user[2]} ({user[3]})": user[0]
            for user in users
        }

        user_choisi = st.selectbox("Choisir un utilisateur à supprimer", list(user_options.keys()))

        if st.button("Supprimer l'utilisateur", key="delete_user"):
            supprimer_utilisateur(user_options[user_choisi])
            st.warning("Utilisateur supprimé.")
            st.rerun()
    else:
        st.info("Aucun utilisateur enregistré.")


def dashboard_admin():
    st.title("👨‍💼 Dashboard Administrateur")

    (
        total_services,
        total_regimes,
        total_users,
        total_chambres,
        total_bons,
        total_normal,
        total_diabetique
    ) = get_stats_admin()

    total_repas = total_normal + total_diabetique

    st.markdown("""
    <div class="custom-card">
        <h3>Bienvenue dans l’espace administrateur</h3>
        <p>
            Cet espace permet de gérer les services, les chambres, les régimes,
            les utilisateurs et de suivre les bons de repas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏥 Services", total_services)
    col2.metric("🛏️ Chambres", total_chambres)
    col3.metric("🥗 Régimes", total_regimes)
    col4.metric("👥 Utilisateurs", total_users)

    st.divider()

    col5, col6, col7 = st.columns(3)

    col5.metric("📄 Bons", total_bons)
    col6.metric("🍽️ Normal", total_normal)
    col7.metric("📊 Total repas", total_repas)


def statistiques_admin():
    st.title("📊 Statistiques Administrateur")

    (
        total_services,
        total_regimes,
        total_users,
        total_chambres,
        total_bons,
        total_normal,
        total_diabetique
    ) = get_stats_admin()

    total_repas = total_normal + total_diabetique

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("🏥 Services", total_services)
    col2.metric("🛏️ Chambres", total_chambres)
    col3.metric("🥗 Régimes", total_regimes)

    col4.metric("👥 Utilisateurs", total_users)
    col5.metric("📄 Bons", total_bons)
    col6.metric("📊 Total repas", total_repas)


def admin_page():
    menu = st.sidebar.radio(
        "Fonctionnalités Admin",
        ["Tableau de bord", "Services", "Chambres", "Régimes", "Utilisateurs", "Statistiques"],
        key="menu_admin"
    )

    if menu == "Tableau de bord":
        dashboard_admin()

    elif menu == "Services":
        gestion_services()

    elif menu == "Chambres":
        gestion_chambres()

    elif menu == "Régimes":
        gestion_regimes()

    elif menu == "Utilisateurs":
        gestion_utilisateurs()

    elif menu == "Statistiques":
        statistiques_admin()