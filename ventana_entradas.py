import tkinter as tk
from tkinter import messagebox

#Funsion para guardar y mostrar los datos
def guardar():
    cedula = txt_cedula.get()
    nombre = txt_nombre.get()
    apellido = txt_apellido.get()
    fecha = txt_fecha.get()
     
    datos = f"Cédula: {cedula}\nNombre: {nombre}\nApellido: {apellido}\nFecha: {fecha}"
    
    messagebox.showinfo("Datos Registrados", datos)

#Crear la ventana principal
ventana = tk.Tk()
ventana.title("Registro de Persona")
ventana.geometry("450x300")
ventana.configure(bg="lightblue")

#craer etiquetas
#titulo
lbl_titulo = tk.Label(
ventana,
text="Formulario de Registro",
font=("Arial", 16, "bold"),
bg="lightblue",
fg="navy"
)
lbl_titulo.pack(pady=10)

#Frame para organizar controles 
frame = tk.Frame(ventana, bg="lightblue")
frame.pack(pady=10)

#Craer etiquetas y de las entradas 
#Nombre
tk.Label(frame, text="Nombre:", bg="lightblue", 
             font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
txt_nombre = tk.Entry(frame, width=25)
txt_nombre.grid(row=1, column=1)


#Cedula
tk.Label(frame, text="Cedula:", bg="lightblue", 
             font=("Arial", 11)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
txt_cedula = tk.Entry(frame, width=25)
txt_cedula.grid(row=2, column=1)

#Apellido
tk.Label(frame, text="Apellido:", bg="lightblue", 
             font=("Arial", 11)).grid(row=3, column=0, padx=5, pady=5, sticky="e")
txt_apellido = tk.Entry(frame, width=25)
txt_apellido.grid(row=3, column=1)

#Fecha
tk.Label(frame, text="Fecha:", bg="lightblue", 
             font=("Arial", 11)).grid(row=4, column=0, padx=5, pady=5, sticky="e")
txt_fecha = tk.Entry(frame, width=25)
txt_fecha.grid(row=4, column=1)
txt_fecha.insert(0, "dd/mm/aaaa")

#Boton para guardar los datos
btn_guardar = tk.Button(ventana, 
text="Guardar", 
font=("Arial", 12, "bold"), 
bg="green", 
fg="white", 
command=guardar)
btn_guardar.pack(pady=15)

#btn salir
btn_salir = tk.Button(ventana,
text="Salir",
font=("Arial", 12, "bold"),
bg="red",
fg="white",
command=ventana.destroy)



#ejecutar ventana 
ventana.mainloop()