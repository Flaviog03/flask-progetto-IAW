# Import standards
from flask import Flask, render_template, session
import sqlite3 as sq3

# Database connection (conn.Commit, conn.Close, conn.cursor())
conn = sq3.connect("SoundWaves_TP_DB.db") # Se "db_name" non è un file .sql verrà creato da SQLite
cursor = conn.cursor()	# anche il cursore va chiuso

# Es:
# sql = "SELECT * FROM PERSONE WHERE nome = (?)"
# cursor.execute(sql, ("Gianni", )) # si mette sempre la ',' per far riconoscere che è una tupla -> trailing

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the homepage
@app.route("/")
def home():
	utente = None
	# Sessione non ancora implementata
	return render_template("home.html", utente = utente)

cursor.close()
conn.close()