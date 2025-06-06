# Import standards
from flask import Flask, render_template, session, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import utils
import os
from werkzeug.utils import secure_filename
from models import User, Ticket, Performance
from db import close_db
from PIL import Image
import dao

# Initialize the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "PeterGriffin"
app.teardown_appcontext(close_db)

# Variabili Globali
UPLOAD_FOLDER = os.path.join("static", "images")
UPLOAD_FOLDER_PERFORMANCES = os.path.join("static", "images", "artists")
PROFILE_IMG_HEIGHT = 130
POST_IMG_WIDTH = 300
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

ruoli = ["ORGANIZZATORE", "PARTECIPANTE"]
giorniFestival = {"Venerdì":"Sabato", "Sabato":"Domenica", "Domenica":None}
idTipiBiglietti = {"Giornaliero":1, "2 Giorni":2, "Full Pass":3}
orariConsentiti = ["08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"]
durateConsentite = ["30", "60", "90", "120"]
palchiConsentiti = {"A":"Main Stage", "B":"Secondary Stage", "C":"Experimental Stage"}

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
                user = load_user(db_user["ID_UTENTE"])
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
                    user = load_user(db_user["ID_UTENTE"])
                    login_user(user)
                    return render_template("home.html")
                else:
                    flash("Errore nell'inserimento", "error")
        else:
            for error in errors:
                flash(error, "error")

    return render_template("register.html", p_ruoli = ruoli)

@app.route("/profile")
@login_required
def profile():
    if current_user.ruolo == ruoli[0]: # Organizzatore
        pp = dao.getPrivatePerformancesByUserID(current_user.id)
        publicPerformances = dao.getPublicPerformancesWithImages()
        print(publicPerformances)
        return render_template("profilo_organizzatore.html", orari = orariConsentiti, durate = durateConsentite, palchi = palchiConsentiti, performancePrivate = dao.getPrivatePerformancesByUserID(current_user.id), publicPerformances = publicPerformances)
    elif current_user.ruolo == ruoli[1]: # Partecipante
        biglietto = dao.getUserTicket(current_user.id)
        return render_template("profilo_partecipante.html", p_biglietto = biglietto, infoBiglietti = dao.getTicketPricesAndDescription())
    else:
        return render_template("home.html")

@app.route("/aggiorna_immagine", methods=["POST"])
@login_required
def aggiorna_immagine():
    file = request.files.get("file")
    if not file or file.filename == "":
        flash("Nessun file selezionato", "danger")
        return redirect(url_for("profile"))

    if utils.allowed_file(file.filename):
        filename = f"{current_user.id}_{secure_filename(file.filename)}"   # elimina o sostituisce caratteri pericolosi o non validi.
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img = Image.open(file)
        img.thumbnail((200,200))
        img.save(filepath)
        current_user.percorso_immagine = filename
        dao.updateImagePath(filename, current_user.id)
        flash("Immagine aggiornata con successo!", "success")
    else:
        flash("Formato file non supportato", "danger")
    return redirect(url_for("profile"))

