import tkinter as tk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi Aplicación")

# Crear el frame del encabezado
encabezado = tk.Frame(ventana, bg="lightblue")
encabezado.pack(fill="x")

# Agregar el título
titulo = tk.Label(encabezado, text="LAB MANAGER", font=("Arial", 16), fg="white")
titulo.pack(side="left", padx=10)

# Agregar los botones
boton_buscar = tk.Button(encabezado, text="BUSCAR PRODUCTOS")
boton_agregar = tk.Button(encabezado, text="AGREGAR PRODUCTOS")
boton_generar = tk.Button(encabezado, text="GENERAR INFORME")
# ... Agregar más botones ...

boton_buscar.pack(side="left", padx=10)
boton_agregar.pack(side="left", padx=10)
boton_generar.pack(side="left", padx=10)

# Agregar el menú desplegable (simplificado)
menu_var = tk.StringVar(ventana)
menu_var.set("INICIAR SESIÓN")
menu = tk.OptionMenu(encabezado, menu_var, "INICIAR SESIÓN", "CERRAR SESIÓN")
menu.pack(side="right", padx=10)

# Agregar el campo de búsqueda (simplificado)
campo_busqueda = tk.Entry(encabezado)
campo_busqueda.pack(side="right", padx=10)

ventana.mainloop()