#Interfaz EStudiantes
"""
interfaz/interfaz_estudiantes.py
---------------------------------
Interfaz gráfica del módulo "Gestión de Estudiantes".
Reproduce la ventana de referencia: formulario con los datos del
estudiante, 4 botones (Guardar / Actualizar / Eliminar / Limpiar)
y un listado (grid) con todos los estudiantes registrados.

Requiere:
    pip install tkcalendar
(tkcalendar da el selector de fecha desplegable que se ve en la
captura de referencia para "Fecha Nacimiento").
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import date

from tkcalendar import DateEntry

from modelos.estudiante import Estudiante, EstudianteDAO


class InterfazEstudiantes(ttk.Frame):
    """
    Hereda de ttk.Frame para poder usarse:
      - como una pestaña dentro de un ttk.Notebook (varios módulos), o
      - sola, metida directo en una ventana Tk() (ver el bloque
        "if __name__ == '__main__'" al final del archivo).
    """

    def __init__(self, contenedor):
        super().__init__(contenedor, padding=15)

        # id_seleccionado guarda el id_estudiante de la fila que el
        # usuario eligió en el grid (doble clic). Si es None, significa
        # que no hay ninguna fila seleccionada (modo "nuevo registro").
        self.id_seleccionado = None

        self._crear_estilos()
        self._construir_titulo()
        self._construir_formulario()
        self._construir_botones()
        self._construir_listado()

        # Al abrir la ventana, se carga el listado de una vez.
        self.cargar_estudiantes()

    # ------------------------------------------------------------------
    # ESTILOS
    # ------------------------------------------------------------------
    def _crear_estilos(self):
        """
        Define estilos ttk reutilizables para que la interfaz se vea
        más prolija que los widgets por defecto de Tkinter.
        """
        estilo = ttk.Style()
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 11, "bold"),
                          foreground="#1a4d8f")
        estilo.configure("Campo.TLabel", font=("Segoe UI", 9))
        estilo.configure("Accion.TButton", font=("Segoe UI", 9, "bold"),
                          padding=6)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        estilo.configure("Treeview", rowheight=24, font=("Segoe UI", 9))

    # ------------------------------------------------------------------
    # TÍTULO DE SECCIÓN
    # ------------------------------------------------------------------
    def _construir_titulo(self):
        titulo = ttk.Label(self, text="Datos del Estudiante", style="Titulo.TLabel")
        # row=0 y columnspan=4 hace que el título abarque todo el ancho.
        titulo.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

    # ------------------------------------------------------------------
    # FORMULARIO (2 columnas de campos, igual que la referencia)
    # ------------------------------------------------------------------
    def _construir_formulario(self):
        # --- Columna izquierda ---
        ttk.Label(self, text="Cédula", style="Campo.TLabel").grid(
            row=1, column=0, sticky="w", pady=4)
        self.entrada_cedula = ttk.Entry(self, width=30)
        self.entrada_cedula.grid(row=1, column=1, sticky="w", padx=(5, 30))

        ttk.Label(self, text="Nombre", style="Campo.TLabel").grid(
            row=2, column=0, sticky="w", pady=4)
        self.entrada_nombre = ttk.Entry(self, width=30)
        self.entrada_nombre.grid(row=2, column=1, sticky="w", padx=(5, 30))

        ttk.Label(self, text="Apellidos", style="Campo.TLabel").grid(
            row=3, column=0, sticky="w", pady=4)
        self.entrada_apellidos = ttk.Entry(self, width=30)
        self.entrada_apellidos.grid(row=3, column=1, sticky="w", padx=(5, 30))

        ttk.Label(self, text="Fecha Nacimiento", style="Campo.TLabel").grid(
            row=4, column=0, sticky="w", pady=4)
        # DateEntry = combo con calendario desplegable (igual a la referencia)
        self.entrada_fecha_nacimiento = DateEntry(
            self, width=27, date_pattern="yyyy-mm-dd",
            maxdate=date.today())
        self.entrada_fecha_nacimiento.grid(row=4, column=1, sticky="w", padx=(5, 30))

        ttk.Label(self, text="Correo electrónico", style="Campo.TLabel").grid(
            row=5, column=0, sticky="w", pady=4)
        self.entrada_correo = ttk.Entry(self, width=30)
        self.entrada_correo.grid(row=5, column=1, sticky="w", padx=(5, 30))

        ttk.Label(self, text="Celular del estudiante", style="Campo.TLabel").grid(
            row=6, column=0, sticky="w", pady=4)
        self.entrada_celular_estudiante = ttk.Entry(self, width=30)
        self.entrada_celular_estudiante.grid(row=6, column=1, sticky="w", padx=(5, 30))

        # --- Columna derecha ---
        ttk.Label(self, text="Nombre del padre/encargado", style="Campo.TLabel").grid(
            row=1, column=2, sticky="w", pady=4)
        self.entrada_nombre_encargado = ttk.Entry(self, width=30)
        self.entrada_nombre_encargado.grid(row=1, column=3, sticky="w", padx=5)

        ttk.Label(self, text="Celular del padre/encargado", style="Campo.TLabel").grid(
            row=2, column=2, sticky="w", pady=4)
        self.entrada_celular_encargado = ttk.Entry(self, width=30)
        self.entrada_celular_encargado.grid(row=2, column=3, sticky="w", padx=5)

    # ------------------------------------------------------------------
    # BOTONES: Guardar / Actualizar / Eliminar / Limpiar
    # ------------------------------------------------------------------
    def _construir_botones(self):
        marco_botones = ttk.Frame(self)
        marco_botones.grid(row=7, column=0, columnspan=4, sticky="w", pady=(15, 15))

        ttk.Button(marco_botones, text="Guardar", style="Accion.TButton",
                   command=self.guardar_estudiante).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(marco_botones, text="Actualizar", style="Accion.TButton",
                   command=self.actualizar_estudiante).grid(row=0, column=1, padx=8)
        ttk.Button(marco_botones, text="Eliminar", style="Accion.TButton",
                   command=self.eliminar_estudiante).grid(row=0, column=2, padx=8)
        ttk.Button(marco_botones, text="Limpiar", style="Accion.TButton",
                   command=self.limpiar_formulario).grid(row=0, column=3, padx=8)

    # ------------------------------------------------------------------
    # LISTADO (grid / Treeview) DE ESTUDIANTES
    # ------------------------------------------------------------------
    def _construir_listado(self):
        ttk.Label(self, text="Listado de Estudiantes", style="Titulo.TLabel").grid(
            row=8, column=0, columnspan=4, sticky="w", pady=(5, 5))

        columnas = ("id", "cedula", "nombre", "apellidos", "nacimiento",
                    "correo", "celular", "encargado", "celular_encargado")

        marco_tabla = ttk.Frame(self)
        marco_tabla.grid(row=9, column=0, columnspan=4, sticky="nsew")

        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings",
                                   height=8)

        # Encabezados visibles al usuario
        encabezados = {
            "id": "ID", "cedula": "Cédula", "nombre": "Nombre",
            "apellidos": "Apellidos", "nacimiento": "Nacimiento",
            "correo": "Correo", "celular": "Celular",
            "encargado": "Padre/Encargado", "celular_encargado": "Celular Enc.",
        }
        anchos = {
            "id": 40, "cedula": 90, "nombre": 110, "apellidos": 130,
            "nacimiento": 90, "correo": 150, "celular": 80,
            "encargado": 130, "celular_encargado": 90,
        }
        for clave in columnas:
            self.tabla.heading(clave, text=encabezados[clave])
            self.tabla.column(clave, width=anchos[clave], anchor="center")

        # Franjas de color alternadas para que se lea mejor (fila par/impar)
        self.tabla.tag_configure("par", background="#f2f6fc")
        self.tabla.tag_configure("impar", background="#ffffff")

        barra_scroll = ttk.Scrollbar(marco_tabla, orient="vertical",
                                      command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra_scroll.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        barra_scroll.grid(row=0, column=1, sticky="ns")

        # Doble clic sobre una fila -> carga esos datos en el formulario
        self.tabla.bind("<Double-1>", self.seleccionar_fila)

    # ------------------------------------------------------------------
    # LÓGICA: cargar datos del grid
    # ------------------------------------------------------------------
    def cargar_estudiantes(self):
        """Limpia el grid y lo vuelve a llenar consultando la base de datos."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        try:
            estudiantes = EstudianteDAO.listar_todos()
        except Exception as error:
            messagebox.showerror("Error de conexión",
                                  f"No se pudo consultar la base de datos.\n{error}")
            return

        for indice, estudiante in enumerate(estudiantes):
            etiqueta = "par" if indice % 2 == 0 else "impar"
            self.tabla.insert("", "end", values=(
                estudiante.id_estudiante, estudiante.cedula, estudiante.nombre,
                estudiante.apellidos, estudiante.fecha_nacimiento,
                estudiante.correo, estudiante.celular_estudiante,
                estudiante.nombre_encargado, estudiante.celular_encargado,
            ), tags=(etiqueta,))

    def seleccionar_fila(self, evento):
        """Al hacer doble clic en una fila, copia sus datos al formulario."""
        item = self.tabla.focus()
        if not item:
            return
        valores = self.tabla.item(item, "values")

        self.id_seleccionado = int(valores[0])
        self.entrada_cedula.delete(0, tk.END)
        self.entrada_cedula.insert(0, valores[1])
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_nombre.insert(0, valores[2])
        self.entrada_apellidos.delete(0, tk.END)
        self.entrada_apellidos.insert(0, valores[3])
        try:
            self.entrada_fecha_nacimiento.set_date(valores[4])
        except Exception:
            pass  # si la fecha viene vacía o en un formato raro, se ignora
        self.entrada_correo.delete(0, tk.END)
        self.entrada_correo.insert(0, valores[5])
        self.entrada_celular_estudiante.delete(0, tk.END)
        self.entrada_celular_estudiante.insert(0, valores[6])
        self.entrada_nombre_encargado.delete(0, tk.END)
        self.entrada_nombre_encargado.insert(0, valores[7])
        self.entrada_celular_encargado.delete(0, tk.END)
        self.entrada_celular_encargado.insert(0, valores[8])

    # ------------------------------------------------------------------
    # VALIDACIONES (según el documento de requerimientos)
    # ------------------------------------------------------------------
    def _validar_campos(self, id_excluir=None):
        cedula = self.entrada_cedula.get().strip()
        nombre = self.entrada_nombre.get().strip()
        apellidos = self.entrada_apellidos.get().strip()
        correo = self.entrada_correo.get().strip()
        celular_estudiante = self.entrada_celular_estudiante.get().strip()
        celular_encargado = self.entrada_celular_encargado.get().strip()

        if not cedula:
            messagebox.showwarning("Validación", "La cédula es obligatoria.")
            return False
        if not cedula.isdigit():
            messagebox.showwarning("Validación", "La cédula debe contener únicamente valores numéricos.")
            return False
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return False
        if not apellidos:
            messagebox.showwarning("Validación", "Los apellidos son obligatorios.")
            return False
        if correo and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo):
            messagebox.showwarning("Validación", "El correo electrónico debe tener un formato válido.")
            return False
        if celular_estudiante and not celular_estudiante.isdigit():
            messagebox.showwarning("Validación", "El celular del estudiante debe ser numérico.")
            return False
        if celular_encargado and not celular_encargado.isdigit():
            messagebox.showwarning("Validación", "El celular del encargado debe ser numérico.")
            return False
        if EstudianteDAO.existe_cedula(cedula, id_excluir):
            messagebox.showwarning("Validación", "Ya existe un estudiante con esa cédula.")
            return False

        return True

    def _construir_objeto_estudiante(self):
        """Arma un objeto Estudiante a partir de lo que hay en el formulario."""
        return Estudiante(
            id_estudiante=self.id_seleccionado,
            cedula=self.entrada_cedula.get().strip(),
            nombre=self.entrada_nombre.get().strip(),
            apellidos=self.entrada_apellidos.get().strip(),
            fecha_nacimiento=self.entrada_fecha_nacimiento.get_date().isoformat(),
            correo=self.entrada_correo.get().strip(),
            celular_estudiante=self.entrada_celular_estudiante.get().strip(),
            nombre_encargado=self.entrada_nombre_encargado.get().strip(),
            celular_encargado=self.entrada_celular_encargado.get().strip(),
        )

    # ------------------------------------------------------------------
    # ACCIONES DE LOS BOTONES
    # ------------------------------------------------------------------
    def guardar_estudiante(self):
        if not self._validar_campos():
            return
        try:
            EstudianteDAO.guardar(self._construir_objeto_estudiante())
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo guardar el estudiante.\n{error}")
            return
        messagebox.showinfo("Éxito", "Estudiante guardado.")
        self.cargar_estudiantes()
        self.limpiar_formulario()

    def actualizar_estudiante(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Actualizar", "Selecciona un estudiante del listado (doble clic).")
            return
        if not self._validar_campos(id_excluir=self.id_seleccionado):
            return
        try:
            EstudianteDAO.actualizar(self._construir_objeto_estudiante())
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo actualizar el estudiante.\n{error}")
            return
        messagebox.showinfo("Éxito", "Estudiante actualizado.")
        self.cargar_estudiantes()
        self.limpiar_formulario()

    def eliminar_estudiante(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Eliminar", "Selecciona un estudiante del listado (doble clic).")
            return
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Eliminar este estudiante? Sus matrículas asociadas también se eliminarán.")
        if not confirmar:
            return
        try:
            EstudianteDAO.eliminar(self.id_seleccionado)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo eliminar el estudiante.\n{error}")
            return
        messagebox.showinfo("Éxito", "Estudiante eliminado.")
        self.cargar_estudiantes()
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.id_seleccionado = None
        self.entrada_cedula.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_apellidos.delete(0, tk.END)
        self.entrada_fecha_nacimiento.set_date(date.today())
        self.entrada_correo.delete(0, tk.END)
        self.entrada_celular_estudiante.delete(0, tk.END)
        self.entrada_nombre_encargado.delete(0, tk.END)
        self.entrada_celular_encargado.delete(0, tk.END)
        self.tabla.selection_remove(self.tabla.selection())


# ----------------------------------------------------------------------
# Bloque de prueba: permite abrir ESTA interfaz sola, sin el resto del
# proyecto, solo para revisar visualmente cómo se ve.
# ----------------------------------------------------------------------
if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.title("Gestión de Estudiantes")
    raiz.geometry("950x600")
    InterfazEstudiantes(raiz).pack(fill="both", expand=True)
    raiz.mainloop()
