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
        bigliettiVenduti = {"Venerdì":0, "Sabato":0, "Domenica":0}
        giorniFestival = {"Venerdì":"Sabato", "Sabato":"Domenica", "Domenica":None}
        tipoBiglietti = ["Giornaliero", "2 Giorni", "Full Pass"]

        rows = db.execute(
            """
            SELECT 
                COUNT(BIGLIETTO.ID_BIGLIETTO) AS BigliettiVenduti,
                BIGLIETTO.giorno_riferimento AS Giorno,
                TIPO_BIGLIETTO.Descrizione AS TipoBiglietto
            FROM BIGLIETTO
            JOIN TIPO_BIGLIETTO 
                ON TIPO_BIGLIETTO.ID_TIPO_BIGLIETTO = BIGLIETTO.ID_TIPO_BIGLIETTO
            GROUP BY 
                BIGLIETTO.giorno_riferimento, 
                TIPO_BIGLIETTO.ID_TIPO_BIGLIETTO
            ORDER BY 
                TIPO_BIGLIETTO.ID_TIPO_BIGLIETTO ASC, 
                BIGLIETTO.giorno_riferimento ASC
            """
        ).fetchall()

        for row in rows:
            if row["TipoBiglietto"] == tipoBiglietti[0]:        # giornaliero
                bigliettiVenduti[row["Giorno"]] += (1 * row["BigliettiVenduti"])
            elif row["TipoBiglietto"] == tipoBiglietti[1]:      # 2 giorni
                bigliettiVenduti[row["Giorno"]] += (1 * row["BigliettiVenduti"])
                bigliettiVenduti[giorniFestival[row["Giorno"]]] += (1 * row["BigliettiVenduti"])
            else:                                               # full pass
                for k in bigliettiVenduti:
                    bigliettiVenduti[k] += (1 * row["BigliettiVenduti"])


        return bigliettiVenduti[Day]
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

