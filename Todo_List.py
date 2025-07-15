import tkinter as tk
import json
from datetime import datetime


def todo_list():
    window = tk.Toplevel()
    window.title("To-Do List")
    window.geometry("350x500")
    window.configure(bg="#F5FFFA")

    task_var = tk.StringVar()
    date_var = tk.StringVar()
    time_var = tk.StringVar()
    catagory_var = tk.StringVar(value="General")
    
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
        
    task_list_frame = tk.Frame(window)
    task_list_frame.pack(fill="both", expand=True)

    def render_tasks():
        for widget in task_list_frame.winfo_children():
            widget.destroy()

        for i, task in enumerate(tasks):
            task_frame = tk.Frame(task_list_frame)
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

            delete_btn =  tk.Button(task_frame, text="X", fg="red", command=delete_task, width=2)
            delete_btn.pack(side="right")
        
    def add_task(event=None):
        text = task_var.get().strip()
        due_date = date_var.get().strip()
        due_time = time_var.get().strip()

        if text:
            due_str = ""
            if due_date:
                due_str = due_date
                if due_time:
                    due_str += f" {due_time}"
            task = {"text": text, "done": False, "category": catagory_var.get()}
            if due_str:
                task["due"] = due_str
            tasks.append(task)

            task_var.set("")
            date_var.set("")
            time_var.set("")
            save_tasks()
            render_tasks()

    input_frame = tk.Frame(window, bg="#F5FFFA")
    input_frame.pack( fill="x", padx=5, pady=10)


    tk.Label(input_frame, text="Task:", bg="#F5FFFA").grid(row=1, column=0, padx=5, sticky="e" )
    task_entry = tk.Entry(input_frame, textvariable=task_var, width=25)
    task_entry.grid(row=0, column=1, columnspan=3, pady=2, sticky="w")
    task_entry.bind("<Return>", add_task)


    tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg="#F5FFFA").grid(row=1, column=0, padx=5, sticky="e")
    date_entry = tk.Entry(input_frame, textvariable=date_var, width=15)
    date_entry.grid(row=1, column=1, pady=2, sticky="w")


    tk.Label(input_frame, text="Time (HH:MM):", bg="#F5FFFA").grid(row=1, column=2, padx=5, sticky="e" )
    time_entry = tk.Entry(input_frame, textvariable=time_var, width=10)
    time_entry.grid(row=1, column=3, pady=10, sticky="e")

    tk.Label(input_frame, text="Catrgory", bg="#F5FFFA").grid(row=2, column=0, padx=5, sticky="e")
    catagory_menu = tk.OptionMenu(input_frame, catagory_var, "General", "Work", "School", "Self-care",
     "Errands", "Health", "Creative")
    
    catagory_menu.grid(row=2, column=1, pady=2, sticky="w")


    add_btn = tk.Button(input_frame, text="Add", command=add_task, bg="#90EE90")
    add_btn.grid(row=2, column=3, pady=10, sticky="e")

    tasks = load_tasks()
    render_tasks()