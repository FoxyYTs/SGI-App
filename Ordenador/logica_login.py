def recover(self):
    correo = self.ui.line_recupero_correo.text()

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
            ejecutar = Menu(usuario)
        else:
            messagebox.showerror("Error", "Credenciales inválidas.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de conexión: {err}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
