from flask_login import UserMixin, LoginManager
import dao

class User(UserMixin):
    def __init__(self, id, password, email, nome, cognome, ruolo, percorso_immagine):
        self.id = id
        self.password = password
        self.email = email
        self.nome = nome
        self.cognome = cognome
        self.ruolo = ruolo
        self.percorso_immagine = percorso_immagine
        