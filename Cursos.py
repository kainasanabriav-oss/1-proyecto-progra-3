class CursoError(Exception):
    # Se usa cuando algo sale mal al guardar/actualizar/eliminar un curso
    # (por ejemplo una referencia repetida, o un error de la base de datos)
    pass

# =========================================================================
# CURSO: solo guarda los datos de un curso
# =========================================================================
class Curso:

    # Así se traduce el combo de la interfaz al valor que se guarda en SQL
    ESTADOS_TEXTO_A_NUMERO = {"Activo": 1, "Inactivo": 0}
    ESTADOS_NUMERO_A_TEXTO = {1: "Activo", 0: "Inactivo"}

    def __init__(self, referencia, descripcion, fecha_inicio, fecha_final,
                 estado, docente, horas_capacitacion, horas_asesoria, mes,
                 id=None):

        # id es None mientras el curso todavía no se ha guardado en la BD.
        # Cuando se guarda, SQL Server le asigna el número automáticamente
        # (es IDENTITY), por eso aquí no lo inventamos nosotros.
        self.id = id
        self.referencia = referencia
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio          # objeto date
        self.fecha_final = fecha_final            # objeto date
        self.estado = estado                      # 1 o 0 (como está en la BD)
        self.docente = docente
        self.horas_capacitacion = horas_capacitacion
        self.horas_asesoria = horas_asesoria
        self.mes = mes

    @property
    def estado_texto(self):
        # Para mostrar "Activo" / "Inactivo" en el combo y en la tabla
        return self.ESTADOS_NUMERO_A_TEXTO.get(self.estado, "")

