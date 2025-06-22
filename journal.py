import tkinter as tk
from datetime import date 
from tkinter import scrolledtext
import os 


def open_journal_screen():
    journal_window = tk.Toplevel()
    journal_window.title("Mind Garden-journal")
    journal_window.geometry("600x500")
    journal_window.configure(bg="#F4f4F4")



    sidebar = tk.Frame(journal_window, bg="#F4F4F4")
    sidebar.pack(side="left", fill="y", padx= 10, pady=10)

    view_frame = tk.Frame(sidebar, bg="#F4F4F4")
    view_frame.pack(side="bottom", fill="y")

    view_btn = tk.Button(sidebar, text="View Past Entries", font=("Arial", 10), command=lambda: list_journal_files())
    view_btn.pack(pady=(0, 10)) 


    
    file_list = tk.Listbox(sidebar, width=30, height=6)
    file_list.pack()
    file_list.bind("<<ListboxSelect>>", lambda e: show_past_entry(file_list.get(tk.ACTIVE)))



    past_entry_box = scrolledtext.ScrolledText(sidebar, width=30, height= 15, font=("Arial", 10))
    past_entry_box.pack(pady=5)
    past_entry_box.config(state= tk.DISABLED)



    def list_journal_files():
        files = [f for f in os.listdir() if f.startswith("journal_") and f.endswith(".txt")]
        file_list.delete(0, tk.END)
        for f in sorted(files, reverse=True):
            file_list.insert(tk.END, f)

    def show_past_entry(filename):
        try:
             with open(filename, "r", encoding="utf-8", ) as file:
                content = file.read()
                past_entry_box.config(state=tk.NORMAL)
                past_entry_box.delete("1.0", tk.END)
                past_entry_box.insert(tk.END, f"--- {filename} ---\n\n{content}")
                past_entry_box.config(state=tk.DISABLED)

        except FileNotFoundError:
            past_entry_box.config(state=tk.NORMAL)
            past_entry_box.insert(tk.END, f"{filename} not found.\n")
            past_entry_box.config(state=tk.DISABLED)


    top_frame = tk.Frame(journal_window, bg="#F4F4F4")
    top_frame.pack(side="top", fill="both", expand=True)
            
    heading = tk.Label(top_frame, text="Mind Garden Journal", font=("Arial", 18, "bold"), bg="#ECEBEB")
    heading.pack(pady=10)

    journal_label = tk.Label(top_frame, text="Write Your Entry Below:", bg="#F4FFE5", font=("Arial", 12))
    journal_label.pack()

    journal_box = scrolledtext.ScrolledText(top_frame, width=70, height=10, font=("Arial", 12), wrap=tk.WORD)
    journal_box.pack(pady=5)
    

    def save_journal():
        text = journal_box.get("1.0", tk.END).strip()
        if text:
            today = date.today().isoformat()
            filename = f"journal_{today}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text)
            status_label.config(text=f"Saved to {filename}")
            print(f"Journal Saved To {filename}")
        else: 
            status_label.config(text="Journal is empty.")


    save_btn = tk.Button(journal_window, text="Save Entry", bg="#F4F4F4", font=("Arial", 10), command=save_journal)
    save_btn.pack(pady=10)

    status_label = tk.Label(journal_window, text="", bg="#d6d5d5", font=("Arial", 10))
    status_label.pack()
    





 




