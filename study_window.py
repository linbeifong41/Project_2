import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter.colorchooser as colorchooser
import tkinter.simpledialog as simpledialog
import csv
import random
import json
import os
import winsound
import datetime





SAVE_FILE = "flashcards.json"
decks = {}
current_deck = None

def save_flashcards():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(decks, f, indent=2)

def load_flashcards():
    global decks
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            decks = json.load(f)



def setup_flashcards(frame):
    global decks, current_deck

    load_flashcards()
    current_deck = tk.StringVar()
    current_index = [0]
    show_back = [False]

    deck_frame = tk.Frame(frame)
    deck_frame.pack(pady=5)

    tk.Label(deck_frame, text="Deck:").pack(side="left")
    deck_dropdown = ttk.Combobox(deck_frame, textvariable=current_deck, state="readonly")
    deck_dropdown.pack(side="left", padx=5)

    def refresh_decks():
        deck_dropdown['values'] = list(decks.keys())
        if not current_deck.get() and decks:
            current_deck.set(list(decks.keys())[0])
    
    def on_deck_change(event=None):
        current_index[0] = 0
        show_back[0] = False
        update_display()
    deck_dropdown.bind("<<ComboboxSelected>>", on_deck_change)
    
    def create_deck():
        new_deck = deck_name_entry.get().strip()
        if new_deck and new_deck not in decks:
            decks[new_deck] = []
            deck_name_entry.delete(0, tk.END)
            refresh_decks()
            current_deck.set(new_deck)
            update_display()
            save_flashcards()

    deck_name_entry = tk.Entry(deck_frame)
    deck_name_entry.pack(side="left", padx=5)
    tk.Button(deck_frame, text="+ Add Deck", command=create_deck).pack(side="left")

    def delete_deck():
        deck = current_deck.get()
        if deck and deck in decks:
            if messagebox.askyesno("Confirm", f"Delete deck '{deck}' and all its cards?"):
                del decks[deck]
                current_deck.set("")
                refresh_decks()
                update_display()
                save_flashcards()
    tk.Button(deck_frame, text="Delete deck", command=delete_deck).pack(side="left", padx=5)

    tk.Label(frame, text="Front:").pack()
    front_entry = tk.Entry(frame)
    front_entry.pack()

    tk.Label(frame, text="Back:").pack()
    back_entry = tk.Entry(frame)
    back_entry.pack()
    

    def add_flashcard():
        front = front_entry.get()
        back = back_entry.get()
        deck= current_deck.get()
        if deck and front and back:
            decks[deck].append((front, back))
            front_entry.delete(0, tk.END)
            back_entry.delete(0, tk.END)
            current_index[0] = len(decks[deck]) - 1 
            show_back[0] = False
            update_display()
            save_flashcards()


    tk.Button(frame, text="Add Flashcard", command=add_flashcard).pack(pady=5)

    display_label = tk.Label(frame, text="No flashcards yet.", wraplength=300, font=("Helvetica", 16), pady=20)
    display_label.pack()


    def update_display():
        deck = current_deck.get()
        if deck and deck in decks and decks[deck]:
            card = decks[deck][current_index[0]]
            if show_back[0]:
                display_label.config(text=f"Card {current_index[0]+1} of {len(decks[deck])}\nBack:\n{card[1]}")
            else:
                display_label.config(text=f"Card {current_index[0]+1} of {len(decks[deck])}\nFront:\n{card[0]}")
        else:
             display_label.config(text="No flashcards yet")

    def delete_flashcard():
        deck = current_deck.get()
        if deck and decks.get(deck):
            if len(decks[deck]) > 0:
                del decks[deck][current_index[0]]
                if current_index[0] >= len(decks[deck]):
                    current_index[0] = max(0, len(decks[deck]) - 1)
                show_back[0] = False
                update_display()
                save_flashcards()
            else: 
                display_label.config(text="No flashcards yet.")

    def edit_flashcard():
        deck = current_deck.get()
        if not deck or not decks.get(deck) or not decks[deck]:
            return
        card = decks[deck][current_index[0]]

        def save_edit():
            new_front = front_edit.get()
            new_back = back_edit.get()
            if new_front and new_back:
                decks[deck][current_index[0]] = (new_front, new_back)
                edit_win.destroy()
                update_display()
                save_flashcards()
        
        edit_win = tk.Toplevel(frame)
        edit_win.title("Edit Flashcard")

        tk.Label(edit_win, text="Front:").pack()
        front_edit =tk.Entry(edit_win)
        front_edit.insert(0, card[0])
        front_edit.pack()

        tk.Label(edit_win, text="Back").pack()
        back_edit = tk.Entry(edit_win)
        back_edit.insert(0, card[1])
        back_edit.pack()

        tk.Button(edit_win, text="Save", command=save_edit).pack(pady=5)
        

    def flip_card():
        if current_deck.get() and decks.get(current_deck.get()):
            show_back[0] = not show_back[0]
            update_display()
    def next_card():
        deck = current_deck.get()
        if not deck or not decks.get(deck):
            return 
        current_index[0] += 1 
        if current_index[0] >= len(decks[deck]):
            random.shuffle(decks[deck])
            current_index[0] = 0
        show_back[0] = False
        update_display()

 

    def previous_card():
        deck = current_deck.get()
        if deck and decks.get(deck):
            current_index[0] = (current_index[0] - 1) % len(decks[deck])
            show_back[0] =False
            update_display()

    def shuffle_flashcards():
        deck = current_deck.get()
        if deck and decks.get(deck):
            random.shuffle(decks[deck])
            current_index[0] = 0
            show_back[0] = False
            update_display()

    def export_deck():
        deck = current_deck.get()
        if not deck or deck not in decks:
            return 
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
        if not filepath:
            return
        try:
            with open(filepath, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Front", "Back"])
                for front, back in decks[deck]:
                    writer.writerow([front, back])
            messagebox.showinfo("Exported", f"Deck '{deck}' exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def import_deck():
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
        if not filepath:
            return
        deck_name = os.path.splitext(os.path.basename(filepath))[0]
        if deck_name in decks:
            if not messagebox.askyesno("Deck exists", f"Deck '{deck_name}' already exists.Overwrite?"):
                return
        new_deck = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                headers = next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        new_deck.append((row[0], row[1]))
            decks[deck_name] = new_deck
            current_deck.set(deck_name)
            deck_dropdown.set(deck_name)
            refresh_decks()
            update_display()
            save_flashcards()
            messagebox.showinfo("Imported", f"Deck '{deck_name}' imported successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10) 

    tk.Button(button_frame, text="🔀 Shuffle", command=shuffle_flashcards).pack(side="left", padx=5)
    tk.Button(button_frame, text="◀ previous", command=previous_card).pack(side="left", padx=5)
    tk.Button(button_frame, text="⏺ flip", command=flip_card).pack(side="left", padx=5)
    tk.Button(button_frame, text="▶ Next", command=next_card).pack(side="left", padx=5)

    tk.Button(button_frame, text="Edit", command=edit_flashcard).pack(side="left", padx=5)
    tk.Button(button_frame, text="Delete", command=delete_flashcard).pack(side="left", padx=5)

    tk.Button(button_frame, text="Save", command=save_flashcards).pack(side="left", padx=5)

    tk.Button(deck_frame, text="Export Deck", command=export_deck).pack(side="left", padx=5)
    tk.Button(deck_frame, text="Import Deck", command=import_deck).pack(side="left",padx=5)

    frame.bind_all("<Right>", lambda e: next_card())
    frame.bind_all("<Left>", lambda e: previous_card())
    frame.bind_all("<space>", lambda e: flip_card())

    refresh_decks()
    if current_deck.get():
        update_display()

    def on_close():
        save_flashcards()
        frame.winfo_toplevel().destroy()
    frame.winfo_toplevel().protocol("WM_DELETE_WINDOW", on_close)




STATE_FILE = "pomodoro_state.json"

PRESET_FILE = "pomodoro_presets.json"

def load_presets():
    if os.path.exists(PRESET_FILE):
        with open(PRESET_FILE, "r") as f:
            return json.load(f)
    return [ 
        {"name": "Deep Focus", "duration": 50, "type": "Study"}, 
        {"name": "Micro Break", "duration": 2, "type": "Break"}, 
        {"name": "Strech Time", "duration": 10, "type": "Break"}
    ]
def save_presets(presets):
    with open(PRESET_FILE, "w") as f:
        json.dump(presets, f)

custom_presets = load_presets()

def open_preset_editor(parent, refresh_preset_menu):
    editor = tk.Toplevel(parent)
    editor.title("Edit Presets")

    tk.Label(editor, text="Name").grid(row=0, column=0)
    tk.Label(editor, text="Duration (min)").grid(row=0, column=1)
    tk.Label(editor, text="Type").grid(row=0, column=2)

    entries = []

    def refresh_editor():
        for widget in editor.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.OptionMenu):
                widget.destroy()

        entries.clear()

        for i, preset in enumerate(custom_presets):
            name_var = tk.StringVar(value=preset["name"])
            duration_var = tk.StringVar(value=preset["duration"])
            type_var = tk.StringVar(value=preset["type"])

            e1 = tk.Entry(editor, textvariable=name_var)
            e1.grid(row=i+1, column=0)
            e2 = tk.Entry(editor, textvariable=duration_var, width=5)
            e2.grid(row=i+1, column=1)
            e3 = tk.OptionMenu(editor, type_var, "Study", "Break")
            e3.grid(row=i+1, column=2)

            del_btn = tk.Button(editor, text="Delete", command=lambda idx=i: delete_preset(idx))
            del_btn.grid(row=i+1, column=3)

            entries.append((name_var, duration_var, type_var))

    def delete_preset(index):
        custom_presets.pop(index)
        save_presets(custom_presets)
        refresh_editor()
    
    def save_all():
        new_presets = []
        for name_var, duration_var, type_var in entries:
            name = name_var.get().strip()
            duration = duration_var.get()
            type_ = type_var.get()
            try:
                duration_int = int(duration)
                if name and duration_int > 0:
                    new_presets.append({"name": name, "duration": duration_int, "type": type_})
            except ValueError:
                continue
        
        custom_presets.clear()
        custom_presets.extend(new_presets)
        save_presets(custom_presets)
        refresh_preset_menu()
        editor.destroy()
    
    def add_new():
        custom_presets.append({"name": "New Preset", "duration": 25, "type": "Study"})
        refresh_editor()
    tk.Button(editor, text="Add Preset", command=add_new).grid(row=999, column=0, pady=10)
    tk.Button(editor, text="Save and Close", command=save_all).grid(row=999, column=1, pady=10)

    refresh_editor()



def setup_pomodoro(frame):
    time_left = tk.StringVar(value="25:00")
    tk.Label(frame, textvariable=time_left, font=("Helvetica", 32)).pack(pady=10)

    study_duration = tk.IntVar(value=25)
    short_break_duration = tk.IntVar(value=5)
    long_break_duration = tk.IntVar(value=15)

    sound_enabled = tk.BooleanVar(value=True)

    auto_start_next = tk.BooleanVar(value=False)

    running = [False]
    minutes = [study_duration.get()]
    seconds = [0]
    session_count = [0]
    completed_study_sessions = [0]
    last_session_date = [str(datetime.date.today())]


    start_session = tk.StringVar(value="Study")

    is_study_session = [start_session.get() == "Study"]

    def check_new_day():
        today =str(datetime.date.today())
        if today != last_session_date[0]:
            completed_study_sessions[0] = 0
            last_session_date[0] = today

    def load_state():
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
                study_duration.set(state.get("study_duration", 25))
                short_break_duration.set(state.get("short_break_duration", 5))
                long_break_duration.set(state.get("long_break_duration", 15))
                start_session.set(state.get("start_session", "Study"))
                minutes[0] = state.get("minutes", 25)
                seconds[0] = state.get("seconds", 0)
                is_study_session[0] = state.get("is_study_session", True)
                session_count[0] = state.get("session_count", 0)
                running[0] = state.get("running", False)
                sound_enabled.set(state.get("sound_enabled", True))
                time_left.set(f"{minutes[0]:02d}:{seconds[0]:02d}")
                auto_start_next.set(state.get("auto_start_next", False))
                completed_study_sessions[0] = state.get("completed_sessions", 0)
                last_session_date[0] = state.get("last_date", str(datetime.date.today()))

    def save_state():
        state= {
            "study_duration": study_duration.get(), 
            "short_break_duration": short_break_duration.get(), 
            "long_break_duration": long_break_duration.get(), 
            "start_session": start_session.get(), 
            "minutes": minutes[0], 
            "seconds": seconds[0], 
            "is_study_session": is_study_session[0], 
            "session_count": session_count[0], 
            "running": running[0], 
            "sound_enabled": sound_enabled.get(),
            "auto_start_next": auto_start_next.get(), 
            "completed_sessions": completed_study_sessions[0], 
            "last_date": last_session_date[0]
        }
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)

    def apply_preset(name):
        preset = next((p for p in custom_presets if p["name"] == name), None)
        if preset: 
            minutes[0] = int(preset["duration"])
            seconds[0] = 0
            is_study_session[0] = (preset["type"] == "Study")
            time_left.set(f"{minutes[0]:02d}:{seconds[0]:02d}")
            save_state()
            

    duration_frame = tk.Frame(frame)
    duration_frame.pack(pady=5)
    
    tk.Label(duration_frame, text="Study:").grid(row=0, column=0)
    tk.Entry(duration_frame, textvariable=study_duration, width=3).grid(row=0, column=1)
    tk.Label(duration_frame, text="min ").grid(row=0, column=2)

    tk.Label(duration_frame, text="Break:").grid(row=0, column=3)
    tk.Entry(duration_frame, textvariable=short_break_duration, width=3).grid(row=0, column=4)
    tk.Label(duration_frame, text="min ").grid(row=0, column=5)

    tk.Label(duration_frame, text="Long Break:").grid(row=0, column=6)
    tk.Entry(duration_frame, textvariable=long_break_duration, width=3).grid(row=0, column=7)
    tk.Label(duration_frame, text="min ").grid(row=0, column=8)

    tk.Checkbutton(frame, text="Enable Sound", variable=sound_enabled).pack(pady=5)
    tk.Checkbutton(frame, text="Auto-Start next session", variable=auto_start_next).pack(pady=2)


    tk.Label(frame, text="Start with:").pack()
    tk.OptionMenu(frame, start_session, "Study", "Short Break", "Long Break").pack()


    def reset_timer():
        running[0] = False

        preset_name = selected_preset.get()
        built_in_types = {"Study", "Short Break", "Long Break"}
        if preset_name and preset_name not in built_in_types:
            preset = next((p for p in custom_presets if p["name"] == preset_name), None)
            if preset:
                minutes[0] = int(preset["duration"])
                seconds[0] = 0
                is_study_session[0] = (preset["type"] == "Study")
                time_left.set(f"{minutes[0]:02d}:{seconds[0]:02d}")
                save_state()
                return
        

        selected = start_session.get()

        if selected == "Study":
            minutes[0] = study_duration.get()
            is_study_session[0] = True
        elif selected == "Short Break":
            minutes[0] = short_break_duration.get()
            is_study_session[0] = False
        elif selected == "Long Break":
            minutes[0] = long_break_duration.get()
            is_study_session[0] = False
        else:
            print("Unknown session type:", selected)

        seconds[0] = 0
        time_left.set(f"{minutes[0]:02d}:{seconds[0]:02d}")
        save_state()
        

    def update_initial_timer(*args):
        reset_timer()
        save_state()

    

    study_duration.trace_add("write", lambda *args: save_state())
    short_break_duration.trace_add("write", lambda *args: save_state())
    long_break_duration.trace_add("write", lambda *args: save_state())
    sound_enabled.trace_add("write", lambda *args: save_state())

    tk.Label(frame, text="Or use preset:").pack()
    selected_preset = tk.StringVar(value="")
    preset_menu = tk.OptionMenu(frame, selected_preset, *[p["name"] for p in custom_presets])
    preset_menu.pack()

    def refresh_preset_menu():
        menu = preset_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="-- None --", command=lambda: selected_preset.set(""))
        for p in custom_presets:
            menu.add_command(label=p["name"], command=lambda name=p["name"]: selected_preset.set(name))

    refresh_preset_menu()

    def on_preset_change(*args):
        name = selected_preset.get()
        if name and name not in {"Study", "Short Break", "Long Break"}:
            apply_preset(name)

    selected_preset.trace_add("write", on_preset_change)


    tk.Button(frame, text="Edit Presets", command=lambda: open_preset_editor(frame, refresh_preset_menu)).pack(pady=5)

    start_session.trace_add("write", update_initial_timer)

    if os.path.exists(STATE_FILE):
        load_state()
    else:
        reset_timer()

    def start_timer():
        running[0] = True
        save_state()
        count_down()
        check_new_day()

    def suggest_long_break():
        response = messagebox.askyesno(
            "Take a long break?", 
            "You've completed 4 study sessions!\nWould you like to take a Long Break?"
        )
        if response:
            selected_preset.set("")
            start_session.set("Long Break")
            reset_timer()
        

    def stop_timer():
        running[0] = False
        save_state()

    def count_down():
        if not running[0]:
            return

        if minutes[0] == 0 and seconds[0] == 0:
            is_study = is_study_session[0]
            session_count[0] += int(is_study)

            if is_study:
                completed_study_sessions[0] += 1 
                if completed_study_sessions[0] % 4 ==0:
                    suggest_long_break()
                    return
                

            if is_study:
                minutes[0] = long_break_duration.get() if session_count[0] % 4 == 0 else short_break_duration.get()
                is_study_session[0] = False
            else:
                minutes[0] = study_duration.get()
                is_study_session[0] = True

            seconds[0] = 0
            if sound_enabled.get():
                winsound.Beep(1000, 500)
            save_state()
            if auto_start_next.get():
                frame.after(1000, count_down)
            else:
                messagebox.showinfo("Pomodoro", "Time's Up!")

        if seconds[0] == 0:
            minutes[0] -= 1
            seconds[0] = 59
        else:
            seconds[0] -= 1

        time_left.set(f"{minutes[0]:02d}:{seconds[0]:02d}")
        frame.after(1000, count_down)

    tk.Button(frame, text="Start", command=start_timer).pack(side="left", padx=10)
    tk.Button(frame, text="Pause", command=stop_timer).pack(side="left", padx=10)
    tk.Button(frame, text="Reset Timer", command=reset_timer).pack(side="left", padx=10)

    if os.path.exists(STATE_FILE):
        load_state()
    else:
        reset_timer()


