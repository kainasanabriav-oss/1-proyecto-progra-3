#Conexion SQL
#Conexion SQL

# Librería:
# pip install pyodbc

import pyodbc


class Conexion:

    def __init__(self, servidor, base_datos, tipo_conexion="Windows",
                 usuario=None, contrasena=None):

        self.servidor = servidor
        self.base_datos = base_datos
        self.tipo_conexion = tipo_conexion   # "Windows" o "SQL"
        self.usuario = usuario               # solo se usa si tipo_conexion = "SQL"
        self.contrasena = contrasena         # solo se usa si tipo_conexion = "SQL"

        self.conexion = None

    # -----------------------------------------------------------------
    # ABRIR LA CONEXIÓN
    # -----------------------------------------------------------------
    def conectar(self):

        if self.tipo_conexion == "Windows":
            cadena = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                f"SERVER={self.servidor};"
                f"DATABASE={self.base_datos};"
                "Trusted_Connection=yes;"
            )
        else:  # tipo_conexion = "SQL" (usuario y contraseña)
            cadena = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                f"SERVER={self.servidor};"
                f"DATABASE={self.base_datos};"
                f"UID={self.usuario};"
                f"PWD={self.contrasena};"
            )

        self.conexion = pyodbc.connect(cadena)

        return self.conexion

    # -----------------------------------------------------------------
    # CERRAR LA CONEXIÓN
    # -----------------------------------------------------------------
    def cerrar(self):

        if self.conexion is not None:
            self.conexion.close()
            self.conexion = None


# ---------------------------------------------------------------------
# PRUEBA RÁPIDA:  python Conexion_SQL.py
# Cambia estos datos por los tuyos antes de probar.
# ---------------------------------------------------------------------
if __name__ == "__main__":

    conexion = Conexion(
        servidor="CHRISIAN\\SERVIDOR",   # la diagonal se escribe doble en Python
        base_datos="ControlAcademico",
        tipo_conexion="SQL",             # porque entraste como "sa", no con Windows
        usuario="sa",
        contrasena="1234567890", 
    )

    try:
        conexion.conectar()
        print("Conexión exitosa.")
    except Exception as error:
        print("No se pudo conectar:", error)
    finally:
        conexion.cerrar()