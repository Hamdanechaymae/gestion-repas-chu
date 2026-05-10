import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

from database import (
    get_bons,
    get_bons_par_date,
    get_totaux_regimes_par_date,
    modifier_statut_bon,
    get_totaux_par_service,
)

def section_header(title, description):
    st.markdown(
        f"""
        <div class="hero" style="padding: 1.2rem 1.4rem; margin-bottom: 1rem;">
            <h1 style="font-size: 1.5rem; margin-bottom: 0.35rem; color: white !important;">{title}</h1>
            <p style="margin-bottom: 0; color: #E0F2FE !important;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def dashboard_cuisine():
    section_header(
        "Tableau de bord cuisine",
        "Vue d'ensemble de la production pour aujourd'hui."
    )
    
    aujourdhui = str(date.today())
    totaux_jour = get_totaux_regimes_par_date(aujourdhui)
    total_general = sum([t[1] for t in totaux_jour]) if totaux_jour else 0
    
    bons_jour = get_bons_par_date(aujourdhui)
    total_bons = len(bons_jour) if bons_jour else 0

    if total_bons == 0:
        st.warning("Aucun bon de repas recu pour aujourd'hui.")
    else:
        st.success(f"Production en cours : {total_general} repas repartis dans {total_bons} commandes.")

    if totaux_jour:
        cols = st.columns(len(totaux_jour))
        for i, (regime, qte) in enumerate(totaux_jour):
            cols[i].metric(f"Repas {regime}", qte)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.subheader("Repartition des repas par type")
        
        df_chart = pd.DataFrame(totaux_jour, columns=["Type", "Total"])
        st.bar_chart(df_chart.set_index("Type"))


def consultation_bons():
    section_header(
        "Consultation des bons",
        "Consultez les bons recus et mettez a jour l'etat d'avancement de la production."
    )

    date_selection = st.date_input("Filtrer par date", value=date.today())
    bons = get_bons_par_date(str(date_selection))
    
    if not bons:
        st.info("Aucun bon enregistre pour cette date.")
        return

    df = pd.DataFrame(
        bons,
        columns=["ID", "Date", "Service", "Chambre", "Detail des Repas", "Statut"]
    )
    
    # ---- Filtre par statut ----
    statuts_disponibles = ["Tous"] + sorted(df["Statut"].unique().tolist())
    filtre_statut = st.selectbox("Filtrer par statut", statuts_disponibles)
    
    if filtre_statut != "Tous":
        df = df[df["Statut"] == filtre_statut]
    
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ---- Export Excel ----
    st.markdown("<br>", unsafe_allow_html=True)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Bons_Repas')
    excel_data = output.getvalue()
    
    st.download_button(
        label="Exporter en Excel",
        data=excel_data,
        file_name=f"bons_repas_{date_selection}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 0.8], gap="large")
    bon_dict = {f"ID {b[0]} - {b[2]} - Chambre {b[3]}": b[0] for b in bons}

    with col1:
        st.subheader("Mise a jour du statut")
        choix = st.selectbox("Choisir un bon", list(bon_dict.keys()))
        id_bon = bon_dict[choix]

        btn1, btn2, btn3 = st.columns(3)

        with btn1:
            if st.button("En preparation", use_container_width=True):
                modifier_statut_bon(id_bon, "En preparation")
                st.rerun()

        with btn2:
            if st.button("Pret / Livre", use_container_width=True):
                modifier_statut_bon(id_bon, "Pret / Livre")
                st.success("Statut mis a jour.")
                st.rerun()
                
        with btn3:
            if st.button("Annule", use_container_width=True):
                modifier_statut_bon(id_bon, "Annule")
                st.warning("Bon annule.")
                st.rerun()

    with col2:
        st.subheader("Consigne")
        st.info("Mettez a jour le statut en temps reel. Le service verra le changement s'afficher sur son propre ecran.")


def totaux_cuisine():
    section_header(
        "Totaux detailles",
        "Consultez les volumes de repas a preparer par service pour une date donnee."
    )

    date_selection = st.date_input("Choisir une date de production", value=date.today())
    totaux_service = get_totaux_par_service(str(date_selection))

    if not totaux_service:
        st.warning("Aucun bon de commande valide pour cette date.")
        return

    df_brut = pd.DataFrame(totaux_service, columns=["Service", "Regime", "Quantite"])
    df_pivot = df_brut.pivot_table(index="Service", columns="Regime", values="Quantite", aggfunc="sum", fill_value=0)
    df_pivot["Total Service"] = df_pivot.sum(axis=1)
    df_pivot = df_pivot.reset_index()

    st.subheader("Tableau de repartition")
    st.dataframe(df_pivot, use_container_width=True, hide_index=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.subheader("Graphique par service")
    
    df_chart = df_pivot.drop(columns=["Total Service"]).set_index("Service")
    st.bar_chart(df_chart)


def cuisine_page():
    st.sidebar.markdown("## Cuisine")
    menu = st.sidebar.radio(
        "Navigation",
        ["Tableau de bord", "Consultation", "Totaux"],
        key="menu_cuisine",
        label_visibility="collapsed"
    )

    if menu == "Tableau de bord":
        dashboard_cuisine()
    elif menu == "Consultation":
        consultation_bons()
    elif menu == "Totaux":
        totaux_cuisine()