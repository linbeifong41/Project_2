import tkinter as tk
from datetime import date 
from tkinter import scrolledtext


def open_journal_screen():
    journal_window = tk.Toplevel()
    journal_window.title("Mind Garden-journal")
    journal_window.geometry("600x500")
    journal_window.configure(bg="#F4f4F4")

    heading =  tk.Label(journal_window, text="Write Your Journal", font=("Arial", 18, "bold"), bg="#ECEBEB")
    heading.pack(pady=10)

    journal_box = scrolledtext.ScrolledText(journal_window, width=70, height=20, font=("Arial", 12), wrap=tk.WORD)
    journal_box.pack(pady=10)
    

    def save_journal():
        text = journal_box.get("1.0", tk.END).strip()
        if text:
            today = date.today().isoformat()
            filename = f"journal_{today}.txt"
            with open(filename, "w", encoding="UTF-8") as file:
                file.write(text)
            status_label.config(text=f"Saved to {filename}")
            print(f"Journal Saved To {filename}")
        else: 
            status_label.config(text="Journal is empty.")
    save_btn = tk.Button(journal_window, text="Save Entry", bg="#F4F4F4", font=("Arial", 10), command=save_journal)
    save_btn.pack(pady=10)

    status_label = tk.Label(journal_window, text="", bg="#d6d5d5", font=("Arial", 10))
    status_label.pack()


        

