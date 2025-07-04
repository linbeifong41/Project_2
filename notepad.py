import tkinter as tk

from tkinter import filedialog, messagebox, font

import os


def notepad():

    root = tk.Toplevel()
    root.title("Simple Notepad")
    root.geometry("700x500")


    current_file = [None]


    text_font_family = tk.StringVar(value="Arial")
    text_font_size = tk.IntVar(value=12)
    text_color = tk.StringVar(value="black")
    status_var = tk.StringVar(value="Ready")


    app_font = font.Font(family=text_font_family.get(), size=text_font_size.get())

    control_frame = tk.Frame(root)
    control_frame.pack(side="top", fill="x")

    toolbar_pinned = [True]

    def toggle_toolbar():
        if toolbar_pinned[0]:
            control_frame.pack_forget()
            toolbar_pinned[0] = False
            pin_button.config(text="📍")
        else: 
            control_frame.pack(side="top", fill="x")
            toolbar_pinned[0] = True
            pin_button.config(text="📌")

    pin_button = tk.button(control_frame, text="📌", command=toggle_toolbar)
    pin_button.pack(side="right", padx=5)

    font_families = sorted(font.families())
    font_family_menu = tk.OptionMenu(control_frame, text_font_family, *font_families, command=update_font_family)
    font_family_menu.pack(side="left", padx=5, pady=5)

    size_spin = tk.Spinbox(control_frame, from_=6, to=72, textvariable=text_font_size, width=4)
    size_spin.pack(side="left", padx=5)
    text_font_size.trace_add("write", lambda *args: update_font_size())


    status_bar = tk.Label(root, textvariable=status_var, anchor="w", relief="sunken")
    status_bar.pack(fill="x", side="bottom")

    text_frame = tk.Frame(root)
    text_frame.pack(fill="both", expand=True, side="bottom")

    v_scroll = tk.Scrollbar(text_frame, orient="vertical")
    v_scroll.pack(side="right", fill="y")

    h_scroll = tk.Scrollbar(text_frame, orient="horizontal")
    h_scroll.pack(side="bottom", fill="x")

    text_area = tk.Text(text_frame, undo=True, wrap="none", font=app_font, fg=text_color.get(), yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    text_area.pack(fill="both", expand=True)

    v_scroll.config(command=text_area.yview)
    h_scroll.config(command=text_area.xview)


    def update_color(color):

        try:
            start = text_area.index("sel.first")
            end = text_area.index("sel.last")
            tag_name = f"color_{color}"

            if tag_name not in text_area.tag_names():
                text_area.tag_config(tag_name, foreground=color)

            text_area.tag_add(tag_name, start, end)

        except tk.TclError:

            text_color.set(color)
            text_area.config(fg=color)




    def update_font_family(family):
        size = text_font_size.get()
        text_font_family.set(family)

        try:
            start = text_area.index("sel.first")
            end = text_area.index("sel.last")
            tag_name = f"font_{family}_{size}"

            if tag_name not in text_area.tag_names():
                text_area.tag_config(tag_name, font=(family, size))
            text_area.tag_add(tag_name, start, end)

        except tk.TclError:
            app_font.config(family=family)


    def update_font_size(*args):
        size = text_font_size.get()
        family = text_font_family.get()

        try:
            start = text_area.index("sel.first")
            end = text_area.index("sel.last")
            tag_name = f"font_{family}_{size}"
            if tag_name not in text_area.tag_names():
                text_area.tag_config(tag_name, font=(family, size))
            text_area.tag_add(tag_name, start, end)
        except tk.TclError:

            app_font.config(size=size)

    def autosave(event=None):
        if current_file[0]:
            try:
                with open(current_file[0], "w", encoding="utf-8") as f:
                    f.write(text_area.get(1.0, tk.END))
                status_var.set("Autosaved")

            except Exception as e:
                status_var.set(f"Autosave failed: {e}")

    text_area.bind("<KeyRelease>", autosave)





    colors = ["black", "red", "green", "blue", "orange", "purple", "brown", "gray"]
    for c in colors:
        btn = tk.Button(control_frame, bg=c, width=2, command=lambda col=c: update_color(col))
        btn.pack(side="left", padx=2)


    menu_bar = tk.Menu(root)

    file_menu = tk.Menu(menu_bar, tearoff=0)


    def new_file():
        text_area.delete(1.0, tk.END)
        current_file[0] = None
        root.title("Simple Notepad")
        status_var.set("New File")

    def open_file():
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:

                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, f.read())
                current_file[0] = file_path
                root.title(f"Simple Notepad - {os.path.basename(file_path)}")
                status_var.set(f"Opened {file_path}")

    def save_file():
        if current_file[0]:
            try:
                with open(current_file[0], "w", encoding="utf-8") as f:
                    f.write(text_area.get(1.0, tk.END))
                messagebox.showinfo("Saved", "File saved successfully!")
                status_var.set("File saved")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
                status_var.set("Save failed")

        else:
            save_as_file()

    def save_as_file():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(text_area.get(1.0, tk.END))
                current_file[0] = file_path
                root.title(f"Simple Notepad - {os.path.basename(file_path)}")
                messagebox.showinfo("Saved", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
                status_var.set("Save failed")


    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open...", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_command(label="Save as...", command=save_as_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)


    root.config(menu=menu_bar)

    root.mainloop()



 