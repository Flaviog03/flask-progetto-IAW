import re   # Modulo per le regex
from datetime import datetime, timedelta

ALLOWED_EXTENSIONS = {'jpg'}
MAX_BIGLIETTI_PER_GIORNO = 200

class InputError:
    NOME_OBBLIGATORIO = "nome_obbligatorio"
    COGNOME_OBBLIGATORIO = "cognome_obbligatorio"
    EMAIL_NON_VALIDA = "email_non_valida"
    PASSWORD_NON_VALIDA = "password_non_valida"
    RUOLO_OBBLIGATORIO = "ruolo_obbligatorio"

def validateRegistrationForm(form):
    errors = []

    nome = form.get("nome", "").strip()
    if not nome:
        errors.append(InputError.NOME_OBBLIGATORIO)

    cognome = form.get("cognome", "").strip()
    if not cognome:
        errors.append(InputError.COGNOME_OBBLIGATORIO)

    email = form.get("email", "").strip()
    email_pattern = r"^[A-Za-z0-9]+@[A-Za-z0-9]+\.\w+$"
    if not email or not re.match(email_pattern, email):
        errors.append(InputError.EMAIL_NON_VALIDA)

    password = form.get("password", "")
    password_pattern = r"^[A-Za-z0-9]{8,20}$"
    if not password or not re.match(password_pattern, password):
        errors.append(InputError.PASSWORD_NON_VALIDA)

    ruolo = form.get("ruolo", "").strip()
    if ruolo not in ["ORGANIZZATORE", "PARTECIPANTE"]:
        errors.append(InputError.RUOLO_OBBLIGATORIO)

    return errors

def validateLoginForm(form):
    errors = []

    email = form.get("email", "").strip()
    email_pattern = r"^[A-Za-z0-9]+@[A-Za-z0-9]+\.\w+$"
    if not email or not re.match(email_pattern, email):
        errors.append(InputError.EMAIL_NON_VALIDA)

    password = form.get("password", "")
    password_pattern = r"^[A-Za-z0-9]{8,20}$"
    if not password or not re.match(password_pattern, password):
        errors.append(InputError.PASSWORD_NON_VALIDA)
    return errors

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checkIfDayTicketAveilable(row):
    if row["numeroBiglietti"] < MAX_BIGLIETTI_PER_GIORNO:
        return True
    return False

def checkIfArtistExists(artistsList, artistName):
    if artistName in artistsList:
        return True
    return False

# Metodo visibile solo all'interno di utils
def __evaluatePerformanceEndTime(oraInizio, durata):
    # 1. Converti ora_inizio in oggetto datetime (senza data)
    inizio = datetime.strptime(oraInizio, "%H:%M")

    # 2. Aggiungi la durata come timedelta
    fine = inizio + timedelta(minutes=int(durata))

    # 3. Converti l'orario finale di nuovo in stringa
    ora_fine = fine.strftime("%H:%M")

    return ora_fine

def __durationOverlapping(t1_i, t1_f, t2_i, t2_f):
    if t1_i < t2_f and t2_i < t1_f:
        return True
    return False

# Controllo su Giorno, Ora, Durata, Palco
def checkOverlappingPerformances(performancesList, performance):
    for p in performancesList:
        if p["Giorno"] == performance.giorno:
            if p["Palco"] == performance.palco:
                if __durationOverlapping(p["Ora"], __evaluatePerformanceEndTime(p["Ora"], p["Durata"]), performance.ora, __evaluatePerformanceEndTime(performance.ora, performance.durata)):
                    return True
    return False