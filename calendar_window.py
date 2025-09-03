
import tkinter as tk
from tkcalendar import Calendar
import os
import json
from datetime import datetime, date
from journal import open_specific_journal

REMINDER_FILE = "reminders.json"

def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reminders(data):
    with open(REMINDER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def open_calendar_screen():
    cal_window = tk.Toplevel()
    cal_window.title("Mind Garden Calendar")
    cal_window.geometry("450x500")
    cal_window.configure(bg="#F0FFF0")

    reminders = load_reminders()

    tk.Label(cal_window, text="Select a Date", font=("Arial", 16, "bold"), bg="#F0FFF0").pack(pady=10)

    cal = Calendar(cal_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=10)

    today = date.today()
    cal.calevent_create(today, "Today", "today")
    cal.tag_config("today", background="#90EE90", foreground="black")

    def highlight_reminders():
        cal.calevent_remove(tag="reminder")
        for d, entries in reminders.items():
            if entries:
                try:
                    d_date = datetime.strptime(d, "%Y-%m-%d").date()
                    cal.calevent_create(d_date, "Reminder", "reminder")
                except Exception:
                    pass
        cal.tag_config("reminder", background="#ADD8E6", foreground="black")

    highlight_reminders()

    btn_frame = tk.Frame(cal_window, bg="#F0FFF0")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Open Journal", width=15, command=lambda: open_specific_journal(cal.get_date())).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Add Reminder", width=15, command=lambda: add_reminder()).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(btn_frame, text="View Reminders", width=15, command=lambda: view_reminders()).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="View All Reminders", width=15, command=lambda: view_all_reminders()).grid(row=1, column=1, padx=5, pady=5)

    def create_scrollable_frame(parent):
        canvas = tk.Canvas(parent, bg="#F0FFF0", highlightthickness=0)
        frame = tk.Frame(canvas, bg="#F0FFF0")
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0,0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        return frame

    def add_reminder():
        top = tk.Toplevel(cal_window)
        top.title("Add Reminder")
        top.geometry("300x250")
        top.configure(bg="#F0FFF0")

        tk.Label(top, text="Reminder Description:", bg="#F0FFF0").pack(pady=5)
        entry_desc = tk.Entry(top, width=35)
        entry_desc.pack(pady=5)

        tk.Label(top, text="Importance:", bg="#F0FFF0").pack(pady=5)
        importance_level = tk.StringVar(value="medium")
        tk.Radiobutton(top, text="High", variable=importance_level, value="high", bg="#F0FFF0").pack()
        tk.Radiobutton(top, text="Medium", variable=importance_level, value="medium", bg="#F0FFF0").pack()
        tk.Radiobutton(top, text="Low", variable=importance_level, value="low", bg="#F0FFF0").pack()

        def save():
            selected_date = cal.get_date()
            desc = entry_desc.get().strip()
            imp = importance_level.get()
            if not desc:
                return
            if selected_date not in reminders:
                reminders[selected_date] = []
            reminders[selected_date].append({
                "description": desc,
                "importance": imp
            })
            save_reminders(reminders)
            highlight_reminders()
            top.destroy()

        tk.Button(top, text="Save", command=save).pack(pady=10)

    def view_reminders():
        selected_date = cal.get_date()
        top = tk.Toplevel(cal_window)
        top.title(f"Reminders for {selected_date}")
        top.geometry("350x300")
        top.configure(bg="#F0FFF0")

        tk.Label(top, text=f"Reminders on {selected_date}:", font=("Arial", 12, "bold"), bg="#F0FFF0").pack(pady=10)

        entries = reminders.get(selected_date, [])
        if not entries:
            tk.Label(top, text="No reminders set.", bg="#F0FFF0").pack(pady=10)
            return

        importance_order = {"high": 0, "medium": 1, "low": 2}
        entries = sorted(entries, key=lambda r: importance_order.get(r.get("importance", "medium")))

        frame = create_scrollable_frame(top)

        for idx, r in enumerate(entries):
            r_frame = tk.Frame(frame, bd=1, relief="solid", padx=5, pady=5, bg="#E0FFFF")
            r_frame.pack(padx=5, pady=5, fill="x")
            text = f"({r['importance'].capitalize()}) {r['description']}"
            tk.Label(r_frame, text=text, wraplength=300, justify="left", bg="#E0FFFF").pack(anchor="w")

            btn_frame = tk.Frame(r_frame, bg="#E0FFFF")
            btn_frame.pack(pady=5)
            
            def edit_reminder(i=idx):
                edit_top = tk.Toplevel(top)
                edit_top.title("Edit Reminder")
                edit_top.geometry("300x220")
                edit_top.configure(bg="#F0FFF0")

                tk.Label(edit_top, text="Edit Description:", bg="#F0FFF0").pack(pady=5)
                entry = tk.Entry(edit_top, width=35)
                entry.insert(0, reminders[selected_date][i]['description'])
                entry.pack(pady=5)

                importance_level = tk.StringVar(value=reminders[selected_date][i].get("importance", "medium"))
                tk.Label(edit_top, text="Edit Importance:", bg="#F0FFF0").pack(pady=5)
                tk.Radiobutton(edit_top, text="High", variable=importance_level, value="high", bg="#F0FFF0").pack()
                tk.Radiobutton(edit_top, text="Medium", variable=importance_level, value="medium", bg="#F0FFF0").pack()
                tk.Radiobutton(edit_top, text="Low", variable=importance_level, value="low", bg="#F0FFF0").pack()

                def save_edit():
                    reminders[selected_date][i]['description'] = entry.get()
                    reminders[selected_date][i]['importance'] = importance_level.get()
                    save_reminders(reminders)
                    highlight_reminders()
                    edit_top.destroy()
                    top.destroy()
                    view_reminders()

                tk.Button(edit_top, text="Save Changes", command=save_edit).pack(pady=10)

            def delete_reminder(i=idx):
                del reminders[selected_date][i]
                if not reminders[selected_date]:
                    del reminders[selected_date]
                save_reminders(reminders)
                highlight_reminders()
                top.destroy()
                view_reminders()

            tk.Button(btn_frame, text="Edit", command=edit_reminder, width=8).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Delete", command=delete_reminder, width=8).pack(side="left", padx=5)

    def view_all_reminders():
        top = tk.Toplevel(cal_window)
        top.title("All Reminders")
        top.geometry("400x500")
        top.configure(bg="#F0FFF0")

        tk.Label(top, text="All Reminders", font=("Arial", 14, "bold"), bg="#F0FFF0").pack(pady=10)

        frame = create_scrollable_frame(top)

        all_dates = sorted(reminders.keys())
        for d in all_dates:
            for entry in reminders[d]:
                r_frame = tk.Frame(frame, bd=1, relief="solid", padx=5, pady=5, bg="#E0FFFF")
                r_frame.pack(padx=5, pady=5, fill="x")
                text = f"{d} - ({entry['importance'].capitalize()}) {entry['description']}"
                tk.Label(r_frame, text=text, wraplength=350, justify="left", bg="#E0FFFF").pack(anchor="w")