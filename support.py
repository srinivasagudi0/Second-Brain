# all the supporting funcrtions stay here

import sqlite3
from openai import OpenAI
import streamlit as st


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
@st.dialog("Confirm Action")
def confirm_dialog(note_id):
    st.write(f"Are you sure you want to delete the note?")
    
    if st.button("Yes"):
        # Save data to session state if needed outside the dialog
        st.session_state.deleted_item = note_id
        # Use st.rerun() to close the dialog and refresh the app
        delete_note(note_id)
        st.rerun()
    if st.button("No"):
        st.rerun()

# edit feature is currently not implemented yet, so this one will work as a edit function
@st.dialog("Edit Note")
def edit_note(note_id):
    import streamlit as st


    #for now will only be able to edit the content, we will get over this soon, we are getting somewhere
    # working to able to edi the category, due date and priority now.
    #with st.dialog("Edit Note"):
    st.write(f"Edit the note with id: {note_id}")

    # shoudl be good now since I took of the note
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT summary, due_date, category, priority FROM notes WHERE id=?", (note_id,))
    note = c.fetchone()
    conn.close()

    # should be patched and maybe perfect for now, if this works we can scale it by a lot.

    if note:
        new_summary = st.text_area("Note summary", value=note[0])
        

        new_due_date = st.date_input("Due date", value=note[1] if note[1] else None)
        new_cat = st.text_input("Category", value=note[2] or "")
        new_priority = st.slider("Priority", min_value=1, max_value=5, value=note[3] if note[3] is not None else 0)

        if st.button("Save"):
            conn = sqlite3.connect(db)
            c = conn.cursor()
            # changed it from content to summary.
            c.execute("UPDATE notes SET summary=?,due_date=?, category=?, priority=? WHERE id=?", (new_summary, new_due_date, new_cat, new_priority, note_id))
            conn.commit()
            conn.close()
            st.rerun()
            st.success("Note updated successfully!")
    
