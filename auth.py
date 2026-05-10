from database import get_connection

def verifier_connexion(email, mot_de_passe_saisi):
    conn = get_connection()
    cursor = conn.cursor()

    # On utilise 'id' et 'password' car ce sont les noms 
    # définis dans le CREATE TABLE de ton fichier database.py
    cursor.execute("""
        SELECT id, nom, email, role
        FROM utilisateur
        WHERE email = ? AND password = ?
    """, (email, mot_de_passe_saisi))

    user = cursor.fetchone()
    conn.close()
    return user