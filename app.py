# Import standards
from flask import Flask, render_template, session
from db import get_db, close_db

# Es:
# sql = "SELECT * FROM PERSONE WHERE nome = (?)"
# cursor.execute(sql, ("Gianni", )) # si mette sempre la ',' per far riconoscere che è una tupla -> trailing

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the homepage
@app.route("/")
def home():
    utente = None
    if session.get("utente_id"):
        db = get_db()
        utente = db.execute("SELECT * FROM utente WHERE id = ?", (session["utente_id"],)).fetchone()
    return render_template("home.html", utente = utente)

@app.route("/login", methods=["GET", "POST"])
def login():
    db = get_db()
    cursor = db.cursor()
    # Qui va la logica di login (form, autenticazione, ecc.)
    sql = ""
    cursor.close()
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    db = get_db()
    cursor = db.cursor()
    # Qui va la logica di registrazione (form, salvataggio utente, ecc.)
    cursor.close()
    return render_template("register.html")

# Questa funzione viene eseguita automaticamente da Flask alla fine di ogni richiesta HTTP,
# sia che la richiesta sia andata a buon fine sia che abbia generato un errore.
# Serve per chiudere la connessione al database associata alla richiesta corrente,
# liberando risorse e prevenendo eventuali perdite di memoria.
# Non deve essere chiamata manualmente nelle route: Flask la gestisce in automatico.
@app.teardown_appcontext
def teardown_db(exception):
     close_db()