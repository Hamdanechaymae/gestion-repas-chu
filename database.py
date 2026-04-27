import sqlite3


# ================= CONNEXION =================
def get_connection():
    return sqlite3.connect("gestion_repas.db", check_same_thread=False)


# ================= INITIALISATION =================
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
        nom_service TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS regime (
        id_regime INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_regime TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chambre (
        id_chambre INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_chambre TEXT NOT NULL,
        id_service INTEGER NOT NULL,
        FOREIGN KEY (id_service) REFERENCES service(id_service),
        UNIQUE(numero_chambre, id_service)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bon_repas (
        id_bon INTEGER PRIMARY KEY AUTOINCREMENT,
        date_bon TEXT NOT NULL,
        id_service INTEGER NOT NULL,
        id_chambre INTEGER,
        normal INTEGER NOT NULL,
        diabetique INTEGER NOT NULL,
        FOREIGN KEY (id_service) REFERENCES service(id_service),
        FOREIGN KEY (id_chambre) REFERENCES chambre(id_chambre)
    )
    """)

    conn.commit()
    conn.close()


# ================= SERVICES =================
def ajouter_service(nom_service):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO service (nom_service) VALUES (?)", (nom_service,))
    conn.commit()
    conn.close()


def get_services():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_service, nom_service
        FROM service
        ORDER BY id_service DESC
    """)
    services = cursor.fetchall()
    conn.close()
    return services


def supprimer_service(id_service):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM service WHERE id_service = ?", (id_service,))
    conn.commit()
    conn.close()


def get_services_dict():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_service, nom_service
        FROM service
        ORDER BY nom_service ASC
    """)
    data = cursor.fetchall()
    conn.close()
    return {nom: id_service for id_service, nom in data}


# ================= CHAMBRES =================
def ajouter_chambre(numero_chambre, id_service):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM chambre
        WHERE numero_chambre = ? AND id_service = ?
    """, (numero_chambre, id_service))

    existe = cursor.fetchone()[0]

    if existe > 0:
        conn.close()
        raise Exception("Cette chambre existe déjà dans ce service.")

    cursor.execute("""
        INSERT INTO chambre (numero_chambre, id_service)
        VALUES (?, ?)
    """, (numero_chambre, id_service))

    conn.commit()
    conn.close()


def get_chambres():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id_chambre, c.numero_chambre, s.nom_service
        FROM chambre c
        JOIN service s ON c.id_service = s.id_service
        ORDER BY s.nom_service ASC, c.numero_chambre ASC
    """)
    chambres = cursor.fetchall()
    conn.close()
    return chambres


def get_chambres_by_service(id_service):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_chambre, numero_chambre
        FROM chambre
        WHERE id_service = ?
        ORDER BY numero_chambre ASC
    """, (id_service,))
    chambres = cursor.fetchall()
    conn.close()
    return chambres


def supprimer_chambre(id_chambre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chambre WHERE id_chambre = ?", (id_chambre,))
    conn.commit()
    conn.close()


def count_chambres():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM chambre")
    total = cursor.fetchone()[0]
    conn.close()
    return total


# ================= RÉGIMES =================
def ajouter_regime(nom_regime):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO regime (nom_regime) VALUES (?)", (nom_regime,))
    conn.commit()
    conn.close()


def get_regimes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_regime, nom_regime
        FROM regime
        ORDER BY id_regime DESC
    """)
    regimes = cursor.fetchall()
    conn.close()
    return regimes


def supprimer_regime(id_regime):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM regime WHERE id_regime = ?", (id_regime,))
    conn.commit()
    conn.close()


# ================= UTILISATEURS =================
def ajouter_utilisateur(nom, email, mot_de_passe, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO utilisateur (nom, email, mot_de_passe, role)
        VALUES (?, ?, ?, ?)
    """, (nom, email, mot_de_passe, role))
    conn.commit()
    conn.close()


def get_utilisateurs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_user, nom, email, role
        FROM utilisateur
        ORDER BY id_user DESC
    """)
    users = cursor.fetchall()
    conn.close()
    return users


def supprimer_utilisateur(id_user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM utilisateur WHERE id_user = ?", (id_user,))
    conn.commit()
    conn.close()


# ================= BONS DE REPAS =================
def ajouter_bon(date_bon, id_service, id_chambre, normal, diabetique):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bon_repas (date_bon, id_service, id_chambre, normal, diabetique)
        VALUES (?, ?, ?, ?, ?)
    """, (date_bon, id_service, id_chambre, normal, diabetique))
    conn.commit()
    conn.close()


def get_bons():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id_bon, b.date_bon, s.nom_service, c.numero_chambre, b.normal, b.diabetique
        FROM bon_repas b
        JOIN service s ON b.id_service = s.id_service
        LEFT JOIN chambre c ON b.id_chambre = c.id_chambre
        ORDER BY b.date_bon DESC, b.id_bon DESC
    """)
    bons = cursor.fetchall()
    conn.close()
    return bons


def modifier_bon(id_bon, date_bon, id_service, id_chambre, normal, diabetique):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE bon_repas
        SET date_bon = ?, id_service = ?, id_chambre = ?, normal = ?, diabetique = ?
        WHERE id_bon = ?
    """, (date_bon, id_service, id_chambre, normal, diabetique, id_bon))
    conn.commit()
    conn.close()


def supprimer_bon(id_bon):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bon_repas WHERE id_bon = ?", (id_bon,))
    conn.commit()
    conn.close()


# ================= STATISTIQUES SERVICE =================
def get_stats_service():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM bon_repas")
    total_bons = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(normal), 0), COALESCE(SUM(diabetique), 0)
        FROM bon_repas
    """)
    total_normal, total_diabetique = cursor.fetchone()

    conn.close()
    return total_bons, total_normal, total_diabetique


def get_derniers_bons(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.date_bon, s.nom_service, c.numero_chambre, b.normal, b.diabetique
        FROM bon_repas b
        JOIN service s ON b.id_service = s.id_service
        LEFT JOIN chambre c ON b.id_chambre = c.id_chambre
        ORDER BY b.id_bon DESC
        LIMIT ?
    """, (limit,))

    bons = cursor.fetchall()
    conn.close()
    return bons


# ================= STATISTIQUES ADMIN =================
def get_stats_admin():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM service")
    total_services = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM regime")
    total_regimes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM utilisateur")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM chambre")
    total_chambres = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bon_repas")
    total_bons = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(normal), 0), COALESCE(SUM(diabetique), 0)
        FROM bon_repas
    """)
    total_normal, total_diabetique = cursor.fetchone()

    conn.close()
    return total_services, total_regimes, total_users, total_chambres, total_bons, total_normal, total_diabetique


# ================= CUISINE =================
def get_bons_par_date(date_bon):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.id_bon, b.date_bon, s.nom_service, c.numero_chambre, b.normal, b.diabetique
        FROM bon_repas b
        JOIN service s ON b.id_service = s.id_service
        LEFT JOIN chambre c ON b.id_chambre = c.id_chambre
        WHERE b.date_bon = ?
        ORDER BY s.nom_service ASC, c.numero_chambre ASC
    """, (date_bon,))

    bons = cursor.fetchall()
    conn.close()
    return bons


def get_stats_cuisine():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM bon_repas")
    total_bons = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(normal), 0), COALESCE(SUM(diabetique), 0)
        FROM bon_repas
    """)
    total_normal, total_diabetique = cursor.fetchone()

    conn.close()
    return total_bons, total_normal, total_diabetique