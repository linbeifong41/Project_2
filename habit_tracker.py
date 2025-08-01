import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

LOG_FILE = "tech_habit_logs.json"

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_log(entry):
    logs = load_logs()
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def get_today_logs():
    today = datetime.now().date()
    logs = load_logs()
    return [
        log for log in logs
        if datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S").date() == today
    ]

def open_habit_tracker():
    window = tk.Toplevel()
    window.title("Tech Habit Tracker")
    window.geometry("550x600")

    selected_index = [None]  

    tk.Label(window, text="Tech Usage Entry:").pack(pady=(10, 0))
    usage_entry = tk.Entry(window, width=50)
    usage_entry.pack(pady=5)

    tk.Label(window, text="Was it intentional?").pack()
    intentional_var = tk.StringVar(value="Yes")
    intent_frame = tk.Frame(window)
    intent_frame.pack()
    tk.Radiobutton(intent_frame, text="Yes", variable=intentional_var, value="Yes").pack(side="left", padx=5)
    tk.Radiobutton(intent_frame, text="No", variable=intentional_var, value="No").pack(side="left", padx=5)

 
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    stats_frame = tk.LabelFrame(window, text="Today's Summary", padx=10, pady=5)
    stats_frame.pack(fill="x", padx=10, pady=(5, 10))

    total_label = tk.Label(stats_frame, text="Total: 0")
    total_label.pack(anchor="w")

    intentional_label = tk.Label(stats_frame, text="Intentional: 0")
    intentional_label.pack(anchor="w")

    unintentional_label = tk.Label(stats_frame, text="Unintentional: 0")
    unintentional_label.pack(anchor="w")

    percent_label = tk.Label(stats_frame, text="Mindful Usage: 0%")
    percent_label.pack(anchor="w")

    def refresh_logs():
        log_listbox.delete(0, tk.END)
        logs = load_logs()
        for log in reversed(logs):
            label = f"[{log['timestamp']}] {'✓' if log['intentional'] == 'Yes' else '✗'} - {log['usage']}"
            log_listbox.insert(tk.END, label)

        today_logs = get_today_logs()
        total = len(today_logs)
        intentional = sum(1 for log in today_logs if log["intentional"] == "Yes")
        unintentional = total - intentional
        percent = (intentional / total * 100) if total else 0

        total_label.config(text=f"Total: {total}")
        intentional_label.config(text=f"Intentional: {intentional}")
        unintentional_label.config(text=f"Unintentional: {unintentional}")
        percent_label.config(text=f"Mindful Usage: {percent:.0f}%")

        if percent >= 80:
            percent_label.config(fg="green")
        elif percent >= 50:
            percent_label.config(fg="orange")
        else:
            percent_label.config(fg="red")
            

    def submit_log():
        text = usage_entry.get().strip()
        if not text:
            messagebox.showwarning("Missing", "Please enter what you did.", parent=window)
            return

        entry = {
            "usage": text,
            "intentional": intentional_var.get(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        logs = load_logs()
        logs.append(entry)
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)
        usage_entry.delete(0, tk.END)
        refresh_logs()
        messagebox.showinfo("Saved", "Your tech habit was logged.", parent=window)

    def delete_log():
        index = log_listbox.curselection()
        if not index:
            return
        actual_index = len(load_logs()) - 1 - index[0]
        logs = load_logs()
        if messagebox.askyesno("Delete", "Are you sure you want to delete this log?", parent=window):
            logs.pop(actual_index)
            with open(LOG_FILE, "w") as f:
                json.dump(logs, f, indent=4)
            usage_entry.delete(0, tk.END)
            selected_index[0] = None
            refresh_logs()

    def load_selected():
        index = log_listbox.curselection()
        if not index:
            return
        actual_index = len(load_logs()) - 1 - index[0]
        logs = load_logs()
        log = logs[actual_index]
        usage_entry.delete(0, tk.END)
        usage_entry.insert(0, log["usage"])
        intentional_var.set(log["intentional"])
        selected_index[0] = actual_index

    def save_edit():
        idx = selected_index[0]
        if idx is None:
            messagebox.showwarning("No Selection", "Select a log to edit first.", parent=window)
            return

        logs = load_logs()
        logs[idx]["usage"] = usage_entry.get().strip()
        logs[idx]["intentional"] = intentional_var.get()

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)
        messagebox.showinfo("Saved", "Changes saved.", parent=window)
        usage_entry.delete(0, tk.END)
        selected_index[0] = None
        refresh_logs()

   
    tk.Button(button_frame, text="Add Entry", command=submit_log).pack(side="left", padx=5)
    tk.Button(button_frame, text="Save Changes", command=save_edit).pack(side="left", padx=5)
    tk.Button(button_frame, text="Delete Entry", command=delete_log).pack(side="left", padx=5)

  
    tk.Label(window, text="Past Logs:").pack(pady=(10, 0))
    log_frame = tk.Frame(window)
    log_frame.pack(fill="both", expand=True, padx=10, pady=5)

    log_listbox = tk.Listbox(log_frame, height=15)
    log_listbox.pack(fill="both", expand=True)
    log_listbox.bind("<<ListboxSelect>>", lambda e: load_selected())

    refresh_logs()