import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, colorchooser
import os, sys, json, datetime
from datetime import date
from journal import open_journal_screen
from calendar_window import open_calendar_screen
from notepad import notepad
from Todo_List import todo_list
from study_window import open_study_tools
from habit_tracker import open_habit_tracker
from utils import user_file_path
from utils import ensure_json_file, ensure_txt_file

FILES_JSON = {
    "reminders.json": [],
    "templates.json": [],
    "daily_goals.json": [],
    "badge_data.json": {},
    "tech_habit_logs.json": [],
    "reflection_notes.json": [],
    "projects.json": []
}

FILES_TXT = [
    "todo.txt"
]


for filename, default_data in FILES_JSON.items():
    ensure_json_file(filename, default_data)


for filename in FILES_TXT:
    ensure_txt_file(filename)

def log_mood(level):
    today = date.today().isoformat()
    with open(user_file_path("mood_log.txt"), "a", encoding="utf-8") as file:
        file.write(f"{today}: Mood {level}/5\n")
    refresh_logs()

root = tk.Tk()
root.title("🌱 Mind Garden")
root.geometry("500x600")
root.configure(bg="#E6F5EB")

style = ttk.Style()
style.configure("Rounded.TButton",
                font=("Segoe UI", 12),
                padding=8)

canvas = tk.Canvas(root, bg="#E6F5EB", highlightthickness=0)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set)

scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = tk.Frame(canvas, bg="#E6F5EB")
window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

def on_canvas_configure(event):
    canvas.itemconfig(window_id, width=event.width)
canvas.bind("<Configure>", on_canvas_configure)

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
scrollable_frame.bind("<Configure>", on_configure)

header = tk.Label(scrollable_frame, text="🌿 Mind Garden", bg="#E6F5EB",
                  font=("Segoe UI", 24, "bold"))
header.pack(pady=(20, 5))

sub_header = tk.Label(scrollable_frame, text="Take care of your mind today 🌸",
                      bg="#E6F5EB", font=("Segoe UI", 12))
sub_header.pack(pady=(0, 15))

mood_frame = tk.LabelFrame(scrollable_frame, text="How are you feeling today?",
                           bg="#E6F5EB", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
mood_frame.pack(padx=20, pady=10, fill="x")

mood_buttons = tk.Frame(mood_frame, bg="#E6F5EB")
mood_buttons.pack(pady=5)

for i, emoji in enumerate(["😞", "😐", "🙂", "😊", "🤩"], start=1):
    ttk.Button(mood_buttons, text=f"{emoji} {i}/5",
               style="Rounded.TButton",
               command=lambda i=i: log_mood(i)).pack(side="left", padx=5)

tools_frame = tk.LabelFrame(scrollable_frame, text="Tools",
                            bg="#E6F5EB", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
tools_frame.pack(padx=20, pady=10, fill="x")

tool_buttons = [
    ("📔 Journal", open_journal_screen),
    ("📅 Calendar", open_calendar_screen),
    ("📝 Notepad", notepad),
    ("✅ To-Do List", todo_list),
    ("📚 Study Tools", open_study_tools),
    ("📊 Habit Tracker", open_habit_tracker),
]

for label, cmd in tool_buttons:
    ttk.Button(tools_frame, text=label, style="Rounded.TButton", command=cmd).pack(pady=5, fill="x")

log_frame = tk.LabelFrame(scrollable_frame, text="Mood Log",
                          bg="#E6F5EB", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
log_frame.pack(padx=20, pady=10, fill="both", expand=True)

mood_log_box = scrolledtext.ScrolledText(log_frame, width=50, height=10, font=("Segoe UI", 11))
mood_log_box.pack(pady=5, fill="both", expand=True)

def refresh_logs():
    mood_log_box.delete("1.0", tk.END)
    try:
        with open(user_file_path("mood_log.txt"), "r", encoding="utf-8") as f:
            mood_log_box.insert(tk.END, f.read())
    except FileNotFoundError:
        mood_log_box.insert(tk.END, "No moods logged yet.")

ttk.Button(log_frame, text="🔄 Refresh Logs", style="Rounded.TButton",
           command=refresh_logs).pack(pady=5)


def _on_mousewheel(event):
    
    canvas.yview_scroll(-1 * int(event.delta / 120), "units")

def _on_mousewheel_mac(event):
    
    canvas.yview_scroll(-1 * int(event.delta), "units")


def _bind_to_mousewheel(event):
    if root.tk.call('tk', 'windowingsystem') == 'aqua': 
        canvas.bind_all("<MouseWheel>", _on_mousewheel_mac)
    else: 
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

def _unbind_from_mousewheel(event):
    canvas.unbind_all("<MouseWheel>")

canvas.bind("<Enter>", _bind_to_mousewheel)
canvas.bind("<Leave>", _unbind_from_mousewheel)


root.protocol("WM_DELETE_WINDOW", lambda: (canvas.unbind_all("<MouseWheel>"), root.destroy()))

refresh_logs()
root.mainloop()