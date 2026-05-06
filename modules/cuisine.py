import streamlit as st
import pandas as pd
from datetime import date

from database import (
    get_bons,
    get_bons_par_date,
    get_stats_cuisine,
    modifier_statut_bon,
    get_totaux_par_service,
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


def dashboard_cuisine():
    total_bons, total_normal, total_diabetique = get_stats_cuisine()
    total_general = total_normal + total_diabetique

    section_header(
        "Tableau de bord cuisine",
        "Vue d’ensemble des bons reçus et des volumes à préparer."
    )

    if total_bons == 0:
        st.warning("Aucun bon de repas reçu pour le moment.")
    elif total_general == 0:
        st.warning("Aucun repas enregistré.")
    else:
        taux_diabetique = (total_diabetique / total_general) * 100

        if taux_diabetique >= 50:
            st.error("Le volume de repas diabétiques est très élevé.")
        elif taux_diabetique >= 30:
            st.warning("Le volume de repas diabétiques est élevé.")
        else:
            st.success("Répartition actuelle des repas stable.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Bons reçus", total_bons)
    col2.metric("Repas normaux", total_normal)
    col3.metric("Repas diabétiques", total_diabetique)
    col4.metric("Total repas", total_general)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.subheader("Répartition des repas par type")

    df_chart = pd.DataFrame(
        {
            "Type": ["Normal", "Diabétique"],
            "Total": [total_normal, total_diabetique],
        }
    )
    st.bar_chart(df_chart.set_index("Type"))


def consultation_bons():
    section_header(
        "Consultation des bons",
        "Consultez les bons reçus et mettez à jour leur statut de traitement."
    )

    bons = get_bons()
    if not bons:
        st.info("Aucun bon enregistré.")
        return

    df = pd.DataFrame(
        bons,
        columns=["ID", "Date", "Service", "Chambre", "Normal", "Diabétique", "Statut"]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 0.8], gap="large")

    bon_dict = {
        f"ID {b[0]} - {b[2]} - Chambre {b[3]}": b[0]
        for b in bons
    }

    with col1:
        st.subheader("Mise à jour du statut")
        choix = st.selectbox("Choisir un bon", list(bon_dict.keys()))
        id_bon = bon_dict[choix]

        btn1, btn2 = st.columns(2)

        with btn1:
            if st.button("Marquer comme préparé", use_container_width=True):
                modifier_statut_bon(id_bon, "Préparé")
                st.success("Statut mis à jour.")
                st.rerun()

        with btn2:
            if st.button("Marquer comme annulé", use_container_width=True):
                modifier_statut_bon(id_bon, "Annulé")
                st.warning("Bon annulé.")
                st.rerun()

    with col2:
        st.subheader("Consigne")
        st.info(
            "Mettez à jour le statut uniquement après vérification de la demande reçue."
        )


def totaux_cuisine():
    section_header(
        "Totaux cuisine",
        "Consultez les volumes de repas à préparer pour une date donnée."
    )

    date_selection = st.date_input("Choisir une date", value=date.today())
    bons = get_bons_par_date(str(date_selection))

    if not bons:
        st.warning("Aucun bon trouvé pour cette date.")
        return

    df = pd.DataFrame(
        bons,
        columns=["ID", "Date", "Service", "Chambre", "Normal", "Diabétique", "Statut"]
    )

    total_normal = df["Normal"].sum()
    total_diabetique = df["Diabétique"].sum()
    total_general = total_normal + total_diabetique

    col1, col2, col3 = st.columns(3)
    col1.metric("Repas normaux", total_normal)
    col2.metric("Repas diabétiques", total_diabetique)
    col3.metric("Total repas", total_general)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    st.subheader("Totaux par service")
    totaux_service = get_totaux_par_service(str(date_selection))

    if totaux_service:
        df_service = pd.DataFrame(
            totaux_service,
            columns=["Service", "Normal", "Diabétique", "Total"]
        )

        st.dataframe(df_service, use_container_width=True, hide_index=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.subheader("Répartition par service")
        st.bar_chart(df_service.set_index("Service")[["Normal", "Diabétique"]])

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.subheader("Détail des bons")
    st.dataframe(df, use_container_width=True, hide_index=True)


def cuisine_page():
    st.sidebar.markdown("## Cuisine")
    menu = st.sidebar.radio(
        "Fonctionnalités Cuisine",
        ["Dashboard", "Consultation", "Totaux"],
        key="menu_cuisine",
        label_visibility="collapsed"
    )

    if menu == "Dashboard":
        dashboard_cuisine()
    elif menu == "Consultation":
        consultation_bons()
    elif menu == "Totaux":
        totaux_cuisine()