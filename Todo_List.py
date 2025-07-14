import tkinter as tk
import json


def todo_list():
    window = tk.Toplevel()
    window.title("To-Do List")
    window.geometry("300x400")

    task_var = tk.StringVar()
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
            if task["done"]:
                display_text = f"\u0336".join(display_text) + "\u0336" 

            label = tk.Label(task_frame, text=display_text, anchor="w")
            label.pack(side="left", fill="x", expand=True)


            def delete_task(index=i):
                tasks.pop(index)
                render_tasks()
                save_tasks()

            delete_btn =  tk.Button(task_frame, text="X", fg="red", command=delete_task, width=2)
            delete_btn.pack(side="right")
        
    def add_task(event=None):
        text = task_var.get().strip()
        if text:
            tasks.append({"text": text, "done": False})
            task_var.set("")
            save_tasks()
            render_tasks()

    input_frame = tk.Frame(window)
    input_frame.pack( fill="x", padx=5, pady=5)


    task_entry = tk.Entry(input_frame, textvariable=task_var)
    task_entry.pack(side="left", fill="x", expand=True)
    task_entry.bind("<Return>", add_task)

    add_btn = tk.Button(input_frame, text="Add", command=add_task)
    add_btn.pack(side="right")

    tasks = load_tasks()
    render_tasks()