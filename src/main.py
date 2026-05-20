from tkinter import *
from functions import *

#---- main window ----
root = Tk()
root.title("DuckyPG")
root.geometry("900x500")
root.configure(bg="#245EDB")

#load saved config
config = load_config()

#current project state
project_state = {
    "folder": config["last_project"]
}

#visible file extensions
ext_var = StringVar(
    value=", ".join(config["extensions"])
)

# top bar
topbar = Frame(root, bg="#0C2D83", height=40)
topbar.pack(fill=X)

# app title (pi po po pi po po pi pu)
title = Label(
    topbar,
    text="🦆 DuckyPG",
    bg="#0C2D83",
    fg="white",
    font=("Tahoma", 14, "bold")
)
title.pack(side=LEFT, padx=10, pady=5)

# left sidebar
sidebar = Frame(root, bg="#dfe8f6", width=200)
sidebar.pack(side=LEFT, fill=Y)

# main content area
main = Frame(root, bg="white")
main.pack(side=LEFT, fill=BOTH, expand=True)

# welcome text
Label(
    main,
    text="Welcome to DuckyPG",
    bg="white",
    fg="black",
    font=("Tahoma", 20, "bold")
).pack(pady=30)

# current project path
path_label = Label(
    main,
    text="📂 no projects open",
    bg="white",
    fg="gray",
    font=("Tahoma", 10)
)
path_label.pack(pady=10)

# extensions label
Label(
    main,
    text="visible extensions:",
    bg="white",
    fg="black",
    font=("Tahoma", 10, "bold")
).pack(pady=(10, 0))

# show current extensions
Label(
    main,
    textvariable=ext_var,
    bg="white",
    fg="gray",
    font=("Tahoma", 10)
).pack(pady=(0, 10))

# file list
file_list = Listbox(
    main,
    font=("Consolas", 10)
)
file_list.pack(fill=BOTH, expand=True, padx=20, pady=10)

# open file with double click
file_list.bind(
    "<Double-Button-1>",
    lambda event: open_file(event, file_list, project_state)
)

# reopen last project if it exists
if project_state["folder"]:
    path_label.config(
        text=f"📂 {project_state['folder']}"
    )

    refresh_file_list(
        project_state["folder"],
        file_list,
        ext_var.get()
    )

# buttons :3

# open projects
Button(
    sidebar,
    text="📂 open projects",
    command=lambda: open_project(root, path_label, file_list, ext_var, project_state),
    font=("Tahoma", 10),
    relief="raised",
    width=20
).pack(pady=10)

# search
Button(
    sidebar,
    text="🔎 search",
    font=("Tahoma", 10),
    relief="raised",
    width=20
).pack(pady=10)

# history
Button(
    sidebar,
    text="📝 history",
    command=lambda: open_history(root),
    font=("Tahoma", 10),
    relief="raised",
    width=20
).pack(pady=10)

# settings
Button(
    sidebar,
    text="⚙ settings",
    command=lambda: open_settings(root, ext_var, project_state, file_list),
    font=("Tahoma", 10),
    relief="raised",
    width=20
).pack(pady=10)

# status bar
status = Frame(root, bg="#C0C0C0", height=25)
status.pack(side=BOTTOM, fill=X)

# moai
Label(
    status,
    text="🗿",
    bg="#C0C0C0",
    fg="black",
    font=("Tahoma", 9)
).pack(side=LEFT, padx=5)

# main loop
root.mainloop()