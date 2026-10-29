# Registro de solicitudes de soporte técnico

**Materia:** PFU-111 - Programación Fundamental
**Actividad:** Semana 13 - Interfaz gráfica para registrar y almacenar solicitudes
**Estudiante:** Denilson Davis Machaca Flores
**Grupo:** 2
**Carrera:** Ingeniería de Sistemas e Innovación Digital - Unifranz

---

## 1. Descripción

Aplicación de escritorio hecha en **Python** con **tkinter** que permite registrar solicitudes de soporte técnico del laboratorio de informática. El programa valida los datos antes de guardarlos y los almacena en un archivo CSV para poder consultarlos después, incluso si se cierra y se vuelve a abrir.

## 2. Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `solicitudes.py` | Código fuente de la aplicación |
| `solicitudes.csv` | Archivo de datos (se crea solo al registrar la primera solicitud) |
| `README.md` | Este documento |
| `PFU111_Grupo2_MachacaFloresDenilson.pdf` | Informe de la actividad |

## 3. Requisitos y ejecución

- Python 3 (tkinter viene incluido en la instalación normal de Python).
- No hay que instalar librerías adicionales.

Para ejecutar, abre una terminal en la carpeta del proyecto y escribe:

```
python solicitudes.py
```

El archivo `solicitudes.csv` se crea **en la misma carpeta donde está `solicitudes.py`**.

## 4. Funcionamiento de la interfaz

La ventana tiene:

- **Nombre del solicitante** (cuadro de texto)
- **Código de estudiante** (cuadro de texto)
- **Tipo de solicitud** (lista desplegable: equipo, software, conectividad)
- **Descripción del problema** (cuadro de varias líneas)
- **Prioridad** (botones de opción: bajo, medio, alto)
- Botones: **Registrar solicitud**, **Consultar solicitudes** y **Limpiar formulario**
- Un **área de resultados** donde se muestran mensajes, errores y los registros

## 5. Explicación del código

### 5.1 Importaciones y variables iniciales

```python
import os
import tkinter as tk
from tkinter import ttk

carpeta = os.path.dirname(os.path.abspath(__file__))
archivo = os.path.join(carpeta, "solicitudes.csv")

tipos = ["equipo", "software", "conectividad"]
prioridades = ["bajo", "medio", "alto"]
```

- `os` sirve para trabajar con rutas de archivos y comprobar si un archivo existe.
- `tkinter` crea la ventana y los controles. `ttk` aporta la lista desplegable (`Combobox`).
- `carpeta` y `archivo` hacen que el CSV siempre se guarde junto al programa, sin importar desde dónde se ejecute.
- `tipos` y `prioridades` son listas con las opciones permitidas. Se usan tanto para llenar los controles como para validar.

### 5.2 Función `mostrar(texto)`

Escribe un mensaje en el área de resultados. El área está en modo solo lectura (`state="disabled"`), así que la función la habilita un momento, borra lo anterior, inserta el texto nuevo y la vuelve a bloquear.

### 5.3 Función `registrar()`

Se ejecuta al presionar **Registrar solicitud**. Funciona en tres pasos:

**Paso 1: leer los datos del formulario.**
Se obtiene el contenido de cada control. A los textos se les aplica `.strip()`, que elimina los espacios al inicio y al final.

**Paso 2: validar.**
Se crea una lista vacía `errores` y se agrega un mensaje por cada problema:

| Campo | Condición de error |
|---|---|
| Nombre | Está vacío (`== ""`) o solo tenía espacios |
| Código | Está vacío o solo tenía espacios |
| Tipo | No está en la lista `tipos` |
| Descripción | Está vacía o solo tenía espacios |
| Prioridad | No está en la lista `prioridades` |

Como `.strip()` ya quitó los espacios, un texto con solo espacios queda como `""` y se detecta como vacío. Si la lista `errores` tiene elementos, se muestran todos en el área de resultados y la función termina con `return`, por lo que **no se guarda nada** hasta corregir los datos.

**Paso 3: guardar en el archivo.**
Antes de guardar, se cambian las comas por `;` y los saltos de línea por espacios para que no se rompa la estructura del CSV. Luego:

```python
existe = os.path.exists(archivo)
f = open(archivo, "a", encoding="utf-8")
if not existe:
    f.write("nombre,codigo,tipo,descripcion,prioridad\n")
f.write(f"{nombre},{codigo},{tipo},{descripcion},{prioridad}\n")
f.close()
```

- El modo `"a"` (append) agrega al final sin borrar lo anterior.
- Si el archivo no existía, primero se escribe el encabezado.
- Todo está dentro de un `try / except OSError`: si ocurre un problema al escribir (por ejemplo, el archivo está abierto en otro programa), se muestra un mensaje y la aplicación no se cierra.

Si todo sale bien, se muestra un mensaje de éxito y se limpia el formulario.

### 5.4 Función `consultar()`

Se ejecuta al presionar **Consultar solicitudes**.

```python
f = open(archivo, "r", encoding="utf-8")
lineas = f.readlines()
f.close()
```

- Abre el archivo en modo lectura `"r"` y guarda todas sus líneas en una lista.
- Si el archivo no existe, `except FileNotFoundError` muestra un mensaje explicando que todavía no hay solicitudes. El programa sigue funcionando.
- Cualquier otro error de lectura se captura con `except OSError`.
- Si solo hay una línea (el encabezado), avisa que no hay solicitudes.
- Si hay registros, recorre las líneas desde la 1 (se salta el encabezado), separa cada una con `.split(",")` y arma un texto con cada campo para mostrarlo.

### 5.5 Funciones `limpiar()` y `limpiar_formulario()`

- `limpiar()` borra todos los campos: vacía los cuadros de texto, deja la lista desplegable sin selección y desmarca la prioridad.
- `limpiar_formulario()` llama a `limpiar()` y además muestra el mensaje "Formulario limpiado." Es la que usa el botón.

### 5.6 Construcción de la ventana

La parte final del código crea la ventana con `tk.Tk()` y va agregando los controles con `.pack()`: etiquetas (`Label`), cuadros de texto (`Entry`), la lista desplegable (`Combobox`), el cuadro de descripción (`Text`), los botones de opción (`Radiobutton`) y los tres botones (`Button`). Cada botón recibe su función con `command=`. Al final, `ventana.mainloop()` mantiene la ventana abierta esperando las acciones del usuario.

## 6. Estructura del archivo de datos

`solicitudes.csv` guarda un registro por línea:

```
nombre,codigo,tipo,descripcion,prioridad
Ana Pérez,EST001,software,Error al abrir el editor,alto
Luis Rojas,EST002,equipo,Teclado defectuoso,medio
```

Los datos del ejemplo son ficticios.

## 7. Pruebas realizadas

| N.º | Prueba | Resultado esperado |
|---|---|---|
| 1 | Registrar con todos los campos vacíos | Mostrar errores de validación |
| 2 | Nombre compuesto solo por espacios | Rechazar el registro |
| 3 | Registrar sin seleccionar el tipo | Solicitar una selección válida |
| 4 | Registrar con datos correctos | Guardar el registro en el archivo |
| 5 | Registrar dos solicitudes consecutivas | Conservar ambos registros |
| 6 | Cerrar y volver a abrir la aplicación | Permitir consultar los registros anteriores |
| 7 | Consultar cuando el archivo no existe | Informar sin cerrar la aplicación |

## 8. Autor

Denilson Davis Machaca Flores - Unifranz