PROJECT_FILE = "projects.json"

def setup_project_tracker(frame):
    if os.path.exists(PROJECT_FILE):
        try:
            with open(PROJECT_FILE, "r") as f:
                projects = json.load(f)
        except Exception as e:
            print("Error loading project file:", e)
            projects = []
    else:
        projects = []

    def save_projects():
        with open(PROJECT_FILE, "w") as f:
            json.dump(projects, f, indent=2)
    
    tag_filter_var = tk.StringVar()
    status_filter_var = tk.StringVar()

    top_frame = ttk.Frame(frame)
    top_frame.pack(fill="x", pady=10, padx=10)

    canvas = tk.Canvas(frame, borderwidth=0, highlightthickness=0)
    scroll_y = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    def on_canvas_resize(event):
        canvas.itemconfig("scroll_window", width=event.width)
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="scroll_window")
    canvas.bind("<Configure>", on_canvas_resize)
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    content_frame = scrollable_frame
    
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    ttk.Label(top_frame, text="Project Name:").pack(side="left", padx=(0, 5))
    new_project_entry = ttk.Entry(top_frame, width=20)
    new_project_entry.pack(side="left", expand=True, fill="x", padx=5)

    ttk.Label(top_frame, text="Due Date:").pack(side="left", padx=(10, 5))
    due_entry = DateEntry(top_frame, width=12, background='darkblue', foreground='white', 
                          borderwhidth=2, year=2025, showweeknumbers=False)
    due_entry.pack(side="left", padx=5)

    ttk.Label(top_frame, text="Category:").pack(side="left", padx=(10, 5))
    cat_entry = ttk.Entry(top_frame, width=15)
    cat_entry.pack(side="left", padx=5)

    ttk.Label(top_frame, text="Tags:").pack(side="left", padx=(10,5))
    tags_entry = ttk.Entry(top_frame, width=15)
    tags_entry.pack(side="left", padx=5)

    ttk.Label(top_frame, text="Status:").pack(side="left", padx=(10, 5))
    status_var = tk.StringVar(value="Not Started")
    status_menu = ttk.OptionMenu(top_frame, status_var, "Not Started", "In Progress", "Stuck",
                                                   "Completed")
    status_menu.pack(side="left", padx=5)

    ttk.Label()


    
    def add_project():
        name = new_project_entry.get().strip()
        due_date = due_entry.get().strip()
        category = cat_entry.get().strip()
        tags = [t.strip() for t in tags_entry.get().split(",") if t.strip()]
        status = status_var.get().strip()
        if name:
            projects.append({
                "name": name,
                "tasks": [], 
                "due": due_date,
                "category": category,
                "notes": "", 
                "attachments": [], 
                "tags": tags, 
                "status": status
                })
            new_project_entry.delete(0, tk.END)
            due_entry.delete(0, tk.END)
            cat_entry.delete(0, tk.END)
            tags_entry.delete(0, tk.END)
            status_var.set("Not Started")
            save_projects()
            refresh_projects()

    ttk.Button(top_frame, text="Add Project", command=add_project).pack(side="right")

    filter_sort_frame = ttk.Frame(frame)
    filter_sort_frame.pack(fill="x", padx=10)

    ttk.Label(filter_sort_frame, text="Filter by Category:").pack(side="left", padx=(0, 5))
    filter_var = tk.StringVar()
    filter_entry = ttk.Entry(filter_sort_frame, textvariable=filter_var, width=15)
    filter_entry.pack(side="left", padx=(0, 15))

    ttk.Label(filter_sort_frame, text="Tag Filter:").pack(side="left", padx=(0, 5))
    ttk.Entry(filter_sort_frame, textvariable=tag_filter_var, width=15).pack(side="left", padx=(0, 10))

    ttk.Label(filter_sort_frame, text="Status Filter:").pack(side="left",padx=(0, 5))
    ttk.Entry(filter_sort_frame, textvariable=status_filter_var).pack(side="left", padx=(0, 15))

    ttk.Label(filter_sort_frame, text="Sort by:").pack(side="left", padx=(0, 5))
    sort_var = tk.StringVar(value="None")
    sort_menu = ttk.Combobox(filter_sort_frame, textvariable=sort_var, state="readonly", width=12,
                              values=["None", "Due Date ↑", "Due Date ↓", "Name A-Z", "Name Z-A" ] )
    sort_menu.pack(side="left", padx=(0, 10))


    ttk.Button(filter_sort_frame, text="Apply", command=lambda: refresh_projects()).pack(side="left", padx=5)
    ttk.Button(filter_sort_frame, text="Clear", command=lambda: (filter_var.set(""), sort_var.set("None"), refresh_projects())).pack(side="left")




    editing_index = None
    task_editing = {}

    def refresh_projects():
        nonlocal editing_index
        nonlocal task_editing
        for widget in content_frame.winfo_children():
            widget.destroy()

        filtered = []
        category_filter = filter_var.get().strip().lower()

        tag_filter = tag_filter_var.get().strip().lower()
        status_filter = status_filter_var.get().strip().lower()

        for proj in projects:
            category_match = not category_filter or category_filter in proj.get("category", "").lower()
            tag_match = not tag_filter or any(tag_filter in tag.lower() for tag in proj.get("tags", []))
            status_match = not status_filter or status_filter == proj.get("status", "").lower()

            if category_match and tag_match and status_match:
                filtered.append(proj)

        sort_by = sort_var.get()
        if sort_by == "Due Date ↑":
            filtered.sort(key=lambda x: x.get("due", "9999-99-99"))
        elif sort_by == "Due Date ↓":
            filtered.sort(key=lambda x: x.get("due", "0000-00-00"), reverse=True)
        elif sort_by == "Name A-Z":
            filtered.sort(key=lambda x: x.get("name", "").lower())
        elif sort_by == "Name Z-A":
            filtered.sort(key=lambda x: x.get("name", "").lower(), reverse=True)

        if not projects:
            empty_label = ttk.Label(content_frame, text="No projects yet.\nAdd one above to get started!",
                            anchor="center", justify="center", font=("Segoe UI", 10))
            empty_label.pack(pady=20)
            return
        elif not filtered:
            empty_label = ttk.Label(content_frame, text="No matching projects found.", anchor="center", 
                            justify="center", font=("Segoe UI", 10))
            empty_label.pack(pady=20)
            return

        for idx, (real_idx, project) in enumerate([(projects.index(p), p) for p in filtered]):
            project_frame = ttk.LabelFrame(content_frame, text="", padding=10)
            project_frame.pack(fill="x", padx=10, pady=5, expand=True)

            title_row = ttk.Frame(project_frame)
            title_row.pack(fill="x", pady=2, expand=True)

            notes_var = tk.StringVar(value=project.get("notes", ""))

            notes_label = ttk.Label(project_frame, text="Notes:")
            notes_label.pack(anchor="w")

            notes_entry = tk.Text(project_frame, height=3, wrap="word")
            notes_entry.insert("1.0", notes_var.get())
            notes_entry.pack(fill="x", pady=(0, 5))

            notes_typing_after_id = [None]

            def make_notes_handlers(i, entry, timer_ref):
                def save_notes(event=None, i=real_idx):
                    projects[i]["notes"] = entry.get("1.0", "end-1c").strip()
                    save_projects()

                def on_notes_change(event=None):
                    projects[i]["notes"] = entry.get("1.0", "end-1c").strip()
                    if timer_ref[0]:
                        entry.after_cancel(timer_ref[0])
                    timer_ref[0] = entry.after(1000, save_projects)
                return save_notes, on_notes_change
            
            save_notes_func, on_change_func = make_notes_handlers(real_idx, 
                                                                  notes_entry, notes_typing_after_id, )

            notes_entry.bind("<KeyRelease>", on_change_func)
            notes_entry.bind("<FocusOut>", save_notes_func)


            def insert_bulletpoint(e=None, widget=None):
                widget.insert("insert", "• ")
            
            bullet_btn = ttk.Button(project_frame, text="• Bullet", width=8, command=lambda w=notes_entry: insert_bulletpoint(widget=w))
            bullet_btn.pack(anchor="w", pady=(0, 3))

            notes_entry.bind("<Control-b>", lambda e, w=notes_entry: insert_bulletpoint(e, w))

            def attach_files(i=real_idx):
                files = filedialog.askopenfilenames(title="Select files to attach.")
                if files:
                    current = projects[i].get("attachments", [])
                    current.extend(files)
                    projects[i]["attachments"] = list(set(current))
                    save_projects()
                    refresh_projects()
            ttk.Button(project_frame, text="Attach Files", command=lambda i=real_idx: attach_files(i)).pack(anchor="w")

            attached_files = project.get("attachments", [])
            if attached_files:
                attach_label = ttk.Label(project_frame, text="Attach File(s):", font=("Segeo UI", 9, "bold"))
                attach_label.pack(anchor="w", pady=(5, 0))

                for file_path in attached_files:
                    file_name = os.path.basename(file_path)
                    def open_file(path=file_path):
                        try:
                            os.startfile(path)
                        except Exception as e:
                            messagebox.showerror("Error",f"Could not open file path.\n\n{e}" )

                    link = ttk.Label(project_frame, text=f"• {file_name}", foreground="blue", cursor="hand2")
                    link.pack(anchor="w", padx=10)
                    link.bind("<Button-1>", lambda e, p=file_path: open_file(p))


            if editing_index == real_idx:
                name_var = tk.StringVar(value=project["name"])
                cat_var = tk.StringVar(value=project.get("category", ""))
                tag_var = tk.StringVar(value=", ".join(project.get("tags", [])))
                status_var = tk.StringVar(value=project.get("status", "Not Started"))
                

                name_entry = ttk.Entry(title_row, textvariable=name_var, width=20)
                name_entry.pack(side="left", padx=(0, 5), fill="x", expand=True)


                info_row = ttk.Frame(project_frame)
                info_row.pack(fill="x", padx=5, pady=5)
    
                due_entry = DateEntry(info_row, width=12, background='darkblue',
                      foreground='white', borderwidth=2, year=2025, showweeknumbers=False)
                try:
                    date_str = project.get("due", "2025-01-01")
                    due_entry.set_date(datetime.datetime.strptime(date_str, "%Y-%m-%d").date())
                except:
                    due_entry.set_date(datetime.datetime.today())
                due_entry.pack(side="left", padx=(0, 5))

                cat_entry = ttk.Entry(info_row, textvariable=cat_var, width=12)
                cat_entry.pack(side="left", padx=(0, 5))


                ttk.Entry(info_row, textvariable=tag_var, width=15).pack(side="left", padx=5)

                status_menu = ttk.OptionMenu(info_row, status_var, status_var.get(), "Not Started",
                                              "In Progress", "Stuck", "Completed")
                status_menu.pack(side="left", padx=5)

                due_entry.pack(side="left", padx=5)

                def save_name(event=None, i=real_idx):
                    new_name = name_var.get().strip()
                    new_due = due_entry.get().strip()
                    new_cat = cat_var.get().strip()
                    new_tags = tag_var.get().strip()
                    new_status = status_var.get().strip()
                    if new_name:
                        projects[i]["name"] = new_name
                        projects[i]["due"] = new_due
                        projects[i]["category"] = new_cat
                        projects[i]["tags"] = [t.strip() for t in new_tags.split(",") if t.strip()]
                        projects[i]["status"] = new_status
                        save_projects()
                    nonlocal editing_index
                    editing_index = None
                    refresh_projects()

                ttk.Button(title_row, text="Save", width=5, command=save_name).pack(side="left")

                name_entry.bind("<Return>", save_name)
                due_entry.bind("<Return>", save_name)
                cat_entry.bind("<Return>", save_name)

                

            else:
                ttk.Label(title_row, text=project["name"], font=("Arial", 12)).pack(side="left", padx=(0, 10))
                ttk.Button(title_row, text="Edit", width=5, command=lambda i=idx: set_edit(i)).pack(side="left")

                ttk.Label(project_frame, text=f"Due: {project.get('due', 'N/A')}", foreground="gray").pack(anchor="w")
                ttk.Label(project_frame, text=f"Category: {project.get('category', 'Uncategorized')}", foreground="gray").pack(anchor="w")

                tags = project.get("tags", [])
                if tags:
                    tag_frame = ttk.Frame(project_frame)
                    tag_frame.pack(anchor="w", pady=2)
                    for tag in tags:
                        lbl = tk.Label(tag_frame, text=tag, bg="#dddddd", fg="black", padx=5, pady=2, relief="groove")
                        lbl.pack(side="left", padx=2)
                        
                        status = project.get("status", "Not Started")
                        status_colors ={
                            "Not Started": "gray", 
                            "In Progress": "blue",
                            "Stuck": "orange", 
                            "Completed": "green"
                        }
                        status_color = status_colors.get(status, "gray")

                        status_lbl = tk.Label(project_frame, text=status, bg=status_color, fg="white", 
                                              padx=6, pady=2)
                        status_lbl.pack(anchor="w", pady=2)




            ttk.Button(title_row, text="Delete", width=6,
                       command=lambda i=idx: (projects.pop(i), save_projects(), refresh_projects())).pack(side="left")
                
            completed = 0

            for t_idx, task in enumerate(project.get("tasks", [])):
                var = tk.BooleanVar(value=task["done"])

                task_frame = ttk.Frame(project_frame)
                task_frame.pack(pady=2, padx=10, fill="x")

                is_editing = task_editing.get((real_idx, t_idx), False)

                def toggle_done(v=var, p=project, ti=t_idx):
                    p["tasks"][ti]["done"] = v.get()
                    save_projects()
                    refresh_projects()

                if is_editing:
                    text_var = tk.StringVar(value=task["text"])
                    entry = ttk.Entry(task_frame, textvariable=text_var)
                    entry.pack(side="left", fill="x", expand=True, padx=(0,5))

                    due_var = tk.StringVar(value=task.get("due date", ""))
                    due_entry = DateEntry(task_frame, textvariable=due_var, width=12, date_pattern="yyyy-mm-dd")
                    due_entry.pack(side="left", padx=(0, 5))

                    def save_task_text(p=project, ti=t_idx, r_idx=real_idx):
                        p["tasks"][ti]["text"] = text_var.get().strip()
                        p["tasks"][ti]["due_date"] = due_var.get().strip()
                        task_editing[(r_idx, ti)] = False
                        save_projects()
                        refresh_projects()

                    entry.bind("<Return>", lambda e: save_task_text())
                    due_entry.bind("<Return>", lambda e: save_task_text())
                    ttk.Button(task_frame, text="Save", width=3, command=save_task_text).pack(side="left", padx=2)
                else:
                    cb = tk.Checkbutton(task_frame, text=task["text"], variable=var, command=toggle_done)
                    cb.pack(side="left", anchor="w", padx=(0, 5))

                    if task.get("due_date"):
                        ttk.Label(task_frame, text=f"Due: {task['due_date']}", foreground="gray").pack(side="left", padx=(0,5))

                    def start_edit(r_idx=real_idx, ti=t_idx):
                        task_editing[(r_idx, ti)] = True 
                        refresh_projects()
                    ttk.Button(task_frame, text="Edit", width=3, command=start_edit).pack(side="left", padx=2)

                def delete_task(p=project, ti=t_idx):
                    del p["tasks"][ti]
                    save_projects()
                    refresh_projects()
                ttk.Button(task_frame, text="Delete", width=3, command=delete_task).pack(side="left", padx=2)

                if task["done"]:
                    completed += 1

            total_tasks = len(project.get("tasks", []))
            percent = int((completed / total_tasks) * 100) if total_tasks else 0

            progress = ttk.Progressbar(project_frame, length=200, value=percent, maximum=100)
            progress.pack(pady=5)

            ttk.Label(project_frame, text=f"{completed} of {total_tasks} tasks complete ({percent}%)").pack()

            task_row = ttk.Frame(project_frame)
            task_row.pack(fill="x", pady=5)

            task_entry = ttk.Entry(task_row)
            task_entry.pack(side="left", padx=5, expand=True, fill="x")

            def add_task(te=task_entry, p=project):
                text = te.get().strip()
                if text:
                    p.setdefault("tasks", []).append({"text": text, "done": False, "due_date": ""})
                    save_projects()
                    refresh_projects()

            ttk.Button(task_row, text="Add Task", command=add_task).pack(side="right")

    def set_edit(index):
        nonlocal editing_index
        editing_index = index
        refresh_projects()

    refresh_projects()

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None

        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip or not self.text.strip():
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip,
            text=self.text,
            background="lightyellow",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10),
            wraplength=200,
            justify="left"
        )
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None 

