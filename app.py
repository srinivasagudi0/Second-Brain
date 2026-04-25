# will add content here once tested and works fine
from datetime import datetime
import time

import streamlit as st
from support import init_db, save_note_to_db, get_all_notes, confirm_dialog, edit_note, init_del_notes_db, add_to_deleted_notes, get_all_deleted_notes, delete_all_notes_delnotes, group_notes_by_due_status

st.set_page_config(page_title="Second Brain", page_icon="🧠", layout="wide")

# before the app even starts we need to check if openai key is set, if not we will show a warning and exit the app.
import os
if "OPENAI_API_KEY" not in os.environ:
    st.warning("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable to use this app.")
    st.stop()

st.title("Second Brain- note taker and task manager")
st.write("A smart note-taking and task-manager app that doesn't just store text, but categorizes, summarizes, and searches your data using AI.")

if "app_ready" not in st.session_state:
    st.session_state.app_ready = False

if not st.session_state.app_ready:
    st.write("loading stuff first, wait a sec")
    with st.spinner("getting things ready..."):
        init_db()
        init_del_notes_db()
        time.sleep(2)
        st.session_state.app_ready = True
    st.rerun()

init_db()
init_del_notes_db()

# complex app, lets speed the development by taking simple steps

# lets make a simple note taking feature.

st.sidebar.title("Navigation")

mode = st.sidebar.selectbox("Select mode", ["TODAY","Take a note", "View notes", "Completed Tasks"]) # ADD MORE MODES HERE LATER
# dumb i fogot

if mode == "Take a note":
    note = st.text_area("Enter your note here:", height=300)
    # Button logic with loading state
    if "loading" not in st.session_state: st.session_state.loading=False
    if st.button("Save Note", disabled=st.session_state.loading):
        if note.strip() != "":
            st.session_state.loading=True
            with st.spinner("organizing your second brain..."):
                time.sleep(1.2)
                save_note_to_db(note)
            st.session_state.loading=False
            st.success("Note saved successfully!")
        else:
            st.warning("Please enter a note before saving.")

if mode == "View notes":
    notes = get_all_notes()
    grouped_notes = group_notes_by_due_status(notes)
    # writing filtering and searching features here now, this is going to be a bit tricky but i did this type of features before so I am pretty sure I can do it again, I will start with a simple search feature and then move on to more complex filtering features.
    index=[]

    for note in notes:
        index.append(note[1])

    # search and everything related to it is here 🔍

    corner, left, middle,right = st.columns([1, 2, 2, 1])
    with corner:
        st.slider('Priority Filter', min_value=1, max_value=5, value=3, key='priority_filter')
    with left:
        search_query = st.selectbox("Search notes by summary", options=[""] + index) 
    with middle:
        due_date_filter = st.date_input("Filter by due date (optional)", value=None)
    with right:
        category_filter = st.text_input("category (optional)")
    
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
    

    #cooldown for easier brain processing
        st.markdown("---")

### now make it editable, flexible.
    if notes:
        if grouped_notes["overdue"]:
            st.write("Overdue")
            for note in grouped_notes["overdue"]:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    if st.checkbox(f"- [{note[5]}] {note[4]} (Due: {note[2]}, Cat: {note[3]}, ID: {note[0]})", key=f"check_{note[0]}"):
                        # add this task to a completed taks db using support.py finction(namee TBD)
                        add_to_deleted_notes(note[1], note[2], note[3], note[4], note[5])
                        # delete_note so it wont be visibel
                        confirm_dialog(note[0])
                        
                        st.success("Task marked as completed and moved to completed tasks!")

                with col2:
                    if st.button("Edit", key=f"edit_{note[0]}"):
                        edit_note(note[0])
                with col3:
                    if st.button("Delete", key=f"delete_{note[0]}"):
                        confirm_dialog(note[0])
                st.markdown("---")

        if grouped_notes["due_soon"]:
            st.write("Due Soon (Next 7 Days)")
            for note in grouped_notes["due_soon"]:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    if st.checkbox(f"- [{note[5]}] {note[4]} (Due: {note[2]}, Cat: {note[3]}, ID: {note[0]})", key=f"check_{note[0]}"):
                        # add this task to a completed taks db using support.py finction(namee TBD)
                        add_to_deleted_notes(note[1], note[2], note[3], note[4], note[5])
                        # delete_note so it wont be visibel
                        confirm_dialog(note[0])
                        
                        st.success("Task marked as completed and moved to completed tasks!")

                with col2:
                    if st.button("Edit", key=f"edit_{note[0]}"):
                        edit_note(note[0])
                with col3:
                    if st.button("Delete", key=f"delete_{note[0]}"):
                        confirm_dialog(note[0])
                st.markdown("---")

        if grouped_notes["other"]:
            st.write("All Other Notes")
            for note in grouped_notes["other"]:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    if st.checkbox(f"- [{note[5]}] {note[4]} (Due: {note[2]}, Cat: {note[3]}, ID: {note[0]})", key=f"check_{note[0]}"):
                        # add this task to a completed taks db using support.py finction(namee TBD)
                        add_to_deleted_notes(note[1], note[2], note[3], note[4], note[5])
                        # delete_note so it wont be visibel
                        confirm_dialog(note[0])
                        
                        st.success("Task marked as completed and moved to completed tasks!")

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

