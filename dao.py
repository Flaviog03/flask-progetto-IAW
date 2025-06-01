from db import get_db

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
            (password, email, nome, cognome, ruolo)
        )
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
