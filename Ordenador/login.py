from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
import mysql.connector
import re
from menu import Menu
import conexion
import funciones as f

expRegPass = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,16}$'
expRegCorreo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.interfaz_inicio()

    def comprobar_campo(self, tipo, campo_1, campo_2=None, campo_3=None, campo_4=None):
        if tipo == "login" and (not campo_1 or not campo_2):
            QMessageBox.critical(self, "Error", "Por favor, ingrese usuario y contraseña.")
            return True
        if tipo == "register" and (not campo_1 or not campo_2 or not campo_3 or not campo_4):
            QMessageBox.critical(self, "Error", "Por favor, complete todos los campos.")
            return True
        if tipo == "recover" and (not campo_1):
            QMessageBox.critical(self, "Error", "Por favor, ingrese un correo electrónico.")
            return True

    def recover(self, entry_correo):
        correo = entry_correo.text()

        if self.comprobar_campo("recover", correo):
            return
        if not re.match(expRegCorreo, correo):
            QMessageBox.critical(self, "Error", "El correo electrónico no es válido.")
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
                asunto = "Recuperar Contraseña"
                url = "http://localhost/SGI-app/restablecer.php?user=" + resultado[0] + "&token=" + token
                cuerpo = f"Hola {resultado[0]} <br /><br />Se ha solicitado un reinicio de contraseña <br/><br/>Para restaurar la contraseña visita la siguiente dirección: <a href='{url}'>Recuperar Contraseña</a>"
                f.enviar_correo(correo, resultado[0], asunto, cuerpo)
                QMessageBox.information(self, "Token Enviado", "El token ha sido enviado al correo electrónico.")
            else:
                QMessageBox.critical(self, "Error", "El correo electrónico no se encuentra registrado.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error de conexión: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def register(self, entry_correo, entry_usuario, entry_clave, entry_con_clave):
        correo = entry_correo.text()
        usuario = entry_usuario.text()
        clave = entry_clave.text()
        con_clave = entry_con_clave.text()

        if self.comprobar_campo("register", usuario, clave, correo, con_clave):
            return
        if not re.match(expRegCorreo, correo):
            QMessageBox.critical(self, "Error", "El correo electrónico no es válido.")
            return
        if not re.match(expRegPass, clave):
            QMessageBox.critical(self, "Error", "La contraseña no es válida.")
            return
        if con_clave != clave:
            QMessageBox.critical(self, "Error", "Las contraseñas no coinciden.")
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
                QMessageBox.critical(self, "Error", "El usuario o correo electrónico ya existen.")
                return

            sql = "INSERT INTO acceso (email, user, pass) VALUES (%s, %s, %s)"
            val = (correo, usuario, pass_encriptada)
            mycursor.execute(sql, val)
            mydb.commit()

            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")
            self.interfaz_inicio()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error de conexión: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def login(self, entry_usuario, entry_clave):
        usuario = entry_usuario.text()
        clave = entry_clave.text()

        if self.comprobar_campo("login", usuario, clave):
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
                QMessageBox.information(self, "Éxito", "Credenciales válidas.")
                self.close()
                ejecutar = Menu(usuario)
            else:
                QMessageBox.critical(self, "Error", "Credenciales inválidas.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error de conexión: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def interfaz_recuperar(self):
        self.clear_layout()

        layout = QVBoxLayout()

        label_correo = QLabel("Correo:")
        self.entry_correo = QLineEdit()
        layout.addWidget(label_correo)
        layout.addWidget(self.entry_correo)

        boton_login = QPushButton("Iniciar Sesión")
        boton_login.clicked.connect(self.interfaz_inicio)
        layout.addWidget(boton_login)

        boton_regis = QPushButton("Registrar Usuario")
        boton_regis.clicked.connect(self.interfaz_registro)
        layout.addWidget(boton_regis)

        boton_forget = QPushButton("Recuperar Contraseña")
        boton_forget.clicked.connect(lambda: self.recover(self.entry_correo))
        layout.addWidget(boton_forget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def interfaz_registro(self):
        self.clear_layout()

        layout = QVBoxLayout()

        label_correo = QLabel("Correo:")
        self.entry_correo = QLineEdit()
        layout.addWidget(label_correo)
        layout.addWidget(self.entry_correo)

        label_usuario = QLabel("Usuario:")
        self.entry_usuario = QLineEdit()
        layout.addWidget(label_usuario)
        layout.addWidget(self.entry_usuario)

        label_clave = QLabel("Contraseña:")
        self.entry_clave = QLineEdit()
        self.entry_clave.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_clave)
        layout.addWidget(self.entry_clave)

        label_con_clave = QLabel("Confirmar Contraseña:")
        self.entry_con_clave = QLineEdit()
        self.entry_con_clave.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_con_clave)
        layout.addWidget(self.entry_con_clave)

        boton_regis = QPushButton("Registrar Usuario")
        boton_regis.clicked.connect(lambda: self.register(self.entry_correo, self.entry_usuario, self.entry_clave, self.entry_con_clave))
        layout.addWidget(boton_regis)

        boton_login = QPushButton("Iniciar Sesión")
        boton_login.clicked.connect(self.interfaz_inicio)
        layout.addWidget(boton_login)

        boton_forget = QPushButton("Olvide mi contraseña")
        boton_forget.clicked.connect(self.interfaz_recuperar)
        layout.addWidget(boton_forget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def interfaz_inicio(self):
        self.clear_layout()

        layout = QVBoxLayout()

        label_usuario = QLabel("Usuario:")
        self.entry_usuario = QLineEdit()
        layout.addWidget(label_usuario)
        layout.addWidget(self.entry_usuario)

        label_clave = QLabel("Contraseña:")
        self.entry_clave = QLineEdit()
        self.entry_clave.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_clave)
        layout.addWidget(self.entry_clave)

        boton_login = QPushButton("Iniciar Sesión")
        boton_login.clicked.connect(lambda: self.login(self.entry_usuario, self.entry_clave))
        layout.addWidget(boton_login)

        boton_regis = QPushButton("Registrar Usuario")
        boton_regis.clicked.connect(self.interfaz_registro)
        layout.addWidget(boton_regis)

        boton_forget = QPushButton("Olvide mi contraseña")
        boton_forget.clicked.connect(self.interfaz_recuperar)
        layout.addWidget(boton_forget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def clear_layout(self):
        if self.centralWidget():
            self.centralWidget().deleteLater()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()