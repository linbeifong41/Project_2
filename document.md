This is where I  will be explaining the code. Websites, books, and media sources such as youtube were used as a learning resource for this project. 

main.py:
"import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import date
from journal import open_journal_screen
from calendar_window import open_calendar_screen
from notepad import notepad
from Todo_List import todo_list
from study_window import open_study_tools
from habit_tracker import open_habit_tracker":

import: used to access code in another module. 

import tkinter as tk: tk is a psuedo you use, so when you type your code in, you don's need to write tkinter. something, you write tk. 

from tkinter import ttk, scrolledtext: python statement used in GUI.

from datetime import date: date is a class from the datetime module, allows you to create date objects without needing to prefix them with datetime. 

from journal import open_journal_screen
from calendar_window import open_calendar_screen
from notepad import notepad
from Todo_List import todo_list
from study_window import open_study_tools
from habit_tracker import open_habit_tracker: access these functions from the other files.  

"def log_mood(level):
    today = date.today().isoformat()
    with open("mood_log.txt", "a") as file:
        file.write(f"{today}: Mood {level}/5\n")
    refresh_logs()": 
         
         def log_mood: defines a function named log_mood.
         level: represents the mood rating. (probability from 1-5)

         date.today: get's today's date
         isoformat tuns it into a string format.
         "with open("mood_log.txt", "a") as file:": opens a file named "mood_log.txt", "a" appends.
         as file: gives you an object file you can write to. 
         file.write(f"{today}: Mood {level}/5\n"): basically writes a string line, starts with date(f"{today}:), then mood logged ({level}/5), the \n means add a new line, or goes to a new line after the log is added. 

         "refresh_logs()": calls on a function, to refresh. 

"root = tk.Tk()
root.title("🌱 Mind Garden")
root.geometry("500x600")
root.configure(bg="#E6F5EB")":
     root is the main window, tk.Tk() to create the window so it opens when the file it run. 
     root.title: makes the white line on top of the window to show the name of the app. 
     root.geometry: width and length of the window, how big or small it is.
     root.configure(bg="#E6F5EB")": configure is used to modify, so it allows us ot chnage the background color here. 
    
style = ttk.Style()
style.configure("Rounded.TButton",font=("Segoe UI", 12),padding=8): 
         style = ttk.Style(): style = (what we want to call it, name), ttk.style(ttk, library, has a fucntio called style that we can use to edit and make the UI look better)
         in this case I made the button have rounded edges, with the font Segoe UI, and font size 12, and the padding(space between the words and the border of the button) 8. 


"canvas = tk.Canvas(root, bg="#E6F5EB", highlightthickness=0)
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
scrollable_frame.bind("<Configure>", on_configure)":


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

root.protocol("WM_DELETE_WINDOW", lambda: (canvas.unbind_all("<MouseWheel>"), root.destroy()))"

        creates a canvas for the scrollframe to work, vertical scrollbar, works on windows currently. Added bind and unbind to prevemt bugs and the function from not working properly or at all.


"header = tk.Label(scrollable_frame, text="🌿 Mind Garden", bg="#E6F5EB",
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

log_frame = tk.LabelFrame(scrollable_frame, text="Mood Log",
                          bg="#E6F5EB", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
log_frame.pack(padx=20, pady=10, fill="both", expand=True)

mood_log_box = scrolledtext.ScrolledText(log_frame, width=50, height=10, font=("Segoe UI", 11))
mood_log_box.pack(pady=5, fill="both", expand=True): 

    The UI with headers and subheaders and emoji's to make it look nicer, it has frames so it loosk neater and everything is devided properly. Each emoji and emotion out of 5 has a button, when pressed it goes to the box for the logged moods. 

"tools_frame = tk.LabelFrame(scrollable_frame, text="Tools",
                            bg="#E6F5EB", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
tools_frame.pack(padx=20, pady=10, fill="x")

tool_buttons = [
    ("📔 Journal", open_journal_screen),
    ("📅 Calendar", open_calendar_screen),
    ("📝 Notepad", notepad),
    ("✅ To-Do List", todo_list),
    ("📚 Study Tools", open_study_tools),
    ("📊 Habit Tracker", open_habit_tracker),
]" : A frame containing the buttons that allow access to other windows on the app. They open as Toplevel windows instead of roots. 