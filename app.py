# will add content here once tested and works fine
import streamlit as st
from support import init_db, save_note_to_db, get_all_notes, confirm_dialog, get_note_by_id, update_note

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

mode = st.selectbox("Select mode", ["Take a note", "View notes", "Edit note"]) # ADD MORE MODES HERE LATER
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

    st.write("Click delete to remove a note. Click edit to modify it.")

    if notes:
        for note in notes:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**[{note[5]}]** {note[4]}")
                st.caption(f"Due: {note[2] or 'N/A'} | Category: {note[3] or 'N/A'} | ID: {note[0]}")
            with col2:
                if st.button("✏️ Edit", key=f"edit_{note[0]}"):
                    st.session_state.edit_note_id = note[0]
                    st.rerun()
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{note[0]}"):
                    confirm_dialog(note[0])
                    st.rerun()
            st.markdown("---")
        if st.checkbox("Show raw data"):
            st.write(notes)
    else:
        st.write("No notes found.")

if mode == "Edit note":
    notes = get_all_notes()
    if not notes:
        st.warning("No notes available to edit.")
    else:
        # Create a list of note summaries for selection
        note_options = {f"[ID: {note[0]}] {note[4][:50]}..." if len(note[4]) > 50 else f"[ID: {note[0]}] {note[4]}": note[0] for note in notes}
        
        selected_note_display = st.selectbox("Select a note to edit:", list(note_options.keys()))
        selected_note_id = note_options[selected_note_display]
        
        # Get the full note details
        note = get_note_by_id(selected_note_id)
        
        if note:
            st.subheader(f"Editing Note ID: {note[0]}")
            
            # Create editable fields
            col1, col2 = st.columns(2)
            
            with col1:
                priority = st.number_input(
                    "Priority (1-5):",
                    min_value=1,
                    max_value=5,
                    value=note[5] if note[5] else 3,
                    key="priority_input"
                )
                due_date = st.text_input(
                    "Due Date (YYYY-MM-DD):",
                    value=note[2] if note[2] else "",
                    key="due_date_input"
                )
            
            with col2:
                category = st.text_input(
                    "Category:",
                    value=note[3] if note[3] else "",
                    key="category_input"
                )
                summary = st.text_input(
                    "Summary:",
                    value=note[4] if note[4] else "",
                    key="summary_input"
                )
            
            content = st.text_area(
                "Content:",
                value=note[1] if note[1] else "",
                height=300,
                key="content_input"
            )
            
            col_save, col_cancel = st.columns(2)
            
            with col_save:
                if st.button("💾 Save Changes"):
                    if content.strip():
                        update_note(selected_note_id, content, due_date if due_date else None, category if category else None, summary if summary else None, priority)
                        st.success("Note updated successfully!")
                        st.rerun()
                    else:
                        st.warning("Content cannot be empty!")
            
            with col_cancel:
                if st.button("Cancel"):
                    st.rerun()

