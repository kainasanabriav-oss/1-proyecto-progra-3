# Principal
# Este es el archivo PRINCIPAL del programa 


# Primero importamos tkinter la libreria que usamos para hacer ventanas
import tkinter as tk

from tkinter import ttk #windgets mas lindos (notebook: es el que hace las pestañas)

# Traemos la clase InterfazEstudiantes desde el archivo InterfazEstudiantes
from InterfazEstudiantes import InterfazEstudiantes

# y aqui tambien la clase InterfazCursos desde el archivo InterfazCursos
from InterfazCursos import InterfazCursos

# ventana principal del programa
ventana = tk.Tk()

# Le ponemos un titulo este es el texto que sale arriba de la ventana :b
ventana.title("Sistema de Control Academico")

# tamaño de la ventana ancho x alto
ventana.geometry("1000x650")

# Creamos el Notebook
pestanas = ttk.Notebook(ventana)

# Hacemos que el Notebook ocupe toda la ventana disponible
pestanas.pack(fill="both", expand=True)# fill="both" quiere decir que crezca en ancho y en alto y el expand=True quiere decir que use el espacio extra si la ventana crece

# Creamos la interfaz de estudiantes va a vivir desntro del Notebook
interfaz_estudiantes = InterfazEstudiantes(pestanas)

# Agregamos esa interfaz como una pestaña nueva con el nombre  Estudiantes
pestanas.add(interfaz_estudiantes, text="Estudiantes")

# Y lo mismo para la interfaz de cursos
interfaz_cursos = InterfazCursos(pestanas)
pestanas.add(interfaz_cursos, text="Cursos")


ventana.mainloop()
