import os
import tkinter as tk
from tkinter import ttk

# El archivo se guarda en la misma carpeta que este programa
carpeta = os.path.dirname(os.path.abspath(__file__))
archivo = os.path.join(carpeta, "solicitudes.csv")

tipos = ["equipo", "software", "conectividad"]
prioridades = ["bajo", "medio", "alto"]


def mostrar(texto):
    # Escribe un texto en el área de resultados
    resultado.config(state="normal")
    resultado.delete("1.0", tk.END)
    resultado.insert(tk.END, texto)
    resultado.config(state="disabled")


def registrar():
    nombre = entrada_nombre.get().strip()
    codigo = entrada_codigo.get().strip()
    tipo = lista_tipo.get()
    descripcion = caja_descripcion.get("1.0", tk.END).strip()
    prioridad = var_prioridad.get()

    # ---------- Validaciones ----------
    errores = []
    if nombre == "":
        errores.append("- El nombre no puede estar vacío.")
    if codigo == "":
        errores.append("- El código de estudiante no puede estar vacío.")
    if tipo not in tipos:
        errores.append("- Debes seleccionar un tipo de solicitud.")
    if descripcion == "":
        errores.append("- La descripción no puede estar vacía.")
    if prioridad not in prioridades:
        errores.append("- Debes seleccionar una prioridad.")

    if len(errores) > 0:
        mensaje = "No se guardó la solicitud:\n\n"
        for e in errores:
            mensaje = mensaje + e + "\n"
        mostrar(mensaje)
        return

    # Quitamos comas y saltos de línea para no dañar el CSV
    nombre = nombre.replace(",", ";")
    codigo = codigo.replace(",", ";")
    descripcion = descripcion.replace(",", ";").replace("\n", " ")

    # ---------- Guardar en el archivo ----------
    try:
        existe = os.path.exists(archivo)
        f = open(archivo, "a", encoding="utf-8")
        if not existe:
            f.write("nombre,codigo,tipo,descripcion,prioridad\n")
        f.write(f"{nombre},{codigo},{tipo},{descripcion},{prioridad}\n")
        f.close()
    except OSError:
        mostrar("Error: no se pudo escribir en el archivo.\n"
                "Revisa que no esté abierto en otro programa.")
        return

    mostrar(f"Solicitud de {nombre} guardada correctamente.")
    limpiar()


def consultar():
    try:
        f = open(archivo, "r", encoding="utf-8")
        lineas = f.readlines()
        f.close()
    except FileNotFoundError:
        mostrar("Todavía no existe el archivo de solicitudes.\n"
                "Registra una solicitud primero.")
        return
    except OSError:
        mostrar("Error: no se pudo leer el archivo.")
        return

    if len(lineas) <= 1:
        mostrar("El archivo no tiene solicitudes todavía.")
        return

    texto = f"Solicitudes registradas: {len(lineas) - 1}\n"
    texto = texto + "-" * 40 + "\n"
    for i in range(1, len(lineas)):
        datos = lineas[i].strip().split(",")
        if len(datos) == 5:
            texto = texto + f"Solicitud {i}\n"
            texto = texto + f"Nombre: {datos[0]}\n"
            texto = texto + f"Código: {datos[1]}\n"
            texto = texto + f"Tipo: {datos[2]}\n"
            texto = texto + f"Descripción: {datos[3]}\n"
            texto = texto + f"Prioridad: {datos[4]}\n"
            texto = texto + "-" * 40 + "\n"
    mostrar(texto)


def limpiar():
    entrada_nombre.delete(0, tk.END)
    entrada_codigo.delete(0, tk.END)
    lista_tipo.set("")
    caja_descripcion.delete("1.0", tk.END)
    var_prioridad.set("")


def limpiar_formulario():
    limpiar()
    mostrar("Formulario limpiado.")


# ---------------- Ventana ----------------
ventana = tk.Tk()
ventana.title("Solicitudes de soporte técnico")
ventana.geometry("520x620")

tk.Label(ventana, text="Registro de solicitudes",
         font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(ventana, text="Nombre del solicitante:").pack()
entrada_nombre = tk.Entry(ventana, width=40)
entrada_nombre.pack(pady=3)

tk.Label(ventana, text="Código de estudiante:").pack()
entrada_codigo = tk.Entry(ventana, width=40)
entrada_codigo.pack(pady=3)

tk.Label(ventana, text="Tipo de solicitud:").pack()
lista_tipo = ttk.Combobox(ventana, values=tipos, state="readonly", width=37)
lista_tipo.pack(pady=3)

tk.Label(ventana, text="Descripción del problema:").pack()
caja_descripcion = tk.Text(ventana, width=40, height=4)
caja_descripcion.pack(pady=3)

tk.Label(ventana, text="Prioridad:").pack()
var_prioridad = tk.StringVar(value="")
marco = tk.Frame(ventana)
marco.pack(pady=3)
for p in prioridades:
    tk.Radiobutton(marco, text=p, variable=var_prioridad, value=p).pack(side="left", padx=10)

marco_botones = tk.Frame(ventana)
marco_botones.pack(pady=10)
tk.Button(marco_botones, text="Registrar solicitud", command=registrar).pack(side="left", padx=5)
tk.Button(marco_botones, text="Consultar solicitudes", command=consultar).pack(side="left", padx=5)
tk.Button(marco_botones, text="Limpiar formulario", command=limpiar_formulario).pack(side="left", padx=5)

tk.Label(ventana, text="Resultados:").pack()
resultado = tk.Text(ventana, width=58, height=14, state="disabled")
resultado.pack(pady=5)

mostrar("Bienvenido. Completa el formulario para registrar una solicitud.")

ventana.mainloop()
