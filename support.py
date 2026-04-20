# all the supporting funcrtions stay here

import sqlite3
from openai import OpenAI

db = "notes.db"

# we will be creating multiple dbs, so it is easy; this note db will be used for storing notes, we can have another db for tasks, and so on. This way we can keep things organized and modular.
def init_db():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)''')
    conn.commit()
    conn.close()

def save_note_to_db(note):
    # will soon add so 

    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO notes (content) VALUES (?)", (note,))
    conn.commit()
    conn.close()

def get_all_notes():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return notes