# Conta il numero di performance pubbliche che un artista ha assegnate
def countArtistPublicPerformances(nomeArtista):
    db = get_db()
    try:
        return db.execute(
            "SELECT COUNT(*) AS numeroPerformance FROM PERFORMANCE JOIN ARTISTA ON ARTISTA.ID_ARTISTA = PERFORMANCE.ID_ARTISTA WHERE PERFORMANCE.Stato = 1 AND ARTISTA.Nome = ?"
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
        """
        INSERT INTO 
        PERCORSO_IMMAGINE_ARTISTA (ID_ARTISTA, Percorso) 
        VALUES (?, ?)
        """
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

def getArtistImagesAsList(artistID):
    db = get_db()
    try:
        imagesList = []
        rows = db.execute(
            """
                SELECT Percorso
                FROM PERCORSO_IMMAGINE_ARTISTA
                WHERE ID_ARTISTA = ?
            """,
            (artistID)
        ).fetchall()

        for r in rows:
            imagesList.append(r["Percorso"])
        return imagesList
    except Exception as e:
        print("Errore:", e)
    return []

def getPrivatePerformancesByUserID(userID):
    db = get_db()
    try:
        performanceList = []
        rows = db.execute("""
            SELECT Giorno, Ora, Durata, PALCO.ID_PALCO AS ID_PALCO,
                   PERFORMANCE.Descrizione AS Descrizione,
                   PALCO.Descrizione AS DescrizionePalco,
                   ARTISTA.Nome AS NomeArtista,
                   PERFORMANCE.ID_ARTISTA AS ID_ARTISTA,
                   PERFORMANCE.Genere_musicale AS Genere,
                   PERFORMANCE.ID_PERFORMANCE AS performanceID
            FROM PERFORMANCE 
            JOIN ARTISTA ON ARTISTA.ID_ARTISTA = PERFORMANCE.ID_ARTISTA
            JOIN PALCO ON PALCO.ID_PALCO = PERFORMANCE.ID_PALCO
            WHERE Stato = 0 AND ID_UTENTE = ?
        """, (userID,)).fetchall()

        for r in rows:
            immagini_rows = db.execute("""
                SELECT Percorso FROM PERCORSO_IMMAGINE_ARTISTA WHERE ID_ARTISTA = ?
            """, (r["ID_ARTISTA"],)).fetchall()

            immagini = list({img["Percorso"] for img in immagini_rows})  # set per evitare duplicati

            performanceList.append({
                "Giorno": r["Giorno"],
                "Ora": r["Ora"],
                "Durata": r["Durata"],
                "Palco": r["ID_PALCO"],
                "DescPalco": r["DescrizionePalco"],
                "Descrizione": r["Descrizione"],
                "NomeArtista": r["NomeArtista"],
                "Genere": r["Genere"],
                "performanceID": r["performanceID"],
                "ImmaginiArtista": immagini
            })
        return performanceList
    except Exception as e:
        print("Errore:", e)
    return []

def getPublicPerformancesWithImages():
    db = get_db()
    try:
        performanceList = []
        rows = db.execute(
            """
            SELECT Giorno, Ora, Durata, PALCO.ID_PALCO AS ID_PALCO,
                   PERFORMANCE.Descrizione AS Descrizione,
                   PALCO.Descrizione AS DescrizionePalco,
                   ARTISTA.Nome AS NomeArtista,
                   PERFORMANCE.ID_ARTISTA AS ID_ARTISTA,
                   PERFORMANCE.Genere_musicale AS Genere,
                   PERFORMANCE.ID_PERFORMANCE AS performanceID
            FROM PERFORMANCE 
            JOIN ARTISTA ON ARTISTA.ID_ARTISTA = PERFORMANCE.ID_ARTISTA
            JOIN PALCO ON PALCO.ID_PALCO = PERFORMANCE.ID_PALCO
            WHERE PERFORMANCE.Stato = 1
            """
        ).fetchall()

        for r in rows:
            immagini_rows = db.execute(
                """
                SELECT Percorso 
                FROM PERCORSO_IMMAGINE_ARTISTA 
                WHERE ID_ARTISTA = ?
                """
                , (r["ID_ARTISTA"],)).fetchall()
            
            immagini_set = set()
            for img in immagini_rows:
                immagini_set.add(img["Percorso"])
            immagini = list(immagini_set)
            performanceList.append(
                {
                    "Giorno": r["Giorno"],
                    "Ora": r["Ora"],
                    "Durata": r["Durata"],
                    "Palco": r["ID_PALCO"],
                    "DescPalco": r["DescrizionePalco"],
                    "Descrizione": r["Descrizione"],
                    "NomeArtista": r["NomeArtista"],
                    "Genere": r["Genere"],
                    "performanceID": r["performanceID"],
                    "ImmaginiArtista": immagini
                }
            )
            
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
    
def update_performance(day, time, duration, description, state, musicType, userID, artistID, stageID, performanceID):
    db = get_db()
    try:
        db.execute(
            """
            UPDATE PERFORMANCE
            SET Giorno = ?, Ora = ?, Durata = ?, Descrizione = ?, Stato = ?, Genere_musicale = ?, ID_UTENTE = ?, ID_ARTISTA = ?, ID_PALCO = ?
            WHERE ID_PERFORMANCE = ?
            """
            ,
            (day, time, duration, description, state, musicType, userID, artistID, stageID, performanceID)
        )
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False

# Inutilizzato
def count_tickets_by_type():
    db = get_db()
    try:
        return db.execute(
            """
            SELECT Descrizione AS TipoBgilietto, COUNT(*) AS NumeroBiglietti
            FROM BIGLIETTO
            JOIN TIPO_BIGLIETTO ON TIPO_BIGLIETTO.ID_TIPO_BIGLIETTO = BIGLIETTO.ID_TIPO_BIGLIETTO
            GROUP BY BIGLIETTO.ID_TIPO_BIGLIETTO
            """
            ).fetchall()
    except Exception as e:
        print(e)
        return None
    
# Inutilizzato
def get_ticket_sales_by_day_and_type():
    db = get_db()
    try:
        return db.execute(
            """
            SELECT 
                COUNT(BIGLIETTO.ID_BIGLIETTO) AS BigliettiVenduti,
                BIGLIETTO.giorno_riferimento AS Giorno,
                TIPO_BIGLIETTO.Descrizione AS TipoBiglietto
            FROM BIGLIETTO
            JOIN TIPO_BIGLIETTO 
                ON TIPO_BIGLIETTO.ID_TIPO_BIGLIETTO = BIGLIETTO.ID_TIPO_BIGLIETTO
            GROUP BY 
                BIGLIETTO.giorno_riferimento, 
                TIPO_BIGLIETTO.ID_TIPO_BIGLIETTO
            ORDER BY 
                TIPO_BIGLIETTO.ID_TIPO_BIGLIETTO ASC, 
                BIGLIETTO.giorno_riferimento ASC;
            """
            ).fetchall()
    except Exception as e:
        print(e)
        return None