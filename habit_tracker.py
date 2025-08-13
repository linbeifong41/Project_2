import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime
from collections import Counter
from datetime import timedelta

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

def get_clean_streak():
    logs = load_logs()

 
    daily_logs = {}
    for log in logs:
        date_str = log["timestamp"].split()[0]
        daily_logs.setdefault(date_str, []).append(log)


    sorted_dates = sorted(daily_logs.keys(), reverse=True)

    streak = 0
    for date_str in sorted_dates:
        day_logs = daily_logs[date_str]
        if any(log["intentional"] == "No" for log in day_logs):
            break  
        streak += 1

    return streak

REFLECTION_FILE = "reflection_notes.json"

def open_reflection_window():
    window = tk.Toplevel()
    window.title("Reflection & Insights")
    window.geometry("700x600")

    logs = load_logs()

    today = datetime.now().date()
    start_date = today - timedelta(days=30)

    recent_logs = [
        log for log in logs 
        if start_date <= datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S").date() <= today
    ]

    total_logs = len(recent_logs)
    intentional_count = sum(1 for log in recent_logs if log["intentional"] == "Yes")
    unintentional_count = total_logs - intentional_count
    intentional_pct = (intentional_count / total_logs * 100) if total_logs else 0

    words = []
    for log in recent_logs:
        words.extend(log["usage"].lower().split())
        words.extend(log.get("notes", "").lower().split())
    word_counts = Counter(words).most_common(5)

    hours = [datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S").hour for log in recent_logs]
    hour_counts = Counter(hours).most_common(3)

    summary_frame = tk.Frame(window)
    summary_frame.pack(pady=10, padx=10, fill="x")

    tk.Label(summary_frame, text=f"Logs in last 30 days: {total_logs}").pack(anchor="w")
    tk.Label(summary_frame, text=f"Intentional usage: {intentional_count} ({intentional_pct:.1f}%)").pack(anchor="w")
    tk.Label(summary_frame, text=f"Unintentional usage: {unintentional_count}").pack(anchor="w")

    tk.Label(summary_frame, text="Top 5 most common words:").pack(anchor="w")
    for word, count in word_counts:
        tk.Label(summary_frame, text=f"- {word}: {count}").pack(anchor="w")

    tk.Label(summary_frame, text="Top 3 peak usage hours:").pack(anchor="w")
    for hour, count in hour_counts:
        tk.Label(summary_frame, text=f"- {hour}:00 — {count} uses").pack(anchor="w")

    tk.Label(window, text="Your Reflection Notes (saved per day):").pack(anchor="w", padx=10, pady=(10,0))

    reflection_text = tk.Text(window, height=8, width=80)
    reflection_text.pack(padx=10, pady=5)

    def load_reflection():
        if os.path.exists(REFLECTION_FILE):
            with open(REFLECTION_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_reflection(text):
        reflections = load_reflection()
        date_key = today.strftime("%Y-%m-%d")
        reflections[date_key] = text
        with open(REFLECTION_FILE, "w") as f:
            json.dump(reflections, f, indent=4)

    reflections = load_reflection()
    reflection_text.insert(tk.END, reflections.get(today.strftime("%Y-%m-%d"), ""))

    def save_reflection_cmd():
        text = reflection_text.get("1.0", tk.END).strip()
        save_reflection(text)
        messagebox.showinfo("Saved", "Reflection notes saved.", parent=window)

    save_btn = tk.Button(window, text="Save Reflection Notes", command=save_reflection_cmd)
    save_btn.pack(pady=(0, 10))

    def export_report():
        lines = [
            f"Reflection Report for {today.strftime('%Y-%m-%d')}\n",
            f"Total logs in last 30 days: {total_logs}",
            f"Intentional usage: {intentional_count} ({intentional_pct:.1f}%)",
            f"Unintentional usage: {unintentional_count}\n",
            "Top 5 most common words:"
        ]
        for word, count in word_counts:
            lines.append(f"- {word}: {count}")
        lines.append("\nTop 3 peak usage hours:")
        for hour, count in hour_counts:
            lines.append(f"- {hour}:00 — {count} uses")
        lines.append("\nYour Reflection Notes:")
        lines.append(reflection_text.get("1.0", tk.END).strip())

        filename = f"reflection_report_{today.strftime('%Y%m%d')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        messagebox.showinfo("Exported", f"Report exported to {filename}", parent=window)

    export_btn = tk.Button(window, text="Export Reflection Report to TXT", command=export_report)
    export_btn.pack(pady=(0,10))


def open_streak_badges():
    streak = get_clean_streak()
    
    badges = [
        {"days": 3, "name": "Bronze Badge"},
        {"days": 7, "name": "Silver Badge"},
        {"days": 14, "name": "Gold Badge"},
        {"days": 30, "name": "Platinum Badge"},
    ]
    
    window = tk.Toplevel()
    window.title("Streak Badges")
    window.geometry("500x200")
    
    tk.Label(window, text=f"Current Clean Streak: {streak} day{'s' if streak != 1 else ''}", font=("Arial", 12, "bold")).pack(pady=10)
    
    badge_frame = tk.Frame(window)
    badge_frame.pack(pady=10)
    
    for badge in badges:
        unlocked = streak >= badge["days"]
        color = "green" if unlocked else "gray"
        
        frame = tk.Frame(badge_frame, width=100, height=100)
        frame.pack(side="left", padx=10)
        frame.pack_propagate(False)
        
        canvas = tk.Canvas(frame, width=80, height=80)
        canvas.pack()
        canvas.create_oval(10, 10, 70, 70, fill=color, outline="black")
        canvas.create_text(40, 40, text=str(badge["days"]), font=("Arial", 12, "bold"), fill="white")
        
        tk.Label(frame, text=badge["name"], font=("Arial", 10)).pack(pady=2)
        
        def make_hover_text(b=badge, u=unlocked):
            def on_enter(event):
                msg = f"Requires {b['days']} day{'s' if b['days'] != 1 else ''} streak.\n"
                msg += "Unlocked!" if u else f"{b['days'] - streak} day{'s' if b['days'] - streak != 1 else ''} to unlock."
                tooltip_label.config(text=msg)
            return on_enter

        canvas.bind("<Enter>", make_hover_text())
    
    tooltip_label = tk.Label(window, text="", font=("Arial", 10), fg="blue")
    tooltip_label.pack(pady=5)



def open_habit_tracker():
    window = tk.Toplevel()
    window.title("Tech Habit Tracker")
    window.geometry("650x750")

    selected_index = [None]


    tk.Label(window, text="Tech Usage Entry:").pack(pady=(10, 0))
    usage_entry = tk.Entry(window, width=50)
    usage_entry.pack(pady=5)

    tk.Label(window, text="Notes / Journal:").pack()
    notes_text = tk.Text(window, width=50, height=4)
    notes_text.pack(pady=5)

    tk.Label(window, text="Keywords (comma-separated):").pack()
    keywords_entry = tk.Entry(window, width=50)
    keywords_entry.pack(pady=5)

    tk.Label(window, text="Date (YYYY-MM-DD) [optional]:").pack()
    date_input_entry = tk.Entry(window, width=20)
    date_input_entry.pack(pady=5)

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
    streak_label = tk.Label(stats_frame, text="Clean Streak: 0 days")
    streak_label.pack(anchor="w", pady=1)

    filter_frame = tk.LabelFrame(window, text="Search & Filter")
    filter_frame.pack(fill="x", padx=10, pady=(0, 5))

    tk.Label(filter_frame, text="Keyword:").grid(row=0, column=0, padx=5, pady=2)
    keyword_var = tk.StringVar()
    keyword_entry = tk.Entry(filter_frame, textvariable=keyword_var, width=15)
    keyword_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(filter_frame, text="Intention:").grid(row=0, column=2, padx=5, pady=2)
    intention_filter_var = tk.StringVar(value="All")
    intention_dropdown = ttk.Combobox(filter_frame, textvariable=intention_filter_var,
                                      values=["All", "Yes", "No"], width=8, state="readonly")
    intention_dropdown.grid(row=0, column=3, padx=5, pady=2)

    tk.Label(filter_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=2)
    date_var = tk.StringVar()
    date_entry = tk.Entry(filter_frame, textvariable=date_var, width=12)
    date_entry.grid(row=0, column=5, padx=5, pady=2)

    def apply_filters(logs):
        keyword = keyword_var.get().strip().lower()
        intention_filter = intention_filter_var.get()
        date_filter = date_var.get().strip()

        filtered = []
        for log in logs:
            if keyword:
                in_usage = keyword in log["usage"].lower()
                in_notes = keyword in log.get("notes", "").lower()
                in_keywords = keyword in " ".join(log.get("keywords", [])).lower()
                if not (in_usage or in_notes or in_keywords):
                    continue
            if intention_filter != "All" and log["intentional"] != intention_filter:
                continue
            if date_filter and not log["timestamp"].startswith(date_filter):
                continue
            filtered.append(log)
        return filtered

    def refresh_logs():
        log_listbox.delete(0, tk.END)
        logs = load_logs()
        logs = apply_filters(logs)

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

        streak = get_clean_streak()
        streak_label.config(text=f"Clean Streak: {streak} day{'s' if streak != 1 else ''}")

    def submit_log():
        text = usage_entry.get().strip()
        notes = notes_text.get("1.0", tk.END).strip()
        keywords = [kw.strip() for kw in keywords_entry.get().split(",") if kw.strip()]
        date_str = date_input_entry.get().strip()

        if not text:
            messagebox.showwarning("Missing", "Please enter what you did.", parent=window)
            return

        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                timestamp = f"{date_str} {datetime.now().strftime('%H:%M:%S')}"
            except ValueError:
                messagebox.showwarning("Invalid Date", "Date must be in YYYY-MM-DD format.", parent=window)
                return
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entry = {
            "usage": text,
            "notes": notes,
            "keywords": keywords,
            "intentional": intentional_var.get(),
            "timestamp": timestamp
        }

        save_log(entry)
        usage_entry.delete(0, tk.END)
        notes_text.delete("1.0", tk.END)
        keywords_entry.delete(0, tk.END)
        date_input_entry.delete(0, tk.END)
        refresh_logs()
        messagebox.showinfo("Saved", "Your tech habit was logged.", parent=window)

    def delete_log():
        index = log_listbox.curselection()
        if not index:
            return
        actual_index = len(apply_filters(load_logs())) - 1 - index[0]
        logs = load_logs()
        if messagebox.askyesno("Delete", "Are you sure you want to delete this log?", parent=window):
            logs.pop(actual_index)
            with open(LOG_FILE, "w") as f:
                json.dump(logs, f, indent=4)
            usage_entry.delete(0, tk.END)
            notes_text.delete("1.0", tk.END)
            keywords_entry.delete(0, tk.END)
            date_input_entry.delete(0, tk.END)
            selected_index[0] = None
            refresh_logs()

    def load_selected():
        index = log_listbox.curselection()
        if not index:
            return
        actual_index = len(apply_filters(load_logs())) - 1 - index[0]
        logs = apply_filters(load_logs())
        log = logs[actual_index]
        usage_entry.delete(0, tk.END)
        usage_entry.insert(0, log["usage"])
        notes_text.delete("1.0", tk.END)
        notes_text.insert(tk.END, log.get("notes", ""))
        keywords_entry.delete(0, tk.END)
        keywords_entry.insert(0, ", ".join(log.get("keywords", [])))
        date_input_entry.delete(0, tk.END)
        date_input_entry.insert(0, log["timestamp"].split()[0])
        intentional_var.set(log["intentional"])
        selected_index[0] = actual_index

    def save_edit():
        idx = selected_index[0]
        if idx is None:
            messagebox.showwarning("No Selection", "Select a log to edit first.", parent=window)
            return

        logs = load_logs()
        logs[idx]["usage"] = usage_entry.get().strip()
        logs[idx]["notes"] = notes_text.get("1.0", tk.END).strip()
        logs[idx]["keywords"] = [kw.strip() for kw in keywords_entry.get().split(",") if kw.strip()]
        logs[idx]["intentional"] = intentional_var.get()
        date_str = date_input_entry.get().strip()
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                logs[idx]["timestamp"] = f"{date_str} {logs[idx]['timestamp'].split()[1]}"
            except ValueError:
                messagebox.showwarning("Invalid Date", "Date must be in YYYY-MM-DD format.", parent=window)
                return

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)
        messagebox.showinfo("Saved", "Changes saved.", parent=window)
        usage_entry.delete(0, tk.END)
        notes_text.delete("1.0", tk.END)
        keywords_entry.delete(0, tk.END)
        date_input_entry.delete(0, tk.END)
        selected_index[0] = None
        refresh_logs()

    tk.Button(button_frame, text="Add Entry", command=submit_log).pack(side="left", padx=5)
    tk.Button(button_frame, text="Save Changes", command=save_edit).pack(side="left", padx=5)
    tk.Button(button_frame, text="Delete Entry", command=delete_log).pack(side="left", padx=5)
    tk.Button(button_frame, text="Open Reflection & Insights", command=open_reflection_window).pack(side="left", padx=5)
    tk.Button(button_frame, text="View Streak Badges", command=open_streak_badges).pack(side="left", padx=5)



    tk.Label(window, text="Past Logs:").pack(pady=(10, 0))
    log_frame = tk.Frame(window)
    log_frame.pack(fill="both", expand=True, padx=10, pady=5)

    log_listbox = tk.Listbox(log_frame, height=15)
    log_listbox.pack(fill="both", expand=True)
    log_listbox.bind("<<ListboxSelect>>", lambda e: load_selected())

    tk.Button(filter_frame, text="Apply Filters", command=refresh_logs).grid(row=0, column=6, padx=5)

    refresh_logs()