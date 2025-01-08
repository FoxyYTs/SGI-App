import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re

import conexion
import funciones as f

expRegPass = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,16}$'
expRegCorreo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

ventana = tk.Tk()

def comprobar_campo(tipo, campo_1, campo_2 = None, campo_3 = None, campo_4 = None):
    if tipo == "login" and (not campo_1 or not campo_2):
        messagebox.showerror("Error", "Por favor, ingrese usuario y contraseña.")
        return True
    if tipo == "register" and (not campo_1 or not campo_2 or not campo_3 or not campo_4):
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return True
    if tipo == "recover" and (not campo_1):
        messagebox.showerror("Error", "Por favor, ingrese un correo electrónico.")
        return True

def recover(entry_correo):
    correo = entry_correo.get()

    if comprobar_campo("recover", correo):
        return
    if not re.match(expRegCorreo, correo):
        messagebox.showerror("Error", "El correo electrónica no es válido.")
        return

    try:
        mydb = conexion.conectar()
        mycursor = mydb.cursor()

        sql = "SELECT * FROM acceso WHERE email = %s"
        val = (correo,)
        mycursor.execute(sql, val)
        resultado = mycursor.fetchone()
        print(resultado)

        if resultado:
            token = f.generar_token_pass(correo)
            asunto = "Recuperar Contraseña"
            url = "http://localhost/SGI-app/restablecer.php?user=" + resultado[0] + "&token=" + token
            cuerpo = f"Hola {resultado[0]} <br /><br />Se ha solicitado un reinicio de contraseña <br/><br/>Para restaurar la contraseña visita la siguiente direccion: <a href='{url}'>Recuperar Contraseña</a>"
            f.enviar_correo(correo, resultado[0], asunto, cuerpo)
            messagebox.showinfo("Token Enviado", "El token ha sido enviado al correo electrónica.")
        else:
            messagebox.showerror("Error", "El correo electrónica no se encuentra registrado.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de conexión: {err}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            
def register(entry_correo, entry_usuario, entry_clave, entry_con_clave):
    correo = entry_correo.get()
    usuario = entry_usuario.get()
    clave = entry_clave.get()
    con_clave = entry_con_clave.get()

    if comprobar_campo("register",usuario, clave, correo, con_clave):
        return
    if not re.match(expRegCorreo, correo):
        messagebox.showerror("Error", "El correo electrónica no es válido.")
        return
    if not re.match(expRegPass, clave):
        messagebox.showerror("Error", "La contraseña no es válida.")
        return
    if con_clave != clave:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
        return

    pass_encriptada = f.encriptar_clave(clave)

    try:
        mydb = conexion.conectar()
        mycursor = mydb.cursor()

        sql = "SELECT * FROM acceso WHERE user = %s OR email = %s"
        val = (usuario, correo)
        mycursor.execute(sql, val)
        resultado = mycursor.fetchone()

        if resultado:
            messagebox.showerror("Error", "El usuario o correo electrónica ya existen.")
            return

        sql = "INSERT INTO acceso (email, user, pass) VALUES (%s, %s, %s)"
        val = (correo, usuario, pass_encriptada)
        mycursor.execute(sql, val)
        mydb.commit()

        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        registro = True

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de conexión: {err}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            return registro

def login(entry_usuario, entry_clave):
    usuario = entry_usuario.get()
    clave = entry_clave.get()

    if comprobar_campo("login",usuario, clave):
        return
    
    clave = f.encriptar_clave(clave)

    try:
        mydb = conexion.conectar()

        mycursor = mydb.cursor()
        sql = "SELECT * FROM acceso WHERE user = %s AND pass = %s"
        val = (usuario, clave)
        mycursor.execute(sql, val)
        resultado = mycursor.fetchone()

        if resultado:
            messagebox.showinfo("Éxito", "Credenciales válidas.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "Credenciales inválidas.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de conexión: {err}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

def interfaz_recuperar():
    def inicio():
        frame_recuperar.pack_forget()
        interfaz_inicio()

    def registro():
        frame_recuperar.pack_forget()
        interfaz_registro()

    def recuperar():
        recover(entry_correo)
        frame_recuperar.pack_forget()
        interfaz_recuperar()

    frame_recuperar = tk.Frame(ventana)
    frame_recuperar.pack()

    ventana.title("Recuperar Contraseña")
    # Etiquetas y campos de entrada

    label_correo = tk.Label(frame_recuperar, text="Correo:")
    label_correo.grid(row=0, column=0, padx=5, pady=5)
    entry_correo = tk.Entry(frame_recuperar)
    entry_correo.grid(row=0, column=1, padx=5, pady=5)

    # Botón de inicio de sesión
    boton_login = tk.Button(frame_recuperar, text="Iniciar Sesión", command=inicio)
    boton_login.grid(row=3, column=1, padx=5, pady=5)

    boton_regis = tk.Button(frame_recuperar, text="Registrar Usuario", command=registro)
    boton_regis.grid(row=3, column=0, padx=5, pady=5)

    boton_forget = tk.Button(frame_recuperar, text="Recuperar Contraseña", command=recuperar)
    boton_forget.grid(row=2, column=0, columnspan=2, pady=5)

def interfaz_registro():

    def inicio():
        frame_registro.pack_forget()
        interfaz_inicio()

    def registro():
        if register(entry_correo, entry_usuario, entry_clave, entry_con_clave):
            frame_registro.pack_forget()
            interfaz_inicio()
        else:
            frame_registro.pack_forget()
            interfaz_registro()

    def recuperar():
        frame_registro.pack_forget()
        interfaz_recuperar()

    frame_registro = tk.Frame(ventana)
    frame_registro.pack()

    ventana.title("Registro de Usuario")
    # Etiquetas y campos de entrada
    label_correo = tk.Label(frame_registro, text="Correo:")
    label_correo.grid(row=0, column=0, padx=5, pady=5)
    entry_correo = tk.Entry(frame_registro)
    entry_correo.grid(row=0, column=1, padx=5, pady=5)

    label_usuario = tk.Label(frame_registro, text="Usuario:")
    label_usuario.grid(row=1, column=0, padx=5, pady=5)
    entry_usuario = tk.Entry(frame_registro)
    entry_usuario.grid(row=1, column=1, padx=5, pady=5)

    label_clave = tk.Label(frame_registro, text="Contraseña:")
    label_clave.grid(row=2, column=0, padx=5, pady=5)
    entry_clave = tk.Entry(frame_registro, show="*") # Oculta la contraseña
    entry_clave.grid(row=2, column=1, padx=5, pady=5)

    label_con_clave = tk.Label(frame_registro, text="Confirmar Contraseña:")
    label_con_clave.grid(row=3, column=0, padx=5, pady=5)
    entry_con_clave = tk.Entry(frame_registro, show="*") # Oculta la contraseña
    entry_con_clave.grid(row=3, column=1, padx=5, pady=5)

    # Botón de inicio de sesión
    boton_regis = tk.Button(frame_registro, text="Registrar Usuario", command=registro)
    boton_regis.grid(row=4, column=0, columnspan=2, pady=5)

    boton_login = tk.Button(frame_registro, text="Iniciar Sesión", command=inicio)
    boton_login.grid(row=5, column=0, padx=5, pady=5)

    boton_forget = tk.Button(frame_registro, text="Olvide mi contraseña", command=recuperar)
    boton_forget.grid(row=5, column=1, padx=5, pady=5)

def interfaz_inicio():

    def inicio():
        login(entry_usuario, entry_clave)
        frame_inicio.pack_forget()
        interfaz_inicio()

    def registro():
        frame_inicio.pack_forget()
        interfaz_registro()
    
    def recuperar():
        frame_inicio.pack_forget()
        interfaz_recuperar()

    frame_inicio = tk.Frame(ventana)
    frame_inicio.pack()

    ventana.title("Inicio de Sesión")
    # Etiquetas y campos de entrada
    label_usuario = tk.Label(frame_inicio, text="Usuario:")
    label_usuario.grid(row=0, column=0, padx=5, pady=5)
    entry_usuario = tk.Entry(frame_inicio)
    entry_usuario.grid(row=0, column=1, padx=5, pady=5)

    label_clave = tk.Label(frame_inicio, text="Contraseña:")
    label_clave.grid(row=1, column=0, padx=5, pady=5)
    entry_clave = tk.Entry(frame_inicio, show="*") # Oculta la contraseña
    entry_clave.grid(row=1, column=1, padx=5, pady=5)

    # Botón de inicio de sesión
    boton_login = tk.Button(frame_inicio, text="Iniciar Sesión", command=inicio)
    boton_login.grid(row=2, column=0, columnspan=2, pady=5)

    boton_regis = tk.Button(frame_inicio, text="Registrar Usuario", command=registro)
    boton_regis.grid(row=3, column=0, padx=5, pady=5)

    boton_forget = tk.Button(frame_inicio, text="Olvide mi contraseña", command=recuperar)
    boton_forget.grid(row=3, column=1, padx=5, pady=5)

interfaz_inicio()
ventana.mainloop()