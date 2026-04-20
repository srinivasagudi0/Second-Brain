# will add content here once tested and works fine
import streamlit as st

st.title("Second Brain- note taker and task manager")
st.write("A smart note-taking and task-manager app that doesn't just store text, but categorizes, summarizes, and searches your data using AI.")

# complex app, lets speed the development by taking simple steps

# lets make a simple note taking feature.

if st.button("Take a note"):
    note = st.text_area("Enter your note here:", height=300)
    if st.button("Save note"):
        st.write("Note saved:", note)
