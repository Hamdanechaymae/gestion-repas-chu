import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect("gestion_repas.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Structure des tables
    cursor.execute("CREATE TABLE IF NOT EXISTS service (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS regime (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS utilisateur (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, email TEXT UNIQUE, password TEXT, role TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS chambre (id INTEGER PRIMARY KEY AUTOINCREMENT, numero TEXT, id_service INTEGER, nombre_patients INTEGER DEFAULT 1, FOREIGN KEY(id_service) REFERENCES service(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS bon_repas (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, id_service INTEGER, id_chambre INTEGER, statut TEXT DEFAULT 'En attente', FOREIGN KEY(id_service) REFERENCES service(id), FOREIGN KEY(id_chambre) REFERENCES chambre(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS detail_bon_repas (id_bon INTEGER, id_regime INTEGER, quantite INTEGER, PRIMARY KEY(id_bon, id_regime), FOREIGN KEY(id_bon) REFERENCES bon_repas(id) ON DELETE CASCADE, FOREIGN KEY(id_regime) REFERENCES regime(id))")
    
    # Nouvelle table : historique des modifications
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historique (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_heure TEXT NOT NULL,
            utilisateur TEXT NOT NULL,
            role TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# --- HISTORIQUE ---
def ajouter_historique(utilisateur, role, action, details=""):
    conn = get_connection()
    cursor = conn.cursor()
    date_heure = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cursor.execute(
        "INSERT INTO historique (date_heure, utilisateur, role, action, details) VALUES (?, ?, ?, ?, ?)",
        (date_heure, utilisateur, role, action, details)
    )
    conn.commit()
    conn.close()

def get_historique():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM historique ORDER BY id DESC")
    res = cursor.fetchall()
    conn.close()
    return res

# --- UTILISATEURS ---
def ajouter_utilisateur(nom, email, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO utilisateur (nom, email, password, role) VALUES (?, ?, ?, ?)", (nom, email, password, role))
    conn.commit()
    conn.close()

def get_utilisateurs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, email, role FROM utilisateur")
    res = cursor.fetchall()
    conn.close()
    return res

def supprimer_utilisateur(id_user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM utilisateur WHERE id=?", (id_user,))
    conn.commit()
    conn.close()

# --- ADMIN (Services, Régimes, Chambres) ---
def ajouter_service(nom):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO service (nom) VALUES (?)", (nom,))
    conn.commit()
    conn.close()

def get_services():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM service")
    res = cursor.fetchall()
    conn.close()
    return res

def get_services_dict():
    services = get_services()
    return {s[1]: s[0] for s in services}

def supprimer_service(id_service):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM service WHERE id=?", (id_service,))
    conn.commit()
    conn.close()

def ajouter_regime(nom):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO regime (nom) VALUES (?)", (nom,))
    conn.commit()
    conn.close()

def get_regimes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM regime")
    res = cursor.fetchall()
    conn.close()
    return res

def supprimer_regime(id_regime):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM regime WHERE id=?", (id_regime,))
    conn.commit()
    conn.close()

def ajouter_chambre(numero, id_service, nombre_patients):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chambre (numero, id_service, nombre_patients) VALUES (?, ?, ?)", (numero, id_service, nombre_patients))
    conn.commit()
    conn.close()

def get_chambres():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT chambre.id, chambre.numero, service.nom, chambre.nombre_patients FROM chambre JOIN service ON chambre.id_service = service.id")
    res = cursor.fetchall()
    conn.close()
    return res

def get_chambres_by_service(id_service):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, numero, nombre_patients FROM chambre WHERE id_service=?", (id_service,))
    res = cursor.fetchall()
    conn.close()
    return res

def supprimer_chambre(id_chambre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chambre WHERE id=?", (id_chambre,))
    conn.commit()
    conn.close()

def get_stats_admin():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM service")
    s = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM regime")
    r = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM utilisateur")
    u = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM chambre")
    c = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM bon_repas")
    b = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(quantite) FROM detail_bon_repas")
    t = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM bon_repas WHERE statut='Pret / Livre'")
    l = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT r.nom, COALESCE(SUM(d.quantite), 0)
        FROM regime r
        LEFT JOIN detail_bon_repas d ON r.id = d.id_regime
        GROUP BY r.id, r.nom
    """)
    totaux_regimes = cursor.fetchall()
    
    conn.close()
    return s, r, u, c, b, t, l, totaux_regimes


# --- SERVICE (Bons, Modifications, Stats) ---
def ajouter_bon(date_bon, id_service, id_chambre, dict_regimes):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO bon_repas (date, id_service, id_chambre) VALUES (?, ?, ?)", (date_bon, id_service, id_chambre))
        id_bon = cursor.lastrowid
        for id_regime, qte in dict_regimes.items():
            if qte > 0:
                cursor.execute("INSERT INTO detail_bon_repas (id_bon, id_regime, quantite) VALUES (?, ?, ?)", (id_bon, id_regime, qte))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def modifier_bon(id_bon, id_chambre, dict_regimes):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE bon_repas SET id_chambre=? WHERE id=?", (id_chambre, id_bon))
        cursor.execute("DELETE FROM detail_bon_repas WHERE id_bon=?", (id_bon,))
        for id_regime, qte in dict_regimes.items():
            if qte > 0:
                cursor.execute("INSERT INTO detail_bon_repas (id_bon, id_regime, quantite) VALUES (?, ?, ?)", (id_bon, id_regime, qte))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_bons():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, b.date, s.nom, c.numero, 
               GROUP_CONCAT(r.nom || ': ' || d.quantite, ' | ') as details,
               b.statut
        FROM bon_repas b
        JOIN service s ON b.id_service = s.id
        JOIN chambre c ON b.id_chambre = c.id
        LEFT JOIN detail_bon_repas d ON b.id = d.id_bon
        LEFT JOIN regime r ON d.id_regime = r.id
        GROUP BY b.id
        ORDER BY b.date DESC
    """)
    res = cursor.fetchall()
    conn.close()
    return res

def supprimer_bon(id_bon):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM detail_bon_repas WHERE id_bon=?", (id_bon,))
    cursor.execute("DELETE FROM bon_repas WHERE id=?", (id_bon,))
    conn.commit()
    conn.close()

def get_stats_service():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM bon_repas")
    total_bons = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(quantite) FROM detail_bon_repas")
    total_repas = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM bon_repas WHERE statut='En attente'")
    en_attente = cursor.fetchone()[0]
    conn.close()
    return total_bons, total_repas, en_attente

def get_derniers_bons():
    return get_bons()[:5]

# --- CUISINE ---
def modifier_statut_bon(id_bon, statut):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE bon_repas SET statut=? WHERE id=?", (statut, id_bon))
    conn.commit()
    conn.close()

def get_bons_par_date(date_choisie):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, b.date, s.nom, c.numero, 
               GROUP_CONCAT(r.nom || ': ' || d.quantite, ' | ') as details,
               b.statut
        FROM bon_repas b
        JOIN service s ON b.id_service = s.id
        JOIN chambre c ON b.id_chambre = c.id
        LEFT JOIN detail_bon_repas d ON b.id = d.id_bon
        LEFT JOIN regime r ON d.id_regime = r.id
        WHERE b.date = ?
        GROUP BY b.id
    """, (str(date_choisie),))
    res = cursor.fetchall()
    conn.close()
    return res

def get_totaux_regimes_par_date(date_choisie):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.nom, SUM(d.quantite)
        FROM detail_bon_repas d
        JOIN bon_repas b ON d.id_bon = b.id
        JOIN regime r ON d.id_regime = r.id
        WHERE b.date = ?
        GROUP BY r.nom
    """, (str(date_choisie),))
    res = cursor.fetchall()
    conn.close()
    return res

def get_totaux_par_service(date_choisie):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.nom, r.nom, SUM(d.quantite)
        FROM detail_bon_repas d
        JOIN bon_repas b ON d.id_bon = b.id
        JOIN service s ON b.id_service = s.id
        JOIN regime r ON d.id_regime = r.id
        WHERE b.date = ?
        GROUP BY s.nom, r.nom
    """, (str(date_choisie),))
    res = cursor.fetchall()
    conn.close()
    return res

init_db()