# Second Brain

**AI-powered note taker + task manager**  
Type chaos. Get structured tasks.

Second Brain turns messy notes into organized task entries with:

- **Summary**
- **Due date**
- **Category**
- **Priority**
- **Type**
- **Tags**

Built for people with too much on their plate.

---

## Tech Stack

- Python  
- Streamlit  
- SQLite  
- OpenAI API  

> SQLite = simple local storage that minds its own business.

---

## Features

- Add messy notes  
- AI organizes them  
- Save tasks to SQLite  
- View:
  - Overdue tasks
  - Due soon
  - Due today
- Completed tasks page  
- Edit, delete, restore tasks  
- Ask an assistant about your notes  
- Quick stats dashboard  

---

## Pages

## TODAY

Dashboard includes:

- Overdue tasks  
- Today's tasks  
- Stats  
- Assistant  

---

## Take a Note

Type something messy like:

```text
finish math homework tomorrow priority high
```

AI cleans it up into structured tasks.

---

## View Notes

Tasks are grouped into:

- Overdue  
- Due Soon  
- Everything Else  

Actions available:

- Edit  
- Delete  
- Complete  

---

## Completed Tasks

See finished items.

Accidentally marked something complete?

You can restore it if you clicked too confidently.

---

## Struggles I Faced

While building this project, I faced a few challenges that took time to fix. I added more features than planned at first (like Today view, stats, assistant, UI changes), which caused me to go back and change things multiple times. Handling Streamlit state and reruns was tricky, especially with buttons, dialogs, and switching views. I also spent time fixing CRUD logic (edit, delete, update), where small mistakes caused bugs. There were many small errors during development, so I had to debug and test a lot to make the app stable. Setting up the database and saving/loading data also needed some work. I also worked on making the AI features more reliable (API key, response handling, fallbacks). In the end, most of my time went into debugging, fixing issues, and improving the app rather than just adding features. Hope you understand!

---

## Important

⚠️ Requires an `OPENAI_API_KEY` or the app will not run.
