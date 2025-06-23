import tkinter as tk
from tkcalendar import Calendar


def open_calendar_screen():
    cal_window = tk.Toplevel()
    cal_window.title("Mind Garden Calendar")
    cal_window.geometry("400x400")
    cal_window.configure(bg="#F0FFF0")

    label = tk.Label(cal_window, text="select a Date", font=("Arial", 14), bg="#F0FFF0")
    label.pack(pady=10)

    cal = Calendar(cal_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)

    def on_date_select():
        selected_date = cal.get_date()
        print(f"You selected: {selected_date}")

    select_btn = tk.Button(cal_window, text="Check Journal", command=on_date_select)
    select_btn.pack(pady=10)

    
