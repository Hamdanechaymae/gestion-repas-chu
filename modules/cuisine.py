import streamlit as st


def cuisine_page():
    menu = st.sidebar.radio(
        "Fonctionnalités Cuisine",
        ["Dashboard", "Consultation", "Totaux"],
        key="menu_cuisine"
    )

    if menu == "Dashboard":
        st.title("🍽️ Dashboard Cuisine")
        st.info("Bienvenue dans l’espace cuisine.")

    elif menu == "Consultation":
        st.title("📋 Consultation des bons")
        st.write("Ici, la cuisine va consulter les bons de repas.")

    elif menu == "Totaux":
        st.title("📊 Totaux des repas")
        st.write("Ici, la cuisine va voir les totaux.")