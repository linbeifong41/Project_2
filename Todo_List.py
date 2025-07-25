import tkinter as tk
import json
from datetime import datetime, timedelta, date
from tkinter import ttk, simpledialog, messagebox
from tkcalendar import DateEntry




def todo_list():
    window = tk.Toplevel()
    window.title("To-Do List")
    window.geometry("350x500")
    window.configure(bg="#F5FFFA")

    task_var = tk.StringVar()
    date_var = tk.StringVar()
    time_var = tk.StringVar()
    category_var = tk.StringVar(value="General")
    last_deleted_task = {"task": None, "index": None}
    
    tasks= []

    
    def save_tasks():
        with open("todo.txt", "w", encoding="utf-8") as f:
             json.dump(tasks, f)
    

      
    def load_tasks():
        try:
            with open("todo.txt", "r", encoding="utf-8") as f:
                loaded_tasks = json.load(f)
           
        except:
            return []

        now = datetime.now()
        
        for task in loaded_tasks:
            repeat = task.get("repeat")
            due_str = task.get("due", "")
            was_done = task.get("done", False)
            if task.get("done") and task.get("repeat") and task.get("due"):
                try:
                    due_dt = datetime.strptime(task["due"], "%Y-%m-%d %H:%M")
                    while due_dt < now:
                        if task["repeat"] == "Daily":
                            due_dt += timedelta(days=1)
                        elif task["repeat"] == "Weekly":
                            due_dt += timedelta(weeks=1)
                        elif task["repeat"] == "Monthly":
                            due_dt += timedelta(days=30)
                        elif task["repeat"] == "Yearly":
                            due_dt += timedelta(days=365)
                        else:
                            break
                        
                    task["due"] = due_dt.strftime("%Y-%m-%d %H:%M")
                    task["done"] = False

                except Exception as e:
                    print("Recurring update error:", e)

        return loaded_tasks
                
                        
        
        
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


    def undo_delete():
        if last_deleted_task["task"] is not None:
            tasks.insert(last_deleted_task["index"], last_deleted_task["task"])
            last_deleted_task["task"] = None
            last_deleted_task["index"] = None
            
            save_tasks()
            render_tasks()


    def add_subtask(task_index):
        subtask_text = simpledialog.askstring("New Subtask", "Enter subtask:")
        if subtask_text:
            if "subtasks" not in tasks[task_index]:
                tasks[task_index]["subtasks"] = []
            tasks[task_index]["subtasks"].append({"text": subtask_text, "done": False})

            save_tasks()
            render_tasks()

    def move_task_up(index):
        if index > 0:
            tasks[index - 1], tasks[index] = tasks[index], tasks[index - 1]
            save_tasks()
            render_tasks()

    def move_task_down(index):
        if index < len(tasks) - 1:
            tasks[index + 1], tasks[index] = tasks[index], tasks[index + 1]
            save_tasks()
            render_tasks()
    

    def move_subtask_up(task_index, sub_index):
        if sub_index > 0:
            subtasks = tasks[task_index]["subtasks"]
            subtasks[sub_index - 1], subtasks[sub_index] = subtasks[sub_index], subtasks[sub_index - 1 ]
            save_tasks()
            render_tasks()

    def move_subtask_down(task_index, sub_index):
        subtasks = tasks[task_index]["subtasks"]
        if sub_index <len(subtasks) - 1:
            subtasks[sub_index + 1], subtasks[sub_index] = subtasks[sub_index], subtasks[sub_index + 1 ]
            save_tasks()
            render_tasks()
    

    def render_tasks():
        for widget in task_list_frame.winfo_children():
            widget.destroy()

        selected_filter = filter_var.get()

        display_tasks = tasks.copy()
        selected_sort = sort_var.get()

        if selected_sort == "Due Date":
            def parse_due(task):
                try:
                    return datetime.strptime(task.get("due", ""), "%Y-%m-%d %H:%M")
                except:
                    return datetime.max
            display_tasks.sort(key=parse_due)

        elif selected_sort == "Category":
            display_tasks.sort(key=lambda t: t.get("category", "").lower())

        elif selected_sort == "Completed":
            display_tasks.sort(key=lambda t: t["done"])

        elif selected_sort == "Alphabetical (A-Z)":
            display_tasks.sort(key=lambda t: t.get("text", "").lower())
        
        elif selected_sort == "Priority":
            display_tasks.sort(key=lambda t: t.get("priority", "").lower())

        elif selected_sort == "Repeated":
            display_tasks.sort(key=lambda t: t.get("repeat", "").lower())

        

        for i, task in enumerate(display_tasks):
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
                            due = task.get("due", "")
                            if not due or not due.startswith(term[5:]):
                                match = False
                                break

                        elif term.startswith("time:"):
                            due = task.get("due", "")
                            if not due or term[5:] not in due:
                                match = False
                                break
                        elif term.startswith("priority:"):
                            if task.get("priority", "medium").lower() != term[9:]:
                                match = False
                                break
                        elif term.startswith("repeat:"):
                            if task.get("repeat", "none").lower() != term[7:]:
                                match = False
                                break
                        else:
                            combined = f"{task.get('text', '')} {task.get('due', '')} {task.get('category', ''), {task.get('priority', '')}, {task.get('repeat', '')}}".lower()
                            if term not in combined:
                                match = False
                                break
                        
                    if not match:
                        continue

            task_frame = tk.Frame(task_list_frame, bg="#F5FFFA")
            task_frame.pack(fill="x", pady=(0, 2))

            top_row = tk.Frame(task_frame, bg="#F5FFFA")
            top_row.pack(fill="x")

            subtask_container = tk.Frame(task_frame, bg="#F5FFFA")
            subtask_container.pack(fill="x", padx=20)


            var = tk.BooleanVar(value=task["done"])

            def toggle_done(index=i, var=var):
                tasks[index]["done"] = var.get()

                if tasks[index]["done"]:
                    tasks[index]["comlpeted_date"] = datetime.today().date().isoformat()
                else:
                    tasks[index].pop("completed_date", None)

                if var.get() and tasks[index].get("repeat") != None:
                    try:
                        due_str = tasks[index].get("due", "")
                        if due_str:
                            due_dt = datetime.strptime(due_str, "%Y-%m-%d %H:%M")

                            if tasks[index]["repeat"] == "Daily":
                                new_due = due_dt + timedelta(days=1)
                            elif tasks[index]["repeat"] == "Weekly":
                                new_due = due_dt + timedelta(weeks=1)
                            elif tasks[index]["repeat"] == "Monthly":
                                new_due = due_dt + timedelta(days=30)
                            elif tasks[index]["repeat"] == "Yearly":
                                new_due = due_dt + timedelta(days=365)
                            else: 
                                new_due = None

                            if new_due:
                                tasks[index]["due"] = new_due.strftime("%Y-%m-%d %H:%M")
                                tasks[index]["done"] = False
                    except Exception as e:
                        print("Reschedule error:", e)

                save_tasks()        
                render_tasks()
               


            check = tk.Checkbutton(top_row, variable=var, command=toggle_done)
            check.pack(side="left")

            display_text = task["task"]
            if "due" in task and task["due"]:
                display_text += f" -Due: {task['due']}"

            if "category" in task and task["category"]:
                display_text += f"[{task['category']}]"

            if task["done"]:
                display_text = f"\u0336".join(display_text) + "\u0336" 

            if "priority" in task:
                display_text += f"({task['priority']})"

            over_due = False
            if "due" in task and  task["due"]:
                try:
                    due_dt = datetime.strptime(task["due"], "%Y-%m-%d %H:%M")
                    if due_dt < datetime.now() and not task["done"]:
                        over_due = True
                except:
                    pass

            priority = task.get("priority", "Medium")
            priority_color = {
                "High": "pink", 
                "Medium": "orange", 
                "low": "gray"
            }.get(priority, "black")

            label_fg = "red" if over_due else priority_color

            label = tk.Label(top_row, text=display_text, anchor="w", bg="#F5FFFA", fg=label_fg)
            label.pack(side="left", fill="x", expand=True)

            tk.Button(top_row, text="subtask", command=lambda i=i: add_subtask(i), bg="#D3FFD3").pack(side="right", padx=2)
            
            tk.Button(top_row, text="↑", command=lambda i=i: move_task_up(i)).pack(side="right", padx=1)
            tk.Button(top_row, text="↓", command=lambda i=i: move_task_down(i)).pack(side="right")

            def delete_task(index=i):
                last_deleted_task["task"] = tasks[index]
                last_deleted_task["index"] = index
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

                new_text_var = tk.StringVar(value=current["task"])
                new_date_var = tk.StringVar(value=current.get("due", "").split()[0] if "due" in current else "")
                new_time_var = tk.StringVar(value=current.get("due", "").split()[1] if "due" in current and " " in current["due"] else "")
                new_cat_var = tk.StringVar(value=current.get("category", "General"))
                new_priority_var = tk.StringVar(value=current.get("priority", "Medium"))
                new_repeat_var = tk.StringVar(value=current.get("repeat", "None"))

                tk.Label(popup, text="Task:", bg="#FAFAD2").pack(anchor="w", padx=10, pady=(10,0))
                tk.Entry(popup, textvariable=new_text_var, width=30).pack(padx=10)

                tk.Label(popup, text="Date (YYYY-MM-DD):", bg="#FAFAD2").pack(anchor="w", padx=10, pady=(10,0))
                DateEntry(popup, textvariable=new_date_var, date_pattern='yyyy-mm-dd', background="darkblue", foreground="white", 
                    borderwidth=2, year=date.today().year, mindate=date(2000, 1, 1), maxdate=date(2100, 12, 31)).pack(padx=10)

                tk.Label(popup, text="Time (HH:MM):", bg="#FAFAD2").pack(anchor="w", padx=10, pady=(10,0))
                ttk.Combobox(popup, textvariable=new_time_var, values=generate_time_options(), width=20).pack(padx=10)

                tk.Label(popup, text="Category:", bg="#FAFAD2").pack(anchor="w", padx=10, pady=(10,0))
                tk.Entry(popup, textvariable=new_cat_var).pack(padx=10)

                tk.Label(popup, text="Priority:", bg="#FAFAD2").pack(anchor="w", padx=10, pady=(10,0))
                ttk.Combobox(popup, textvariable=new_priority_var, values=["Low", "Medium", "High" ], state="readonly", width=20).pack(padx=10)

                tk.Label(popup, text="Repeat:", bg="#FAFAD2").pack(anchor="w", padx=10, pady=(10, 0))   
                ttk.Combobox(popup, textvariable=new_repeat_var, values=["None", "Daily", "Weekly", "Monthly", "Yearly"], state="readonly", width=20).pack(padx=10)         

                def save_edit():
                    current["text"] = new_text_var.get().strip()
                    new_due = new_date_var.get().strip()
                    if new_time_var.get().strip():
                        new_due += f" {new_time_var.get().strip()}"
                    current["due"] = new_due.strip()
                    current["category"] = new_cat_var.get().strip() if new_cat_var.get().strip() else "General"
                    current["priority"] =  new_priority_var.get()
                    current["repeat"] = new_repeat_var.get()


                    save_tasks()
                    update_filter_options()
                    render_tasks()
                    popup.destroy()

                tk.Button(popup, text="Save", command=save_edit, bg="#90EE90").pack(pady=10)
                tk.Button(popup, text="Cancel", command=popup.destroy, bg="#FFC0CB").pack(pady=5)
            
            tk.Button(top_row, text="Edit", command=edit_task, width=4, bg="#FFFFCC").pack(side="right", padx=2)
            
            delete_btn =  tk.Button(top_row, text="X", fg="red", command=delete_task, width=2).pack(side="right")

            if "subtasks" in task:
                for j, subtask in enumerate(task["subtasks"]):
                    subtask_frame = tk.Frame(subtask_container, bg="#F5FFFA")
                    subtask_frame.pack(fill="x", padx=1, pady=1)

                    sub_var = tk.BooleanVar(value=subtask["done"])

                    def toggle_sub_done(index=i, sub_index=j, var=sub_var):
                        tasks[index]["subtasks"][sub_index]["done"] = var.get()

                        save_tasks()
                        render_tasks()

                    tk.Checkbutton(subtask_frame, variable=sub_var, command=toggle_sub_done).pack(side="left")

                    if subtask.get("editing"):

                        sub_text_var = tk.StringVar(value=subtask["text"])
                        entry = tk.Entry(subtask_frame, textvariable=sub_text_var, font=("Arial", 10))
                        entry.pack(side="left", fill="x", expand=True)
                        sub_label = tk.Label(subtask_frame, textvariable=sub_text_var, relief="flat", bg="#F5FFFA", borderwidth=0, font=("Arial", 10))
                        sub_label.pack(side="left", fill="x", expand=True, padx=(2, 5))

                        save_btn = tk.Button(subtask_frame, text="✓", command=lambda i=i, j=j, var=sub_text_var: save_subtask(i, j, var), bg="#DFFFD6", width=2, height=1, padx=1, pady=1)
                        save_btn.pack(side="right", padx=1)

                    else:
                        label = tk.Label(subtask_frame, text=subtask["text"], bg="#F5FFFA", anchor="w", font=("Arial", 10))
                        label.pack(side="left", fill="x", expand=True)

                        tk.Button(subtask_frame, text="↑", width=2, command=lambda i=i, j=j: move_subtask_up(i, j)).pack(side="right", padx=1)
                        tk.Button(subtask_frame, text="↓", width=2, command=lambda i=i, j=j: move_subtask_down(i, j)).pack(side="right", padx=1)

                        if subtask["done"]:
                            sub_label.config(fg="gray", font=("Arial", 10, "overstrike"))

                        edit_btn = tk.Button(subtask_frame, text="edit", command=lambda i=i, j=j: toggle_subtask_edit(i, j), 
                                             bg="#E6E6FA", width=2, height=1, padx=1, pady=1)
                        edit_btn.pack(side="right", padx=1)
                    
                    del_btn = tk.Button(
                        subtask_frame, text="Del", command=lambda i=i, j=j: delete_subtask(i, j),
                              bg="#FFD6D6", width=2, height=1, padx=1, pady=1).pack(side="right", padx=1)

        
    def add_task(event=None):
        text = task_var.get().strip()
        due_date = date_var.get().strip()
        due_time = time_var.get().strip()
        category = category_var.get().strip()
        priority = priority_var.get().strip()


        if text:
            due_str = ""
            if due_date:
                due_str = due_date
                if due_time:
                    due_str += f" {due_time}"
            task = {
                    "task": text, 
                    "done": False,
                    "category": category,
                    "subtasks": [], 
                    "priority": priority,
                    "repeat": repeat_var.get()
            }
            
            if due_str:
                task["due"] = due_str

            tasks.append(task)
            task_var.set("")
            date_var.set("")
            time_var.set("")
            save_tasks()
            render_tasks()
            update_filter_options()

    def save_subtask(task_index, sub_index, var):
        tasks[task_index]["subtasks"][sub_index]["text"] = var.get()
        tasks[task_index]["subtasks"][sub_index]["editing"] = False 
        save_tasks()
        render_tasks()

    def delete_subtask(task_index,sub_index):
        tasks[task_index]["subtasks"].pop(sub_index)
        save_tasks()
        render_tasks()

    def toggle_subtask_edit(task_index, subtask_index):
        tasks[task_index]["subtasks"][subtask_index]["editing"] = True
        render_tasks()


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

    tk.Label(input_frame, text="Priority", bg="#F5FFFA").grid(row=3, column=0, padx=5, sticky="e")

    priority_var = tk.StringVar(value="Medium")
    priority_dropdown = ttk.Combobox(input_frame, textvariable=priority_var, values=["High", "Medium", "Low"], width=15)
    priority_dropdown.grid(row=3, column=1, pady=2, sticky="w")

    
    tk.Label(input_frame, text="Repeat:", bg="#F5FFFA").grid(row=3, column=2, padx=5, sticky="e")
    repeat_var = tk.StringVar(value="None")
    repeat_dropdown = ttk.Combobox(input_frame, textvariable=repeat_var, values=["None", "Daily", "Weekly", "Monthly", "Yearly"], width=10)
    repeat_dropdown.grid(row=3, column=3, pady=2, sticky="w")


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

    clear_btn = tk.Button(search_frame, text="Clear", command=lambda: search_var.set(""), bg="#FFDAB9")
    clear_btn.pack(side="left", padx=5)

    sort_var = tk.StringVar(value="Default")
    sort_options = ["Default", "Due Date", "Category", "Completed", "Alphabetical (A-Z)", "Priority", "Repeated"]
    sort_dropdown = ttk.Combobox(window, textvariable=sort_var, values=sort_options, width=25)
    sort_dropdown.pack(pady=5)
    sort_dropdown.bind("<<ComboboxSelected>>", lambda e: render_tasks())



    def on_search_change(*args):
        render_tasks()

    search_var.trace_add("write", on_search_change)

    undo_btn = tk.Button(window, text="Undo Delete", bg="#E0FFFF", command=lambda: undo_delete())
    undo_btn.pack(pady=5)
    

    tasks = load_tasks()
    render_tasks()
    update_filter_options()