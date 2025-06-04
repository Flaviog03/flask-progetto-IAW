import sqlite3
from flask import g

DATABASE = "SoundWaves_TP_DB.db"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # così ogni riga si comporta come un dizionario
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()