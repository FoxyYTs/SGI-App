import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_generated.login_ui import Ui_SGI_Login
from core.auth import login as auth_login, register as auth_register, recover as auth_recover
from core.conexion import conectar
from core.funciones import Funciones # Asumiendo que ahora es una clase o un módulo

class MainWindow(QMainWindow):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion
        self.ui = Ui_SGI_Login()
        self.ui.setupUi(self)
        self.f = Funciones() # Instancia de la clase Funciones

        # 🔹 Conectar botones a métodos
        self.ui.btn_inicio_iniciar.clicked.connect(self.login)
        self.ui.btn_inicio_registrar.clicked.connect(self.show_register)
        self.ui.btn_inicio_recuperar.clicked.connect(self.show_recover)

        self.ui.btn_registro_registrar.clicked.connect(self.register)
        self.ui.btn_registro_iniciar.clicked.connect(self.show_login)

        self.ui.btn_recupero_recuperar.clicked.connect(self.recover)
        self.ui.btn_recupero_iniciar.clicked.connect(self.show_login)

    # ========== Métodos de manejo de eventos ==========
    def login(self):
        usuario = self.ui.line_inicio_usuario.text()
        clave = self.ui.line_inicio_clave.text()
        
        # Llama a la función del módulo auth, pasándole la conexión y los datos
        auth_login(self.conexion, self.f, usuario, clave)

    def register(self):
        correo = self.ui.line_registro_correo.text()
        usuario = self.ui.line_registro_usuario.text()
        clave = self.ui.line_registro_clave.text()
        con_clave = self.ui.line_registro_con_clave.text()
        
        auth_register(self.conexion, self.f, correo, usuario, clave, con_clave)

    def recover(self):
        correo = self.ui.line_recupero_correo.text()
        print(correo)
        auth_recover(self.conexion, self.f, correo)

    # ========== Navegación ==========
    def show_login(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.inicio)

    def show_register(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.registro)

    def show_recover(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.recupero)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 🚨 Se establece la conexión aquí y se pasa a la ventana
    conexion = conectar()
    if conexion:
        window = MainWindow(conexion)
        window.show()
        sys.exit(app.exec())
    else:
        QMessageBox.critical(None, "Error de Conexión", "No se pudo conectar a la base de datos.")