import os
import json
import subprocess
from tkinter import (
    filedialog, Toplevel, Label, Button, Checkbutton,
    BooleanVar, Frame, Entry, END, Scale, StringVar, HORIZONTAL
)

# common extensions
COMMON_EXTENSIONS = [
    ".py", ".html", ".css", ".js", ".json",
    ".txt", ".md", ".png", ".jpg", ".jpeg"
]

# themes
normal_th = {
    "root_bg": "#FFFFFF",
    "topbar": "#DDDDDD",
    "sidebar": "#CCCCCC",
    "main_bg": "#FFFFFF",

    "text": "#000000",
    "subtext": "#666666",

    "status": "#C0C0C0",

    "button_bg": "#E8E8E8",
    "button_fg": "#000000",

    "entry_bg": "#FFFFFF",
    "entry_fg": "#000000",

    "listbox_bg": "#FFFFFF",
    "listbox_fg": "#000000",

    "accent": "#245EDB",
}

THEMES = {
    "Dark": {
        **normal_th,

        "root_bg": "#1E1E1E",
        "topbar": "#2A2A2A",
        "sidebar": "#252526",
        "main_bg": "#1E1E1E",

        "text": "#FFFFFF",
        "subtext": "#B0B0B0",

        "status": "#333333",

        "button_bg": "#3A3A3A",
        "button_fg": "#FFFFFF",

        "entry_bg": "#2D2D30",
        "entry_fg": "#FFFFFF",

        "listbox_bg": "#2D2D30",
        "listbox_fg": "#FFFFFF",
    },

    "Blue": {
        **normal_th,

        "root_bg": "#245EDB",
        "topbar": "#0C2D83",
        "sidebar": "#315692",
        "main_bg": "#829FFF",

        "button_bg": "#4E7FE9",
    }
}


