from database import get_connection

def verifier_connexion(email, mot_de_passe):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_user, nom, email, role
        FROM utilisateur
        WHERE email = ? AND mot_de_passe = ?
    """, (email, mot_de_passe))

    user = cursor.fetchone()
    conn.close()
    return user