#Estudiantes 
# Una clas como  "molde" para crear estudiantes
# Cada vez que creamos un estudiante nuevo usamos este molde.

class Estudiante:

    # Aqui esta el constructor se ejecuta cuando creamos un nuevo estudiante

    def __init__(self, id, cedula, nombre, apellidos, nacimiento, correo,
                 celular, encargado, celular_encargado):

        # Esto es para guardar cada dato que nos llega del estudiante
     
        self.id = id
        self.cedula = cedula
        self.nombre = nombre
        self.apellidos = apellidos
        self.nacimiento = nacimiento
        self.correo = correo
        self.celular = celular
        self.encargado = encargado
        self.celular_encargado = celular_encargado

    # Este metodo simplemente muestra en pantalla los datos del estudiante
    def mostrar_datos(self):
        print("ID:", self.id)
        print("Cedula:", self.cedula)
        print("Nombre:", self.nombre)
        print("Apellidos:", self.apellidos)
        print("Fecha de nacimiento:", self.nacimiento)
        print("Correo:", self.correo)
        print("Celular del estudiante:", self.celular)
        print("Nombre del encargado:", self.encargado)
        print("Celular del encargado:", self.celular_encargado)

if __name__ == "__main__":

    # Creamos un estudiante de prueba pasandole los datos en orden
    estudiante1 = Estudiante(
        1,
        "120160779",
        "Ashley Tatiana",
        "Cascante Ruiz",
        "2026-09-07",
        "tatiana@gmail.com",
        "70101564",
        "Luis Cascante",
        "70151500"
    )

    # Mostramos sus datos en la consola
    estudiante1.mostrar_datos()