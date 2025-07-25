# Mind Garden

Mind Garden is a desktop mental wellness application built with Python and Tkinter. It helps users track their moods, journal their thoughts, manage reminders via a calendar, organize tasks in a to-do list, and write notes—all in one simple, lightweight app.

---

## Features

- **Mood Logging:** Rate your mood daily on a scale of 1 to 5 and keep a log for self-reflection.
- **Journal:** Write and save daily journal entries with optional tags. Easily view and edit past entries.
- **Calendar & Reminders:** Manage reminders by date with customizable importance levels. Link calendar dates to journal entries.
- **Notepad:** Simple text editor for notes with file operations (New, Open, Save, Save As).
- **To-Do List:** Create, categorize, and track tasks with optional due dates and times. Mark tasks as done or delete them.

---

## Tech Stack

- Python 3  
- Tkinter (for GUI)  
- JSON (for task storage)  
- Standard Python libraries (datetime, os, json)

---

## Installation & Setup

1. Ensure you have Python 3 installed on your system.  
2. Clone or download this repository.  
3. Run the `main.py` file to launch the app:

   ```bash
   python main.py

Usage
Upon launching, the main window lets you log your mood by clicking 1-5.

Use the buttons to open your journal, calendar/reminder system, notepad, or to-do list.

Your mood logs are saved in a text file (mood_log.txt) and can be refreshed to view.

Journal entries are saved daily as text files with optional tags.

The calendar interface allows adding, editing, and deleting reminders by date.

The notepad provides basic text editing with file save/load support.

The to-do list supports adding tasks with categories, due dates, marking completion, and deletion.

Project Structure
bash

MindGarden/\
│\
├── main.py # Main application launcher with mood logging and navigation\
├── journal.py # Journal entry windows, saving, and tag management\
├── calendar_window.py # Calendar GUI, reminders management linked with journal\
├── notepad.py # Simple text editor with file operations\
├── todo_list.py # To-Do list UI, task management with JSON storage\
├── mood_log.txt # Mood logs saved here (auto-created)\
├── todo.txt # To-Do tasks saved here (auto-created)\
└── journal_<date>.txt # Daily journal files, one per date