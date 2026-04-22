import sqlite3

def get_connection():
    return sqlite3.connect("gestion_repas.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilisateur (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        mot_de_passe TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS service (
        id_service INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_service TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS regime (
        id_regime INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_regime TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bon_repas (
        id_bon INTEGER PRIMARY KEY AUTOINCREMENT,
        date_bon TEXT NOT NULL,
        id_service INTEGER NOT NULL,
        normal INTEGER NOT NULL,
        diabetique INTEGER NOT NULL,
        FOREIGN KEY (id_service) REFERENCES service(id_service)
    )
    """)

    conn.commit()
    conn.close()