# =========================================================================
# CURSOREPOSITORIO: todo el SQL de la tabla cursos vive aquí
# =========================================================================
class CursoRepositorio:

    def __init__(self, conexion):
        # "conexion" es un objeto Conexion (de Conexion_SQL.py)
        self.conexion = conexion

    # ---------------------------------------------------------------
    # LISTAR: trae todos los cursos de la base de datos
    # ---------------------------------------------------------------
    def listar(self):

        sql = """
            SELECT id, referencia, descripcion, fecha_inicio, fecha_final,
                   estado, docente, horas_capacitacion, horas_asesoria, mes
            FROM cursos
            ORDER BY fecha_inicio DESC
        """

        conexion = self.conexion.conectar()
        cursor = conexion.cursor()
        cursor.execute(sql)
        filas = cursor.fetchall()
        cursor.close()

        cursos = []

        for fila in filas:
            curso = Curso(
                id=fila[0],
                referencia=fila[1],
                descripcion=fila[2],
                fecha_inicio=fila[3],
                fecha_final=fila[4],
                estado=int(fila[5]),
                docente=fila[6],
                horas_capacitacion=fila[7],
                horas_asesoria=fila[8],
                mes=fila[9],
            )
            cursos.append(curso)

        return cursos

    # ---------------------------------------------------------------
    # EXISTE: revisa si ya hay un curso con esa referencia
    # (la referencia debe ser única aunque ya no sea la llave primaria)
    # ---------------------------------------------------------------
    def existe(self, referencia):

        sql = "SELECT 1 FROM cursos WHERE referencia = ?"

        conexion = self.conexion.conectar()
        cursor = conexion.cursor()
        cursor.execute(sql, (referencia,))
        fila = cursor.fetchone()
        cursor.close()

        return fila is not None

    # ---------------------------------------------------------------
    # GUARDAR: inserta un curso nuevo (el id lo asigna SQL Server solo)
    # ---------------------------------------------------------------
    def guardar(self, curso):

        if self.existe(curso.referencia):
            raise CursoError("Ya existe un curso con esa referencia.")

        sql = """
            INSERT INTO cursos
                (referencia, descripcion, fecha_inicio, fecha_final,
                 estado, docente, horas_capacitacion, horas_asesoria, mes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        parametros = (
            curso.referencia, curso.descripcion, curso.fecha_inicio,
            curso.fecha_final, curso.estado, curso.docente,
            curso.horas_capacitacion, curso.horas_asesoria, curso.mes,
        )

        try:
            conexion = self.conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute(sql, parametros)
            conexion.commit()
            cursor.close()
        except Exception as error:
            raise CursoError(f"No se pudo guardar el curso: {error}")

    # ---------------------------------------------------------------
    # ACTUALIZAR: modifica un curso que ya existe (busca por id)
    # ---------------------------------------------------------------
    def actualizar(self, curso):

        sql = """
            UPDATE cursos
            SET referencia = ?, descripcion = ?, fecha_inicio = ?,
                fecha_final = ?, estado = ?, docente = ?,
                horas_capacitacion = ?, horas_asesoria = ?, mes = ?
            WHERE id = ?
        """

        parametros = (
            curso.referencia, curso.descripcion, curso.fecha_inicio,
            curso.fecha_final, curso.estado, curso.docente,
            curso.horas_capacitacion, curso.horas_asesoria, curso.mes,
            curso.id,
        )

        try:
            conexion = self.conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute(sql, parametros)
            conexion.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
        except Exception as error:
            raise CursoError(f"No se pudo actualizar el curso: {error}")

        if filas_afectadas == 0:
            raise CursoError("El curso ya no existe en la base de datos.")

    # ---------------------------------------------------------------
    # ELIMINAR: borra un curso por su id
    # ---------------------------------------------------------------
    def eliminar(self, id_curso):

        sql = "DELETE FROM cursos WHERE id = ?"

        try:
            conexion = self.conexion.conectar()
            cursor = conexion.cursor()
            cursor.execute(sql, (id_curso,))
            conexion.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
        except Exception as error:
            raise CursoError(f"No se pudo eliminar el curso: {error}")

        if filas_afectadas == 0:
            raise CursoError("El curso ya no existe en la base de datos.")

# =========================================================================
# PRUEBA RÁPIDA SIN BASE DE DATOS:  python Cursos.py
# Usa una "conexión falsa" solo para comprobar que el SQL y la lógica
# funcionan, sin necesitar SQL Server instalado.
# =========================================================================
if __name__ == "__main__":

    from datetime import date

    class CursorFalso:
        """Imita a un cursor de pyodbc guardando los datos en memoria."""

        def __init__(self, tabla, contador):
            self.tabla = tabla
            self.contador = contador   # simula el IDENTITY
            self._resultado = []
            self.rowcount = 0

        def execute(self, sql, parametros=()):
            sql = sql.strip()

            if sql.startswith("SELECT 1"):
                referencia = parametros[0]
                existe = any(fila[1] == referencia for fila in self.tabla.values())
                self._resultado = [(1,)] if existe else []

            elif sql.startswith("SELECT"):
                self._resultado = list(self.tabla.values())

            elif sql.startswith("INSERT"):
                self.contador[0] += 1
                nuevo_id = self.contador[0]
                self.tabla[nuevo_id] = (nuevo_id,) + parametros
                self.rowcount = 1

            elif sql.startswith("UPDATE"):
                id_curso = parametros[-1]
                if id_curso not in self.tabla:
                    self.rowcount = 0
                else:
                    self.tabla[id_curso] = (id_curso,) + parametros[:-1]
                    self.rowcount = 1

            elif sql.startswith("DELETE"):
                id_curso = parametros[0]
                self.rowcount = 1 if self.tabla.pop(id_curso, None) is not None else 0

        def fetchall(self):
            return self._resultado

        def fetchone(self):
            return self._resultado[0] if self._resultado else None

        def close(self):
            pass

    class ConexionFalsa:
        """Imita a Conexion_SQL: conectar() devuelve un objeto con cursor()."""

        def __init__(self):
            self.tabla = {}
            self.contador = [0]   # lista de 1 elemento para poder modificarlo

        def conectar(self):
            return self

        def cursor(self):
            return CursorFalso(self.tabla, self.contador)

        def commit(self):
            pass

    repositorio = CursoRepositorio(ConexionFalsa())

    curso = Curso("PROG3-01", "Programación III", date(2026, 9, 1),
                   date(2026, 11, 30), 1, "Audie Ruiz", 120, 10.5, "SETIEMBRE")

    repositorio.guardar(curso)
    cursos = repositorio.listar()
    print("Cursos guardados:", [(c.id, c.referencia) for c in cursos])

    curso_guardado = cursos[0]
    curso_guardado.descripcion = "Programación III (modificado)"
    repositorio.actualizar(curso_guardado)
    print("Descripción actualizada:", repositorio.listar()[0].descripcion)

    try:
        repositorio.guardar(curso)   # debe fallar: referencia repetida
    except CursoError as error:
        print("Error esperado:", error)

    repositorio.eliminar(curso_guardado.id)
    print("Cursos después de eliminar:", repositorio.listar())


