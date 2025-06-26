import tkinter as tk
from tkcalendar import Calendar
import os
import json
from journal import open_specific_journal


REMINDER_FILE = "reminders.json"

def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reminders(data):
    with open(REMINDER_FILE, "w") as f:
        json.dump(data, f, indent=4 )


def open_calendar_screen():
    reminders = load_reminders()

    cal_window = tk.Toplevel()
    cal_window.title("Mind Garden Calendar")
    cal_window.geometry("400x400")
    cal_window.configure(bg="#F0FFF0")

    label = tk.Label(cal_window, text="select a Date", font=("Arial", 14), bg="#F0FFF0")
    label.pack(pady=10)

    cal = Calendar(cal_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)

    def highlight_reminders():
        for tag in cal._tags:
            cal.calevent_remove(tag=tag)
        for date, entries in reminders.items():
            if entries:
                cal.calevent_create(date, "Reminder", "reminder")
        cal.tag_config("reminder", background="lightblue", foreground="black")

    highlight_reminders()

    def add_reminder():
        selected_date = cal.get_date()


        top = tk.Toplevel(cal_window)
        top.title("Add Reminder")
        top.geometry("200x300")

        tk.Label(top, text="Reminder Description:").pack(pady=5)
        entry_desc = tk.Entry(top, width=30)
        entry_desc.pack(pady=5)

        reminder_type = tk.StringVar(value="assignment")
        tk.Radiobutton(top, text="Assignment", variable=reminder_type, value="assignment").pack()
        tk.Radiobutton(top, text="Exam", variable=reminder_type, value="exam").pack()


        def save():
            desc = entry_desc.get()
            r_type = reminder_type.get()

            if not desc:
                return 
            if selected_date not in reminders:
                reminders[selected_date] = []

            reminders[selected_date].append({
                "description" : desc, 
                "type": r_type
            })

            save_reminders(reminders)
            highlight_reminders()
            top.destroy()



        tk.Button(top, text="Save", command=save).pack(pady=10)

    def view_reminders():
        selected_date = cal.get_date()
        top = tk.Toplevel(cal_window)
        top.title("Reminders for" + selected_date)
        top.geometry("300x250")

        tk.Label(top, text=f"Reminders on {selected_date}:", font=("Arial", 12)).pack(pady=10)

        entries = reminders.get(selected_date, [])
        if not entries:
            tk.Label(top, text="No reminders set.").pack()
        else:
            for r in entries:
                text = f"- ({r['type']}) {r['description']}"
                tk.Label(top, text=text, wraplength=250, justify="left").pack(anchor='w', padx=10)




    def open_journal_for_date():
        selected_date = cal.get_date()
        open_specific_journal(selected_date)

    tk.Button(cal_window, text="Open Journal", command=open_journal_for_date).pack(pady=5)
    tk.Button(cal_window, text="Add Reminder", command=add_reminder).pack(pady=5)
    tk.Button(cal_window, text="View Reminders", command=view_reminders).pack(pady=5)

    
