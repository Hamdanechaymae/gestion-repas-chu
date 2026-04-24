# Dossier modules
regimes = [("Normal",), ("Diabétique",)]
for regime in regimes:
   from database import init_db, get_connection

init_db()

conn = get_connection()
cursor = conn.cursor()

users = [
    ("Administrateur", "admin@chu.ma", "1234", "admin"),
    ("Agent Service", "service@chu.ma", "1234", "service"),
    ("Cuisine Centrale", "cuisine@chu.ma", "1234", "cuisine"),
]

for user in users:
    try:
        cursor.execute("""
            INSERT INTO utilisateur (nom, email, mot_de_passe, role)
            VALUES (?, ?, ?, ?)
        """, user)
    except:
        pass

regimes = [("Normal",), ("Diabétique",)]

for regime in regimes:
    try:
        cursor.execute("""
            INSERT INTO regime (nom_regime)
            VALUES (?)
        """, regime)
    except:
        pass

conn.commit()
conn.close()

print("Utilisateurs et régimes ajoutés.")