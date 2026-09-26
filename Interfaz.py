#Interfaz Estudaintes

"""
main_prueba.py
--------------
Archivo SOLO para probar visualmente las 2 interfaces juntas, dentro
de un ttk.Notebook (pestañas), igual a como se ven en la referencia.
Este no es un requisito del profesor, es nada más para que puedas
correr "python main_prueba.py" y ver el resultado.

Para que cargue el listado necesitas tener SQL Server corriendo con
la base de datos y las tablas 'estudiantes' y 'cursos' ya creadas
(ver conexion.py para configurar servidor/base de datos).
"""

import tkinter as tk
from tkinter import ttk

from interfaz.interfaz_estudiantes import InterfazEstudiantes
from interfaz.interfaz_cursos import InterfazCursos

raiz = tk.Tk()
raiz.title("Sistema de Control Académico")
raiz.geometry("1000x650")

pestañas = ttk.Notebook(raiz)
pestañas.pack(fill="both", expand=True)

pestañas.add(InterfazEstudiantes(pestañas), text="Estudiantes")
pestañas.add(InterfazCursos(pestañas), text="Cursos")

raiz.mainloop()