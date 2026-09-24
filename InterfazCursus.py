
# Interfaz Cursos

# Librería 
# pip install tkcalendar

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import DateEntry


class InterfazCursos(ttk.Frame):

    ESTADOS = ("Activo", "Inactivo")

    def __init__(self, contenedor):
        super().__init__(contenedor, padding=15)

        # Lista donde se guardan los cursos temporalmente
        self.cursos = []

        # Guarda el índice del curso seleccionado
        self.id_seleccionado = None

        self.crear_estilos()
        self.crear_titulo()
        self.crear_formulario()
        self.crear_botones()
        self.crear_listado()

        self.cargar_cursos()

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

        estilo.configure(
            "Campo.TLabel",
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Accion.TButton",
            font=("Segoe UI", 9, "bold"),
            padding=6
        )

    # ---------------------------------------------------------
    # TÍTULO
    # ---------------------------------------------------------

    def crear_titulo(self):
        titulo = ttk.Label(
            self,
            text="Datos del Curso",
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
    # ---------------------------------------------------------

    def crear_formulario(self):

        # Referencia
        ttk.Label(
            self,
            text="Referencia"
        ).grid(row=1, column=0, sticky="w", pady=4)

        self.entrada_referencia = ttk.Entry(
            self,
            width=32
        )

        self.entrada_referencia.grid(
            row=1,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # Descripción
        ttk.Label(
            self,
            text="Descripción"
        ).grid(row=2, column=0, sticky="w", pady=4)

        self.entrada_descripcion = ttk.Entry(
            self,
            width=32
        )

        self.entrada_descripcion.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # Fecha de inicio
        ttk.Label(
            self,
            text="Fecha Inicio"
        ).grid(row=3, column=0, sticky="w", pady=4)

        self.entrada_fecha_inicio = DateEntry(
            self,
            width=29,
            date_pattern="yyyy-mm-dd"
        )

        self.entrada_fecha_inicio.grid(
            row=3,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # Cuando cambia la fecha, coloca automáticamente el mes
        self.entrada_fecha_inicio.bind(
            "<<DateEntrySelected>>",
            self.autocompletar_mes
        )

        # Fecha final
        ttk.Label(
            self,
            text="Fecha Final"
        ).grid(row=4, column=0, sticky="w", pady=4)

        self.entrada_fecha_final = DateEntry(
            self,
            width=29,
            date_pattern="yyyy-mm-dd"
        )

        self.entrada_fecha_final.grid(
            row=4,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # Estado
        ttk.Label(
            self,
            text="Estado"
        ).grid(row=5, column=0, sticky="w", pady=4)

        self.combo_estado = ttk.Combobox(
            self,
            width=29,
            values=self.ESTADOS,
            state="readonly"
        )

        self.combo_estado.current(0)

        self.combo_estado.grid(
            row=5,
            column=1,
            sticky="w",
            padx=(5, 30)
        )

        # -----------------------------------------------------
        # COLUMNA DERECHA
        # -----------------------------------------------------

        # Docente
        ttk.Label(
            self,
            text="Docente"
        ).grid(row=1, column=2, sticky="w", pady=4)

        self.entrada_docente = ttk.Entry(
            self,
            width=32
        )

        self.entrada_docente.grid(
            row=1,
            column=3,
            sticky="w",
            padx=5
        )

        # Horas de capacitación
        ttk.Label(
            self,
            text="Horas de Capacitación"
        ).grid(row=2, column=2, sticky="w", pady=4)

        self.entrada_horas_capacitacion = ttk.Entry(
            self,
            width=32
        )

        self.entrada_horas_capacitacion.grid(
            row=2,
            column=3,
            sticky="w",
            padx=5
        )

        # Horas de asesoría
        ttk.Label(
            self,
            text="Horas de Asesoría"
        ).grid(row=3, column=2, sticky="w", pady=4)

        self.entrada_horas_asesoria = ttk.Entry(
            self,
            width=32
        )

        self.entrada_horas_asesoria.grid(
            row=3,
            column=3,
            sticky="w",
            padx=5
        )

        # Mes
        ttk.Label(
            self,
            text="Mes"
        ).grid(row=4, column=2, sticky="w", pady=4)

        self.entrada_mes = ttk.Entry(
            self,
            width=32
        )

        self.entrada_mes.grid(
            row=4,
            column=3,
            sticky="w",
            padx=5
        )

    # ---------------------------------------------------------
    # COLOCAR EL MES AUTOMÁTICAMENTE
    # ---------------------------------------------------------

    def autocompletar_mes(self, evento=None):

        meses = (
            "ENERO", "FEBRERO", "MARZO", "ABRIL",
            "MAYO", "JUNIO", "JULIO", "AGOSTO",
            "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
        )

        fecha = self.entrada_fecha_inicio.get_date()

        self.entrada_mes.delete(0, tk.END)

        self.entrada_mes.insert(
            0,
            meses[fecha.month - 1]
        )

    # ---------------------------------------------------------
    # BOTONES
    # ---------------------------------------------------------

    def crear_botones(self):

        marco_botones = ttk.Frame(self)

        marco_botones.grid(
            row=6,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(15, 15)
        )

        ttk.Button(
            marco_botones,
            text="Guardar",
            command=self.guardar_curso
        ).grid(row=0, column=0, padx=8)

        ttk.Button(
            marco_botones,
            text="Actualizar",
            command=self.actualizar_curso
        ).grid(row=0, column=1, padx=8)

        ttk.Button(
            marco_botones,
            text="Eliminar",
            command=self.eliminar_curso
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
            text="Listado de Cursos",
            style="Titulo.TLabel"
        ).grid(
            row=7,
            column=0,
            columnspan=4,
            sticky="w",
            pady=5
        )

        columnas = (
            "id",
            "referencia",
            "descripcion",
            "inicio",
            "final",
            "estado",
            "docente",
            "horas_cap",
            "horas_ases",
            "mes"
        )

        marco_tabla = ttk.Frame(self)

        marco_tabla.grid(
            row=8,
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
            "referencia": "Referencia",
            "descripcion": "Descripción",
            "inicio": "Inicio",
            "final": "Final",
            "estado": "Estado",
            "docente": "Docente",
            "horas_cap": "Horas Cap.",
            "horas_ases": "Horas Ases.",
            "mes": "Mes"
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
    # MOSTRAR CURSOS EN LA TABLA
    # ---------------------------------------------------------

    def cargar_cursos(self):

        # Primero limpia la tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Agrega los cursos guardados
        for curso in self.cursos:

            self.tabla.insert(
                "",
                "end",
                values=(
                    curso["id"],
                    curso["referencia"],
                    curso["descripcion"],
                    curso["inicio"],
                    curso["final"],
                    curso["estado"],
                    curso["docente"],
                    curso["horas_cap"],
                    curso["horas_ases"],
                    curso["mes"]
                )
            )

    # ---------------------------------------------------------
    # SELECCIONAR CURSO
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

        self.entrada_referencia.delete(0, tk.END)
        self.entrada_referencia.insert(0, valores[1])

        self.entrada_descripcion.delete(0, tk.END)
        self.entrada_descripcion.insert(0, valores[2])

        self.entrada_fecha_inicio.set_date(
            valores[3]
        )

        self.entrada_fecha_final.set_date(
            valores[4]
        )

        self.combo_estado.set(
            valores[5]
        )

        self.entrada_docente.delete(0, tk.END)
        self.entrada_docente.insert(0, valores[6])

        self.entrada_horas_capacitacion.delete(
            0,
            tk.END
        )

        self.entrada_horas_capacitacion.insert(
            0,
            valores[7]
        )

        self.entrada_horas_asesoria.delete(
            0,
            tk.END
        )

        self.entrada_horas_asesoria.insert(
            0,
            valores[8]
        )

        self.entrada_mes.delete(
            0,
            tk.END
        )

        self.entrada_mes.insert(
            0,
            valores[9]
        )

    # ---------------------------------------------------------
    # VALIDAR DATOS
    # ---------------------------------------------------------

    def validar_datos(self):

        referencia = self.entrada_referencia.get().strip()
        descripcion = self.entrada_descripcion.get().strip()
        horas_cap = self.entrada_horas_capacitacion.get().strip()
        horas_ases = self.entrada_horas_asesoria.get().strip()

        if referencia == "":
            messagebox.showwarning(
                "Validación",
                "La referencia es obligatoria."
            )
            return False

        if descripcion == "":
            messagebox.showwarning(
                "Validación",
                "La descripción es obligatoria."
            )
            return False

        if self.entrada_fecha_final.get_date() < self.entrada_fecha_inicio.get_date():

            messagebox.showwarning(
                "Validación",
                "La fecha final no puede ser menor que la fecha inicial."
            )

            return False

        if not horas_cap.isdigit():

            messagebox.showwarning(
                "Validación",
                "Las horas de capacitación deben ser un número entero."
            )

            return False

        try:
            float(horas_ases)
        except ValueError:

            messagebox.showwarning(
                "Validación",
                "Las horas de asesoría deben ser un número."
            )

            return False

        return True

    # ---------------------------------------------------------
    # GUARDAR
    # ---------------------------------------------------------

    def guardar_curso(self):

        if not self.validar_datos():
            return

        # Crear un nuevo ID
        nuevo_id = len(self.cursos) + 1

        curso = {
            "id": nuevo_id,
            "referencia": self.entrada_referencia.get().strip(),
            "descripcion": self.entrada_descripcion.get().strip(),
            "inicio": self.entrada_fecha_inicio.get_date().isoformat(),
            "final": self.entrada_fecha_final.get_date().isoformat(),
            "estado": self.combo_estado.get(),
            "docente": self.entrada_docente.get().strip(),
            "horas_cap": int(
                self.entrada_horas_capacitacion.get()
            ),
            "horas_ases": float(
                self.entrada_horas_asesoria.get()
            ),
            "mes": self.entrada_mes.get().strip()
        }

        self.cursos.append(curso)

        messagebox.showinfo(
            "Éxito",
            "Curso guardado correctamente."
        )

        self.cargar_cursos()
        self.limpiar_formulario()

    # ---------------------------------------------------------
    # ACTUALIZAR
    # ---------------------------------------------------------

    def actualizar_curso(self):

        if self.id_seleccionado is None:

            messagebox.showwarning(
                "Actualizar",
                "Selecciona un curso de la tabla."
            )

            return

        if not self.validar_datos():
            return

        for curso in self.cursos:

            if curso["id"] == self.id_seleccionado:

                curso["referencia"] = self.entrada_referencia.get().strip()
                curso["descripcion"] = self.entrada_descripcion.get().strip()
                curso["inicio"] = self.entrada_fecha_inicio.get_date().isoformat()
                curso["final"] = self.entrada_fecha_final.get_date().isoformat()
                curso["estado"] = self.combo_estado.get()
                curso["docente"] = self.entrada_docente.get().strip()

                curso["horas_cap"] = int(
                    self.entrada_horas_capacitacion.get()
                )

                curso["horas_ases"] = float(
                    self.entrada_horas_asesoria.get()
                )

                curso["mes"] = self.entrada_mes.get().strip()

        messagebox.showinfo(
            "Éxito",
            "Curso actualizado correctamente."
        )

        self.cargar_cursos()
        self.limpiar_formulario()

    # ---------------------------------------------------------
    # ELIMINAR
    # ---------------------------------------------------------

    def eliminar_curso(self):

        if self.id_seleccionado is None:

            messagebox.showwarning(
                "Eliminar",
                "Selecciona un curso de la tabla."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Deseas eliminar este curso?"
        )

        if not confirmar:
            return

        for curso in self.cursos:

            if curso["id"] == self.id_seleccionado:
                self.cursos.remove(curso)
                break

        messagebox.showinfo(
            "Éxito",
            "Curso eliminado correctamente."
        )

        self.cargar_cursos()
        self.limpiar_formulario()

    # ---------------------------------------------------------
    # LIMPIAR
    # ---------------------------------------------------------

    def limpiar_formulario(self):

        self.id_seleccionado = None

        self.entrada_referencia.delete(
            0,
            tk.END
        )

        self.entrada_descripcion.delete(
            0,
            tk.END
        )

        self.entrada_fecha_inicio.set_date(
            date.today()
        )

        self.entrada_fecha_final.set_date(
            date.today()
        )

        self.combo_estado.current(0)

        self.entrada_docente.delete(
            0,
            tk.END
        )

        self.entrada_horas_capacitacion.delete(
            0,
            tk.END
        )

        self.entrada_horas_asesoria.delete(
            0,
            tk.END
        )

        self.entrada_mes.delete(
            0,
            tk.END
        )


# ---------------------------------------------------------
# EJECUTAR PROGRAMA
# ---------------------------------------------------------

if __name__ == "__main__":

    ventana = tk.Tk()

    ventana.title("Gestión de Cursos")

    ventana.geometry("1000x600")

    InterfazCursos(ventana).pack(
        fill="both",
        expand=True
    )

    ventana.mainloop()

