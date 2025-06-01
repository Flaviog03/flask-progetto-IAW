import re   # Modulo per le regex

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