import streamlit as st
import pandas as pd
from datetime import date


from database import (
    get_bons,
    get_bons_par_date,
    get_stats_cuisine,
    modifier_statut_bon,
    get_totaux_par_service
)


# ================= DASHBOARD =================
def dashboard_cuisine():
    st.title("Dashboard Cuisine")

    # ✅ D’ABORD les données
    total_bons, total_normal, total_diabetique = get_stats_cuisine()
    total_general = total_normal + total_diabetique

    # ✅ ENSUITE les alertes
    if total_bons == 0:
        st.warning("⚠️ Aucun bon de repas reçu pour le moment.")
        
    elif total_general == 0:
        st.warning("⚠️ Aucun repas enregistré.")

    else:
        taux_diabetique = (total_diabetique / total_general) * 100

        if taux_diabetique >= 50:
            st.error("🚨 Attention : trop de repas diabétiques !")

        elif taux_diabetique >= 30:
            st.warning("⚠️ Les repas diabétiques sont élevés.")

        else:
            st.success("✅ Situation normale : répartition équilibrée.")

    # metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📄 Bons reçus", total_bons)
    col2.metric("🍽️ Normaux", total_normal)
    col3.metric("🥗 Diabétiques", total_diabetique)
    col4.metric("📊 Total", total_general)

    st.divider()

    # graphique
    df_chart = pd.DataFrame({
        "Type": ["Normal", "Diabétique"],
        "Total": [total_normal, total_diabetique]
    })

    st.subheader("📊 Répartition des repas par type")
    st.bar_chart(df_chart.set_index("Type"))


# ================= CONSULTATION =================
def consultation_bons():
    st.title("📋 Consultation des bons")

    bons = get_bons()

    if not bons:
        st.info("Aucun bon enregistré.")
        return

    df = pd.DataFrame(
        bons,
        columns=["ID", "Date", "Service", "Chambre", "Normal", "Diabétique", "Statut"]
    )

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("⚙️ Modifier le statut")

    bon_dict = {
        f"ID {b[0]} - {b[2]} - Chambre {b[3]}": b[0]
        for b in bons
    }

    choix = st.selectbox("Choisir un bon", list(bon_dict.keys()))
    id_bon = bon_dict[choix]

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Préparé"):
            modifier_statut_bon(id_bon, "Préparé")
            st.success("Statut mis à jour")
            st.rerun()

    with col2:
        if st.button("❌ Annulé"):
            modifier_statut_bon(id_bon, "Annulé")
            st.warning("Bon annulé")
            st.rerun()


# ================= TOTAUX =================
def totaux_cuisine():
    st.title("📊 Totaux cuisine")

    date_selection = st.date_input("Choisir une date", value=date.today())

    bons = get_bons_par_date(str(date_selection))

    if not bons:
        st.warning("Aucun bon trouvé pour cette date.")
        return

    df = pd.DataFrame(
        bons,
        columns=["ID", "Date", "Service", "Chambre", "Normal", "Diabétique", "Statut"]
    )

    # Totaux globaux
    total_normal = df["Normal"].sum()
    total_diabetique = df["Diabétique"].sum()
    total_general = total_normal + total_diabetique

    col1, col2, col3 = st.columns(3)

    col1.metric("🍽️ Normal", total_normal)
    col2.metric("🥗 Diabétique", total_diabetique)
    col3.metric("📊 Total", total_general)

    st.divider()

    # Totaux par service
    st.subheader("🏥 Totaux par service")

    totaux_service = get_totaux_par_service(str(date_selection))

    if totaux_service:
        df_service = pd.DataFrame(
            totaux_service,
            columns=["Service", "Normal", "Diabétique", "Total"]
        )

        st.dataframe(df_service, use_container_width=True, hide_index=True)

        st.subheader("📊 Graphique par service")
        st.bar_chart(df_service.set_index("Service")[["Normal", "Diabétique"]])

    st.divider()

    st.subheader("📋 Détail des bons")
    st.dataframe(df, use_container_width=True, hide_index=True)


# ================= MENU =================
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