@app.route("/nuova_bozza", methods=["POST"])
@login_required
def nuova_bozza():    
    azione = request.form.get("azione") # Nuova o Aggiorna

    form_data = {
        "Artista":request.form.get("nomeArtista").strip(),
        "Giorno":request.form.get("giornoInizio").strip(),
        "Ora":request.form.get("oraInizio").strip(),
        "Durata":request.form.get("durata").strip(),
        "Descrizione":request.form.get("descrizione").strip(),
        "IDpalco":request.form.get("palco").strip(),
        "Genere":request.form.get("genere").strip(),
        "Immagine":request.files.get("file"),
        "Pubblica":1 if request.form.get("bozzaPubblica") else 0
    }

    # Un artista può essere stato inserito nel db senza avere assegnata alcuna performance pubblicata
    if utils.checkIfArtistExists(dao.getArtistsList(), form_data["Artista"]):
        if dao.countArtistPublicPerformances(form_data["Artista"])["numeroPerformance"] != 0:
            flash("L'artista inserito ha già una performance pubblica assegnata", "danger")
            redirect(url_for("profile"))
    else:
        if not dao.insert_artist(form_data["Artista"].strip()):
            flash("Errore nell'inserimento dell'artista", "danger")
            redirect(url_for("profile"))
        
    # Verifica che la performance NON si sovrapponga ad altre già pubblicate sullo stesso giorno e palco
    performance = Performance(form_data["Giorno"], form_data["Ora"], form_data["Durata"], form_data["IDpalco"])
    if not utils.checkOverlappingPerformances(dao.getPublicPerformancesInGivenDay(form_data["Giorno"]), performance):       # Il controllo si fa solo sulle performance pubblicate
        if azione == "Nuova":
            if dao.insert_performance(form_data["Giorno"], form_data["Ora"], form_data["Durata"], form_data["Descrizione"], form_data["Pubblica"], form_data["Genere"], current_user.id, dao.getArtistIdByName(form_data["Artista"])["idArtista"], form_data["IDpalco"]):    # Il [0] perché il primo valore è quello che indica successo o meno dell'inserimento
                flash("Inserimento avvenuto con successo", "success")
            else:
                flash("Errore, la performance che si sta provando ad inserire si sovrappone ad una già esistente", "danger")
                redirect(url_for("profile"))
        elif azione == "Aggiorna":
            idPerformance = request.form.get("idPerformance").strip()
            if not dao.update_performance(form_data["Giorno"], form_data["Ora"], form_data["Durata"], form_data["Descrizione"], form_data["Pubblica"], form_data["Genere"], current_user.id, dao.getArtistIdByName(form_data["Artista"])["idArtista"], form_data["IDpalco"], idPerformance):
                flash("Errore nell'aggiornamento della performance", "danger")
                redirect(url_for("profile"))
        
        # Inserisco l'immagine caricata
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_PERFORMANCES
        file = form_data["Immagine"]

        if file:
            if utils.allowed_file(file.filename) and utils.isFileNameUnique(file.filename, dao.getArtistImagesAsList(dao.getArtistIdByName(form_data["Artista"])["idArtista"])):
                filename = f"{form_data['Artista']}_{secure_filename(file.filename)}"   # elimina o sostituisce caratteri pericolosi o non validi.
                if dao.insertNewArtistImageWithPath((dao.getArtistIdByName(form_data["Artista"])["idArtista"]), filename):
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    img = Image.open(file)

                    
                    
                    img.thumbnail((200,200))
                    img.save(filepath)
                    flash("Immagine aggiornata con successo!", "success")
                    flash("Aggiornamento avvenuto con successo", "success")
                else:
                    flash("Errore nell'aggiornamento immagine, file non supportato o nome dell'immagine non univoco", "danger")
            else:
                flash("Formato file non supportato", "danger")
        else:
            flash("Aggiornamento avvenuto con successo", "success")

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # Restore dell'upload folder

    return redirect(url_for("profile"))


@app.route("/acquista_biglietto", methods=["POST"])
@login_required
def acquista_biglietto():
    if(current_user.ruolo != "PARTECIPANTE"):
        flash("Non è possibile acquistare dei biglietti da organizzatore", "error")
        return render_template("home.html")

    tipo_biglietto = request.form.get("tipo_biglietto")
    prezzo = request.form.get("prezzo")
    giorno = request.form.get("giornoSelezionato")
    esaurito = False

    # Controlli sul biglietto
    if tipo_biglietto == "Giornaliero":
        esaurito = not utils.checkIfDayTicketAveilable(dao.countTicketsPerGivenDay(giorno))
    elif tipo_biglietto == "2 Giorni":
        altro_giorno = giorniFestival.get(giorno)
        esaurito = (not utils.checkIfDayTicketAveilable(dao.countTicketsPerGivenDay(giorno))
                    or not utils.checkIfDayTicketAveilable(dao.countTicketsPerGivenDay(altro_giorno)))
    else:
        for giorno_singolo in giorniFestival:
            if not utils.checkIfDayTicketAveilable(dao.countTicketsPerGivenDay(giorno_singolo)):
                esaurito = True
                break

    if esaurito:
        flash("Biglietti esauriti per uno dei giorni selezionato", "danger")
        return redirect(url_for("profile"))
    
    # Inserisco il biglietto
    id_biglietto = dao.insert_ticket(idTipiBiglietti[tipo_biglietto], giorno)

    # Lo assegno all'utente
    if not id_biglietto:
        flash("Errore durante l'acquisto del biglietto.", "danger")
        return redirect(url_for("profile"))

    successo = dao.insert_purchase(current_user.id, id_biglietto)

    if successo:
        flash("Biglietto acquistato con successo!", "success")
    else:
        flash("Errore durante l'acquisto del biglietto.", "danger")

    return redirect(url_for("profile"))

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
            percorso_immagine = db_user["percorso_immagine"]
    )
    return user