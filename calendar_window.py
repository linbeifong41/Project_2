import tkinter as tk
from tkcalendar import Calendar
import os
import json
from journal import open_specific_journal
from datetime import datetime, date


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

    cal_window = tk.Toplevel()
    cal_window.title("Mind Garden Calendar")
    cal_window.geometry("400x400")
    cal_window.configure(bg="#F0FFF0")

    reminders = load_reminders()

    label = tk.Label(cal_window, text="select a Date", font=("Arial", 14), bg="#F0FFF0")
    label.pack(pady=10)

    cal = Calendar(cal_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)

    today = date.today()
    cal.calevent_create(today, "Today", "today")
    cal.tag_config("today", background="lightgreen", foreground="black")


    def highlight_reminders():

        cal.calevent_remove(tag="reminder")

        for d, entries in reminders.items():
            if entries:
                try:
                    d_date = datetime.strptime(d, "%Y-%m-%d").date()
                    cal.calevent_create(d_date, "Reminder", "reminder")
                except Exception:
                    pass
        cal.tag_config("reminder", background="lightblue", foreground="black")


    highlight_reminders()

    def add_reminder():

        top = tk.Toplevel(cal_window)
        top.title("Add Reminder")
        top.geometry("200x300")

        tk.Label(top, text="Reminder Description:").pack(pady=5)
        entry_desc = tk.Entry(top, width=30)
        entry_desc.pack(pady=5)

        tk.Label(top, text="Importance:").pack(pady=5)
        importance_level = tk.StringVar(value="medium")
        tk.Radiobutton(top, text="High 🔴", variable=importance_level, value="high").pack()
        tk.Radiobutton(top, text="Medium 🟡", variable=importance_level, value="medium").pack()
        tk.Radiobutton(top, text="Low 🟢", variable=importance_level, value="low").pack()


        def save():

            selected_date = cal.get_date()
            desc = entry_desc.get().strip()
            imp = importance_level.get()

            if not desc:
                return 
            if selected_date not in reminders:
                reminders[selected_date] = []

            reminders[selected_date].append({
                "description" : desc, 
                "importance": imp
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

        importance_order = {"high": 0, "medium": 1, "low": 2}
        entries = sorted(reminders.get(selected_date, []), key=lambda r: importance_order.get(r.get("importance", "medium")))

        if not entries:
            tk.Label(top, text="No reminders set.").pack()
            return 
        

        canvas = tk.Canvas(top)
        frame = tk.Frame(canvas)
        scrollbar = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)


        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")


        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)

        for idx, r in enumerate(entries):
            r_frame = tk.Frame(frame, bd=1, relief="solid", padx=5, pady=5)
            r_frame.pack(padx=5, pady=5, fill="x")

            text = f"({r['importance'].capitalize()}) {r['description']}"
            tk.Label(r_frame, text=text, wraplength=250, justify="left").pack(anchor='w')


            def edit_reminder(i=idx):
                edit_top = tk.Toplevel(top)
                edit_top.title("Edit Reminder")
                edit_top.geometry("300x200")

                tk.Label(edit_top, text="Edit Description:").pack(pady=5)
                entry = tk.Entry(edit_top, width=30)
                entry.insert(0, reminders[selected_date][i]['description'])
                entry.pack(pady=5)

                importance_level = tk.StringVar(value=reminders[selected_date][i].get("importance", "medium"))
                tk.Label(edit_top, text="Edit Importance:").pack(pady=5)
                tk.Radiobutton(edit_top, text="High 🔴", variable=importance_level, value="high").pack()
                tk.Radiobutton(edit_top, text="Medium 🟡", variable=importance_level, value="medium").pack()
                tk.Radiobutton(edit_top, text="Low 🟢", variable=importance_level, value="low").pack()

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
                if selected_date in reminders:
                    del reminders[selected_date][i]
                    if not reminders[selected_date]:
                        del reminders[selected_date]
                    save_reminders(reminders)
                    highlight_reminders()
                    top.destroy()
                    view_reminders()

                    
            btn_frame = tk.Frame(r_frame)
            btn_frame.pack(pady=5)

            tk.Button(btn_frame, text="Edit", command=edit_reminder).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Delete", command=delete_reminder).pack(side="left", padx=5)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))



    def open_journal_for_date():
        selected_date = cal.get_date()
        open_specific_journal(selected_date)

    def view_all_reminders():
        top = tk.Toplevel(cal_window)
        top.title("All Reminders")
        top.geometry("400x500")

        tk.Label(top, text="All Reminders", font=("Arial", 14)).pack(pady=10)

        canvas = tk.Canvas(top)
        frame = tk.Frame(canvas)
        scrollbar = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0,0), window=frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)

        all_dates = sorted(reminders.keys())

        for d in all_dates:
            entry_list = reminders[d]
            for entry in entry_list:
                r_frame = tk.Frame(frame, bd=1, relief="solid", padx=5, pady=5)
                r_frame.pack(padx=5, pady=5, fill="x")
                text = f"{d} - ({entry['importance'].capitalize()}) {entry['description']}"
                tk.Label(r_frame, text=text, wraplength=350, justify="left").pack(anchor="w")

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


    tk.Button(cal_window, text="Open Journal", command=open_journal_for_date).pack(pady=5)
    tk.Button(cal_window, text="Add Reminder", command=add_reminder).pack(pady=5)
    tk.Button(cal_window, text="View Reminders", command=view_reminders).pack(pady=5)
    tk.Button(cal_window, text="View All Reminders", command=view_all_reminders).pack(pady=5)



    tk.Label(cal_window, text="🟢 = Today 🔵 = Reminder", font=("Arial", 10), bg="#F0FFF0").pack(pady=5)

    

