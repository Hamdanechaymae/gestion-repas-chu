import sqlite3
import os
from database import init_db, get_connection

# 1. On réinitialise la base de données pour être sûr qu'elle est propre
if os.path.exists("gestion_repas.db"):
    try:
        os.remove("gestion_repas.db")
        print("Ancienne base de données supprimée.")
    except PermissionError:
        print("Note: Impossible de supprimer la base car elle est ouverte ailleurs.")

# 2. On crée les tables avec la nouvelle structure
init_db()

conn = get_connection()
cursor = conn.cursor()

# 3. Ajout des utilisateurs (Attention : on utilise 'password' comme dans database.py)
users = [
    ("Administrateur", "admin@chu.ma", "1234", "admin"),
    ("Agent Service", "service@chu.ma", "1234", "service"),
    ("Cuisine Centrale", "cuisine@chu.ma", "1234", "cuisine"),
]

print("Ajout des utilisateurs...")
for user in users:
    try:
        cursor.execute("""
            INSERT INTO utilisateur (nom, email, password, role)
            VALUES (?, ?, ?, ?)
        """, user)
    except Exception as e:
        print(f"Erreur utilisateur {user[1]}: {e}")

# 4. Ajout des régimes de base (Attention : la colonne s'appelle 'nom' dans database.py)
regimes = [("Normal",), ("Diabétique",), ("Sans Sel",), ("Mixé",)]

print("Ajout des régimes...")
for regime in regimes:
    try:
        cursor.execute("""
            INSERT INTO regime (nom)
            VALUES (?)
        """, regime)
    except Exception as e:
        print(f"Erreur régime {regime[0]}: {e}")

conn.commit()
conn.close()

print("---")
print("✅ Configuration terminée avec succès !")
print("Identifiants : admin@chu.ma / 1234")