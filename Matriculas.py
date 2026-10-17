#Matriculas

class Matricula:

    # El Constructor se ejecuta cada vez que creamos una matricula nueva
    
    def __init__(self, id, cedula, nombre, apellidos, referencia,
                 descripcion, fecha, estado):

        # Guardamos cada dato que nos llegaa en una variable de la matricula
        self.id = id
        self.cedula = cedula
        self.nombre = nombre
        self.apellidos = apellidos
        self.referencia = referencia
        self.descripcion = descripcion
        self.fecha = fecha
        self.estado = estado

    # Muestra en pantalla los datos de la matricula
    def mostrar_datos(self):
        print("ID:", self.id)
        print("Cedula:", self.cedula)
        print("Nombre:", self.nombre)
        print("Apellidos:", self.apellidos)
        print("Curso (referencia):", self.referencia)
        print("Descripcion del curso:", self.descripcion)
        print("Fecha de matricula:", self.fecha)
        print("Estado:", self.estado)


