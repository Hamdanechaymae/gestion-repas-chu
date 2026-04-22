import streamlit as st
import pandas as pd
from database import init_db, get_connection
from auth import verifier_connexion
from style import load_css


# =========================
# CONFIGURATION
# =========================
st.set_page_config(
    page_title="Gestion des repas hospitaliers",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
init_db()

if "user" not in st.session_state:
    st.session_state.user = None


def logout():
    st.session_state.user = None
    st.rerun()


# =========================
# AVANT CONNEXION
# =========================
if st.session_state.user is None:
    menu_public = st.sidebar.radio(
        "Navigation",
        ["Accueil", "Connexion"]
    )

    if menu_public == "Accueil":
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM service")
        nb_services = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM utilisateur")
        nb_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM regime")
        nb_regimes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM bon_repas")
        nb_bons = cursor.fetchone()[0]

        conn.close()

        st.title("🏥 Gestion des bons de repas hospitaliers")
        st.markdown(
            '<div class="subtitle">Application du CHU Oujda</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Services", nb_services)
        col2.metric("Utilisateurs", nb_users)
        col3.metric("Régimes", nb_regimes)
        col4.metric("Bons enregistrés", nb_bons)

        st.markdown("""
        <div class="custom-card">
            <h3>Présentation de l’application</h3>
            <p>
                Cette application permet la gestion numérique des bons de repas hospitaliers
                au sein du CHU Oujda.
            </p>
            <p>Elle offre trois espaces utilisateurs :</p>
            <ul>
                <li><b>Administrateur</b> : gestion des services, des régimes et des utilisateurs.</li>
                <li><b>Agent de service</b> : saisie, modification et consultation des bons de repas.</li>
                <li><b>Cuisine</b> : consultation des repas et affichage des totaux.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="custom-card">
            <h3>Fonctionnalités principales</h3>
            <ul>
                <li>Connexion sécurisée selon le rôle</li>
                <li>Gestion des services</li>
                <li>Gestion des régimes</li>
                <li>Gestion des utilisateurs</li>
                <li>Création d’un bon de repas</li>
                <li>Modification et suppression d’un bon</li>
                <li>Consultation des bons</li>
                <li>Affichage des totaux</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.info("Utilise le menu de gauche pour accéder à la page de connexion.")

    elif menu_public == "Connexion":
        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.title("🔐 Connexion")
            st.markdown(
                '<div class="subtitle">Accès réservé aux utilisateurs autorisés</div>',
                unsafe_allow_html=True
            )

            st.markdown("""
            <div class="custom-card">
                <h3>Accès par rôle</h3>
                <p>Après connexion, chaque utilisateur accède à son propre espace :</p>
                <ul>
                    <li><b>Admin</b> → dashboard administrateur</li>
                    <li><b>Service</b> → saisie et gestion des bons</li>
                    <li><b>Cuisine</b> → consultation et totaux</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.subheader("Se connecter")

            email = st.text_input("Email")
            mot_de_passe = st.text_input("Mot de passe", type="password")

            if st.button("Se connecter", use_container_width=True):
                user = verifier_connexion(email, mot_de_passe)

                if user:
                    st.session_state.user = {
                        "id": user[0],
                        "nom": user[1],
                        "email": user[2],
                        "role": user[3]
                    }
                    st.rerun()
                else:
                    st.error("Email ou mot de passe incorrect.")

            st.markdown('</div>', unsafe_allow_html=True)

# =========================
# APRÈS CONNEXION
# =========================
else:
    user = st.session_state.user
    conn = get_connection()
    cursor = conn.cursor()

    st.sidebar.success(f"Connecté : {user['nom']}")
    st.sidebar.write(f"Rôle : {user['role']}")

    if st.sidebar.button("Déconnexion", use_container_width=True):
        logout()

    # ==========================================================
    # ADMIN
    # ==========================================================
    if user["role"] == "admin":
        menu = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Services", "Régimes", "Utilisateurs"]
        )

        if menu == "Dashboard":
            st.title("Dashboard Administrateur")
            st.markdown(
                f'<div class="subtitle">Bienvenue {user["nom"]}</div>',
                unsafe_allow_html=True
            )

            cursor.execute("SELECT COUNT(*) FROM service")
            nb_services = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM utilisateur")
            nb_users = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM regime")
            nb_regimes = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM bon_repas")
            nb_bons = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(normal), 0) FROM bon_repas")
            total_normal = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(diabetique), 0) FROM bon_repas")
            total_diabetique = cursor.fetchone()[0]

            col1, col2, col3 = st.columns(3)
            col4, col5, col6 = st.columns(3)

            col1.metric("Services", nb_services)
            col2.metric("Utilisateurs", nb_users)
            col3.metric("Régimes", nb_regimes)
            col4.metric("Bons enregistrés", nb_bons)
            col5.metric("Total normal", total_normal)
            col6.metric("Total diabétique", total_diabetique)

            st.markdown("""
            <div class="custom-card">
                <h3>Résumé</h3>
                <p>
                    L’administrateur peut gérer les services, les régimes et les utilisateurs.
                    Il peut également superviser les bons enregistrés.
                </p>
            </div>
            """, unsafe_allow_html=True)

        elif menu == "Services":
            st.title("Gestion des services")

            col1, col2 = st.columns([1, 1.5])

            with col1:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("Ajouter un service")

                nom_service = st.text_input("Nom du service")

                if st.button("Ajouter le service", use_container_width=True):
                    if nom_service.strip():
                        try:
                            cursor.execute(
                                "INSERT INTO service (nom_service) VALUES (?)",
                                (nom_service.strip(),)
                            )
                            conn.commit()
                            st.success("Service ajouté avec succès.")
                            st.rerun()
                        except Exception:
                            st.error("Ce service existe déjà.")
                    else:
                        st.warning("Veuillez saisir un nom de service.")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("Liste des services")

                cursor.execute("SELECT id_service, nom_service FROM service ORDER BY id_service")
                services = cursor.fetchall()

                if services:
                    df_services = pd.DataFrame(services, columns=["ID", "Nom du service"])
                    st.dataframe(df_services, use_container_width=True, hide_index=True)
                else:
                    st.info("Aucun service enregistré.")
                st.markdown('</div>', unsafe_allow_html=True)

        elif menu == "Régimes":
            st.title("Gestion des régimes")

            col1, col2 = st.columns([1, 1.5])

            with col1:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("Ajouter un régime")

                nom_regime = st.text_input("Nom du régime")

                if st.button("Ajouter le régime", use_container_width=True):
                    if nom_regime.strip():
                        try:
                            cursor.execute(
                                "INSERT INTO regime (nom_regime) VALUES (?)",
                                (nom_regime.strip(),)
                            )
                            conn.commit()
                            st.success("Régime ajouté avec succès.")
                            st.rerun()
                        except Exception:
                            st.error("Ce régime existe déjà.")
                    else:
                        st.warning("Veuillez saisir un nom de régime.")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("Liste des régimes")

                cursor.execute("SELECT id_regime, nom_regime FROM regime ORDER BY id_regime")
                regimes = cursor.fetchall()

                if regimes:
                    df_regimes = pd.DataFrame(regimes, columns=["ID", "Nom du régime"])
                    st.dataframe(df_regimes, use_container_width=True, hide_index=True)
                else:
                    st.info("Aucun régime enregistré.")
                st.markdown('</div>', unsafe_allow_html=True)

        elif menu == "Utilisateurs":
            st.title("Gestion des utilisateurs")

            col1, col2 = st.columns([1, 1.5])

            with col1:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("Ajouter un utilisateur")

                nom = st.text_input("Nom complet")
                email_user = st.text_input("Email utilisateur")
                mot_de_passe_user = st.text_input("Mot de passe", type="password")
                role = st.selectbox("Rôle", ["admin", "service", "cuisine"])

                if st.button("Ajouter l'utilisateur", use_container_width=True):
                    if nom.strip() and email_user.strip() and mot_de_passe_user.strip():
                        try:
                            cursor.execute("""
                                INSERT INTO utilisateur (nom, email, mot_de_passe, role)
                                VALUES (?, ?, ?, ?)
                            """, (nom.strip(), email_user.strip(), mot_de_passe_user.strip(), role))
                            conn.commit()
                            st.success("Utilisateur ajouté avec succès.")
                            st.rerun()
                        except Exception:
                            st.error("Cet utilisateur existe déjà.")
                    else:
                        st.warning("Veuillez remplir tous les champs.")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("Liste des utilisateurs")

                cursor.execute("""
                    SELECT id_user, nom, email, role
                    FROM utilisateur
                    ORDER BY id_user
                """)
                users = cursor.fetchall()

                if users:
                    df_users = pd.DataFrame(users, columns=["ID", "Nom", "Email", "Rôle"])
                    st.dataframe(df_users, use_container_width=True, hide_index=True)
                else:
                    st.info("Aucun utilisateur enregistré.")
                st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================
    # SERVICE
    # ==========================================================
    elif user["role"] == "service":
        menu = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Ajouter un bon", "Mes bons", "Modifier un bon"]
        )

        if menu == "Dashboard":
            st.title("Dashboard Service")
            st.markdown(
                f'<div class="subtitle">Bienvenue {user["nom"]}</div>',
                unsafe_allow_html=True
            )

            cursor.execute("SELECT COUNT(*) FROM bon_repas")
            nb_bons = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(normal), 0) FROM bon_repas")
            total_normal = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(diabetique), 0) FROM bon_repas")
            total_diabetique = cursor.fetchone()[0]

            col1, col2, col3 = st.columns(3)
            col1.metric("Bons enregistrés", nb_bons)
            col2.metric("Total normal", total_normal)
            col3.metric("Total diabétique", total_diabetique)

            st.info("Utilise le menu à gauche pour ajouter, consulter ou modifier les bons de repas.")

        elif menu == "Ajouter un bon":
            st.title("Ajouter un bon de repas")

            cursor.execute("SELECT id_service, nom_service FROM service ORDER BY nom_service")
            services = cursor.fetchall()

            if not services:
                st.warning("Aucun service disponible. Contacte l’administrateur.")
            else:
                col1, col2 = st.columns([1, 1.3])

                with col1:
                    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                    st.subheader("Nouveau bon")

                    date_bon = st.date_input("Date du bon")

                    service_dict = {nom: id_ for id_, nom in services}
                    service_nom = st.selectbox("Service", list(service_dict.keys()))
                    id_service = service_dict[service_nom]

                    normal = st.number_input("Régime normal", min_value=0, step=1)
                    diabetique = st.number_input("Régime diabétique", min_value=0, step=1)

                    if st.button("Enregistrer le bon", use_container_width=True):
                        cursor.execute("""
                            INSERT INTO bon_repas (date_bon, id_service, normal, diabetique)
                            VALUES (?, ?, ?, ?)
                        """, (str(date_bon), id_service, normal, diabetique))
                        conn.commit()
                        st.success("Bon enregistré avec succès.")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                    st.subheader("Récapitulatif")
                    st.write(f"**Date :** {date_bon}")
                    st.write(f"**Service :** {service_nom}")
                    st.write(f"**Régime normal :** {normal}")
                    st.write(f"**Régime diabétique :** {diabetique}")
                    st.markdown('</div>', unsafe_allow_html=True)

        elif menu == "Mes bons":
            st.title("Mes bons de repas")

            cursor.execute("""
                SELECT b.id_bon, b.date_bon, s.nom_service, b.normal, b.diabetique
                FROM bon_repas b
                JOIN service s ON b.id_service = s.id_service
                ORDER BY b.date_bon DESC, b.id_bon DESC
            """)
            bons = cursor.fetchall()

            if bons:
                df_bons = pd.DataFrame(
                    bons,
                    columns=["ID", "Date", "Service", "Normal", "Diabétique"]
                )
                st.dataframe(df_bons, use_container_width=True, hide_index=True)

                st.divider()
                st.subheader("Supprimer un bon")

                bon_options = {
                    f"Bon #{id_bon} - {date_bon} - {nom_service}": id_bon
                    for id_bon, date_bon, nom_service, normal, diabetique in bons
                }

                bon_supprimer = st.selectbox(
                    "Choisir un bon à supprimer",
                    list(bon_options.keys())
                )

                if st.button("Supprimer le bon", use_container_width=True):
                    cursor.execute(
                        "DELETE FROM bon_repas WHERE id_bon = ?",
                        (bon_options[bon_supprimer],)
                    )
                    conn.commit()
                    st.warning("Bon supprimé avec succès.")
                    st.rerun()
            else:
                st.info("Aucun bon enregistré.")

        elif menu == "Modifier un bon":
            st.title("Modifier un bon de repas")

            cursor.execute("""
                SELECT b.id_bon, b.date_bon, s.nom_service, b.normal, b.diabetique, b.id_service
                FROM bon_repas b
                JOIN service s ON b.id_service = s.id_service
                ORDER BY b.date_bon DESC, b.id_bon DESC
            """)
            bons = cursor.fetchall()

            cursor.execute("SELECT id_service, nom_service FROM service ORDER BY nom_service")
            services = cursor.fetchall()

            if not bons:
                st.info("Aucun bon à modifier.")
            else:
                bon_options = {
                    f"Bon #{id_bon} - {date_bon} - {nom_service}": (
                        id_bon, date_bon, nom_service, normal, diabetique, id_service
                    )
                    for id_bon, date_bon, nom_service, normal, diabetique, id_service in bons
                }

                choix = st.selectbox("Choisir un bon", list(bon_options.keys()))
                bon = bon_options[choix]

                id_bon = bon[0]
                date_bon_actuelle = bon[1]
                normal_actuel = bon[3]
                diabetique_actuel = bon[4]
                id_service_actuel = bon[5]

                st.markdown('<div class="custom-card">', unsafe_allow_html=True)

                nouvelle_date = st.date_input(
                    "Date du bon",
                    value=pd.to_datetime(date_bon_actuelle)
                )

                service_dict = {nom: id_ for id_, nom in services}
                noms_services = list(service_dict.keys())

                service_index = 0
                for i, (nom, id_) in enumerate(service_dict.items()):
                    if id_ == id_service_actuel:
                        service_index = i
                        break

                nouveau_service_nom = st.selectbox(
                    "Service",
                    noms_services,
                    index=service_index
                )
                nouveau_id_service = service_dict[nouveau_service_nom]

                nouveau_normal = st.number_input(
                    "Régime normal",
                    min_value=0,
                    step=1,
                    value=normal_actuel
                )
                nouveau_diabetique = st.number_input(
                    "Régime diabétique",
                    min_value=0,
                    step=1,
                    value=diabetique_actuel
                )

                if st.button("Mettre à jour le bon", use_container_width=True):
                    cursor.execute("""
                        UPDATE bon_repas
                        SET date_bon = ?, id_service = ?, normal = ?, diabetique = ?
                        WHERE id_bon = ?
                    """, (
                        str(nouvelle_date),
                        nouveau_id_service,
                        nouveau_normal,
                        nouveau_diabetique,
                        id_bon
                    ))
                    conn.commit()
                    st.success("Bon modifié avec succès.")
                    st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================
    # CUISINE
    # ==========================================================
    elif user["role"] == "cuisine":
        menu = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Consultation", "Totaux"]
        )

        if menu == "Dashboard":
            st.title("Dashboard Cuisine")
            st.markdown(
                f'<div class="subtitle">Bienvenue {user["nom"]}</div>',
                unsafe_allow_html=True
            )

            cursor.execute("SELECT COUNT(*) FROM bon_repas")
            nb_bons = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(normal), 0) FROM bon_repas")
            total_normal = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(diabetique), 0) FROM bon_repas")
            total_diabetique = cursor.fetchone()[0]

            col1, col2, col3 = st.columns(3)
            col1.metric("Bons enregistrés", nb_bons)
            col2.metric("Total normal", total_normal)
            col3.metric("Total diabétique", total_diabetique)

            st.info("Consulte les bons enregistrés et les totaux des repas.")

        elif menu == "Consultation":
            st.title("Consultation des bons")

            cursor.execute("""
                SELECT b.id_bon, b.date_bon, s.nom_service, b.normal, b.diabetique
                FROM bon_repas b
                JOIN service s ON b.id_service = s.id_service
                ORDER BY b.date_bon DESC, b.id_bon DESC
            """)
            bons = cursor.fetchall()

            if bons:
                df_bons = pd.DataFrame(
                    bons,
                    columns=["ID", "Date", "Service", "Normal", "Diabétique"]
                )
                st.dataframe(df_bons, use_container_width=True, hide_index=True)
            else:
                st.info("Aucun bon enregistré.")

        elif menu == "Totaux":
            st.title("Totaux des repas")

            cursor.execute("SELECT COALESCE(SUM(normal), 0) FROM bon_repas")
            total_normal = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(diabetique), 0) FROM bon_repas")
            total_diabetique = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(normal + diabetique), 0) FROM bon_repas")
            total_global = cursor.fetchone()[0]

            col1, col2, col3 = st.columns(3)
            col1.metric("Total régime normal", total_normal)
            col2.metric("Total régime diabétique", total_diabetique)
            col3.metric("Total global", total_global)

    conn.close()