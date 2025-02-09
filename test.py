import tkinter as tk

root = tk.Tk()

# Crear un marco para agrupar las etiquetas
frame = tk.Frame(root)
frame.pack()

# Crear las etiquetas con el texto alineado a la izquierda
label_id = tk.Label(frame, text="ID Implemento: 13", font=("Arial", 12), anchor="w")
label_nombre = tk.Label(frame, text="Nombre Implemento: Balón de fondo plano de 100 ml", font=("Arial", 12), anchor="w")

# Empaquetar las etiquetas en el marco
label_id.pack()
label_nombre.pack()

root.mainloop()