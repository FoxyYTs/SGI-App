import tkinter as tk
from tkinter import messagebox

import mysql.connector

import conexion

class menu:
    def __init__(self, user):
        self.ventana = tk.Tk()
        self.ventana.title("SGI LAB MANAGER")
        self.ventana.geometry("1280x720")
        
        self.encabezado = tk.Frame(self.ventana, bg="white", )
        self.encabezado.pack(fill="x")
        
        self.etiqueta = tk.Label(self.encabezado, text="LAB MANAGER", font=("Arial", 16, "bold"), fg="blue", bg="white")
        self.etiqueta.pack(side="left", padx=10)

        self.contenedor = tk.Frame(self.ventana, bg="gray")
        self.contenedor.pack(fill="both", expand=True)

        self.pestanas(user)

        self.inicio()

        self.center_window()
        self.ventana.mainloop()

    def center_window(self):
        """
        Centra la ventana en la pantalla.

        Esta función actualiza las tareas inactivas de la ventana, calcula las coordenadas x e y para centrar la ventana y
        establece la geometría de la ventana en consecuencia.

        Parámetros:
            self (objeto): La instancia de la clase.

        Retorna:
            Ninguno
        """
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - (self.ventana.winfo_width() // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (self.ventana.winfo_height() // 2)
        self.ventana.geometry(f'{self.ventana.winfo_width()}x{self.ventana.winfo_height()}+{x}+{y}')

    def click_handler(self, data):
        print("asd")
        self.frame.pack_forget()
        if data == "INICIO":
            self.inicio()
        elif data == "BUSCAR IMPLEMENTOS":
            self.buscar_implemento()
        elif data == "AGREGAR IMPLEMENTOS":
            self.agregar_implemento()
        elif data == "GENERAR INFORME":
            self.generar_informe()
        elif data == "GESTIONAR ROLES":
            self.gestionar_roles()
        elif data == "GESTIONAR IMPLEMENTOS":
            self.gestionar_implementos()
        elif data == "GESTIONAR MOVIMIENTOS":
            self.gestionar_movimientos()
        elif data == "GESTIONAR TABLAS MAESTRAS":
            self.gestionar_tablas_maestras()
        elif data == "GESTIONAR PERMISOS":
            self.gestionar_permisos()
        elif data == "GESTIONAR MOVIMIENTOS ADMINISTRADOR":
            self.gestionar_movimientos_administrador()
    def pestanas(self, user):
        
            
        try:
            mydb = conexion.conectar()
            mycursor = mydb.cursor()

            sql = "SELECT a.user AS nombre_usuario, r.nombre_rol, p.nombre_permiso, p.archivo FROM acceso AS a JOIN roles AS r ON a.roles_fk = r.id_rol JOIN permiso_rol AS pr ON r.id_rol = pr.rol_fk JOIN permisos AS p ON p.id_permisos = pr.permiso_fk WHERE a.user = %s AND p.nombre_permiso NOT LIKE 'GESTION%'"
            val = (user,)
            mycursor.execute(sql, val)
            resultado = mycursor.fetchall()

            if resultado:
                for i in resultado:
                    label = tk.Label(self.encabezado, text=i[2], font=("Arial", 12), cursor="hand2", bg="white")
                    label.bind("<Button-1>", lambda event, data=i[2]: self.click_handler(data))
                    
                    label.pack(side="left", padx=10)
            else:
                messagebox.showerror("Error", "Credenciales inválidas.")

            sql = sql = "SELECT a.user AS nombre_usuario, r.nombre_rol, p.nombre_permiso, p.archivo FROM acceso AS a JOIN roles AS r ON a.roles_fk = r.id_rol JOIN permiso_rol AS pr ON r.id_rol = pr.rol_fk JOIN permisos AS p ON p.id_permisos = pr.permiso_fk WHERE a.user = %s AND p.nombre_permiso LIKE 'GESTION%'"
            mycursor.execute(sql, val)
            resultado = mycursor.fetchall()

            if resultado:
                opciones = []
                for i in resultado:
                    opciones.append(i[2])
                variables = tk.StringVar(self.encabezado)
                variables.set("GESTIONAR")

                dropdown = tk.OptionMenu(self.encabezado, variables, *opciones)
                dropdown.pack(side="left", padx=10)


            variables.trace("w", lambda *args: self.click_handler(variables.get()))

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error de conexión: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def inicio(self):
        self.frame = tk.Frame(self.contenedor, bg="gray")
        self.frame.pack(fill="both", expand=True)

        label = tk.Label(self.frame, bg="gray")
        label.place(relx=0.5, rely=0.5, anchor="center")

        etiqueta = tk.Label(label, text="Bienvenido al SIG LAB MANAGER", font=("Arial", 16, "bold"), fg="blue", bg="gray")
        etiqueta.grid(row=0, column=0, padx=10, pady=10)

        etiqueta = tk.Label(label, text="WORK IN PROGRESS", font=("Arial", 16, "bold"), fg="blue", bg="gray")
        etiqueta.grid(row=1, column=0, padx=10, pady=10)

        etiqueta = tk.Label(label, text="¡Explora y disfruta de las funcionalidades del sistema!", font=("Arial", 16, "bold"), fg="blue", bg="gray")
        etiqueta.grid(row=2, column=0, padx=10, pady=10)

        print("asdasda")
    
    def buscar_implemento(self):
        print("Buscar Implemento")
    
    def agregar_implemento(self):
        print("Registrar Implemento")

    def generar_informe(self):
        print("Generar Informe")

    def gestionar_roles(self):
        print("Gestionar Roles")

    def gestionar_implementos(self):
        print("Gestionar Implementos")

    def gestionar_movimientos(self):
        print("Gestionar Movimientos")

    def gestionar_tablas_maestras(self):
        print("Gestionar Tablas Maestras")

    def gestionar_permisos(self):
        print("Gestionar Permisos")

    def gestionar_movimientos_administrador(self):
        print("Gestionar Movimientos Administrador")

menu("JoseDaza")