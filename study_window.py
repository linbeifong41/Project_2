import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random




def setup_flashcards(frame):
    global flashcards
    flashcards = []

    current_index = [0]
    show_back = [False]
    tk.Label(frame, text="Front:").pack()
    front_entry = tk.Entry(frame)
    front_entry.pack()

    tk.Label(frame, text="Back:").pack()
    back_entry = tk.Entry(frame)
    back_entry.pack()
    

    def add_flashcard():
        front = front_entry.get()
        back = back_entry.get()
        flashcards.append((front, back))
        front_entry.delete(0, tk.END)
        back_entry.delete(0, tk.END)


    tk.Button(frame, text="Add Flashcard", command=add_flashcard).pack(pady=5)
    display_label = tk.Label(frame, text="No flashcards yet.", wraplength=300, font=("Helvetica", 16), pady=20)
    display_label.pack()

    def update_display():
        if flashcards:
            card = flashcards[current_index[0]]
            if show_back[0]:
                display_label.config(text=f"Back:\n{card[1]}")
            else:
                display_label.config(text=f"Front:\n{card[0]}")
        else:
             display_label.config(text="No flashcards yet")

    def flip_card():
        if flashcards:
            show_back[0] = not show_back[0]
            update_display()
    def next_card():
        if flashcards:
            current_index[0] = (current_index[0] + 1) %len(flashcards)
            show_back[0] = False
            update_display()

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10)  

    def previous_card():
        if flashcards:
            current_index[0] = (current_index[0] - 1) % len(flashcards)
            show_back[0] =False
            update_display()

    def shuffle_flashcards():
        random.shuffle(flashcards)
        current_index[0] = 0
        show_back[0] = False
        update_display()

    tk.Button(button_frame, text="Shuffle", command=shuffle_flashcards).pack(side="left", padx=5)
    tk.Button(button_frame, text="previous", command=previous_card).pack(side="left", padx=5)
    tk.Button(button_frame, text="flip", command=flip_card).pack(side="left", padx=5)
    tk.Button(button_frame, text="Next", command=next_card).pack(side="left", padx=5)

def setup_pomodoro(frame):
    time_left = tk.StringVar(value="25:00")
    timer_label = tk.Label(frame, textvariable=time_left, font=("Helvetica", 32)).pack(pady=20)

    running = [False]
    minutes = [25]
    seconds = [0]

    def start_timer():
        running[0] = True
        count_down()
        
    def reset_timer():
        running[0] = False
        minutes[0], seconds[0] = 25, 0
        time_left.set("25:00")

    def count_down():
        nonlocal running, minutes, seconds
        if running[0]:
            if minutes[0] == 0 and seconds[0] == 0:
                running = False
                messagebox.showinfo("Pomodoro", "Time's Up!")
                return
            if seconds[0] == 0:
                minutes[0] -= 1
                seconds[0] = 59
            else: 
                seconds[0] -= 1
            time_left.set(f"{minutes[0]:02d}:{seconds[0]:02d}")
            frame.after(1000, count_down)
        
    tk.Button(frame, text="Start", command=start_timer).pack(side="left", padx=10)
    tk.Button(frame, text="Reset Timer", command=reset_timer).pack(side="left", padx=10)


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



