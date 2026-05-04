import sqlite3

conn = sqlite3.connect("gestion_repas.db")
cursor = conn.cursor()

# Ajouter statut
try:
    cursor.execute("ALTER TABLE bon_repas ADD COLUMN statut TEXT DEFAULT 'En attente'")
    print("Colonne statut ajoutée")
except:
    print("statut existe déjà")

# Ajouter id_chambre
try:
    cursor.execute("ALTER TABLE bon_repas ADD COLUMN id_chambre INTEGER")
    print("Colonne id_chambre ajoutée")
except:
    print("id_chambre existe déjà")

conn.commit()
conn.close()