# new mode aftr a long time
if mode == "Completed Tasks":
    #st.write("This is where completed tasks will be shown. This feature is still under development, but it will be available soon. Stay tuned!")
    # use support.py to help retrive all the tasks from the completed tasks db and show them here, maybe add a feature to delete them and then move them back to notes if they are not completed by mistake.
    completed_tasks = get_all_deleted_notes()
    left, right = st.columns([4, 5])

    with left:
        # maybe addd retricval over here
        pass
    
    with right:

        if st.button("Clear Completed Tasks"):
            # add a safety check before deleting all notes, this is a dangerous operation, so we need to make sure that the user really wants to do it.
            
            delete_all_notes_delnotes()
            st.success("All completed tasks have been cleared.")
            st.rerun()

    if completed_tasks:
        for task in completed_tasks:
            st.write(f"- [{task[5]}] {task[4]} (Due: {task[2]}, Cat: {task[3]}, ID: {task[0]})")
    #Added duesoon and overdue 
### mode = TODAY
if mode == "TODAY":
    #THIS one will show if there any tasks due and has like a dev dashboard vibe, maybe add some fixed widgets, this is going to be like a quick overview of what needs to be done 
    today_view = st.selectbox("Select view", ["Select Mode", 'Today', "Assistant"]) # Not going to complicate this.
    # Overdue will be shown in red and will be at the top no matter what the mode is
    #fetch overdue
    notes = get_all_notes()
    grouped_notes = group_notes_by_due_status(notes)
    if grouped_notes["overdue"]:
        st.write("Overdue Tasks")
        for note in grouped_notes["overdue"]:
            st.error(f"- [{note[5]}] {note[4]} (Due: {note[2]}, Cat: {note[3]}, ID: {note[0]})")
        st.markdown("---")
    
    
    # why not make assistant feature like an achievement, it should be allowed only if the user has atleast 2 notes, this will encourage the user to use the app more and then they can unlock the assistant feature which will help them with summarization, categorization and all that good stuff, this is going to be a fun feature to implement and use, Also reduces random bla-bla-bla chat.
    if today_view == "Today":
        # todays task and that stuff
        notes = get_all_notes()
        grouped_notes = group_notes_by_due_status(notes)
        today=datetime.now().date()
        # took a lot of time time just to think about htis line
        todays_tasks = [
            note for note in grouped_notes["due_soon"]
            if note[2] and datetime.strptime(note[2], "%Y-%m-%d").date() == today
        ]

        st.write("Today's tasks")

        if todays_tasks:
            for note in todays_tasks:
                st.write(f"- [{note[5]}] {note[4]} (Due: {note[2]}, Cat: {note[3]}, ID: {note[0]})")
        else:
            st.write("No tasks due today.")
    if today_view == "Assistant":
        # this is chatbot 
        notes = get_all_notes()
        if len(notes) < 2:
            st.warning("Not so Fast, you need to have at least 2 notes to unlock the assistant feature. Please add more notes to use this feature.")
        else:
            left, right = st.columns([4, 1])

            with left:
                st.text_input("Ask about your notes or tasks", placeholder="e.g. What are my overdue tasks? or Summarize my notes for me", key="assistant_input")
                response_box = st.empty()
                if "assistant_answer" not in st.session_state: st.session_state.assistant_answer=""

            with right:
                # leveling it 
                st.write(" ")
                st.write(" ")
                if st.button("Ask Assistant", key="ask_assistant"):
                    st.write("Assistant is thinking...")
                    # add a spinner while the assistant is thinking.
                    with st.spinner("Assistant is thinking..."):
                        time.sleep(2)
                        # add a function in support.py that takes the user input and the notes and then returns the answer, this function will use openai api to get the answer, this is going to be a fun feature to implement and use, also reduces random bla-bla-bla chat.
                        from support import ask_assistant
                        st.session_state.assistant_answer = ask_assistant(st.session_state.assistant_input, notes)

                if st.session_state.assistant_answer:
                    st.write("Assistant says:")
                    # the response is all the way at the end of the screen, how to 
                    #st.empty() though this would work, guess why i commented  it out!.
                    response_box.write(st.session_state.assistant_answer)

    # thought of making buttons but that is harder so sticking to the selectbox as it is easier to implement and will do the job for now, maybe add buttons later if I have time.
        
