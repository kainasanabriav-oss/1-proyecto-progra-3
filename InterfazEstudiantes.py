#Interfaz Estudiantes

# Librería
# pip install tkcalendar

import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import date
from tkcalendar import DateEntry


class InterfazEstudiantes(ttk.Frame):

    def __init__(self, contenedor):
        super().__init__(contenedor, padding=15)

        # Lista donde se guardan los estudiantes temporalmente
        self.estudiantes = []

        # Guarda el id del estudiante seleccionado
        self.id_seleccionado = None

        self.crear_estilos()
        self.crear_titulo()
        self.crear_formulario()
        self.crear_botones()
        self.crear_listado()

        self.cargar_estudiantes()

    # ---------------------------------------------------------
    # ESTILOS
    # ------------------------------------------------------

    def crear_estilos(self):
        estilo = ttk.Style()

        estilo.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 11, "bold"),
            foreground="#1a4d8f"
        )

    # ------------------------------------------------------
    # TÍTULO
    # ---------------------------------------------------------

    def crear_titulo(self):
        titulo = ttk.Label(
            self,
            text="Datos del Estudiante",
            style="Titulo.TLabel"
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 10)
        )

    # ---------------------------------------------------------
    # FORMULARIO
    # -------------------------------------------------------

    def crear_formulario(self):

        # Cédula
        ttk.Label(
            self,
            text="Cédula"
        ).grid(row=1, column=0, sticky="w", pady=4)

        self.entrada_cedula = ttk.Entry(
            self,
            width=30
        )

        self.entrada_cedula.grid(
            row=1,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # Nombre
        ttk.Label(
            self,
            text="Nombre"
        ).grid(row=2, column=0, sticky="w", pady=4)

        self.entrada_nombre = ttk.Entry(
            self,
            width=30
        )

        self.entrada_nombre.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # Apellidos
        ttk.Label(
            self,
            text="Apellidos"
        ).grid(row=3, column=0, sticky="w", pady=4)

        self.entrada_apellidos = ttk.Entry(
            self,
            width=30
        )

        self.entrada_apellidos.grid(
            row=3,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # Fecha de nacimiento
        ttk.Label(
            self,
            text="Fecha Nacimiento"
        ).grid(row=4, column=0, sticky="w", pady=4)

        self.entrada_fecha_nacimiento = DateEntry(
            self,
            width=27,
            date_pattern="yyyy-mm-dd"
        )

        self.entrada_fecha_nacimiento.grid(
            row=4,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # Correo electrónico
        ttk.Label(
            self,
            text="Correo electrónico"
        ).grid(row=5, column=0, sticky="w", pady=4)

        self.entrada_correo = ttk.Entry(
            self,
            width=30
        )

        self.entrada_correo.grid(
            row=5,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # Celular del estudiante
        ttk.Label(
            self,
            text="Celular del estudiante"
        ).grid(row=6, column=0, sticky="w", pady=4)

        self.entrada_celular_estudiante = ttk.Entry(
            self,
            width=30
        )

        self.entrada_celular_estudiante.grid(
            row=6,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # -----------------------------------------------------
        # COLUMNA DERECHA
        # -----------------------------------------------------

        # Nombre del padre/encargado
        ttk.Label(
            self,
            text="Nombre del padre/encargado"
        ).grid(row=1, column=2, sticky="w", pady=4)

        self.entrada_nombre_encargado = ttk.Entry(
            self,
            width=30
        )

        self.entrada_nombre_encargado.grid(
            row=1,
            column=3,
            sticky="w",
            padx=5
        )

        # Celular del padre/encargado
        ttk.Label(
            self,
            text="Celular del padre/encargado"
        ).grid(row=2, column=2, sticky="w", pady=4)

        self.entrada_celular_encargado = ttk.Entry(
            self,
            width=30
        )

        self.entrada_celular_encargado.grid(
            row=2,
            column=3,
            sticky="w",
            padx=5
        )

    # ---------------------------------------------------------
    # BOTONES
    # -------------------------------------------------------

    def crear_botones(self):

        marco_botones = ttk.Frame(self)

        marco_botones.grid(
            row=7,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(15, 15)
        )

        ttk.Button(
            marco_botones,
            text="Guardar",
            command=self.guardar_estudiante
        ).grid(row=0, column=0, padx=8)

        ttk.Button(
            marco_botones,
            text="Actualizar",
            command=self.actualizar_estudiante
        ).grid(row=0, column=1, padx=8)

        ttk.Button(
            marco_botones,
            text="Eliminar",
            command=self.eliminar_estudiante
        ).grid(row=0, column=2, padx=8)

        ttk.Button(
            marco_botones,
            text="Limpiar",
            command=self.limpiar_formulario
        ).grid(row=0, column=3, padx=8)

    # --------------------------------------------------------
    # TABLA
    # ---------------------------------------------------------

    def crear_listado(self):

        ttk.Label(
            self,
            text="Listado de Estudiantes",
            style="Titulo.TLabel"
        ).grid(
            row=8,
            column=0,
            columnspan=4,
            sticky="w",
            pady=5
        )

        columnas = (
            "id",
            "cedula",
            "nombre",
            "apellidos",
            "nacimiento",
            "correo",
            "celular",
            "encargado",
            "celular_encargado"
        )

        marco_tabla = ttk.Frame(self)

        marco_tabla.grid(
            row=9,
            column=0,
            columnspan=4,
            sticky="nsew"
        )

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            height=8
        )

        nombres = {
            "id": "ID",
            "cedula": "Cédula",
            "nombre": "Nombre",
            "apellidos": "Apellidos",
            "nacimiento": "Nacimiento",
            "correo": "Correo",
            "celular": "Celular",
            "encargado": "Padre/Encargado",
            "celular_encargado": "Celular Enc."
        }

        for columna in columnas:

            self.tabla.heading(
                columna,
                text=nombres[columna]
            )

            self.tabla.column(
                columna,
                width=90,
                anchor="center"
            )

        barra_scroll = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=barra_scroll.set
        )

        self.tabla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        barra_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        # Doble clic para seleccionar
        self.tabla.bind(
            "<Double-1>",
            self.seleccionar_fila
        )

    # ---------------------------------------------------------
    # MOSTRAR ESTUDIANTES EN LA TABLA
    # -------------------------------------------------------

    def cargar_estudiantes(self):

        # Primero limpia la tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Agrega los estudiantes guardados
        for estudiante in self.estudiantes:

            self.tabla.insert(
                "",
                "end",
                values=(
                    estudiante["id"],
                    estudiante["cedula"],
                    estudiante["nombre"],
                    estudiante["apellidos"],
                    estudiante["nacimiento"],
                    estudiante["correo"],
                    estudiante["celular"],
                    estudiante["encargado"],
                    estudiante["celular_encargado"]
                )
            )

    # -------------------------------------------------------
    # SELECCIONAR ESTUDIANTE
    # ---------------------------------------------------------

    def seleccionar_fila(self, evento):

        fila = self.tabla.focus()

        if not fila:
            return

        valores = self.tabla.item(
            fila,
            "values"
        )

        self.id_seleccionado = int(valores[0])

        self.entrada_cedula.delete(0, tk.END)
        self.entrada_cedula.insert(0, valores[1])

        self.entrada_nombre.delete(0, tk.END)
        self.entrada_nombre.insert(0, valores[2])

        self.entrada_apellidos.delete(0, tk.END)
        self.entrada_apellidos.insert(0, valores[3])

        self.entrada_fecha_nacimiento.set_date(
            valores[4]
        )

        self.entrada_correo.delete(0, tk.END)
        self.entrada_correo.insert(0, valores[5])

        self.entrada_celular_estudiante.delete(0, tk.END)
        self.entrada_celular_estudiante.insert(0, valores[6])

        self.entrada_nombre_encargado.delete(0, tk.END)
        self.entrada_nombre_encargado.insert(0, valores[7])

        self.entrada_celular_encargado.delete(0, tk.END)
        self.entrada_celular_encargado.insert(0, valores[8])

    # ---------------------------------------------------------
    # VALIDAR DATOS
    # -------------------------------------------------------

    def validar_datos(self):

        cedula = self.entrada_cedula.get().strip()
        nombre = self.entrada_nombre.get().strip()
        apellidos = self.entrada_apellidos.get().strip()
        correo = self.entrada_correo.get().strip()
        celular_estudiante = self.entrada_celular_estudiante.get().strip()
        celular_encargado = self.entrada_celular_encargado.get().strip()

        if cedula == "":
            messagebox.showwarning(
                "Validación",
                "La cédula es obligatoria."
            )
            return False

        if not cedula.isdigit():
            messagebox.showwarning(
                "Validación",
                "La cédula debe contener únicamente valores numéricos."
            )
            return False

        if nombre == "":
            messagebox.showwarning(
                "Validación",
                "El nombre es obligatorio."
            )
            return False

        if apellidos == "":
            messagebox.showwarning(
                "Validación",
                "Los apellidos son obligatorios."
            )
            return False

        if correo != "" and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo):
            messagebox.showwarning(
                "Validación",
                "El correo electrónico debe tener un formato válido."
            )
            return False

        if celular_estudiante != "" and not celular_estudiante.isdigit():
            messagebox.showwarning(
                "Validación",
                "El celular del estudiante debe ser numérico."
            )
            return False

        if celular_encargado != "" and not celular_encargado.isdigit():
            messagebox.showwarning(
                "Validación",
                "El celular del encargado debe ser numérico."
            )
            return False

        # Revisa que la cédula no esté repetida en la lista
        for estudiante in self.estudiantes:
            if estudiante["cedula"] == cedula and estudiante["id"] != self.id_seleccionado:
                messagebox.showwarning(
                    "Validación",
                    "Ya existe un estudiante con esa cédula."
                )
                return False

        return True

    # ---------------------------------------------------------
    # GUARDAR
    # ----------------------------------------------------

    def guardar_estudiante(self):

        if not self.validar_datos():
            return

        # Crear un nuevo ID
        nuevo_id = len(self.estudiantes) + 1

        estudiante = {
            "id": nuevo_id,
            "cedula": self.entrada_cedula.get().strip(),
            "nombre": self.entrada_nombre.get().strip(),
            "apellidos": self.entrada_apellidos.get().strip(),
            "nacimiento": self.entrada_fecha_nacimiento.get_date().isoformat(),
            "correo": self.entrada_correo.get().strip(),
            "celular": self.entrada_celular_estudiante.get().strip(),
            "encargado": self.entrada_nombre_encargado.get().strip(),
            "celular_encargado": self.entrada_celular_encargado.get().strip()
        }

        self.estudiantes.append(estudiante)

        messagebox.showinfo(
            "Éxito",
            "Estudiante guardado."
        )

        self.cargar_estudiantes()
        self.limpiar_formulario()

    # ------------------------------------------------------
    # ACTUALIZAR
    # ---------------------------------------------------------

    def actualizar_estudiante(self):

        if self.id_seleccionado is None:

            messagebox.showwarning(
                "Actualizar",
                "Selecciona un estudiante de la tabla."
            )

            return

        if not self.validar_datos():
            return

        for estudiante in self.estudiantes:

            if estudiante["id"] == self.id_seleccionado:

                estudiante["cedula"] = self.entrada_cedula.get().strip()
                estudiante["nombre"] = self.entrada_nombre.get().strip()
                estudiante["apellidos"] = self.entrada_apellidos.get().strip()
                estudiante["nacimiento"] = self.entrada_fecha_nacimiento.get_date().isoformat()
                estudiante["correo"] = self.entrada_correo.get().strip()
                estudiante["celular"] = self.entrada_celular_estudiante.get().strip()
                estudiante["encargado"] = self.entrada_nombre_encargado.get().strip()
                estudiante["celular_encargado"] = self.entrada_celular_encargado.get().strip()

        messagebox.showinfo(
            "Éxito",
            "Estudiante actualizado."
        )

        self.cargar_estudiantes()
        self.limpiar_formulario()

    # ---------------------------------------------------------
    # ELIMINAR
    # -------------------------------------------------------

    def eliminar_estudiante(self):

        if self.id_seleccionado is None:

            messagebox.showwarning(
                "Eliminar",
                "Selecciona un estudiante de la tabla."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Deseas eliminar este estudiante?"
        )

        if not confirmar:
            return

        for estudiante in self.estudiantes:

            if estudiante["id"] == self.id_seleccionado:
                self.estudiantes.remove(estudiante)
                break

        messagebox.showinfo(
            "Éxito",
            "Estudiante eliminado."
        )

        self.cargar_estudiantes()
        self.limpiar_formulario()

    # ---------------------------------------------------------
    # LIMPIAR
    # ------------------------------------------------------

    def limpiar_formulario(self):

        self.id_seleccionado = None

        self.entrada_cedula.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_apellidos.delete(0, tk.END)

        self.entrada_fecha_nacimiento.set_date(
            date.today()
        )

        self.entrada_correo.delete(0, tk.END)
        self.entrada_celular_estudiante.delete(0, tk.END)
        self.entrada_nombre_encargado.delete(0, tk.END)
        self.entrada_celular_encargado.delete(0, tk.END)


# ------------------------------------------------------
# EJECUTAR PROGRAMA
# ---------------------------------------------------------

if __name__ == "__main__":

    ventana = tk.Tk()

    ventana.title("Gestión de Estudiantes")

    ventana.geometry("1000x600")

    InterfazEstudiantes(ventana).pack(
        fill="both",
        expand=True
    )

    ventana.mainloop()