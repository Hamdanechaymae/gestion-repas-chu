import streamlit as st
import sqlite3
import pandas as pd

st.title("📊 Statistiques Administrateur")
st.caption("Statistiques globales de l'application")

conn = sqlite3.connect("gestion_repas.db")
cursor = conn.cursor()

# --- KPIs ---
cursor.execute("SELECT COUNT(*) FROM service")
nb_services = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM users")
nb_users = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM bon")
nb_bons = cursor.fetchone()[0]

cursor.execute("SELECT SUM(qte_normal), SUM(qte_diabetique) FROM bon")
result = cursor.fetchone()

total_normal = result[0] if result[0] else 0
total_diabetique = result[1] if result[1] else 0

# --- AFFICHAGE KPIs ---
col1, col2, col3 = st.columns(3)

col1.metric("🏥 Services", nb_services)
col2.metric("👤 Utilisateurs", nb_users)
col3.metric("📄 Bons", nb_bons)

st.divider()

col4, col5 = st.columns(2)

col4.metric("🍽️ Total normal", total_normal)
col5.metric("🥗 Total diabétique", total_diabetique)

# --- GRAPHIQUE PAR SERVICE ---
st.divider()
st.subheader("📈 Répartition des repas par service")

df = pd.read_sql_query("""
SELECT service.nom_service, 
       SUM(bon.qte_normal) as normal, 
       SUM(bon.qte_diabetique) as diabetique
FROM bon
JOIN service ON bon.service_id = service.id_service
GROUP BY service.nom_service
""", conn)

if not df.empty:
    st.bar_chart(df.set_index("nom_service"))
else:
    st.info("Aucune donnée disponible pour le graphique")

conn.close()