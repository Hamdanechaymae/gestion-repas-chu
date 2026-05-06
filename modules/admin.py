import streamlit as st
import pandas as pd

from database import (
    ajouter_service,
    get_services,
    supprimer_service,
    get_services_dict,
    ajouter_regime,
    get_regimes,
    supprimer_regime,
    ajouter_utilisateur,
    get_utilisateurs,
    supprimer_utilisateur,
    ajouter_chambre,
    get_chambres,
    supprimer_chambre,
    get_stats_admin,
)


def section_header(title, description):
    st.markdown(
        f"""
        <div class="hero" style="padding: 1.2rem 1.4rem; margin-bottom: 1rem;">
            <h1 style="font-size: 1.5rem; margin-bottom: 0.35rem;">{title}</h1>
            <p style="margin-bottom: 0;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def gestion_services():
    section_header(
        "Gestion des services",
        "Ajoutez, consultez et supprimez les services hospitaliers utilisés dans l’application."
    )

    col_form, col_table = st.columns([1, 1.4], gap="large")

    with col_form:
        st.subheader("Ajouter un service")
        nom_service = st.text_input("Nom du service", placeholder="Ex : Pédiatrie")

        if st.button("Ajouter le service", key="add_service", use_container_width=True):
            if nom_service.strip():
                try:
                    ajouter_service(nom_service.strip())
                    st.success("Service ajouté avec succès.")
                    st.rerun()
                except Exception:
                    st.error("Ce service existe déjà.")
            else:
                st.warning("Veuillez saisir le nom du service.")

    with col_table:
        st.subheader("Liste des services")
        services = get_services()

        if services:
            df = pd.DataFrame(services, columns=["ID", "Nom du service"])
            st.dataframe(df, use_container_width=True, hide_index=True)

            service_options = {service[1]: service[0] for service in services}
            service_choisi = st.selectbox(
                "Choisir un service à supprimer",
                list(service_options.keys())
            )

            if st.button("Supprimer le service", key="delete_service", use_container_width=True):
                supprimer_service(service_options[service_choisi])
                st.warning("Service supprimé.")
                st.rerun()
        else:
            st.info("Aucun service enregistré.")


def gestion_regimes():
    section_header(
        "Gestion des régimes",
        "Gérez les régimes alimentaires disponibles pour les bons de repas."
    )

    col_form, col_table = st.columns([1, 1.4], gap="large")

    with col_form:
        st.subheader("Ajouter un régime")
        nom_regime = st.text_input("Nom du régime", placeholder="Ex : Normal")

        if st.button("Ajouter le régime", key="add_regime", use_container_width=True):
            if nom_regime.strip():
                try:
                    ajouter_regime(nom_regime.strip())
                    st.success("Régime ajouté avec succès.")
                    st.rerun()
                except Exception:
                    st.error("Ce régime existe déjà.")
            else:
                st.warning("Veuillez saisir le nom du régime.")

    with col_table:
        st.subheader("Liste des régimes")
        regimes = get_regimes()

        if regimes:
            df = pd.DataFrame(regimes, columns=["ID", "Nom du régime"])
            st.dataframe(df, use_container_width=True, hide_index=True)

            regime_options = {regime[1]: regime[0] for regime in regimes}
            regime_choisi = st.selectbox(
                "Choisir un régime à supprimer",
                list(regime_options.keys())
            )

            if st.button("Supprimer le régime", key="delete_regime", use_container_width=True):
                supprimer_regime(regime_options[regime_choisi])
                st.warning("Régime supprimé.")
                st.rerun()
        else:
            st.info("Aucun régime enregistré.")


def gestion_chambres():
    section_header(
        "Gestion des chambres",
        "Associez les chambres aux services hospitaliers pour fiabiliser la saisie des bons."
    )

    services = get_services_dict()
    if not services:
        st.warning("Ajoutez d’abord un service avant d’ajouter des chambres.")
        return

    col_form, col_table = st.columns([1, 1.5], gap="large")

    with col_form:
        st.subheader("Ajouter une chambre")
        numero_chambre = st.text_input("Numéro de chambre", placeholder="Ex : 101")
        service_nom = st.selectbox("Service", list(services.keys()), key="service_chambre")

        if st.button("Ajouter la chambre", key="add_chambre", use_container_width=True):
            if numero_chambre.strip():
                try:
                    ajouter_chambre(numero_chambre.strip(), services[service_nom])
                    st.success("Chambre ajoutée avec succès.")
                    st.rerun()
                except Exception:
                    st.error("Erreur lors de l’ajout de la chambre.")
            else:
                st.warning("Veuillez saisir le numéro de chambre.")

    with col_table:
        st.subheader("Liste des chambres")
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

            if st.button("Supprimer la chambre", key="delete_chambre", use_container_width=True):
                supprimer_chambre(chambre_options[chambre_choisie])
                st.warning("Chambre supprimée.")
                st.rerun()
        else:
            st.info("Aucune chambre enregistrée.")


def gestion_utilisateurs():
    section_header(
        "Gestion des utilisateurs",
        "Créez les accès selon le rôle de chaque utilisateur dans l’application."
    )

    col_form, col_table = st.columns([1, 1.5], gap="large")

    with col_form:
        st.subheader("Ajouter un utilisateur")
        nom = st.text_input("Nom complet")
        email = st.text_input("Email")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        role = st.selectbox("Rôle", ["admin", "service", "cuisine"])

        if st.button("Ajouter l'utilisateur", key="add_user", use_container_width=True):
            if nom.strip() and email.strip() and mot_de_passe.strip():
                try:
                    ajouter_utilisateur(nom.strip(), email.strip(), mot_de_passe.strip(), role)
                    st.success("Utilisateur ajouté avec succès.")
                    st.rerun()
                except Exception:
                    st.error("Cet email existe déjà.")
            else:
                st.warning("Veuillez remplir tous les champs.")

    with col_table:
        st.subheader("Liste des utilisateurs")
        users = get_utilisateurs()

        if users:
            df = pd.DataFrame(users, columns=["ID", "Nom", "Email", "Rôle"])
            st.dataframe(df, use_container_width=True, hide_index=True)

            user_options = {
                f"{user[1]} - {user[2]} ({user[3]})": user[0]
                for user in users
            }
            user_choisi = st.selectbox(
                "Choisir un utilisateur à supprimer",
                list(user_options.keys())
            )

            if st.button("Supprimer l'utilisateur", key="delete_user", use_container_width=True):
                supprimer_utilisateur(user_options[user_choisi])
                st.warning("Utilisateur supprimé.")
                st.rerun()
        else:
            st.info("Aucun utilisateur enregistré.")


def dashboard_admin():
    (
        total_services,
        total_regimes,
        total_users,
        total_chambres,
        total_bons,
        total_normal,
        total_diabetique,
    ) = get_stats_admin()

    total_repas = total_normal + total_diabetique

    section_header(
        "Tableau de bord administrateur",
        "Vue d’ensemble de la structure, des utilisateurs et de l’activité liée aux bons de repas."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Services", total_services)
    col2.metric("Chambres", total_chambres)
    col3.metric("Régimes", total_regimes)
    col4.metric("Utilisateurs", total_users)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    col5, col6, col7 = st.columns(3)
    col5.metric("Bons", total_bons)
    col6.metric("Repas normaux", total_normal)
    col7.metric("Total repas", total_repas)

    st.info(
        "Utilisez le menu de gauche pour gérer les référentiels et maintenir la qualité des données."
    )


def statistiques_admin():
    (
        total_services,
        total_regimes,
        total_users,
        total_chambres,
        total_bons,
        total_normal,
        total_diabetique,
    ) = get_stats_admin()

    total_repas = total_normal + total_diabetique

    section_header(
        "Statistiques administrateur",
        "Indicateurs globaux de suivi pour contrôler la structure et l’usage de l’application."
    )

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("Services", total_services)
    col2.metric("Chambres", total_chambres)
    col3.metric("Régimes", total_regimes)
    col4.metric("Utilisateurs", total_users)
    col5.metric("Bons", total_bons)
    col6.metric("Total repas", total_repas)


def admin_page():
    st.sidebar.markdown("## Administration")
    menu = st.sidebar.radio(
        "Fonctionnalités Admin",
        [
            "Tableau de bord",
            "Services",
            "Chambres",
            "Régimes",
            "Utilisateurs",
            "Statistiques",
        ],
        key="menu_admin",
        label_visibility="collapsed"
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