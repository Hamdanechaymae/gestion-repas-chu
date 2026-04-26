import streamlit as st
import pandas as pd
from datetime import date

from database import (
    get_bons,
    get_bons_par_date,
    get_stats_cuisine
)


def dashboard_cuisine():
    st.title("🍽️ Dashboard Cuisine")

    total_bons, total_normal, total_diabetique = get_stats_cuisine()
    total_general = total_normal + total_diabetique

    st.markdown("""
    <div class="custom-card">
        <h3>Bienvenue dans l’espace cuisine</h3>
        <p>
            Cet espace permet à la cuisine de consulter les bons de repas,
            suivre les quantités et préparer les repas selon les régimes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📄 Bons reçus", total_bons)
    col2.metric("🍽️ Repas normaux", total_normal)
    col3.metric("🥗 Repas diabétiques", total_diabetique)
    col4.metric("📊 Total repas", total_general)


def consultation_bons():
    st.title("📋 Consultation des bons")

    bons = get_bons()

    if bons:
        df = pd.DataFrame(
            bons,
            columns=["ID", "Date", "Service", "Normal", "Diabétique"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun bon enregistré.")


def totaux_cuisine():
    st.title("📊 Totaux cuisine")

    date_selection = st.date_input(
        "Choisir une date",
        value=date.today()
    )

    bons = get_bons_par_date(str(date_selection))

    if bons:
        df = pd.DataFrame(
            bons,
            columns=["ID", "Date", "Service", "Normal", "Diabétique"]
        )

        total_normal = df["Normal"].sum()
        total_diabetique = df["Diabétique"].sum()
        total_general = total_normal + total_diabetique

        col1, col2, col3 = st.columns(3)

        col1.metric("🍽️ Total normal", total_normal)
        col2.metric("🥗 Total diabétique", total_diabetique)
        col3.metric("📊 Total général", total_general)

        st.divider()

        st.subheader("📋 Détail des bons du jour")
        st.dataframe(df, use_container_width=True, hide_index=True)

    else:
        st.warning("Aucun bon trouvé pour cette date.")


def cuisine_page():
    menu = st.sidebar.radio(
        "Fonctionnalités Cuisine",
        ["Dashboard", "Consultation", "Totaux"],
        key="menu_cuisine"
    )

    if menu == "Dashboard":
        dashboard_cuisine()

    elif menu == "Consultation":
        consultation_bons()

    elif menu == "Totaux":
        totaux_cuisine()