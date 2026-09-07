import tkinter as tk
from tkinter import messagebox

# Función que se ejecuta al hacer clic en el botón
def mostrar_nombre():
    nombre_completo = entrada_nombre.get()
    # Verifica si el campo no está vacío
    if nombre_completo:
        messagebox.showinfo("Información", f"¡Hola, {nombre_completo}! Tu nombre ha sido registrado.")
    else:
        messagebox.showwarning("Atención", "Por favor, ingresa tu nombre completo.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Introducción a Python y Tkinter") # Título de la ventana
ventana.geometry("400x250") # Tamaño de la ventana (ancho x alto)

# Etiqueta de instrucciones
etiqueta_instruccion = tk.Label(ventana, text="Ingresa tu nombre completo:")
etiqueta_instruccion.pack(pady=20) # Espaciado vertical

# Campo de entrada de texto
entrada_nombre = tk.Entry(ventana, width=40)
entrada_nombre.pack(pady=10)

# Botón para confirmar
boton_confirmar = tk.Button(ventana, text="Confirmar", command=mostrar_nombre)
boton_confirmar.pack(pady=20)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
