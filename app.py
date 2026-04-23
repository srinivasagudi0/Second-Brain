# will add content here once tested and works fine
from datetime import datetime

import streamlit as st
from support import init_db, save_note_to_db, get_all_notes, confirm_dialog, edit_note


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
    # writing filtering and searching features here now, this is going to be a bit tricky but i did this type of features before so I am pretty sure I can do it again, I will start with a simple search feature and then move on to more complex filtering features.
    index=[]

    for note in notes:
        index.append(note[1])

    # search and everything related to it is here 🔍

    corner, left, middle,right, rightcorner = st.columns([1, 2, 2, 1, 1])
    with corner:
        st.slider('Priority Filter', min_value=1, max_value=5, value=3, key='priority_filter')
    with left:
        search_query = st.selectbox("Search notes by summary", options=[""] + index) 
    with middle:
        due_date_filter = st.date_input("Filter by due date (optional)", value=None)
    with right:
        category_filter = st.text_input("category (optional)")
    with rightcorner:
        if st.button("Apply Filters"):
            filtered_notes = notes
            if search_query:
                filtered_notes = [note for note in filtered_notes if search_query.lower() in note[1].lower()]
            if due_date_filter:
                filtered_notes = [note for note in filtered_notes if note[2] and datetime.strptime(note[2], "%Y-%m-%d").date() == due_date_filter]
            if category_filter:
                filtered_notes = [note for note in filtered_notes if note[3] and category_filter.lower() in note[3].lower()]
            st.write("Filtered results:")
            if filtered_notes:
                for note in filtered_notes:
                    st.caption(f'**{note[4]} is due on {note[2]} and is in category {note[3]} with a priority of {note[5]}**')
            else:
                st.write("No notes found matching the filters.")
    

    #search_query = st.selectbox("Search notes by summary", options=[""] + index) 
    '''
    if search_query:
        filtered_notes = [note for note in notes if search_query.lower() in note[1].lower()]
        st.write("Search results:")
        if filtered_notes:
            st.caption(f'**{note[4]} is due on {note[2]} and is in category {note[3]} with a priority of {note[5]}**')

    st.write("Your notes:")
    ''' 

### now make it editable, flexible.
    if notes:
        for note in notes:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"- [{note[5]}] {note[4]} (Due: {note[2]}, Cat: {note[3]}, ID: {note[0]})")
            with col2:
                if st.button("Edit", key=f"edit_{note[0]}"):
                    edit_note(note[0])
            with col3:
                if st.button("Delete", key=f"delete_{note[0]}"):
                    confirm_dialog(note[0])
            st.markdown("---")
        if st.checkbox("Show raw data"):
            st.write(notes)
    else:
        st.write("No notes found.")

