import os
from tkinter import filedialog, Toplevel, Label, Button, Checkbutton, BooleanVar, Frame, Entry, END
import json
import subprocess
ext_comunes = [
    ".py", ".html", ".css", ".js", ".json",
    ".txt", ".md", ".png", ".jpg", ".jpeg"
]

#!"#$%&/()=!"#$%&/()=?¨!"#$%&/()=!"#$%&/()= guardar o sacar del json !"#$%&/()=!"#$%&/()=?¨!"#$%&/()=!"#$%&/()=
def guardar_config(ext_var, proyecto_state):
    datos = {
        "extensions": parse_extensions(ext_var.get()),
        "last_project": proyecto_state.get("carpeta", "")
    }

    with open("config.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)

def cargar_config():
    try:
        with open("config.json", "r") as archivo:
            return json.load(archivo)

    except:
        return {
            "extensions": [".py", ".html", ".css"],
            "last_project": ""
        }
    
def parse_extensions(texto):
    partes = [e.strip() for e in texto.split(",")]
    return [e for e in partes if e]


def actualizar_lista_archivos(carpeta, lista_archivos, ext_texto):
    lista_archivos.delete(0, END)
    if not carpeta:
        return
    extensiones = parse_extensions(ext_texto)

    for carpeta_actual, subcarpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            if any(archivo.lower().endswith(ext.lower()) for ext in extensiones):
                ruta_relativa = os.path.relpath(
                    os.path.join(carpeta_actual, archivo),
                    carpeta
                )
                lista_archivos.insert(END, ruta_relativa)


def abrir_proyecto(root, ruta_label, lista_archivos, ext_var, proyecto_state):
    carpeta = filedialog.askdirectory(parent=root)
    if carpeta:
        proyecto_state["carpeta"] = carpeta
        guardar_config(ext_var, proyecto_state)
        ruta_label.config(text=f"📂 {carpeta}")
        actualizar_lista_archivos(carpeta, lista_archivos, ext_var.get())

def abrir_archivo(event, lista_archivos, proyecto_state):
    seleccion = lista_archivos.curselection()

    if seleccion:
        archivo = lista_archivos.get(seleccion[0])
        ruta_completa = os.path.join(
            proyecto_state["carpeta"],
            archivo
        )
        subprocess.Popen(ruta_completa, shell=True)

def abrir_historial(root):
    ventana = Toplevel(root)
    ventana.title("Historial")
    ventana.geometry("320x520")
    ventana.configure(bg="#dfe8f6")
    ventana.resizable(True, True)

    Label(
        ventana,
        text="Comming soon",
        bg="#dfe8f6",
        fg="black",
        font=("Tahoma", 14, "bold")
    ).pack(pady=10)

# -------------- lo prncipla n1 -----------------
def abrir_config(root, ext_var, proyecto_state, lista_archivos):
    ventana = Toplevel(root)
    ventana.title("Settings")
    ventana.geometry("320x520")
    ventana.configure(bg="#dfe8f6")
    ventana.resizable(False, False)

    Label(
        ventana,
        text="⚙ Settings",
        bg="#dfe8f6",
        fg="black",
        font=("Tahoma", 14, "bold")
    ).pack(pady=10)
    Label(
        ventana,
        text="Visible extensions:",
        bg="#dfe8f6",
        fg="black",
        font=("Tahoma", 10)
    ).pack(pady=(0, 8))

    entrada_custom = Entry(
        ventana,
        font=("Tahoma", 10)
    )
    entrada_custom.pack(pady=5)
    
    #!"#$%&/()=!"#$%&/()=?!"#$%&/()=!"#$%&/()=!"#$%&/()=?"
    def agregar_ext():
        nueva = entrada_custom.get().strip()

        if nueva and not nueva.startswith("."):
            nueva = "." + nueva

        if nueva:

            if nueva not in vars_ext:

                var = BooleanVar(value=True)

                vars_ext[nueva] = var

                Checkbutton(
                    contenedor,
                    text=nueva,
                    variable=var,
                    bg="#dfe8f6",
                    font=("Tahoma", 10)
                ).pack(anchor="w")

                entrada_custom.delete(0, END)

    Button(
        ventana,
        text="+ Add Extension",
        command=agregar_ext,
        font=("Tahoma", 9, "bold"),
        relief="raised",
        width=18
    ).pack(pady=10)
    #!"#$%&/()=!"#$%&/()=?!"#$%&/()=!"#$%&/()=!"#$%&/()=?"

    actuales = set(parse_extensions(ext_var.get()))
    vars_ext = {}

    contenedor = Frame(ventana, bg="#dfe8f6")
    contenedor.pack(fill="both", expand=True, padx=20)

    for ext in ext_comunes:
        var = BooleanVar(value=(ext in actuales))
        vars_ext[ext] = var

        Checkbutton(
            contenedor,
            text=ext,
            variable=var,
            bg="#dfe8f6",
            font=("Tahoma", 10)
        ).pack(anchor="w")

    def guardar():
        seleccionadas = [ext for ext, var in vars_ext.items() if var.get()]

        if seleccionadas:
            ext_var.set(", ".join(seleccionadas))
        else:
            ext_var.set(".py")

        carpeta = proyecto_state.get("carpeta", "")
        if carpeta:
            actualizar_lista_archivos(carpeta, lista_archivos, ext_var.get())

        guardar_config(ext_var, proyecto_state)
        ventana.destroy()

    Button(
        ventana,
        text="save",
        command=guardar,
        font=("Tahoma", 10, "bold"),
        width=12
    ).pack(pady=15)