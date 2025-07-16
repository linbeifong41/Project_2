import tkinter as tk
import json
from datetime import datetime
from tkinter import ttk, simpledialog, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from  datetime import date


def todo_list():
    window = tk.Toplevel()
    window.title("To-Do List")
    window.geometry("350x500")
    window.configure(bg="#F5FFFA")

    task_var = tk.StringVar()
    date_var = tk.StringVar()
    time_var = tk.StringVar()
    category_var = tk.StringVar(value="General")
    
    tasks= []

    
    def save_tasks():
        with open("todo.txt", "w", encoding="utf-8") as f:
             json.dump(tasks, f)
    

      
    def load_tasks():
        try:
            with open("todo.txt", "r", encoding="utf-8") as f:
                return json.load(f)
            
        except:
            return []
        
    def update_filter_options():
         filter_dropdown['values'] = ["ALL"] + list(set([task.get("category", "General") for task in tasks]))

        

    canvas = tk.Canvas(window, bg="#F5FFFA", highlightthickness=0)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#F5FFFA")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    task_list_frame = scrollable_frame

    search_var = tk.StringVar()

    def render_tasks():
        for widget in task_list_frame.winfo_children():
            widget.destroy()

        selected_filter = filter_var.get()

        for i, task in enumerate(tasks):
            if selected_filter != "ALL" and task.get("category", "General") != selected_filter:
                continue

            search_text = search_var.get().lower()
            if search_text:
                    search_terms = search_text.lower().split()
                    match = True 

                    for term in search_terms:
                        if term.startswith("cat:"):
                            if task.get("category", "").lower() != term[4:]:
                                match = False 
                                break
                        elif term.startswith("date:"): 
                            if task.get()

                    continue

            task_frame = tk.Frame(task_list_frame, bg="#F5FFFA")
            task_frame.pack(fill="x", pady=2)

            var = tk.BooleanVar(value=task["done"])

            def toggle_done(index=i, var=var):
                tasks[index]["done"] = var.get()
                render_tasks()
                save_tasks()


            check = tk.Checkbutton(task_frame, variable=var, command=toggle_done)
            check.pack(side="left")

            display_text = task["text"]
            if "due" in task and task["due"]:
                display_text += f" -Due: {task['due']}"

            if "category" in task and task["category"]:
                display_text += f"[{task['category']}]"

            if task["done"]:
                display_text = f"\u0336".join(display_text) + "\u0336" 

            label = tk.Label(task_frame, text=display_text, anchor="w", bg="#F5FFFA")
            label.pack(side="left", fill="x", expand=True)


            def delete_task(index=i):
                tasks.pop(index)
                render_tasks()
                save_tasks()
                update_filter_options()

            def edit_task(index=i):
                current = tasks[index]

                popup = tk.Toplevel(window)
                popup.title("Edit Task")
                popup.geometry("300x250")
                popup.configure(bg="#FAFAD2")

                new_text_var = tk.StringVar(value=current["text"])
                new_date_var = tk.StringVar(value=current.get("due", "").split()[0] if "due" in current else "")
                new_time_var = tk.StringVar(value=current.get("due", "").split()[1] if "due" in current and " " in current["due"] else "")
                new_cat_var = tk.StringVar(value=current.get("category", "General"))

                tk.Label(popup, text="Task:", bg="#FAFAD2").pack(anchor="w", padx=10, pady=(10,0))
                tk.Entry(popup, textvariable=new_text_var, width=30).pack(padx=10)

                tk.Label(popup, text="Date (YYYY-MM-DD):", bg="#FAFAD2").pack(anchor="w", padx=10, pady=(10,0))
                DateEntry(popup, textvariable=new_date_var, date_pattern='yyyy-mm-dd', background="darkblue", foreground="white", 
                    borderwidth=2, year=date.today().year, mindate=date(2000, 1, 1), maxdate=date(2100, 12, 31)).pack(padx=10)

                tk.Label(popup, text="Time (HH:MM):", bg="#FAFAD2").pack(anchor="w", padx=10, pady=(10,0))
                ttk.Combobox(popup, textvariable=new_time_var, values=generate_time_options(), width=20).pack(padx=10)

                tk.Label(popup, text="Category:", bg="#FAFAD2").pack(anchor="w", padx=10, pady=(10,0))
                tk.Entry(popup, textvariable=new_cat_var).pack(padx=10)                

                def save_edit():
                    current["text"] = new_text_var.get().strip()
                    new_due = new_date_var.get().strip()
                    if new_time_var.get().strip():
                        new_due += f" {new_time_var.get().strip()}"
                    current["due"] = new_due.strip()
                    current["category"] = new_cat_var.get().strip() if new_cat_var.get().strip() else "General"


                    save_tasks()
                    update_filter_options()
                    render_tasks()
                    popup.destroy()


                tk.Button(popup, text="Save", command=save_edit, bg="#90EE90").pack(pady=10)
                tk.Button(popup, text="Cancel", command=popup.destroy, bg="#FFC0CB").pack(pady=5)
            
            tk.Button(task_frame, text="Edit", command=edit_task, width=4, bg="#FFFFCC").pack(side="right", padx=2)
            
            delete_btn =  tk.Button(task_frame, text="X", fg="red", command=delete_task, width=2)
            delete_btn.pack(side="right")
        
    def add_task(event=None):
        text = task_var.get().strip()
        due_date = date_var.get().strip()
        due_time = time_var.get().strip()
        category = category_var.get().strip()

        if text:
            due_str = ""
            if due_date:
                due_str = due_date
                if due_time:
                    due_str += f" {due_time}"
            task = {"text": text, "done": False, "category": category}
            if due_str:
                task["due"] = due_str

            tasks.append(task)
            task_var.set("")
            date_var.set("")
            time_var.set("")
            save_tasks()
            render_tasks()
            update_filter_options()


    def add_category():
        new_cat = simpledialog.askstring("New Category", "Enter Category name:")
        if new_cat and new_cat not in category_list:
            category_list.append(new_cat)
            category_dropdown['values'] = category_list
            category_var.set(new_cat)

            update_filter_options()
            render_tasks()

    def generate_time_options():
        times =[]
        for hour in range(24):
            for minute in (0, 15, 30, 45):
                times.append(f"{hour:02}:{minute:02}")
        return times
    



    input_frame = tk.Frame(window, bg="#F5FFFA")
    input_frame.pack( fill="x", padx=5, pady=10)



    tk.Label(input_frame, text="Task:", bg="#F5FFFA").grid(row=1, column=0, padx=5, sticky="e" )
    task_entry = tk.Entry(input_frame, textvariable=task_var, width=25)
    task_entry.grid(row=0, column=1, columnspan=3, pady=2, sticky="w")
    task_entry.bind("<Return>", add_task)


    tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg="#F5FFFA").grid(row=1, column=0, padx=5, sticky="e")
    date_entry = DateEntry(input_frame, textvariable=date_var, width=15, date_pattern='yyyy-mm-dd', background="darkblue", 
        foreground="white",  borderwidth=2, year=date.today().year, mindate=date(2000,1, 1), maxdate=date(2100, 12, 31))
    
    date_entry.grid(row=1, column=1, pady=2, sticky="w")


    tk.Label(input_frame, text="Time (HH:MM):", bg="#F5FFFA").grid(row=1, column=2, padx=5, sticky="e" )
    time_entry = ttk.Combobox(input_frame, textvariable=time_var, values=generate_time_options(), width=10)
    time_entry.grid(row=1, column=3, pady=10, sticky="e")


    category_list = ["General", "Work", "School", "Self-care", "Errands", "Health", "Creative" ]
    category_var = tk.StringVar(value="General")

    tk.Label(input_frame, text="Category", bg="#F5FFFA").grid(row=2, column=0, padx=5, sticky="e")
    category_dropdown = ttk.Combobox(input_frame, textvariable=category_var, values=category_list, width=15)
    
    category_dropdown.grid(row=2, column=1, pady=2, sticky="w")

    tk.Button(input_frame, text="+", command=add_category, bg="#D3FFD3").grid(row=2, column=2, padx=2, sticky="w")

    add_btn = tk.Button(input_frame, text="Add", command=add_task, bg="#90EE90")
    add_btn.grid(row=2, column=3, pady=10, sticky="e")

    filter_var = tk.StringVar(value="ALL")
    filter_dropdown = ttk.Combobox(window, textvariable=filter_var, values=["ALL"] + category_list, width=20)
    filter_dropdown.pack(pady=5)
    filter_dropdown.bind("<<ComboboxSelected>>", lambda e: render_tasks())

    search_frame = tk.Frame(window, bg="#F5FFFA")
    search_frame.pack(pady=2)

    tk.Label(search_frame, text="Search:", bg="#F5FFFA").pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=25)
    search_entry.pack(side="left",padx=5)

    clear_btn =tk.Button(search_frame, text="Clear", command=lambda e: search_var.set("", bg="#FFDAB9"))
    clear_btn.pack(side="left", padx=5)

    def on_search_change(*args):
        render_tasks()

    search_var.trace_add("write", on_search_change)

    tasks = load_tasks()
    render_tasks()
    update_filter_options()