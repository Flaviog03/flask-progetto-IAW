# Import standards
from flask import Flask, render_template, session, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import utils
from models import User

import dao


# Initialize the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "PeterGriffin"

login_manager = LoginManager()
login_manager.init_app(app)

# Variabili Globali
ruoli = ["ORGANIZZATORE", "PARTECIPANTE"]


# Define a route for the homepage
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_form = request.form.to_dict()
        errors = utils.validateLoginForm(user_form)

        if not errors:
            db_user = dao.get_user_by_email(user_form["email"].strip())
            if db_user and check_password_hash(db_user["Password"], user_form["password"].strip()):
                user = User(id=db_user["ID_UTENTE"],
                password=db_user["Password"],
                email=db_user["Email"],
                nome=db_user["Nome"],
                cognome=db_user["Cognome"],
                ruolo = db_user["Ruolo"],
                )
                login_user(user)
                return render_template("home.html")
            else:
                flash("Utente non trovato o password errata", "danger")
                return render_template("login.html")
        else:
            for error in errors:
                flash(error, "error")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_form = request.form.to_dict()
        errors = utils.validateRegistrationForm(user_form)

        # Se la lista di errori è vuota
        if not errors: 
            if(dao.get_user_by_email(user_form["email"].strip())):
                app.logger.error("Utente già esistente")
                flash("Utente già esistente", "error")
                return render_template("register.html", p_ruoli = ruoli)
            else:
                if dao.insert_user(user_form["nome"], user_form["cognome"], user_form["email"], generate_password_hash(user_form["password"]), user_form["ruolo"]):
                    flash("Inserimento avvenuto con successo", "success")
                    db_user = dao.get_user_by_email(user_form["email"])
                    user = User(
                        id=db_user["ID_UTENTE"],
                        password=db_user["Password"],
                        email=db_user["Email"],
                        nome=db_user["Nome"],
                        cognome=db_user["Cognome"],
                        ruolo=db_user["Ruolo"],
                    )
                    login_user(user)
                    return render_template("home.html")
                else:
                    flash("Errore nell'inserimento", "error")
        else:
            for error in errors:
                flash(error, "error")

    return render_template("register.html", p_ruoli = ruoli)

# Routine per il logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

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