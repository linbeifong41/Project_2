import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import csv
import random
import json
import os
import winsound




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

def open_preset_editor(parent):
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
            type_var = tk.Stringvar(value=preset["type"])

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
            if name and duration > 0:
                new_presets.append({"name": name, "duration": duration, "type": type_})

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

    start_session = tk.StringVar(value="Study")

    is_study_session = [start_session.get() == "Study"]

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
            "auto_start_next": auto_start_next.get()
        }
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)

    def apply_preset(name):
        preset = next((p for p in custom_presets if p["name"] == name), None)
        if preset: 
            minutes[0] = preset["duration"]
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
        selected = start_session.get()

        if selected == "Study":
            minutes[0] = study_duration.get()
            is_study_session[0] = True
        elif selected == "Short Break":
            minutes[0] = short_break_duration.get()
            is_study_session[0] = False
        else:  
            minutes[0] = long_break_duration.get()
            is_study_session[0] = False

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
    selected_preset = tk.StringVar(value=custom_presets[0]["name"])
    preset_menu = tk.OptionMenu(frame, selected_preset, *[])
    preset_menu.pack()
    refresh_preset_menu()

    def refresh_preset_menu():
        menu = preset_menu["menu"]
        menu.delete(0, "end")
        for p in custom_presets:
            menu.add_command(label=p["name"], command=lambda name=p["name"]: selected_preset.set(name))

    selected_preset.trace_add("write", lambda *args: apply_preset(selected_preset.get()))

    tk.Button(frame, text="Edit Presets", command=lambda: open_preset_editor(frame)).pack(pady=5)

    start_session.trace_add("write", update_initial_timer)

    if os.path.exists(STATE_FILE):
        load_state()
    else:
        reset_timer()

    def start_timer():
        running[0] = True
        save_state()
        count_down()
        

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


def open_study_tools():
    study_winow = tk.Toplevel()
    study_winow.title("Study Tools")
    study_winow.geometry("400x500")

    tab_control = ttk.Notebook(study_winow)

    flashcard_tab = ttk.Frame(tab_control)
    pomodoro_tab = ttk.Frame(tab_control)

    tab_control.add(flashcard_tab, text="Flashcards")
    tab_control.add(pomodoro_tab, text="Pomodoro Timer")
    tab_control.pack(expand=1, fill="both")

    setup_flashcards(flashcard_tab)
    setup_pomodoro(pomodoro_tab)


