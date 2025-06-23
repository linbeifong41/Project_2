import tkinter as tk 
from datetime import date 
from journal import  open_journal_screen
from tkinter import scrolledtext
from calendar_window import open_calendar_screen


def log_mood(level):
    today = date.today().isoformat()
    with open("mood_log.txt", "a") as file:
        file.write(f"{today}: Mood {level}/5\n")
    print(f"Mood {level} logged for {today}!")

root = tk.Tk()
root.title("Mind Garden")
root.geometry("400x300")
root.configure(bg="#E6F5EB")

label = tk.Label(root, text="How are you feeling today?", bg="#E6F5EB", font=("Arial", 14))
label.pack(pady=20)

for i in range(1, 6):
    btn = tk.Button(root, text=f"{i}", width=10, font=("Arial", 12), command=lambda i=i: log_mood(i))
    btn.pack(pady=5)

journal_button = tk.Button(root, text="Open Journal", command=open_journal_screen, font=("Arial", 12))
journal_button.pack(pady=10)

calendar_button = tk.Button(root, text="View Calendar", command=open_calendar_screen, font=("Arial", 12))
calendar_button.pack(pady=10)


mood_log_box = scrolledtext.ScrolledText(root, width=40, height=10, font=("Arial",12))
mood_log_box.pack(pady=10)

def refresh_logs(): 
    mood_log_box.delete("1.0", tk.END)

    try:
        with open("mood_log.txt", "r") as f:
            mood_log_box.insert(tk.END, f.read())
    except FileNotFoundError:
        mood_log_box.insert(tk.END, "No moods logged yet.")

refresh_btn = tk.Button(root, text="Refresh Logs", command=refresh_logs, font=("Arial", 12))
refresh_btn.pack(pady=5)


root.mainloop()

