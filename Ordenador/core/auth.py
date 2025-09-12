import re
from PySide6.QtWidgets import QMessageBox

expRegPass = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,16}$'
expRegCorreo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def comprobar_campo(tipo, campo_1, campo_2=None, campo_3=None, campo_4=None):
    if tipo == "login" and (not campo_1 or not campo_2):
        QMessageBox.critical(None, "Error", "Por favor, ingrese usuario y contraseña.")
        return True
    if tipo == "register" and (not campo_1 or not campo_2 or not campo_3 or not campo_4):
        QMessageBox.critical(None, "Error", "Por favor, complete todos los campos.")
        return True
    if tipo == "recover" and (not campo_1):
        QMessageBox.critical(None, "Error", "Por favor, ingrese un correo electrónico.")
        return True
    return False

def login(conexion, funciones_utiles, usuario, clave):
    if comprobar_campo("login", usuario, clave):
        return False
    
    clave_encriptada = funciones_utiles.encriptar_clave(clave)
    
    try:
        mycursor = conexion.cursor()
        sql = "SELECT * FROM acceso WHERE user = %s AND pass = %s"
        val = (usuario, clave_encriptada)
        mycursor.execute(sql, val)
        resultado = mycursor.fetchone()
        
        if resultado:
            QMessageBox.information(None, "Éxito", "Credenciales válidas.")
            return True # Retorna True si es exitoso
        else:
            QMessageBox.critical(None, "Error", "Credenciales inválidas.")
            return False
            
    except Exception as err:
        QMessageBox.critical(None, "Error", f"Error en la operación: {err}")
        return False

def register(conexion, funciones_utiles, correo, usuario, clave, con_clave):
    if comprobar_campo("register", usuario, clave, correo, con_clave):
        return False
    if not re.match(expRegCorreo, correo):
        QMessageBox.critical(None, "Error", "El correo electrónico no es válido.")
        return False
    if not re.match(expRegPass, clave):
        QMessageBox.critical(None, "Error", "La contraseña no es válida.")
        return False
    if con_clave != clave:
        QMessageBox.critical(None, "Error", "Las contraseñas no coinciden.")
        return False

    pass_encriptada = funciones_utiles.encriptar_clave(clave)
    
    try:
        mycursor = conexion.cursor()
        
        sql = "SELECT * FROM usuario WHERE user = %s OR email = %s"
        val = (usuario, correo)
        mycursor.execute(sql, val)
        if mycursor.fetchone():
            QMessageBox.critical(None, "Error", "El usuario o correo ya existen.")
            return False

        sql = "INSERT INTO usuario (email, user, pass) VALUES (%s, %s, %s)"
        val = (correo, usuario, pass_encriptada)
        mycursor.execute(sql, val)
        conexion.commit()

        QMessageBox.information(None, "Éxito", "Usuario registrado correctamente.")
        return True

    except Exception as err:
        QMessageBox.critical(None, "Error", f"Error en la operación: {err}")
        return False

def recover(conexion, funciones_utiles, correo):
    print("Hola ", correo)
    if comprobar_campo("recover", correo):
        return False
    if not re.match(expRegCorreo, correo):
        QMessageBox.critical(None, "Error", "El correo electrónico no es válido.")
        return False

    try:
        mycursor = conexion.cursor()
        
        sql = "SELECT * FROM acceso WHERE email = %s"
        val = (correo,)
        mycursor.execute(sql, val)
        resultado = mycursor.fetchone()
        
        if resultado:
            token = funciones_utiles.generar_token_pass(correo)
            asunto = "Recuperar Contraseña"
            url = f"http://localhost/SGI-app/restablecer.php?user={resultado[0]}&token={token}"
            cuerpo = f"Hola {resultado[0]} <br /><br />Se ha solicitado un reinicio de contraseña <br/><br/>Para restaurar la contraseña visita la siguiente dirección: <a href='{url}'>Recuperar Contraseña</a>"
            funciones_utiles.enviar_correo(correo, resultado[0], asunto, cuerpo)
            QMessageBox.information(None, "Token Enviado", "El token ha sido enviado al correo electrónico.")
            return True
        else:
            QMessageBox.critical(None, "Error", "El correo electrónico no se encuentra registrado.")
            return False

    except Exception as err:
        QMessageBox.critical(None, "Error", f"Error en la operación: {err}")
        return False