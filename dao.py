from db import get_db
import datetime

def get_user_by_id(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM UTENTE WHERE ID_UTENTE = ?", (user_id,)).fetchone()
    return user

def get_user_by_email(email):
    db = get_db()
    user = db.execute("SELECT * FROM UTENTE WHERE Email = ?", (email,)).fetchone()
    return user

def insert_user(nome, cognome, email, password, ruolo):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO UTENTE (Password, Email, Nome, Cognome, Ruolo) VALUES (?, ?, ?, ?, ?)",
            (password, email, nome, cognome, ruolo,)
        )
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
    
def getUserTicket(userID):
    db = get_db()
    try:
        return db.execute(
            "SELECT A.ID_BIGLIETTO, T.Descrizione, T.Prezzo, B.giorno_riferimento, A.TimeStamp_emissione " \
            "FROM ACQUISTARE A " \
            "JOIN BIGLIETTO B ON A.ID_BIGLIETTO = B.ID_BIGLIETTO " \
            "JOIN TIPO_BIGLIETTO T ON B.ID_TIPO_BIGLIETTO = T.ID_TIPO_BIGLIETTO "\
            "WHERE A.ID_UTENTE = ?", (userID,)
        ).fetchone()
    except Exception as e:
        print(e)
        return None

def getTicketPricesAndDescription():
    db = get_db()
    try:
        return db.execute(
            "SELECT Prezzo, Descrizione " \
            "FROM TIPO_BIGLIETTO " \
            "ORDER BY Prezzo ASC"
        ).fetchall()
    except Exception as e:
        print(e)
    
    return None

def countTicketsPerGivenDay(Day):
    db = get_db()
    try:
        return db.execute(
            "SELECT COUNT(*) as numeroBiglietti FROM BIGLIETTO WHERE giorno_riferimento = ?", (Day,)
        ).fetchone()
    except Exception as e:
        print(e)
    
    return None

def insert_ticket(ticketTypeID, reportingDay):
    db = get_db()
    try:
        cursor = db.execute(
            "INSERT INTO BIGLIETTO (ID_TIPO_BIGLIETTO, giorno_riferimento) VALUES (?, ?)",
            (ticketTypeID, reportingDay,)
        )
        db.commit()
        return cursor.lastrowid
    except Exception as e:
        print(e)
    return None

def insert_purchase(userID, ticketID):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO ACQUISTARE (ID_UTENTE, ID_BIGLIETTO, TimeStamp_emissione) VALUES (?, ?, ?)",
            (userID, ticketID, datetime.datetime.now(),)
        )
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False

def countArtistPerformances(nomeArtista):
    db = get_db()
    try:
        return db.execute(
            "SELECT COUNT(*) AS numeroPerformance FROM PERFORMANCE JOIN ARTISTA ON ARTISTA.ID_ARTISTA = PERFORMANCE.ID_ARTISTA WHERE ARTISTA.Nome = ?"
            ,(nomeArtista,)
        ).fetchone()
    except Exception as e:
        print(e)
    return None

def getArtistsList():
    db = get_db()
    try:
        nameList = []
        rows = db.execute(
            "SELECT Nome FROM ARTISTA"
        ).fetchall()
        for r in rows:
            nameList.append(r["Nome"])
        return nameList
    except Exception as e:
        print(e)
    return []

def insert_artist(artistName):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO ARTISTA (Nome) VALUES (?)",
            (artistName,)
        )
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False

def updateImagePath(newPath, userID):
    db = get_db()
    try:
        db.execute(
        "UPDATE UTENTE SET percorso_immagine = ? WHERE ID_UTENTE = ?",
            (newPath, userID)
        )
        db.commit()
        return True
    except Exception as e:
        return False
    
def insertNewArtistImageWithPath(artistID, newPath):
    db = get_db()
    try:
        db.execute(
        "INSERT INTO " \
        "PERCORSO_IMMAGINE_ARTISTA (ID_ARTISTA, Percorso) "\
        "VALUES (?, ?)"
        ,(artistID, newPath,)
        )
        db.commit()
        return True
    except Exception as e:
        return False

def getPublicPerformancesInGivenDay(givenDay):
    db = get_db()
    try:
        performanceList = []
        rows = db.execute(
            "SELECT Giorno, Ora, Durata, ID_PALCO FROM PERFORMANCE WHERE Giorno = ? AND Stato = 1", (givenDay,)
        ).fetchall()
        for r in rows:
            performanceList.append({
                "Giorno": r["Giorno"],
                "Ora": r["Ora"],
                "Durata": r["Durata"],
                "Palco": r["ID_PALCO"]
            })
        return performanceList
    except Exception as e:
        print("Errore:", e)
    return []

def getPrivatePerformancesByUserID(userID):
    db = get_db()
    try:
        performanceList = []
        rows = db.execute(
            """
            SELECT Giorno, Ora, Durata, PALCO.ID_PALCO AS ID_PALCO, PERFORMANCE.Descrizione AS Descrizione, PALCO.Descrizione AS DescrizionePalco, ARTISTA.Nome as NomeArtista
            FROM PERFORMANCE 
            JOIN ARTISTA ON ARTISTA.ID_ARTISTA = PERFORMANCE.ID_ARTISTA
            JOIN PALCO ON PALCO.ID_PALCO = PERFORMANCE.ID_PALCO
            WHERE Stato = 0 AND ID_UTENTE = ?
            """, (userID,)).fetchall()
        for r in rows:
            performanceList.append({
                "Giorno": r["Giorno"],
                "Ora": r["Ora"],
                "Durata": r["Durata"],
                "Palco": r["ID_PALCO"],
                "DescPalco": r["DescrizionePalco"],
                "Descrizione": r["Descrizione"],
                "NomeArtista":r["NomeArtista"]
            })
        return performanceList
    except Exception as e:
        print("Errore:", e)
    return []

def getArtistIdByName(name):
    db = get_db()
    try:
        return db.execute(
            "SELECT ID_ARTISTA as idArtista FROM ARTISTA WHERE Nome = ?", (name,)
            ).fetchone()
    except Exception as e:
        print(e)
        return None

def insert_performance(day, time, duration, description, state, musicType, userID, artistID, stageID):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO " \
            "PERFORMANCE (Giorno, Ora, Durata, Descrizione, Stato, Genere_musicale, ID_UTENTE, ID_ARTISTA, ID_PALCO) "\
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"\
            ,
            (day, time, duration, description, state, musicType, userID, artistID, stageID, )
        )
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False