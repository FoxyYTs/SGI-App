import tkinter as tk
from tkinter import messagebox

import mysql.connector

import conexion

class menu:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("SGI LAB MANAGER")
        self.ventana.geometry("1280x720")
        
        self.encabezado = tk.Frame(self.ventana, bg="white")
        self.encabezado.pack(fill="x")

        self.etiqueta = tk.Label(self.encabezado, text="LAB MANAGER", font=("Arial", 16, "bold"), fg="blue", bg="white")
        self.etiqueta.pack(side="left", padx=30)

        self.pestanas("JoseDaza")

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

    def pestanas(self, user):
        
        try:
            mydb = conexion.conectar()

            mycursor = mydb.cursor()
            sql = "SELECT a.user AS nombre_usuario, r.nombre_rol, p.nombre_permiso, p.archivo FROM acceso AS a JOIN roles AS r ON a.roles_fk = r.id_rol JOIN permiso_rol AS pr ON r.id_rol = pr.rol_fk JOIN permisos AS p ON p.id_permisos = pr.permiso_fk WHERE a.user = %s AND p.nombre_permiso NOT LIKE 'GESTION%'"
            val = (user, )
            mycursor.execute(sql, val)
            resultado = mycursor.fetchone()

            if resultado:
                messagebox.showinfo("Éxito", "Credenciales válidas.")
            else:
                messagebox.showerror("Error", "Credenciales inválidas.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error de conexión: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()
        
    def inicio(self):
        print("Inicio")
    
    def buscar_implemento(self):
        print("Buscar Implemento")
menu()