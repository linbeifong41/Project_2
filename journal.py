import tkinter as tk
from datetime import date 
from tkinter import scrolledtext
from utils import user_file_path
import os 


def open_journal_screen():
    journal_window = tk.Toplevel()
    journal_window.title("Mind Garden-journal")
    journal_window.geometry("600x500")
    journal_window.configure(bg="#F4f4F4")


    selected_filename = tk.StringVar(value="")


    sidebar = tk.Frame(journal_window, bg="#F4F4F4")
    sidebar.pack(side="left", fill="y", padx= 10, pady=10)

    search_entry = tk.Entry(sidebar, width=10, font=("Arial", 10))
    search_entry.pack(pady=(0, 5))
    search_entry.insert(0, "Search...")

    file_list = tk.Listbox(sidebar, width=30, height=6)
    file_list.pack()


    past_entry_box = scrolledtext.ScrolledText(sidebar, width=30, height= 15, font=("Arial", 10))
    past_entry_box.pack(pady=5)
    past_entry_box.config(state= tk.DISABLED)


    def list_journal_files(search_filter=""):
        files = [f for f in os.listdir(user_file_path("")) if f.startswith("journal_") and f.endswith(".txt")]
        filtered_files = [f for f in sorted(files, reverse=True) if search_filter.strip() == "" or search_filter.lower() in f.lower()]
        file_list.delete(0, tk.END)
        
        if filtered_files:
                for f in filtered_files:
    
                    file_list.insert(tk.END, f)

        else: 
             file_list.insert(tk.END, "No matching entries.")


    def show_past_entry(filename):
        if filename == "No matching entries":
            return 
    
        full_path = user_file_path(filename) 
        try:
            with open(full_path, "r", encoding="utf-8") as file:
                content = file.read()
                past_entry_box.config(state=tk.NORMAL)
                past_entry_box.delete("1.0", tk.END)
                past_entry_box.insert(tk.END, f"--- {filename} ---\n\n{content}")
                past_entry_box.config(state=tk.DISABLED)
                selected_filename.set(full_path)
                
        except FileNotFoundError:
            past_entry_box.config(state=tk.NORMAL)
            past_entry_box.delete("1.0", tk.END)
            past_entry_box.insert(tk.END, f"{filename} not found.\n")
            past_entry_box.config(state=tk.DISABLED)

    def on_file_select(event):
        selected = file_list.get(tk.ACTIVE)
        show_past_entry(selected)



    def enable_editing():
        if not selected_filename.get():
            return
        past_entry_box.config(state=tk.NORMAL)
        edit_btn.config(text="Save Edit", command=save_edited_entry)

    
    def save_edited_entry():
        if selected_filename.get():
            with open(selected_filename.get(), "w", encoding="utf-8") as file:
                content = past_entry_box.get("1.0", tk.END).strip()
                file.write(content)
            past_entry_box.config(state=tk.DISABLED)
            edit_btn.config(text="Edit Entry", command=enable_editing)
            print(f"{selected_filename.get()} Updated")


    file_list.bind("<<ListboxSelect>>", on_file_select)
    search_entry.bind("<KeyRelease>", lambda event: list_journal_files(search_entry.get()))


    
    view_btn = tk.Button(sidebar, text="View Past Entries", font=("Arial", 10), command=lambda: list_journal_files())
    view_btn.pack(pady=(5, 5)) 


    edit_btn = tk.Button(sidebar, text= "Edit Entry", font=("Arial", 10), command=enable_editing)
    edit_btn.pack(pady=(0, 5))


    top_frame = tk.Frame(journal_window, bg="#F4F4F4")
    top_frame.pack(side="top", fill="both", expand=True)
            
    heading = tk.Label(top_frame, text="Mind Garden Journal", font=("Arial", 18, "bold"), bg="#ECEBEB")
    heading.pack(pady=10)

    journal_label = tk.Label(top_frame, text="Write Your Entry Below:", bg="#F4FFE5", font=("Arial", 12))
    journal_label.pack()

    journal_box = scrolledtext.ScrolledText(top_frame, width=70, height=10, font=("Arial", 12), wrap=tk.WORD)
    journal_box.pack(pady=5)

    tag_label = tk.Label(top_frame, width=50, font=("Arial", 10))
    tag_label.pack()
    tag_entry = tk.Entry(top_frame, width=50, font=("Arial", 10))
    tag_entry.pack(pady=(0, 10))

    status_label = tk.Label(journal_window, text="", bg="#d6d5d5", font=("Arial", 10))
    status_label.pack()
    

    def save_journal():
        text = journal_box.get("1.0", tk.END).strip()
        if text:
            today = date.today().isoformat()
            filename = user_file_path(f"journal_{today}.txt") 

            os.makedirs(os.path.dirname(filename), exist_ok=True)
        
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)

            status_label.config(text=f"Saved to {filename}")
            print(f"Journal Saved To {filename}")
            list_journal_files()
        else: 
            status_label.config(text="Journal is empty.")


    def save_tags_only():
        tags = tag_entry.get().strip()
        today = date.today().isoformat()
        filename = user_file_path(f"journal_{today}.txt")

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()

            if lines and lines[0].startswith("[TAGS]:"):
                lines[0] = f"[TAGS]: {tags}\n"
            
            else: 
                lines.insert(0, f"[TAGS]: {tags}\n")

            with open(filename, "w", encoding="utf-8") as file:
                file.writelines(lines)

            status_label.config(text=f"Tags updated for {filename}")
            print(f"Updatedtags in {filename}")
            list_journal_files()


    save_btn = tk.Button(journal_window, text="Save Entry", bg="#F4F4F4", font=("Arial", 10), command=save_journal)
    save_btn.pack(pady=10)

    save_tags_btn = tk.Button(journal_window, text="Save Tags", bg="#F4F4F4", font=("Arial", 10), command=save_tags_only)
    save_tags_btn.pack(pady=(0, 10))

    status_label = tk.Label(journal_window, text="", bg="#d6d5d5", font=("Arial", 10))
    status_label.pack()

    list_journal_files()



def open_specific_journal(date_str):
    journal_window = tk.Toplevel()
    journal_window.title(f"Journal - {date_str}")
    journal_window.geometry("600x500")
    journal_window.configure(bg="#F4f4F4")

    filename = user_file_path(f"journal_{date_str}.txt")

    heading = tk.Label(journal_window, text=f"Journal for {date_str}", font=("Arial", 16, "bold"), bg="#ECEBEB")
    heading.pack(pady=10)

    journal_box = scrolledtext.ScrolledText(journal_window, width=70, height=20, font=("Arial", 12), wrap=tk.WORD)
    journal_box.pack(pady=10)

    
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            journal_box.insert(tk.END, file.read())

    def save_entry():
        content = journal_box.get("1.0", tk.END).strip()
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        status_label.config(text=f"Saved to {filename}")

    save_btn = tk.Button(journal_window, text="Save Entry", command=save_entry)
    save_btn.pack(pady=5)

    status_label = tk.Label(journal_window, text="", bg="#d6d5d5", font=("Arial", 10))
    status_label.pack()