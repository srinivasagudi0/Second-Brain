# will add content here once tested and works fine
import streamlit as st
from support import init_db, save_note_to_db, get_all_notes, delete_note

# before the app even starts we need to check if openai key is set, if not we will show a warning and exit the app.
import os
if "OPENAI_API_KEY" not in os.environ:
    st.warning("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable to use this app.")
    st.stop()

st.title("Second Brain- note taker and task manager")
st.write("A smart note-taking and task-manager app that doesn't just store text, but categorizes, summarizes, and searches your data using AI.")

init_db()

# complex app, lets speed the development by taking simple steps

# lets make a simple note taking feature.

mode = st.selectbox("Select mode", ["Take a note", "View notes"]) # ADD MORE MODES HERE LATER
# dumb i fogot
if mode == "Take a note":
    note = st.text_area("Enter your note here:", height=300)
    if st.button("Save Note"):
        # Here I would send it to support and save it in a db.
        if note.strip() != "":
            # here I will call later call AI to summarize, categorize and many more things, but for now lets just save it in a db.
            save_note_to_db(note)
            st.success("Note saved successfully!")
        else:
            st.warning("Please enter a note before saving.")

if mode == "View notes":
    notes = get_all_notes()
    if notes:
        for note in notes:
            if st.checkbox(f"- [{note[5]}] {note[4]} (Due: {note[2]}, Cat: {note[3]}, ID: {note[0]})"):
                delete_note(note[0])
                st.rerun()  # Refresh the page to update the notes list after deletion
                st.snow()
            st.markdown("---")
        if st.checkbox("Show raw data"):
            st.write(notes)
        


    else:
        st.write("No notes found.")
