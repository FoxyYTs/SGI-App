import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_generated.login_ui import Ui_SGI_Login   # este es el archivo que mostraste

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SGI_Login()     # instanciamos la UI
        self.ui.setupUi(self)        # "pegamos" la UI a la ventana

        # 🔹 Conectar botones a métodos
        self.ui.btn_inicio_iniciar.clicked.connect(self.login)
        self.ui.btn_inicio_registrar.clicked.connect(self.show_register)
        self.ui.btn_inicio_recuperar.clicked.connect(self.show_recover)

        self.ui.btn_registro_registrar.clicked.connect(self.register)
        self.ui.btn_registro_iniciar.clicked.connect(self.show_login)

        self.ui.btn_recupero_recuperar.clicked.connect(self.recover)
        self.ui.btn_recupero_iniciar.clicked.connect(self.show_login)

    # ========== Métodos de lógica ==========
    def login(self):
        usuario = self.ui.line_inicio_usuario.text()
        clave = self.ui.line_inicio_clave.text()
        print(f"Intentando login: {usuario} / {clave}")

    def register(self):
        usuario = self.ui.line_registro_usuario.text()
        correo = self.ui.line_registro_correo.text()
        clave = self.ui.line_registro_clave.text()
        reclave = self.ui.line_registro_reclave.text()
        if clave != reclave:
            print("❌ Las contraseñas no coinciden")
        else:
            print(f"✅ Usuario {usuario} registrado con {correo}")

    def recover(self):
        correo = self.ui.line_recupero_correo.text()
        print(f"📩 Enviar correo de recuperación a: {correo}")

    # ========== Navegación ==========
    def show_login(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.inicio)

    def show_register(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.registro)

    def show_recover(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.recupero)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
