# Second-Brain
A smart note-taking and task-manager app that doesn't just store text, but categorizes, summarizes, and searches your data using AI. Also works best in CLI(you get an api) and UI(try my Streamlit app).



# Trying to Achieve

The Project: "The AI-Powered Second Brain"
Build a smart note-taking and task-manager app that doesn't just store text, but categorizes, summarizes, and searches your data using AI.

1. The Stack (All Free except openai)
Frontend: Streamlit.

Logic: Python.

Database: SQLite (for local dev)

Note: Since SQLite disappears on Streamlit Cloud

AI API: Google Gemini 2.5 Flash (via Google AI Studio).

Cost: $0 (up to 500 requests/day).

Why: It can summarize your notes, extract "To-Do" items from a long paragraph of text, and even "chat" with your database.

2. Features to Build
Smart Entry: You type a messy note like "Need to buy milk, also don't forget the meeting with Sarah at 4 PM to discuss the API project."

AI Processing: The Python backend sends this to Gemini. Gemini returns a JSON object:

task: "Buy milk"

meeting: "Meeting with Sarah, 4 PM"

topic: "API Project"

Database Integration: Your app automatically saves these into your tasks and notes tables.

Auth Integration: Use Streamlit Authenticator (a simple library) to create a login page so your "Brain" stays private.

3. How to keep the DB "Permanent"
If you really want to stick to SQLite, you can use a clever trick: GitHub Persistence.

Your app runs on Streamlit.

When a user saves data, the app updates the database.db file.

You use the GitPython library to automatically commit and push that .db file back to your private GitHub repo.

Cost: $0. Permanence: Infinite.
