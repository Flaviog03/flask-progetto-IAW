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

class Ticket():
    def __init__(self, id, id_tipoBiglietto, giorno_riferimento):
        self.id = id
        self.id_tipoBiglietto = id_tipoBiglietto
        self.giorno_riferimento = giorno_riferimento
        
class Performance():
    def __init__(self, giorno, ora, durata, palco):
        self.giorno = giorno
        self.ora = ora
        self.durata = durata
        self.palco = palco