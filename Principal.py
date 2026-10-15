# Principal


# Importamos tkinter, que es la libreria que usamos para hacer ventanass
import tkinter as tk

# ttk trae widgets un poco mas bonitos que tkinter normal entre ellos el "Notebook"

from tkinter import ttk

# Traemos la clase InterfazEstudiantes desde el archivo InterfazEstudiantes.py
from InterfazEstudiantes import InterfazEstudiantes

# Traemos la clase InterfazCursos desde el archivo InterfazCursos.py
from InterfazCursos import InterfazCursos

# Traemos la clase InterfazMatriculas desde el archivo InterfazMatriculas.py
from InterfazMatriculas import InterfazMatriculas


# Creamos la ventana principal del programa
ventana = tk.Tk()

# Le ponemos un titulo este es el texto que sale arriba de la ventana
ventana.title("Sistema de Control Academico")

# Le decimos el tamaño inicial de la ventana: ancho x alto
ventana.geometry("1000x650")

# Creamos el Notebook el Notebook osea el "contenedor" de pestañas

pestanas = ttk.Notebook(ventana)

# Hacemos que el Notebook ocupe toda la ventana disponible
# fill="both" quiere decir que crezca en ancho y en alto
# expand=True quiere decir que use el espacio extra si la ventana crece
pestanas.pack(fill="both", expand=True)

# Creamos la interfaz de estudiantes, esta interfaz va a vivir DENTRO del Notebook

interfaz_estudiantes = InterfazEstudiantes(pestanas)

# Agregamos esa interfaz como una pestaña nueva, con el nombre "Estudiantes"
pestanas.add(interfaz_estudiantes, text="Estudiantes")

# Hacemos lo mismo para la interfaz de cursos
interfaz_cursos = InterfazCursos(pestanas)
pestanas.add(interfaz_cursos, text="Cursos")

# Matriculas necesita ver la lista de estudiantes y la lista de cursos
# por eso se las pasamos (interfaz_estudiantes y
# interfaz_cursos son las listas que ya tienen cargadas)
interfaz_matriculas = InterfazMatriculas(
    pestanas,
    interfaz_estudiantes.estudiantes,
    interfaz_cursos.cursos
)
pestanas.add(interfaz_matriculas, text="Matriculas")


ventana.mainloop()