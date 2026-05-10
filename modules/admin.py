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
    ajouter_historique,
    get_historique,
)

def section_header(title, description):
    st.markdown(
        f"""
        <div class="hero" style="padding: 1.5rem; margin-bottom: 1.5rem; text-align: left;">
            <h1 style="font-size: 1.8rem; margin-bottom: 0.5rem; color: white !important;">{title}</h1>
            <p style="margin-bottom: 0; color: #E0F2FE !important; font-size: 1rem;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def dashboard_admin():
    (
        total_services,
        total_regimes,
        total_users,
        total_chambres,
        total_bons,
        total_repas,
        total_livres,
        totaux_regimes,
    ) = get_stats_admin()

    section_header(
        "Tableau de bord administrateur",
        "Vue d'ensemble de la structure hospitaliere et de l'activite des repas."
    )

    st.markdown('<p class="section-title">Structure de l\'etablissement</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Configuration des unites hospitalieres</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Services", total_services)
    with col2:
        st.metric("Chambres", total_chambres)
    with col3:
        st.metric("Regimes", total_regimes)
    with col4:
        st.metric("Utilisateurs", total_users)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<p class="section-title">Activite des bons de repas</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Suivi des commandes et de la production</p>', unsafe_allow_html=True)
    
    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("Bons emis", total_bons)
    with col6:
        st.metric("Total repas commandes", total_repas)
    with col7:
        st.metric("Bons livres", total_livres)

    st.markdown("<br>", unsafe_allow_html=True)

    if totaux_regimes:
        st.markdown('<p class="section-title">Repartition par regime</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Distribution des repas selon les prescriptions medicales</p>', unsafe_allow_html=True)
        
        df_regimes = pd.DataFrame(totaux_regimes, columns=["Regime", "Quantite"])
        df_regimes = df_regimes.set_index("Regime")
        st.bar_chart(df_regimes, height=300)
    else:
        st.info("Aucune donnee de repas disponible.")


def gestion_services():
    section_header(
        "Gestion des services",
        "Administration des departements et unites de soins du CHU."
    )

    with st.expander("Ajouter un nouveau service", expanded=False):
        nom_service = st.text_input("Nom du service", placeholder="Ex : Pediatrie, Cardiologie...")
        if st.button("Enregistrer le service", key="add_service", type="primary"):
            if nom_service.strip():
                try:
                    ajouter_service(nom_service.strip())
                    user = st.session_state.get("user", {})
                    ajouter_historique(
                        utilisateur=user.get("nom", "Inconnu"),
                        role=user.get("role", "admin"),
                        action="Ajout d'un service",
                        details=f"Service: {nom_service.strip()}"
                    )
                    st.toast("Service ajoute avec succes.")
                    st.rerun()
                except Exception:
                    st.error("Ce service existe deja.")
            else:
                st.warning("Veuillez saisir le nom du service.")

    st.markdown("### Liste des services actifs")
    services = get_services()

    if services:
        df = pd.DataFrame(services, columns=["ID", "Nom du service"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        with st.expander("Supprimer un service"):
            service_options = {service[1]: service[0] for service in services}
            service_choisi = st.selectbox("Selectionnez un service a retirer", list(service_options.keys()))
            confirmation = st.checkbox("Je confirme la suppression de ce service")
            if st.button("Confirmer la suppression", key="delete_service", disabled=not confirmation):
                supprimer_service(service_options[service_choisi])
                user = st.session_state.get("user", {})
                ajouter_historique(
                    utilisateur=user.get("nom", "Inconnu"),
                    role=user.get("role", "admin"),
                    action="Suppression d'un service",
                    details=f"Service: {service_choisi}"
                )
                st.toast("Service supprime.")
                st.rerun()
    else:
        st.info("Aucun service enregistre dans le systeme.")


def gestion_regimes():
    section_header(
        "Gestion des regimes",
        "Configuration des regimes alimentaires (normes medicales)."
    )

    with st.expander("Ajouter un regime", expanded=False):
        nom_regime = st.text_input("Nom du regime", placeholder="Ex : Sans sel, Mixe...")
        if st.button("Enregistrer le regime", key="add_regime", type="primary"):
            if nom_regime.strip():
                try:
                    ajouter_regime(nom_regime.strip())
                    user = st.session_state.get("user", {})
                    ajouter_historique(
                        utilisateur=user.get("nom", "Inconnu"),
                        role=user.get("role", "admin"),
                        action="Ajout d'un regime",
                        details=f"Regime: {nom_regime.strip()}"
                    )
                    st.toast("Regime ajoute avec succes.")
                    st.rerun()
                except Exception:
                    st.error("Ce regime existe deja.")
            else:
                st.warning("Veuillez saisir le nom du regime.")

    st.markdown("### Liste des regimes")
    regimes = get_regimes()

    if regimes:
        df = pd.DataFrame(regimes, columns=["ID", "Nom du regime"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        with st.expander("Supprimer un regime"):
            regime_options = {regime[1]: regime[0] for regime in regimes}
            regime_choisi = st.selectbox("Selectionnez un regime a retirer", list(regime_options.keys()))
            confirmation = st.checkbox("Je confirme la suppression de ce regime")
            if st.button("Confirmer la suppression", key="delete_regime", disabled=not confirmation):
                supprimer_regime(regime_options[regime_choisi])
                user = st.session_state.get("user", {})
                ajouter_historique(
                    utilisateur=user.get("nom", "Inconnu"),
                    role=user.get("role", "admin"),
                    action="Suppression d'un regime",
                    details=f"Regime: {regime_choisi}"
                )
                st.toast("Regime supprime.")
                st.rerun()
    else:
        st.info("Aucun regime enregistre.")


def gestion_chambres():
    section_header(
        "Gestion des chambres",
        "Rattachement des chambres et lits aux services correspondants."
    )

    services = get_services_dict()
    if not services:
        st.warning("Vous devez d'abord creer un service avant de pouvoir y ajouter des chambres.")
        return

    with st.expander("Ajouter une nouvelle chambre", expanded=False):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            numero_chambre = st.text_input("Numero ou identifiant", placeholder="Ex : 101, 102A...")
        with col2:
            service_nom = st.selectbox("Affecter au service", list(services.keys()), key="service_chambre")
        with col3:
            nombre_patients = st.number_input("Nombre de lits", min_value=1, max_value=10, value=1, step=1)
            
        if st.button("Enregistrer la chambre", key="add_chambre", type="primary"):
            if numero_chambre.strip():
                try:
                    ajouter_chambre(numero_chambre.strip(), services[service_nom], nombre_patients)
                    user = st.session_state.get("user", {})
                    ajouter_historique(
                        utilisateur=user.get("nom", "Inconnu"),
                        role=user.get("role", "admin"),
                        action="Ajout d'une chambre",
                        details=f"Chambre: {numero_chambre.strip()} | Service: {service_nom} | Lits: {nombre_patients}"
                    )
                    st.toast(f"Chambre {numero_chambre} ajoutee avec {nombre_patients} lit(s).")
                    st.rerun()
                except Exception:
                    st.error("Cette chambre existe deja dans ce service.")
            else:
                st.warning("Veuillez saisir le numero de la chambre.")

    st.markdown("### Cartographie des chambres")
    chambres = get_chambres()

    if chambres:
        df = pd.DataFrame(chambres, columns=["ID", "Numero de chambre", "Service de rattachement", "Capacite (Lits)"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        with st.expander("Retirer une chambre"):
            chambre_options = {f"Chambre {c[1]} - {c[2]} ({c[3]} lits)": c[0] for c in chambres}
            chambre_choisie = st.selectbox("Selectionnez la chambre a supprimer", list(chambre_options.keys()))
            confirmation = st.checkbox("Je confirme la suppression de cette chambre")
            if st.button("Confirmer la suppression", key="delete_chambre", disabled=not confirmation):
                supprimer_chambre(chambre_options[chambre_choisie])
                user = st.session_state.get("user", {})
                ajouter_historique(
                    utilisateur=user.get("nom", "Inconnu"),
                    role=user.get("role", "admin"),
                    action="Suppression d'une chambre",
                    details=f"Chambre: {chambre_choisie}"
                )
                st.toast("Chambre supprimee.")
                st.rerun()
    else:
        st.info("Aucune chambre repertoriee.")


def gestion_utilisateurs():
    section_header(
        "Gestion des acces",
        "Administration des comptes du personnel (cuisine, services, administration)."
    )

    with st.expander("Creer un nouveau compte", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom complet du professionnel")
            email = st.text_input("Adresse email professionnelle")
        with col2:
            role = st.selectbox("Niveau d'acces (Role)", ["admin", "service", "cuisine"])
            mot_de_passe = st.text_input("Mot de passe temporaire", type="password")
            
        if st.button("Creer le compte", key="add_user", type="primary"):
            if nom.strip() and email.strip() and mot_de_passe.strip():
                try:
                    ajouter_utilisateur(nom.strip(), email.strip(), mot_de_passe.strip(), role)
                    user = st.session_state.get("user", {})
                    ajouter_historique(
                        utilisateur=user.get("nom", "Inconnu"),
                        role=user.get("role", "admin"),
                        action="Creation d'un utilisateur",
                        details=f"Utilisateur: {nom.strip()} | Role: {role} | Email: {email.strip()}"
                    )
                    st.toast("Compte utilisateur cree.")
                    st.rerun()
                except Exception:
                    st.error("Un compte avec cette adresse email existe deja.")
            else:
                st.warning("Tous les champs sont obligatoires.")

    st.markdown("### Annuaire du personnel autorise")
    users = get_utilisateurs()

    if users:
        df = pd.DataFrame(users, columns=["ID", "Nom", "Email", "Role"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        with st.expander("Revoquer un acces"):
            user_options = {f"{u[1]} ({u[3]}) - {u[2]}": u[0] for u in users}
            user_choisi = st.selectbox("Selectionnez l'utilisateur a retirer", list(user_options.keys()))
            confirmation = st.checkbox("Je confirme la revocation de cet acces")
            if st.button("Confirmer la revocation", key="delete_user", disabled=not confirmation):
                supprimer_utilisateur(user_options[user_choisi])
                user = st.session_state.get("user", {})
                ajouter_historique(
                    utilisateur=user.get("nom", "Inconnu"),
                    role=user.get("role", "admin"),
                    action="Revocation d'un utilisateur",
                    details=f"Utilisateur: {user_choisi}"
                )
                st.toast("Acces revoque.")
                st.rerun()
    else:
        st.info("Aucun utilisateur dans l'annuaire.")


def page_historique():
    section_header(
        "Historique des actions",
        "Traçabilite complete des operations effectuees dans l'application."
    )
    
    historique = get_historique()
    
    if historique:
        df = pd.DataFrame(
            historique,
            columns=["ID", "Date/Heure", "Utilisateur", "Role", "Action", "Details"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune action enregistree dans l'historique.")


def admin_page():
    st.sidebar.markdown("## Administration")
    
    menu = st.sidebar.radio(
        "Navigation",
        [
            "Tableau de bord",
            "Services",
            "Chambres",
            "Regimes",
            "Utilisateurs",
            "Historique"
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
    elif menu == "Regimes":
        gestion_regimes()
    elif menu == "Utilisateurs":
        gestion_utilisateurs()
    elif menu == "Historique":
        page_historique()