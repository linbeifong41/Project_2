import tkinter as tk 
from datetime import date 
from journal import  open_journal_screen
from tkinter import scrolledtext
from calendar_window import open_calendar_screen
from notepad import notepad
from Todo_List import todo_list
from study_window import open_study_tools


def log_mood(level):
    today = date.today().isoformat()
    with open("mood_log.txt", "a") as file:
        file.write(f"{today}: Mood {level}/5\n")
    print(f"Mood {level} logged for {today}!")

root = tk.Tk()
root.title("Mind Garden")
root.geometry("400x300")
root.configure(bg="#E6F5EB")

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


content = tk.Frame(scrollable_frame, bg="#E6F5EB")
content.pack(pady=20, anchor="center")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind( "<Configure>", on_configure)


label = tk.Label(content, text="How are you feeling today?", bg="#E6F5EB", font=("Arial", 14))
label.pack(pady=20)

for i in range(1, 6):
    btn = tk.Button(content, text=f"{i}", width=10, font=("Arial", 12), command=lambda i=i: log_mood(i))
    btn.pack(pady=5)

journal_button = tk.Button(content, text="Open Journal", command=open_journal_screen, font=("Arial", 12))
journal_button.pack(pady=10)

calendar_button = tk.Button(content, text="View Calendar", command=open_calendar_screen, font=("Arial", 12))
calendar_button.pack(pady=10)

button = tk.Button(content, text="Open Notepad", command=notepad, font=("Arial", 12))
button.pack(pady=10)

todo_list_btn = tk.Button(content, text="Open To-Do List", command=todo_list, font=("Arial", 12))
todo_list_btn.pack(pady=10)

study_window_btn = tk.Button(content, text="Open Study Window", command=open_study_tools, font=("Arial", 10))
study_window_btn.pack(pady=10)

mood_log_box = scrolledtext.ScrolledText(content, width=40, height=10, font=("Arial",12))
mood_log_box.pack(pady=10)



def refresh_logs(): 
    mood_log_box.delete("1.0", tk.END)

    try:
        with open("mood_log.txt", "r") as f:
            mood_log_box.insert(tk.END, f.read())
    except FileNotFoundError:
        mood_log_box.insert(tk.END, "No moods logged yet.")

refresh_btn = tk.Button(content, text="Refresh Logs", command=refresh_logs, font=("Arial", 12))
refresh_btn.pack(pady=5)



def _on_mousewheel(event):
    canvas.yview_scroll(-1*int((event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)


root.mainloop()

