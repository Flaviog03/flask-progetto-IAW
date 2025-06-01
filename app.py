# Import standards
from flask import Flask, render_template, session, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import get_db, close_db
from models import User
import dao

# Es:
# sql = "SELECT * FROM PERSONE WHERE nome = (?)"
# cursor.execute(sql, ("Gianni", )) # si mette sempre la ',' per far riconoscere che è una tupla -> trailing

# Initialize the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "PeterGriffin"

login_manager = LoginManager()
login_manager.init_app(app)


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
    if request.method == "POST":
        user_form = request.form.to_dict()
        db_user = dao.get_user_by_email(user_form["email"].strip())

        if db_user and db_user["Password"] == user_form["password"].strip():
            user = User(id=db_user["ID_UTENTE"],
            password=db_user["Password"],
            email=db_user["Email"],
            nome=db_user["Nome"],
            cognome=db_user["Cognome"],
            ruolo = db_user["Ruolo"],
            )
            login_user(user)
            return render_template("home.html", utente = user)
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    db = get_db()
    cursor = db.cursor()
    # Qui va la logica di registrazione (form, salvataggio utente, ecc.)
    cursor.close()
    return render_template("register.html")

# Routine per il logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# Questa funzione viene eseguita automaticamente da Flask alla fine di ogni richiesta HTTP,
# sia che la richiesta sia andata a buon fine sia che abbia generato un errore.
# Serve per chiudere la connessione al database associata alla richiesta corrente,
# liberando risorse e prevenendo eventuali perdite di memoria.
# Non deve essere chiamata manualmente nelle route: Flask la gestisce in automatico.
@app.teardown_appcontext
def teardown_db(exception):
     close_db()

@login_manager.user_loader
def load_user(user_id):
    db_user = dao.get_user_by_id(user_id)
    user = User(id=db_user["ID_UTENTE"],
            password=db_user["Password"],
            email=db_user["Email"],
            nome=db_user["Nome"],
            cognome=db_user["Cognome"],
            ruolo = db_user["Ruolo"],
    )
    return user