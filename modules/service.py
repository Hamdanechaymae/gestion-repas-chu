import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
from database import (
    get_services,
    get_chambres_by_service,
    get_regimes,
    ajouter_bon,
    get_bons,
    supprimer_bon,
    modifier_bon,
    get_stats_service,
    ajouter_historique,
)

def dashboard_service():
    service_nom = st.session_state.get('user_service', "Non specifie")
    st.subheader(f"Tableau de bord - Service {service_nom}")
    
    total_bons, total_repas, en_attente = get_stats_service()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Bons du jour", total_bons)
    col2.metric("Total repas", total_repas)
    col3.metric("Bons en attente", en_attente)

def ajouter_bon_page():
    st.header("Saisie d'un nouveau bon de repas")
    
    id_service = st.session_state.get('id_service') 
    chambres = get_chambres_by_service(id_service)
    
    if not chambres:
        st.warning("Aucune chambre enregistree pour ce service.")
        return

    chambre_options = {f"Chambre {c[1]} ({c[2]} lit(s))": (c[0], c[2]) for c in chambres}
    choix_chambre = st.selectbox("Chambre", list(chambre_options.keys()))
    id_chambre, nb_patients = chambre_options[choix_chambre]

    st.info(f"Cette chambre contient {nb_patients} patient(s). Veuillez choisir le regime pour chaque patient.")
    
    regimes_dispo = get_regimes()
    final_regimes_dict = {}

    for p in range(1, nb_patients + 1):
        st.markdown(f"**Patient - Lit n.{p}**")
        choix_regime = st.selectbox(
            f"Regime du patient lit {p}", 
            options=[(r[0], r[1]) for r in regimes_dispo],
            format_func=lambda x: x[1],
            key=f"patient_{p}_select"
        )
        
        id_regime = choix_regime[0]
        final_regimes_dict[id_regime] = final_regimes_dict.get(id_regime, 0) + 1

    st.markdown("---")
    if final_regimes_dict:
        st.write("**Recapitulatif du bon :**")
        for id_regime, qte in final_regimes_dict.items():
            nom_regime = next((r[1] for r in regimes_dispo if r[0] == id_regime), "Inconnu")
            st.write(f"- {nom_regime} : {qte} repas")

    if st.button("Enregistrer le bon", type="primary"):
        if final_regimes_dict:
            ajouter_bon(str(date.today()), id_service, id_chambre, final_regimes_dict)
            
            # Enregistrer dans l'historique
            user = st.session_state.get("user", {})
            ajouter_historique(
                utilisateur=user.get("nom", "Inconnu"),
                role=user.get("role", "service"),
                action="Creation d'un bon",
                details=f"Service: {st.session_state.get('user_service', 'N/A')} | Chambre: {choix_chambre}"
            )
            
            st.success("Bon enregistre et transmis a la cuisine.")
        else:
            st.error("Aucun regime selectionne.")

def consultation_page():
    st.header("Historique des bons")
    bons = get_bons()
    if not bons:
        st.info("Aucun bon enregistre.")
        return

    df = pd.DataFrame(bons, columns=["ID", "Date", "Service", "Chambre", "Details", "Statut"])
    
    statuts_disponibles = ["Tous"] + sorted(df["Statut"].unique().tolist())
    filtre_statut = st.selectbox("Filtrer par statut", statuts_disponibles)
    
    if filtre_statut != "Tous":
        df = df[df["Statut"] == filtre_statut]
    
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_exp, col_supp = st.columns(2)
    
    with col_exp:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Bons_Repas')
        excel_data = output.getvalue()
        
        st.download_button(
            label="Exporter en Excel",
            data=excel_data,
            file_name=f"bons_repas_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col_supp:
        with st.expander("Supprimer un bon"):
            bon_dict = {f"Bon n.{b[0]} - {b[2]} - Chambre {b[3]}": b[0] for b in bons}
            bon_choisi = st.selectbox("Selectionnez le bon a supprimer", list(bon_dict.keys()))
            confirmation = st.checkbox("Je confirme la suppression de ce bon")
            if st.button("Confirmer la suppression", key="delete_bon", disabled=not confirmation):
                supprimer_bon(bon_dict[bon_choisi])
                
                # Enregistrer dans l'historique
                user = st.session_state.get("user", {})
                ajouter_historique(
                    utilisateur=user.get("nom", "Inconnu"),
                    role=user.get("role", "service"),
                    action="Suppression d'un bon",
                    details=f"Bon supprime: {bon_choisi}"
                )
                
                st.toast("Bon supprime.")
                st.rerun()

def modification_page():
    st.header("Modification d'un bon")
    
    bons = get_bons()
    if not bons:
        st.info("Aucun bon a modifier.")
        return

    bon_dict = {f"Bon n.{b[0]} - {b[2]} - Chambre {b[3]} - {b[4]}": b[0] for b in bons}
    bon_choisi = st.selectbox("Selectionnez le bon a modifier", list(bon_dict.keys()))
    id_bon = bon_dict[bon_choisi]

    id_service = st.session_state.get('id_service')
    chambres = get_chambres_by_service(id_service)
    if not chambres:
        st.warning("Aucune chambre disponible.")
        return

    chambre_options = {f"Chambre {c[1]} ({c[2]} lit(s))": (c[0], c[2]) for c in chambres}
    nouvelle_chambre = st.selectbox("Nouvelle chambre", list(chambre_options.keys()))
    id_chambre, nb_patients = chambre_options[nouvelle_chambre]

    st.info(f"Cette chambre contient {nb_patients} patient(s).")
    
    regimes_dispo = get_regimes()
    final_regimes_dict = {}

    for p in range(1, nb_patients + 1):
        st.markdown(f"**Patient - Lit n.{p}**")
        choix_regime = st.selectbox(
            f"Regime du patient lit {p}", 
            options=[(r[0], r[1]) for r in regimes_dispo],
            format_func=lambda x: x[1],
            key=f"modif_patient_{p}_select"
        )
        
        id_regime = choix_regime[0]
        final_regimes_dict[id_regime] = final_regimes_dict.get(id_regime, 0) + 1

    if st.button("Enregistrer les modifications", type="primary"):
        if final_regimes_dict:
            modifier_bon(id_bon, id_chambre, final_regimes_dict)
            
            # Enregistrer dans l'historique
            user = st.session_state.get("user", {})
            ajouter_historique(
                utilisateur=user.get("nom", "Inconnu"),
                role=user.get("role", "service"),
                action="Modification d'un bon",
                details=f"Bon modifie: {bon_choisi} | Nouvelle chambre: {nouvelle_chambre}"
            )
            
            st.success("Bon modifie avec succes.")
            st.rerun()
        else:
            st.error("Aucun regime selectionne.")

def service_page():
    st.sidebar.title("Navigation Service")
    menu = st.sidebar.radio("Menu", [
        "Tableau de bord", 
        "Ajouter un bon", 
        "Consulter les bons", 
        "Modifier un bon"
    ])

    if menu == "Tableau de bord":
        dashboard_service()
    elif menu == "Ajouter un bon":
        ajouter_bon_page()
    elif menu == "Consulter les bons":
        consultation_page()
    elif menu == "Modifier un bon":
        modification_page()