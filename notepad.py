import tkinter as tk

from tkinter import filedialog, messagebox, font

from spellchecker import SpellChecker

from language_tool_python import LanguageTool

import re

from tkinter import Menu

import os

spell = SpellChecker()

tool = LanguageTool('eng-US')

ignored_words = set()

ignored_grammar_offsets = set()


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

    top_container = tk.Frame(root)
    top_container.pack(side="top", fill="x")

    pin_frame = tk.Frame(top_container)
    pin_frame.pack(side="top", fill="x")

    control_frame = tk.Frame(top_container)
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

    pin_button = tk.Button(pin_frame, text="📌", command=toggle_toolbar)
    pin_button.pack(side="right", padx=5)

    font_families = sorted(font.families())
    font_family_menu = tk.OptionMenu(control_frame, text_font_family, *font_families, command=lambda f: update_font_family(f))
    font_family_menu.pack(side="left", padx=5, pady=5)

    size_spin = tk.Spinbox(control_frame, from_=6, to=72, textvariable=text_font_size, width=4)
    size_spin.pack(side="left", padx=5)


    def generate_tag_with(weight=None, slant=None):
        return f"style_{current_style['family']}_{current_style['size']}_" \
        f"{weight or current_style['weight']}_" \
        f"{slant or current_style['slant']}_" \
        f"{current_style['color']}" 
    
    def register_tag_with(tag, weight=None, slant=None):
        font_config = font.Font(
            family=current_style["family"],
            size=current_style["size"],
            weight=weight or current_style["weight"],
            slant=slant or current_style["slant"]
        )

        text_area.tag_config(tag, font=font_config, foreground=current_style["color"])



    def toggle_bold():

        try:
            start = text_area.index("sel.first")
            end = text_area.index("sel.last")

        except tk.TclError:
            return 
        
        current_weight = current_style["weight"]
        new_weight = "bold" if current_style["weight"] == "normal" else "normal"

        tag = generate_tag_with(weight=new_weight)
        if tag not in text_area.tag_names():

            register_tag_with(tag, weight=new_weight)

        old_tag = generate_tag_with(weight=current_weight)
        text_area.tag_remove(old_tag, start, end)

        text_area.tag_add(tag, start, end)
        current_style["weight"] = new_weight

    
    def toggle_italics():

        try:
            start = text_area.index("sel.first")
            end = text_area.index("sel.last")
        
        except tk.TclError:
            return 
        
        current_slant = current_style["slant"]
        new_slant = "italic" if current_style["slant"] == "roman" else "roman"

        tag = generate_tag_with(slant=new_slant)

        if tag not in text_area.tag_names():
            register_tag_with(tag, slant=new_slant)
        
        old_tag = generate_tag_with(slant=current_slant)
        text_area.tag_remove(old_tag, start, end)

        text_area.tag_add(tag, start, end)
        current_style["slant"] = new_slant
            


    bold_btn = tk.Button(control_frame, text="B", font=("Arial", 10, "bold"), width=2, command=toggle_bold)
    bold_btn.pack(side="left")

    italic_btn = tk.Button(control_frame, text="I", font=("Arial", 10, "italic"), width=2, command=toggle_italics)
    italic_btn.pack(side="left")

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

    colors = ["black", "red", "green", "blue", "orange", "purple", "brown", "gray"]
    for c in colors:
        btn = tk.Button(control_frame, bg=c, width=2, command=lambda col=c: update_color(col))
        btn.pack(side="left", padx=2)


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


    status_bar = tk.Label(root, textvariable=status_var, anchor="w", relief="sunken")
    status_bar.pack(fill="x", side="bottom")


    text_area.tag_configure("misspelled", underline=True, foreground="red")



    def index_from_offset(offset):
        return text_area.index(f"1.0 + {offset}c")
    

    def highlight_misspellings_and_grammar(event=None):

        text_area.tag_remove("misspelled", "1.0", tk.END)
        text_area.tag_remove("grammar", "1.0", tk.END)

        content = text_area.get("1.0", "end-1c")

        words = list(re.finditer(r'\b\w+\b', content))
        misspelled = spell.unknown([match.group() for match in words])

        for match in words:
            word = match.group()

            if word.lower() in ignored_words:
                continue

            if word.lower() in misspelled:
                start_index = index_from_offset(match.start())
                end_index = index_from_offset(match.end())
                text_area.tag_add("misspelled", start_index, end_index)

        matches = tool.check(content)
        for match in matches:
            
            if match.offset in ignored_grammar_offsets:
                continue

            start = index_from_offset(match.offset)
            end = index_from_offset(match.offset + match.errorLength)
            text_area.tag_add("grammar", start, end)


    def replace_word(start, end, replacement):

        text_area.delete(start, end)
        text_area.insert(start, replacement)
        highlight_misspellings_and_grammar()


    def show_suggestions(event):

        index = text_area.index(f"@{event.x},{event.y}")
        word_start = text_area.index(f"{index} wordstart")
        word_end = text_area.index(f"{index} wordend")
        word = text_area.get(word_start, word_end)

        content = text_area.get("1.0", "end-1c")
        offset = text_area.count("1.0", index, "chars")[0]

        menu = Menu(text_area, tearoff=0)


        if word.lower()  in spell.unknown([word]):

            for suggestion in spell.candidates(word):
                menu.add_command(label=suggestion, command=lambda s=suggestion: replace_word(word_start, word_end, s))
            menu.add_separator()
            menu.add_command(label="Ignore Spelling", command=lambda: (ignored_words.add(word.lower()), text_area.tag_remove("misspelled", word_start, word_end)))

        matches = tool.check(content)

        for match in matches:
            if match.offset <= offset < match.offset + match.errorLength:
                start = index_from_offset(match.offset)
                end = index_from_offset(match.offset + match.errorLength)
                for rep in match.replacements[:5]:
                    menu.add_command(label=f"Grammar: {rep}", command=lambda r=rep, s=start, e=end: replace_word(s, e, r))
                menu.add_command(label="Ignore Grammar", command=lambda o=match.offset: ignored_grammar_offsets.add(0))
                break

       
        try:
            menu.tk_popup(event.x_root, event.y_root)

        finally:
            menu.grab_release()

    text_area.bind("<Button-3>", show_suggestions)
        



    current_style = {
        "family": text_font_family.get(),
        "size": text_font_size.get(),
        "weight": "normal",
        "slant": "roman",
        "color": text_color.get()
    }


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
        current_style["size"] = size

        try:
            start = text_area.index("sel.first")
            end = text_area.index("sel.last")
            tag = generate_current_tag()
            if tag not in text_area.tag_names():
                register_current_tag(tag)
            text_area.tag_add(tag, start, end)
        except tk.TclError:

            app_font.config(size=size)

    def generate_current_tag():
        return f"style_{current_style['family']}_{current_style['size']}_{current_style['weight']}_{current_style['slant']}_{current_style['color']}"
    
    def register_current_tag(tag):
        text_area.tag_config(
            tag, 
            font=(current_style["family"], current_style["size"], current_style["weight"], current_style["slant"]),
            foreground=current_style["color"]
        )

    def apply_style_to_new_text(event=None):
        index = text_area.index("insert -1c")
        tag = generate_current_tag()
        if tag not in text_area.tag_names():
            register_current_tag(tag)
        text_area.tag_add(tag, index, index + "+1c")

    text_area.bind("<Key>", apply_style_to_new_text)



    text_font_size.trace_add("write", lambda *a: update_font_size())

    def autosave_and_highlight(event=None):
        if current_file[0]:
            try:
                with open(current_file[0], "w", encoding="utf-8") as f:
                    f.write(text_area.get(1.0, tk.END))
                status_var.set("Autosaved")
                root.after(2000, lambda: status_var.set("Ready"))

            except Exception as e:
                status_var.set(f"Autosave failed: {e}")

        root.after(100, highlight_misspellings_and_grammar)

    text_area.bind("<KeyRelease>", autosave_and_highlight)



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
                highlight_misspellings_and_grammar()

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



    
    menu_bar = tk.Menu(root)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open...", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_command(label="Save as...", command=save_as_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)


    root.config(menu=menu_bar)

    root.mainloop()



 