import streamlit as st
import pandas as pd
from datetime import date

from database import (
    ajouter_bon,
    get_services_dict,
    get_bons,
    modifier_bon,
    supprimer_bon,
    get_stats_service,
    get_derniers_bons
)


def dashboard_service_page():
    st.title("🏥 Dashboard Service")

    total_bons, total_normal, total_diabetique = get_stats_service()
    total_general = total_normal + total_diabetique

    st.markdown("""
    <div class="custom-card">
        <h3>Bienvenue dans l’espace service</h3>
        <p>
            Cet espace permet de créer, consulter et modifier les bons de repas
            envoyés à la cuisine hospitalière.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📄 Bons", total_bons)
    col2.metric("🍽️ Repas normaux", total_normal)
    col3.metric("🥗 Repas diabétiques", total_diabetique)
    col4.metric("📊 Total repas", total_general)

    st.divider()

    st.subheader("🕒 Derniers bons enregistrés")

    derniers = get_derniers_bons()

    if derniers:
        df = pd.DataFrame(
            derniers,
            columns=["Date", "Service", "Normal", "Diabétique"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun bon enregistré pour le moment.")


def ajouter_bon_page():
    st.title("📝 Ajouter un bon de repas")

    services = get_services_dict()

    if not services:
        st.warning("Aucun service disponible. L’administrateur doit d’abord ajouter des services.")
        return

    st.subheader("Nouveau bon")

    date_bon = st.date_input("Date du bon", value=date.today())

    service_nom = st.selectbox(
        "Service",
        list(services.keys()),
        key="service_add_bon"
    )

    normal = st.number_input(
        "Nombre de repas normal",
        min_value=0,
        step=1,
        key="normal_add_bon"
    )

    diabetique = st.number_input(
        "Nombre de repas diabétique",
        min_value=0,
        step=1,
        key="diabetique_add_bon"
    )

    if st.button("Enregistrer le bon", key="btn_add_bon"):
        if normal == 0 and diabetique == 0:
            st.warning("Veuillez saisir au moins un repas.")
        else:
            ajouter_bon(
                str(date_bon),
                services[service_nom],
                normal,
                diabetique
            )
            st.success("Bon de repas ajouté avec succès.")
            st.rerun()


def mes_bons_page():
    st.title("📄 Mes bons de repas")

    bons = get_bons()

    if bons:
        df = pd.DataFrame(
            bons,
            columns=["ID", "Date", "Service", "Normal", "Diabétique"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun bon enregistré.")


def modifier_bon_page():
    st.title("✏️ Modifier / Supprimer un bon")

    bons = get_bons()
    services = get_services_dict()

    if not bons:
        st.info("Aucun bon disponible.")
        return

    if not services:
        st.warning("Aucun service disponible.")
        return

    bon_options = {
        f"ID {b[0]} - {b[1]} - {b[2]}": b
        for b in bons
    }

    choix = st.selectbox(
        "Choisir un bon",
        list(bon_options.keys()),
        key="select_bon_modifier"
    )

    bon = bon_options[choix]

    id_bon = bon[0]
    date_actuelle = pd.to_datetime(bon[1]).date()
    service_actuel = bon[2]
    normal_actuel = bon[3]
    diabetique_actuel = bon[4]

    st.subheader("Modifier les informations du bon")

    nouvelle_date = st.date_input(
        "Date",
        value=date_actuelle,
        key="date_modifier_bon"
    )

    services_noms = list(services.keys())

    try:
        service_index = services_noms.index(service_actuel)
    except ValueError:
        service_index = 0

    nouveau_service = st.selectbox(
        "Service",
        services_noms,
        index=service_index,
        key="service_modifier_bon"
    )

    nouveau_normal = st.number_input(
        "Nombre de repas normal",
        min_value=0,
        step=1,
        value=int(normal_actuel),
        key="normal_modifier_bon"
    )

    nouveau_diabetique = st.number_input(
        "Nombre de repas diabétique",
        min_value=0,
        step=1,
        value=int(diabetique_actuel),
        key="diabetique_modifier_bon"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Modifier", key="btn_modifier_bon"):
            modifier_bon(
                id_bon,
                str(nouvelle_date),
                services[nouveau_service],
                nouveau_normal,
                nouveau_diabetique
            )
            st.success("Bon modifié avec succès.")
            st.rerun()

    with col2:
        if st.button("🗑️ Supprimer", key="btn_supprimer_bon"):
            supprimer_bon(id_bon)
            st.warning("Bon supprimé avec succès.")
            st.rerun()


def service_page():
    menu = st.sidebar.radio(
        "Fonctionnalités Service",
        ["Dashboard", "Ajouter un bon", "Mes bons", "Modifier un bon"],
        key="menu_service"
    )

    if menu == "Dashboard":
        dashboard_service_page()

    elif menu == "Ajouter un bon":
        ajouter_bon_page()

    elif menu == "Mes bons":
        mes_bons_page()

    elif menu == "Modifier un bon":
        modifier_bon_page()