def export_to_pdf():
    global planner_data
    planner_data = load_planner_data()

    if not planner_data:
        messagebox.showinfo("Export", "No sessions to export.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    x, y = 50, height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "Study Planner Export")
    y -= 30

    for day in planner_data:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y, day)
        y -= 20

        for time in sorted(planner_data[day]):
            session = planner_data[day][time]
            title = session.get("title", "")
            notes = session.get("notes", "")
            text = f"{time} - {title}"
            c.setFont("Helvetica", 11)
            c.drawString(x + 20, y, text)
            y -= 15

            if notes:
                c.setFont("Helvetica-Oblique", 10)
                wrapped = wrap_text(notes, 80)
                for line in wrapped:
                    c.drawString(x + 40, y, line)
                    y -= 13

            y -= 5

            if y < 50:
                c.showPage()
                y = height - 50

    c.save()

def wrap_text(text, width):
    import textwrap
    return textwrap.wrap(text, width)  

PLANNER_DATA_FILE = "study_planner_data.json"
planner_data = {}

def save_planner_data():
    with open(PLANNER_DATA_FILE, "w") as f:
        json.dump(planner_data, f, indent=2)

def load_planner_data():
    if os.path.exists(PLANNER_DATA_FILE):
        with open(PLANNER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def add_session(day, time_label, cell_label):
    popup = tk.Toplevel()
    popup.title(f"{day}, {time_label}")

    existing = planner_data.get(day, {}).get(time_label, {})

    tk.Label(popup, text=f"{day}, {time_label}", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Label(popup, text="Title:").pack()
    title_entry = tk.Entry(popup, width=30)
    title_entry.pack(pady=2)
    title_entry.insert(0, existing.get("title", ""))

    tk.Label(popup, text="Notes:").pack()
    notes_entry = tk.Text(popup, height=4, width=30)
    notes_entry.pack(pady=2)
    notes_entry.insert("1.0", existing.get("notes", ""))

    color_var = tk.StringVar(value=existing.get("color", ""))

    def choose_color():
        color = colorchooser.askcolor(title="Pick Color")[1]
        if color:
            color_var.set(color)

    color_btn = tk.Button(popup, text="Choose Color", command=choose_color)
    color_btn.pack(pady=5)

    def save_session():
        title = title_entry.get()
        notes = notes_entry.get("1.0", "end-1c")
        color = color_var.get()

        if not title:
            return
        if day not in planner_data:
            planner_data[day] = {}

        planner_data[day][time_label] = {
            "title": title,
            "notes": notes,
            "color": color
        }

        cell_label.config(text=title, bg=color or "white", wraplength=80)
        Tooltip(cell_label, notes)
        save_planner_data()
        popup.destroy()

    def delete_session():
        if day in planner_data and time_label in planner_data[day]:
            del planner_data[day][time_label]
            if not planner_data[day]:
                del planner_data[day]
            cell_label.config(text="", bg="white")
            save_planner_data()
        popup.destroy()

    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Save", command=save_session).pack(side="left", padx=5)

    if existing:
        tk.Button(btn_frame, text="Delete", command=delete_session).pack(side="left", padx=5)

    tk.Button(btn_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=5)


def setup_study_planner(study_planner_tab):
    global planner_data
    planner_data = load_planner_data()

    planner_control_frame = ttk.Frame(study_planner_tab)
    planner_control_frame.pack(pady=10)

    ttk.Label(planner_control_frame, text="Start Hour:").pack(side="left", padx=5)
    planner_start_var = ttk.Combobox(planner_control_frame, values=list(range(0, 24)), width=5)
    planner_start_var.set("8")
    planner_start_var.pack(side="left")

    ttk.Label(planner_control_frame, text="End Hour:").pack(side="left", padx=5)
    planner_end_var = ttk.Combobox(planner_control_frame, values=list(range(1, 25)), width=5)
    planner_end_var.set("20")
    planner_end_var.pack(side="left")

    canvas_frame = ttk.Frame(study_planner_tab)
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

    planner_canvas = tk.Canvas(canvas_frame)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=planner_canvas.yview)
    planner_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    planner_canvas.pack(side="left", fill="both", expand=True)

    planner_grid_frame = ttk.Frame(planner_canvas)
    planner_canvas.create_window((0, 0), window=planner_grid_frame, anchor="nw")

    def on_frame_configure(event):
        planner_canvas.configure(scrollregion=planner_canvas.bbox("all"))

    planner_grid_frame.bind("<Configure>", on_frame_configure)

    def generate_time_slots(start_hour, end_hour):
        slots = []
        for hour in range(start_hour, end_hour):
            period = "AM" if hour < 12 else "PM"
            display_hour = hour % 12 or 12
            slots.append(f"{display_hour}:00 {period}")
        return slots
    
    def update_planner_grid():
        for widget in planner_grid_frame.winfo_children():
            widget.destroy()

        try:
            start = int(planner_start_var.get())
            end = int(planner_end_var.get())
            if start >= end:
                raise ValueError
        except:
            return
        
        time_slots = generate_time_slots(start, end)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

      
        tk.Label(planner_grid_frame, text="Time", width=12, relief="ridge").grid(row=0, column=0, sticky="nsew")
        for col, day in enumerate(days, start=1):
            tk.Label(planner_grid_frame, text=day, width=14, relief="ridge").grid(row=0, column=col, sticky="nsew")


        for row, time_label in enumerate(time_slots, start=1):
            tk.Label(planner_grid_frame, text=time_label, width=12, relief="ridge").grid(row=row, column=0, sticky="nsew")

            for col, day in enumerate(days, start=1):
                cell = tk.Label(planner_grid_frame, text="", bg="white", relief="ridge", width=15, borderwidth=1, height=2)
                cell.grid(row=row, column=col, sticky="nsew")

                
                session = planner_data.get(day, {}).get(time_label)
                if session:
                    cell.config(text=session.get("title", ""), bg=session.get("color", "white"), wraplength=80)
                    Tooltip(cell, session.get("notes", ""))

                cell.bind("<Button-1>", lambda e, d=day, t=time_label, c=cell: add_session(d, t, c))

    ttk.Button(planner_control_frame, text="Update Grid", command=update_planner_grid).pack(side="left", padx=10)
    update_planner_grid()
    export_btn = tk.Button(planner_control_frame,  text="Export to PDF", command=export_to_pdf)
    export_btn.pack(pady=5)



def open_study_tools():
    study_winow = tk.Toplevel()
    study_winow.title("Study Tools")
    study_winow.geometry("400x500")

    tab_control = ttk.Notebook(study_winow)

    flashcard_tab = ttk.Frame(tab_control)
    pomodoro_tab = ttk.Frame(tab_control)
    project_tracker_tab = ttk.Frame(tab_control)
    study_planner_tab = ttk.Frame(tab_control)

    tab_control.add(flashcard_tab, text="Flashcards")
    tab_control.add(pomodoro_tab, text="Pomodoro Timer")
    tab_control.add(project_tracker_tab, text="Project Tracker")
    tab_control.add(study_planner_tab, text="Planner")
    tab_control.pack(expand=1, fill="both")

    setup_flashcards(flashcard_tab)
    setup_pomodoro(pomodoro_tab)
    setup_project_tracker(project_tracker_tab)
    setup_study_planner(study_planner_tab)