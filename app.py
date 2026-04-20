# will add content here once tested and works fine
import streamlit as st

st.title("Second Brain- note taker and task manager")
st.write("A smart note-taking and task-manager app that doesn't just store text, but categorizes, summarizes, and searches your data using AI.")

# complex app, lets speed the development by taking simple steps

# lets make a simple note taking feature.

mode = st.selectbox("Select mode", ["Take a note"]) # ADD MORE MODES HERE LATER

if mode == "Take a note":
    note = st.text_area("Enter your note here:", height=300)
    if st.button("Save Note"):
        # Here I would send it to support and save it in a db.
        if note.strip() != "":
            # save_note_to_db(note) # This is a placeholder for the actual function that would save the note to a database.
            st.success("Note saved successfully!")
        else:
            st.warning("Please enter a note before saving.")