#save config to json
def save_config(ext_var, project_state):
    data = {
        "extensions": parse_extensions(ext_var.get()),
        "last_project": project_state.get("folder", "")
    }

    with open("config.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

#load config from json
def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {
            "extensions": [".py", ".html", ".css"],
            "last_project": ""
        }

#convert text into extension list
def parse_extensions(text):
    parts = [ext.strip() for ext in text.split(",")]
    return [ext for ext in parts if ext]

#refresh visible files
def refresh_file_list(folder, file_list, ext_text):
    file_list.delete(0, END)

    if not folder:
        return

    extensions = parse_extensions(ext_text)

    for current_folder, subfolders, files in os.walk(folder):
        for file_name in files:
            if any(file_name.lower().endswith(ext.lower()) for ext in extensions):
                relative_path = os.path.relpath(
                    os.path.join(current_folder, file_name),
                    folder
                )
                file_list.insert(END, relative_path)

#open project folder
def open_project(root, path_label, file_list, ext_var, project_state):
    folder = filedialog.askdirectory(parent=root)

    if folder:
        project_state["folder"] = folder
        save_config(ext_var, project_state)
        path_label.config(text=f" {folder}")
        refresh_file_list(folder, file_list, ext_var.get())

#open selected file
def open_file(event, file_list, project_state):
    selected = file_list.curselection()

    if not selected:
        return

    file_name = file_list.get(selected[0])
    full_path = os.path.join(project_state["folder"], file_name)

    try:
        os.startfile(full_path)  # windows moment, very powerful
    except AttributeError:
        subprocess.Popen(["xdg-open", full_path])  # linux moment, also powerful

#open history window
def open_history(root):
    window = create_window(root, "history", False, "320x520")

    Label(
        window,
        text="coming soon",
        bg="#dfe8f6",
        fg="black",
        font=("Tahoma", 14, "bold")
    ).pack(pady=10)

#---- settings window ----
def open_settings(root, ext_var, project_state, file_list):
    window = create_window(root, "settings", False, "320x520")

    Label(
        window,
        text="⚙ settings",
        bg="#dfe8f6",
        fg="black",
        font=("Tahoma", 14, "bold")
    ).pack(pady=10)

    Label(
        window,
        text="visible extensions:",
        bg="#dfe8f6",
        fg="black",
        font=("Tahoma", 10)
    ).pack(pady=(0, 8))

    #custom extension input, because humans keep inventing file types
    entry_custom = Entry(
        window,
        font=("Tahoma", 10)
    )
    entry_custom.pack(pady=5)

    current_extensions = set(parse_extensions(ext_var.get()))
    ext_vars = {}

    container = Frame(window, bg="#dfe8f6")
    container.pack(fill="both", expand=True, padx=20)

    #add a new extension
    def add_extension():
        new_ext = entry_custom.get().strip()

        if new_ext and not new_ext.startswith("."):
            new_ext = "." + new_ext

        if new_ext and new_ext not in ext_vars:
            var = BooleanVar(value=True)
            ext_vars[new_ext] = var

            Checkbutton(
                container,
                text=new_ext,
                variable=var,
                bg="#dfe8f6",
                font=("Tahoma", 10)
            ).pack(anchor="w")

            entry_custom.delete(0, END)

    Button(
        window,
        text="+ add extension",
        command=add_extension,
        font=("Tahoma", 9, "bold"),
        relief="raised",
        width=18
    ).pack(pady=10)

    #default extension list
    for ext in COMMON_EXTENSIONS:
        var = BooleanVar(value=(ext in current_extensions))
        ext_vars[ext] = var

        Checkbutton(
            container,
            text=ext,
            variable=var,
            bg="#dfe8f6",
            font=("Tahoma", 10)
        ).pack(anchor="w")

    #save settings
    def save():
        selected = [ext for ext, var in ext_vars.items() if var.get()]

        if selected:
            ext_var.set(", ".join(selected))
        else:
            ext_var.set(".py")  # backup mode, because chaos is not allowed

        folder = project_state.get("folder", "")
        if folder:
            refresh_file_list(folder, file_list, ext_var.get())

        save_config(ext_var, project_state)
        window.destroy()

    Button(
        window,
        text="save",
        command=save,
        font=("Tahoma", 10, "bold"),
        width=12
    ).pack(pady=15)

# reusable window :D
def create_window(root, title:str, resize:bool=True, geometry:str="350x400"):
    window = Toplevel(root)
    window.title(title)
    window.geometry(geometry)
    window.configure(bg="#d1e2fd")
    window.resizable(resize, resize)

    return window

#new: styles!!!
def open_styles(root):
    window = create_window(root, "Styles", False, "380x220")

    theme_names = list(THEMES.keys())
    current_theme = StringVar(value=theme_names[0]) 

    title = Label(
        window,
        text="🪅 Theme mode",
        bg=window.cget("bg"),
        fg="black",
        font=("Tahoma", 14, "bold")
    )
    title.pack(pady=(12, 4))

    theme_label = Label(
        window,
        textvariable=current_theme,
        bg=window.cget("bg"),
        fg="black",
        font=("Tahoma", 12, "bold")
    )
    theme_label.pack(pady=(0, 8))

    preview = Frame(window, bg="#E9EEF9", bd=2, relief="groove")
    preview.pack(fill="x", padx=20, pady=5)

    Label(
        preview,
        text="Swipe to switch modes",
        bg="#E9EEF9",
        fg="#333333",
        font=("Tahoma", 10)
    ).pack(pady=8)

    def apply_theme(theme_name):
        theme = THEMES[theme_name]

        def paint(widget):
            cls = widget.winfo_class()

            try:
                if cls in ("Tk", "Toplevel"):
                    widget.configure(bg=theme["root_bg"])

                elif cls in ("Frame", "LabelFrame"):
                    widget.configure(bg=theme["main_bg"])

                elif cls == "Label":
                    widget.configure(bg=theme["main_bg"], fg=theme["text"])

                elif cls == "Button":
                    widget.configure(
                        bg=theme["button_bg"],
                        fg=theme["button_fg"],
                        activebackground=theme["accent"],
                        activeforeground="white"
                    )

                elif cls == "Checkbutton":
                    widget.configure(
                        bg=theme["main_bg"],
                        fg=theme["text"],
                        activebackground=theme["main_bg"],
                        activeforeground=theme["text"],
                        selectcolor=theme["main_bg"]
                    )

                elif cls == "Entry":
                    widget.configure(
                        bg=theme["entry_bg"],
                        fg=theme["entry_fg"],
                        insertbackground=theme["entry_fg"]
                    )

                elif cls == "Listbox":
                    widget.configure(
                        bg=theme["listbox_bg"],
                        fg=theme["listbox_fg"],
                        selectbackground=theme["accent"],
                        selectforeground="white"
                    )

                elif cls == "Text":
                    widget.configure(
                        bg=theme["entry_bg"],
                        fg=theme["entry_fg"],
                        insertbackground=theme["entry_fg"]
                    )

                elif cls == "Scale":
                    widget.configure(
                        bg=theme["main_bg"],
                        fg=theme["text"],
                        troughcolor=theme["status"],
                        highlightthickness=0
                    )

                elif cls == "Scrollbar":
                    widget.configure(bg=theme["main_bg"])

            except Exception:
                pass

            for child in widget.winfo_children():
                paint(child)

        paint(root)

    def on_change(value):
        idx = int(float(value))
        theme_name = theme_names[idx]
        current_theme.set(theme_name)
        apply_theme(theme_name)

    slider = Scale(
        window,
        from_=0,
        to=len(theme_names) - 1,
        orient=HORIZONTAL,
        showvalue=False,
        length=260,
        resolution=1,
        command=on_change
    )
    slider.pack(pady=10)

    slider.set(0)
    apply_theme("Blue")


# i need less code, in a other update i clean the code :)