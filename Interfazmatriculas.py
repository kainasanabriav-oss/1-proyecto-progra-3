# Interfaz de matriculas 




# pip install tkcalendar  

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


class InterfazMatriculas(ttk.Frame):

    # Estados que puede tener una matricula)
    ESTADOS = ("Activa", "Retirado", "Finalizado", "Desertor")

    # Esta interfaz necesita ver la lista de estudiantes y la lista de cursos para poder llenar los combobox
   
    def __init__(self, contenedor, lista_estudiantes, lista_cursos):
        super().__init__(contenedor, padding=15)

        # Guardamos las listas que nos pasaron, para usarlas despues
        self.lista_estudiantes = lista_estudiantes
        self.lista_cursos = lista_cursos

        # Lista donde se guardan las matriculas hechas
        self.matriculas = []

        # Guarda el id de la matricula seleccionada en la tabla
        self.id_seleccionado = None

        self.crear_estilos()
        self.crear_titulo()
        self.crear_formulario()
        self.crear_botones()
        self.crear_listado()

        self.cargar_matriculas()

    # ---------------------------------------------------------
    # ESTILOS
    # ---------------------------------------------------------

    def crear_estilos(self):
        estilo = ttk.Style()

        estilo.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 11, "bold"),
            foreground="#1a4d8f"
        )

    # ---------------------------------------------------------
    # TÍTULO
    # ---------------------------------------------------------

    def crear_titulo(self):
        ttk.Label(
            self,
            text="Gestión de Matrículas",
            style="Titulo.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

    # ---------------------------------------------------------
    # FORMULARIO
    # ---------------------------------------------------------

    def crear_formulario(self):

        # Combobox de Estudiante state="readonly" evita que el usuario escriba texto libre osea solo puede elegir en la lista 
        #
        ttk.Label(
            self,
            text="Estudiante"
        ).grid(row=1, column=0, sticky="w", pady=4)

        self.combo_estudiante = ttk.Combobox(
            self,
            width=45,
            state="readonly"
        )

        self.combo_estudiante.grid(row=1, column=1, sticky="w", padx=5)

        # Cada vez que el usuario le da clic al combo, refrescamos
        # la lista de opciones (por si agregaron estudiantes nuevos)
        self.combo_estudiante.bind(
            "<Button-1>",
            self.actualizar_combo_estudiantes
        )

        # Combobox de Curso, funciona igual que el de Estudiante
        ttk.Label(
            self,
            text="Curso"
        ).grid(row=2, column=0, sticky="w", pady=4)

        self.combo_curso = ttk.Combobox(
            self,
            width=45,
            state="readonly"
        )

        self.combo_curso.grid(row=2, column=1, sticky="w", padx=5)

        self.combo_curso.bind(
            "<Button-1>",
            self.actualizar_combo_cursos
        )

        # Combobox de Estado, ya trae sus opciones fijas (ESTADOS)
        ttk.Label(
            self,
            text="Estado"
        ).grid(row=3, column=0, sticky="w", pady=4)

        self.combo_estado = ttk.Combobox(
            self,
            width=45,
            values=self.ESTADOS,
            state="readonly"
        )

        self.combo_estado.current(0)
        self.combo_estado.grid(row=3, column=1, sticky="w", padx=5)

    # Arma el texto "cedula - nombre apellidos" para cada estudiante
    # y lo pone como opciones del combobox
    def actualizar_combo_estudiantes(self, evento=None):
        opciones = []

        for estudiante in self.lista_estudiantes:
            texto = estudiante["cedula"] + " - " + estudiante["nombre"] + " " + estudiante["apellidos"]
            opciones.append(texto)

        self.combo_estudiante["values"] = opciones

    # Arma el texto "referencia - descripcion" para cada curso
    # y lo pone como opciones del combobox
    def actualizar_combo_cursos(self, evento=None):
        opciones = []

        for curso in self.lista_cursos:
            texto = curso["referencia"] + " - " + curso["descripcion"]
            opciones.append(texto)

        self.combo_curso["values"] = opciones

    # ---------------------------------------------------------
    # BOTONES
    # ---------------------------------------------------------

    def crear_botones(self):

        marco_botones = ttk.Frame(self)

        marco_botones.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(15, 15)
        )

        ttk.Button(
            marco_botones,
            text="Matricular",
            command=self.matricular
        ).grid(row=0, column=0, padx=8)

        ttk.Button(
            marco_botones,
            text="Actualizar Estado",
            command=self.actualizar_estado
        ).grid(row=0, column=1, padx=8)

        ttk.Button(
            marco_botones,
            text="Eliminar Matrícula",
            command=self.eliminar_matricula
        ).grid(row=0, column=2, padx=8)

        ttk.Button(
            marco_botones,
            text="Limpiar",
            command=self.limpiar_formulario
        ).grid(row=0, column=3, padx=8)

    # ---------------------------------------------------------
    # TABLA
    # ---------------------------------------------------------

    def crear_listado(self):

        ttk.Label(
            self,
            text="Listado de Matrículas",
            style="Titulo.TLabel"
        ).grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

        columnas = (
            "id",
            "cedula",
            "nombre",
            "apellidos",
            "referencia",
            "descripcion",
            "fecha",
            "estado"
        )

        marco_tabla = ttk.Frame(self)

        marco_tabla.grid(row=6, column=0, columnspan=2, sticky="nsew")

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
            "referencia": "Curso",
            "descripcion": "Descripción",
            "fecha": "Fecha",
            "estado": "Estado"
        }

        for columna in columnas:
            self.tabla.heading(columna, text=nombres[columna])
            self.tabla.column(columna, width=100, anchor="center")

        barra_scroll = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(yscrollcommand=barra_scroll.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        barra_scroll.grid(row=0, column=1, sticky="ns")

        self.tabla.bind("<Double-1>", self.seleccionar_fila)

    # ---------------------------------------------------------
    # MOSTRAR MATRICULAS EN LA TABLA
    # ---------------------------------------------------------

    def cargar_matriculas(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for matricula in self.matriculas:
            self.tabla.insert(
                "",
                "end",
                values=(
                    matricula["id"],
                    matricula["cedula"],
                    matricula["nombre"],
                    matricula["apellidos"],
                    matricula["referencia"],
                    matricula["descripcion"],
                    matricula["fecha"],
                    matricula["estado"]
                )
            )

    # ---------------------------------------------------------
    # SELECCIONAR MATRICULA
    # ---------------------------------------------------------

    def seleccionar_fila(self, evento):

        fila = self.tabla.focus()

        if not fila:
            return

        valores = self.tabla.item(fila, "values")

        # Guardamos el id para que "Actualizar Estado" y "Eliminar"
        # sepan sobre cual matricula trabajar
        self.id_seleccionado = int(valores[0])

        # Ponemos en el combobox de Estado el estado actual de esa fila
        self.combo_estado.set(valores[7])

    # ---------------------------------------------------------
    # MATRICULAR (GUARDAR)
    # ---------------------------------------------------------

    def matricular(self):

        estudiante_texto = self.combo_estudiante.get()
        curso_texto = self.combo_curso.get()

        if estudiante_texto == "":
            messagebox.showwarning("Validación", "Debes seleccionar un estudiante.")
            return

        if curso_texto == "":
            messagebox.showwarning("Validación", "Debes seleccionar un curso.")
            return

        # El texto del combo es "cedula - nombre apellidos", entonces
        # partimos el texto por " - " y nos quedamos con la primera parte
        cedula = estudiante_texto.split(" - ")[0]
        referencia = curso_texto.split(" - ")[0]

        # No se permiten matriculas duplicadas (mismo estudiante y curso)
        for matricula in self.matriculas:
            if matricula["cedula"] == cedula and matricula["referencia"] == referencia:
                messagebox.showwarning(
                    "Validación",
                    "Ese estudiante ya está matriculado en ese curso."
                )
                return

        # Buscamos los datos completos del estudiante con esa cedula
        estudiante_encontrado = None
        for estudiante in self.lista_estudiantes:
            if estudiante["cedula"] == cedula:
                estudiante_encontrado = estudiante

        # Buscamos los datos completos del curso con esa referencia
        curso_encontrado = None
        for curso in self.lista_cursos:
            if curso["referencia"] == referencia:
                curso_encontrado = curso

        nuevo_id = len(self.matriculas) + 1

        matricula = {
            "id": nuevo_id,
            "cedula": estudiante_encontrado["cedula"],
            "nombre": estudiante_encontrado["nombre"],
            "apellidos": estudiante_encontrado["apellidos"],
            "referencia": curso_encontrado["referencia"],
            "descripcion": curso_encontrado["descripcion"],
            "fecha": date.today().isoformat(),
            "estado": self.combo_estado.get()
        }

        self.matriculas.append(matricula)

        messagebox.showinfo("Éxito", "Matrícula registrada.")

        self.cargar_matriculas()
        self.limpiar_formulario()

    # ---------------------------------------------------------
    # ACTUALIZAR ESTADO
    # ---------------------------------------------------------

    def actualizar_estado(self):

        if self.id_seleccionado is None:
            messagebox.showwarning("Actualizar", "Selecciona una matrícula de la tabla.")
            return

        for matricula in self.matriculas:
            if matricula["id"] == self.id_seleccionado:
                matricula["estado"] = self.combo_estado.get()

        messagebox.showinfo("Éxito", "Estado actualizado.")

        self.cargar_matriculas()
        self.limpiar_formulario()

    # ---------------------------------------------------------
    # ELIMINAR MATRICULA
    # ---------------------------------------------------------

    def eliminar_matricula(self):

        if self.id_seleccionado is None:
            messagebox.showwarning("Eliminar", "Selecciona una matrícula de la tabla.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Deseas eliminar esta matrícula?")

        if not confirmar:
            return

        for matricula in self.matriculas:
            if matricula["id"] == self.id_seleccionado:
                self.matriculas.remove(matricula)
                break

        messagebox.showinfo("Éxito", "Matrícula eliminada.")

        self.cargar_matriculas()
        self.limpiar_formulario()

    # ---------------------------------------------------------
    # LIMPIAR
    # ---------------------------------------------------------

    def limpiar_formulario(self):

        self.id_seleccionado = None
        self.combo_estudiante.set("")
        self.combo_curso.set("")
        self.combo_estado.current(0)


# ---------------------------------------------------------
# EJECUTAR PROGRAMA (prueba sola, con datos de ejemplo)
# ---------------------------------------------------------

if __name__ == "__main__":

    # Como esta interfaz necesita estudiantes y cursos para funcionar,
    # aqui le damos un par de datos de prueba para poder verla sola.
    estudiantes_prueba = [
        {"cedula": "120160779", "nombre": "Ashley", "apellidos": "Cascante Ruiz"}
    ]

    cursos_prueba = [
        {"referencia": "2407.FH.CSTI15009.1", "descripcion": "Hoja de Calculo G1"}
    ]

    ventana = tk.Tk()
    ventana.title("Gestión de Matrículas")
    ventana.geometry("1000x600")

    InterfazMatriculas(ventana, estudiantes_prueba, cursos_prueba).pack(
        fill="both",
        expand=True
    )

    ventana.mainloop()