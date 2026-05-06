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
    get_chambres_by_service,
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


def dashboard_service_page():
    total_bons, total_normal, total_diabetique = get_stats_service()
    total_general = total_normal + total_diabetique

    section_header(
        "Tableau de bord service",
        "Suivi rapide des bons de repas saisis et aperçu des dernières opérations enregistrées."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Bons", total_bons)
    col2.metric("Repas normaux", total_normal)
    col3.metric("Repas diabétiques", total_diabetique)
    col4.metric("Total repas", total_general)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.subheader("Derniers bons enregistrés")

    derniers = get_derniers_bons()
    if derniers:
        df = pd.DataFrame(
            derniers,
            columns=["Date", "Service", "Chambre", "Normal", "Diabétique", "Statut"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun bon enregistré.")


def ajouter_bon_page():
    section_header(
        "Ajouter un bon de repas",
        "Enregistrez un nouveau bon pour un service et une chambre donnés."
    )

    services = get_services_dict()
    if not services:
        st.warning("Aucun service disponible.")
        return

    col_form, col_info = st.columns([1.15, 0.85], gap="large")

    with col_form:
        st.subheader("Saisie du bon")

        date_bon = st.date_input("Date", value=date.today())
        service_nom = st.selectbox("Service", list(services.keys()))
        id_service = services[service_nom]

        chambres = get_chambres_by_service(id_service)
        if not chambres:
            st.warning("Aucune chambre disponible pour ce service.")
            return

        chambre_dict = {f"Chambre {c[1]}": c[0] for c in chambres}
        chambre_choisie = st.selectbox("Chambre", list(chambre_dict.keys()))

        normal = st.number_input("Repas normal", min_value=0, step=1)
        diabetique = st.number_input("Repas diabétique", min_value=0, step=1)

        if st.button("Enregistrer le bon", use_container_width=True):
            if normal == 0 and diabetique == 0:
                st.warning("Veuillez saisir au moins un repas.")
            else:
                try:
                    ajouter_bon(
                        str(date_bon),
                        id_service,
                        chambre_dict[chambre_choisie],
                        normal,
                        diabetique
                    )
                    st.success("Bon ajouté avec succès.")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    with col_info:
        st.subheader("Résumé")
        total = normal + diabetique
        st.metric("Total repas", total)
        st.info(
            "Vérifiez le service, la chambre et les quantités avant validation."
        )


def mes_bons_page():
    section_header(
        "Mes bons de repas",
        "Consultez l’ensemble des bons enregistrés par le service."
    )

    bons = get_bons()
    if bons:
        df = pd.DataFrame(
            bons,
            columns=["ID", "Date", "Service", "Chambre", "Normal", "Diabétique", "Statut"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun bon enregistré.")


def modifier_bon_page():
    section_header(
        "Modifier ou supprimer un bon",
        "Mettez à jour les informations d’un bon existant ou supprimez-le si nécessaire."
    )

    bons = get_bons()
    services = get_services_dict()

    if not bons:
        st.info("Aucun bon disponible.")
        return

    bon_options = {
        f"ID {b[0]} - {b[1]} - {b[2]} - Chambre {b[3]}": b
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
    statut_actuel = bon[6]

    col_form, col_side = st.columns([1.15, 0.85], gap="large")

    with col_form:
        st.subheader("Mise à jour du bon")

        nouvelle_date = st.date_input("Date", value=date_actuelle)

        services_noms = list(services.keys())
        index_service = services_noms.index(service_actuel) if service_actuel in services_noms else 0
        nouveau_service = st.selectbox("Service", services_noms, index=index_service)
        id_service = services[nouveau_service]

        chambres = get_chambres_by_service(id_service)
        if not chambres:
            st.warning("Aucune chambre disponible pour ce service.")
            return

        chambre_dict = {f"Chambre {c[1]}": c[0] for c in chambres}
        chambre_labels = list(chambre_dict.keys())
        default_chambre = f"Chambre {chambre_actuelle}"
        index_chambre = chambre_labels.index(default_chambre) if default_chambre in chambre_labels else 0

        chambre_choisie = st.selectbox("Chambre", chambre_labels, index=index_chambre)

        nouveau_normal = st.number_input("Repas normal", min_value=0, value=int(normal_actuel))
        nouveau_diabetique = st.number_input("Repas diabétique", min_value=0, value=int(diabetique_actuel))

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Enregistrer les modifications", use_container_width=True):
                if nouveau_normal == 0 and nouveau_diabetique == 0:
                    st.warning("Veuillez saisir au moins un repas.")
                else:
                    try:
                        modifier_bon(
                            id_bon,
                            str(nouvelle_date),
                            id_service,
                            chambre_dict[chambre_choisie],
                            nouveau_normal,
                            nouveau_diabetique
                        )
                        st.success("Bon modifié avec succès.")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

        with col_btn2:
            if st.button("Supprimer le bon", use_container_width=True):
                supprimer_bon(id_bon)
                st.warning("Bon supprimé.")
                st.rerun()

    with col_side:
        st.subheader("Informations actuelles")
        st.write(f"**Statut :** {statut_actuel}")
        st.metric("Total actuel", int(normal_actuel) + int(diabetique_actuel))
        st.info(
            "La suppression doit être utilisée seulement en cas d’erreur de saisie ou d’annulation."
        )


def service_page():
    st.sidebar.markdown("## Service hospitalier")
    menu = st.sidebar.radio(
        "Fonctionnalités Service",
        ["Dashboard", "Ajouter un bon", "Mes bons", "Modifier un bon"],
        key="menu_service",
        label_visibility="collapsed"
    )

    if menu == "Dashboard":
        dashboard_service_page()
    elif menu == "Ajouter un bon":
        ajouter_bon_page()
    elif menu == "Mes bons":
        mes_bons_page()
    elif menu == "Modifier un bon":
        modifier_bon_page()