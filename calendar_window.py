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

            text = f"({r['type']}) {r['description']}"
            tk.Label(r_frame, text=text, wraplength=250, justify="left").pack(anchor='w')


            def edit_reminder(i=idx):
                edit_top = tk.Toplevel(top)
                edit_top.title("Edit Reminder")
                edit_top.geometry("300x200")

                tk.Label(edit_top, text="Edit Description:").pack(pady=5)
                entry = tk.Entry(edit_top, width=30)
                entry.insert(0, reminders[selected_date][i]['description'])
                entry.pack(pady=5)

                reminder_type = tk.StringVar(value=reminders[selected_date][i]['type'])
                tk.Radiobutton(edit_top, text="Assignment", variable=reminder_type, value="assignment").pack()
                tk.Radiobutton(edit_top, text="Exam", variable=reminder_type, value="exam").pack()

                def save_edit():
                    reminders[selected_date][i]['description'] = entry.get()
                    reminders[selected_date][i]['type'] = reminder_type.get()
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



    def open_journal_for_date():
        selected_date = cal.get_date()
        open_specific_journal(selected_date)

    tk.Button(cal_window, text="Open Journal", command=open_journal_for_date).pack(pady=5)
    tk.Button(cal_window, text="Add Reminder", command=add_reminder).pack(pady=5)
    tk.Button(cal_window, text="View Reminders", command=view_reminders).pack(pady=5)

    

