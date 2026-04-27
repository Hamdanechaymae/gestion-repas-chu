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
    get_derniers_bons,
    get_chambres_by_service
)


# ================= DASHBOARD =================
def dashboard_service_page():
    st.title("🏥 Dashboard Service")

    total_bons, total_normal, total_diabetique = get_stats_service()
    total_general = total_normal + total_diabetique

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📄 Bons", total_bons)
    col2.metric("🍽️ Normaux", total_normal)
    col3.metric("🥗 Diabétiques", total_diabetique)
    col4.metric("📊 Total", total_general)

    st.divider()

    derniers = get_derniers_bons()

    if derniers:
        df = pd.DataFrame(
            derniers,
            columns=["Date", "Service", "Chambre", "Normal", "Diabétique"]
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun bon enregistré.")


# ================= AJOUT BON =================
def ajouter_bon_page():
    st.title("📝 Ajouter un bon de repas")

    services = get_services_dict()

    if not services:
        st.warning("Aucun service disponible.")
        return

    date_bon = st.date_input("Date", value=date.today())

    service_nom = st.selectbox("Service", list(services.keys()))
    id_service = services[service_nom]

    # 🔥 CHAMBRES PAR SERVICE
    chambres = get_chambres_by_service(id_service)

    if not chambres:
        st.warning("Aucune chambre pour ce service.")
        return

    chambre_dict = {f"Chambre {c[1]}": c[0] for c in chambres}
    chambre_choisie = st.selectbox("Chambre", list(chambre_dict.keys()))

    normal = st.number_input("Repas normal", min_value=0, step=1)
    diabetique = st.number_input("Repas diabétique", min_value=0, step=1)

    if st.button("Enregistrer le bon"):
        if normal == 0 and diabetique == 0:
            st.warning("Veuillez saisir au moins un repas.")
        else:
            ajouter_bon(
                str(date_bon),
                id_service,
                chambre_dict[chambre_choisie],
                normal,
                diabetique
            )
            st.success("Bon ajouté avec succès")
            st.rerun()


# ================= MES BONS =================
def mes_bons_page():
    st.title("📄 Mes bons de repas")

    bons = get_bons()

    if bons:
        df = pd.DataFrame(
            bons,
            columns=["ID", "Date", "Service", "Chambre", "Normal", "Diabétique"]
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun bon enregistré.")


# ================= MODIFIER BON =================
def modifier_bon_page():
    st.title("✏️ Modifier / Supprimer un bon")

    bons = get_bons()
    services = get_services_dict()

    if not bons:
        st.info("Aucun bon disponible.")
        return

    bon_options = {
        f"ID {b[0]} - {b[1]} - {b[2]}": b
        for b in bons
    }

    choix = st.selectbox("Choisir un bon", list(bon_options.keys()))
    bon = bon_options[choix]

    id_bon = bon[0]
    date_actuelle = pd.to_datetime(bon[1]).date()
    service_actuel = bon[2]
    chambre_actuelle = bon[3]
    normal_actuel = bon[4]
    diabetique_actuel = bon[5]

    nouvelle_date = st.date_input("Date", value=date_actuelle)

    services_noms = list(services.keys())
    index_service = services_noms.index(service_actuel) if service_actuel in services_noms else 0

    nouveau_service = st.selectbox("Service", services_noms, index=index_service)
    id_service = services[nouveau_service]

    # 🔥 CHAMBRES PAR SERVICE
    chambres = get_chambres_by_service(id_service)
    chambre_dict = {f"Chambre {c[1]}": c[0] for c in chambres}

    chambre_choisie = st.selectbox("Chambre", list(chambre_dict.keys()))

    nouveau_normal = st.number_input("Repas normal", value=int(normal_actuel))
    nouveau_diabetique = st.number_input("Repas diabétique", value=int(diabetique_actuel))

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Modifier"):
            modifier_bon(
                id_bon,
                str(nouvelle_date),
                id_service,
                chambre_dict[chambre_choisie],
                nouveau_normal,
                nouveau_diabetique
            )
            st.success("Bon modifié")
            st.rerun()

    with col2:
        if st.button("🗑️ Supprimer"):
            supprimer_bon(id_bon)
            st.warning("Bon supprimé")
            st.rerun()


# ================= MENU =================
def service_page():
    menu = st.sidebar.radio(
        "Fonctionnalités Service",
        ["Dashboard", "Ajouter un bon", "Mes bons", "Modifier un bon"]
    )

    if menu == "Dashboard":
        dashboard_service_page()
    elif menu == "Ajouter un bon":
        ajouter_bon_page()
    elif menu == "Mes bons":
        mes_bons_page()
    elif menu == "Modifier un bon":
        modifier_bon_page()