from tkinter import *
from functions import *

root = Tk()
root.title("DuckyPG")
root.geometry("900x500")
root.configure(bg="#245EDB")

#estado
config = cargar_config()

proyecto_state = {
    "carpeta": config["last_project"]
}

#extensiones por defecto (por si no sabias tu que lees esto)
ext_var = StringVar(
    value=", ".join(config["extensions"])
)

# ----- barra de arriba ----
topbar = Frame(root, bg="#0C2D83", height=40)
topbar.pack(fill=X)

titulo = Label(
    topbar,
    text="🦆 DuckyPG",
    bg="#0C2D83",
    fg="white",
    font=("Tahoma", 14, "bold")
)
titulo.pack(side=LEFT, padx=10, pady=5)

#-- menu lateral ----
sidebar = Frame(root, bg="#dfe8f6", width=200)
sidebar.pack(side=LEFT, fill=Y)

# -- la parte del el centro donde se ven todo los archivos y esas cosas que nececita una persona como tu el que lees esto para poder ser mas ordenado---
main = Frame(root, bg="white")
main.pack(side=LEFT, fill=BOTH, expand=True)

Label(
    main,
    text="Welcome to DuckyPG",
    bg="white",
    fg="black",
    font=("Tahoma", 20, "bold")
).pack(pady=30)

ruta_label = Label(
    main,
    text="📂 No projects open",
    bg="white",
    fg="gray",
    font=("Tahoma", 10)
)
ruta_label.pack(pady=10)

Label(
    main,
    text="Visible extensions:",
    bg="white",
    fg="black",
    font=("Tahoma", 10, "bold")
).pack(pady=(10, 0))

Label(
    main,
    textvariable=ext_var,
    bg="white",
    fg="gray",
    font=("Tahoma", 10)
).pack(pady=(0, 10))

lista_archivos = Listbox(
    main,
    font=("Consolas", 10)
)
lista_archivos.pack(fill=BOTH, expand=True, padx=20, pady=10)
lista_archivos.bind(
    "<Double-Button-1>", #doble click hacer abrir
    lambda event: abrir_archivo(
        event,
        lista_archivos,
        proyecto_state
    )
)

if proyecto_state["carpeta"]:
    ruta_label.config(
        text=f"📂 {proyecto_state['carpeta']}"
    )

    actualizar_lista_archivos(
        proyecto_state["carpeta"],
        lista_archivos,
        ext_var.get()
    )

# --- botone ----
Button(
    sidebar,
    text="📂 Open proyects",
    command=lambda: abrir_proyecto(root, ruta_label, lista_archivos, ext_var, proyecto_state),
    font=("Tahoma", 10),
    relief="raised",
    width=20
).pack(pady=10)

Button(
    sidebar,
    text="🔎 Search",
    font=("Tahoma", 10),
    relief="raised",
    width=20
).pack(pady=10)

Button(
    sidebar,
    text="📝 Historial",
    command=lambda: abrir_historial(root),
    font=("Tahoma", 10),
    relief="raised",
    width=20
).pack(pady=10)

Button(
    sidebar,
    text="⚙ Settings",
    command=lambda: abrir_config(root, ext_var, proyecto_state, lista_archivos),
    font=("Tahoma", 10),
    relief="raised",
    width=20
).pack(pady=10)

# ---- lito ----
status = Frame(root, bg="#C0C0C0", height=25)
status.pack(side=BOTTOM, fill=X)

Label(
    status,
    text="🗿🗿",
    bg="#C0C0C0",
    fg="black",
    font=("Tahoma", 9)
).pack(side=LEFT, padx=5)

root.mainloop()