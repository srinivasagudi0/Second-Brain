# all the supporting funcrtions stay here

import sqlite3
from openai import OpenAI

db = "notes.db"

# we will be creating multiple dbs, so it is easy; this note db will be used for storing notes, we can have another db for tasks, and so on. This way we can keep things organized and modular.
def init_db():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              content TEXT,
              due_date TEXT,
              category TEXT,
              summary TEXT,
              priority INTEGER
              )''')
    conn.commit()
    conn.close()

def get_gpt_response(prompt):
    import os

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = """
You are a helpful assistant that helps users manage notes, tasks, and other information.
Return ONLY strict JSON with this exact structure and valid JSON syntax:
{
  "content": "exact content of the note, without extra formatting",
  "due_date": "YYYY-MM-DD or null",
  "category": "category name or null",
  "summary": "brief summary of the note",
  "priority": 1
}
Rules:
- Output JSON only. No markdown, no explanations.
- "priority" must be an integer 1 to 5, or null.
- If unknown, use null.
-  the summary should be a concise one-line TODO summary, ideally starting with a verb (e.g. "Buy groceries", "Call Alice", "Finish report").
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt + "Today's date and time is: " + __import__("datetime").datetime.now().isoformat()},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f'{{"error":"{str(e)}"}}'

# Backwards-compatible alias (common misspelling in app code / imports).
def get_gpt_ressponse(prompt):
    return get_gpt_response(prompt)

def save_note_to_db(note):
    import json

    content = None
    due_date = None
    category = None
    summary = None
    priority = None
    original_text = None

    # Accept a dict-like note, a JSON string from GPT, or raw freeform text.
    if isinstance(note, dict):
        parsed = note
    elif isinstance(note, str):
        note_str = note.strip()
        original_text = note_str
        parsed = None
        if note_str.startswith("{") and note_str.endswith("}"):
            try:
                parsed = json.loads(note_str)
            except Exception:
                parsed = None

        # If it's not valid JSON, enrich it via GPT (best-effort).
        if parsed is None and note_str:
            try:
                parsed = json.loads(get_gpt_ressponse(note_str))
            except Exception:
                parsed = None

        if parsed is None:
            parsed = {"content": note_str}
    else:
        original_text = str(note)
        parsed = {"content": original_text}

    content = parsed.get("content")
    due_date = parsed.get("due_date")
    category = parsed.get("category")
    summary = parsed.get("summary")
    priority = parsed.get("priority")

    # If GPT failed (e.g. {"error": ...}) or content is missing, fall back to the original text.
    if not content and original_text:
        content = original_text

    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(
        "INSERT INTO notes (content, due_date, category, summary, priority) VALUES (?, ?, ?, ?, ?)",
        (content, due_date, category, summary, priority),
    )
    conn.commit()
    conn.close()

def get_all_notes():
   # update to get stuff from the new db structure
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT id, content, due_date, category, summary, priority FROM notes")
    notes = c.fetchall()
    conn.close()
    return notes

# delete th note by id
def delete_note(note_id):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

# add a safety check before deleting all notes, this is a dangerous operation, so we need to make sure that the user really wants to do it.
def confirm_del(note_id):
    import streamlit as st

    if st.checkbox("I understand that this will delete the note."):
        if st.button("Delete Note"):
            delete_note(note_id)
            st.success("Note has been deleted.")
            
