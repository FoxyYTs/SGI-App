import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QComboBox
from PySide6.QtCore import Qt
import mysql.connector
import conexion
from buscar_implementos import BuscarImplementos
from agregar_implemento import AgregarImplemento

class Menu(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.verificar_user(user)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SGI LAB MANAGER")
        self.setGeometry(0, 0, 1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.encabezado = QFrame()
        self.encabezado.setStyleSheet("background-color: white;")
        self.layout.addWidget(self.encabezado)

        self.encabezado_layout = QHBoxLayout(self.encabezado)

        self.etiqueta = QLabel("LAB MANAGER", self.encabezado)
        self.etiqueta.setStyleSheet("font: bold 16px Arial; color: blue;")
        self.encabezado_layout.addWidget(self.etiqueta)

        self.contenedor = QFrame()
        self.contenedor.setStyleSheet("background-color: gray;")
        self.layout.addWidget(self.contenedor)

        self.pestanas(self.user)
        self.inicio = Inicio(self.contenedor)

        self.center_window()
        self.show()

    def verificar_user(self, user):
        if not user:
            QMessageBox.critical(self, "Error", "Error con el usuario.")
            sys.exit()

        try:
            mydb = conexion.conectar()
            mycursor = mydb.cursor()

            sql = "SELECT * FROM acceso WHERE user = %s"
            val = (user,)
            mycursor.execute(sql, val)
            resultado = mycursor.fetchone()

            if not resultado:
                QMessageBox.critical(self, "Error", "Hubo un error con el usuario.")
                sys.exit()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error de conexión: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def cambio(self):
        for i in reversed(range(self.contenedor.layout().count())):
            self.contenedor.layout().itemAt(i).widget().setParent(None)

    def center_window(self):
        frame_geometry = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def click_handler(self, data):
        self.cambio()
        if data == "INICIO":
            self.inicio = Inicio(self.contenedor)
        elif data == "BUSCAR IMPLEMENTOS":
            self.buscar_implementos = BuscarImplementos(self.contenedor)
        elif data == "AGREGAR IMPLEMENTOS":
            self.agregar_implemento = AgregarImplemento(self.contenedor)
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
                    label = QLabel(i[2], self.encabezado)
                    label.setStyleSheet("font: 12px Arial; color: black; cursor: pointer;")
                    label.mousePressEvent = lambda event, data=i[2]: self.click_handler(data)
                    self.encabezado_layout.addWidget(label)
            else:
                QMessageBox.critical(self, "Error", "Credenciales inválidas.")

            sql = "SELECT a.user AS nombre_usuario, r.nombre_rol, p.nombre_permiso, p.archivo FROM acceso AS a JOIN roles AS r ON a.roles_fk = r.id_rol JOIN permiso_rol AS pr ON r.id_rol = pr.rol_fk JOIN permisos AS p ON p.id_permisos = pr.permiso_fk WHERE a.user = %s AND p.nombre_permiso LIKE 'GESTION%'"
            mycursor.execute(sql, val)
            resultado = mycursor.fetchall()

            if resultado:
                opciones = [i[2] for i in resultado]
                self.dropdown = QComboBox(self.encabezado)
                self.dropdown.addItems(opciones)
                self.dropdown.setCurrentText("GESTIONAR")
                self.dropdown.currentTextChanged.connect(self.click_handler)
                self.encabezado_layout.addWidget(self.dropdown)
            else:
                QMessageBox.critical(self, "Error", "Credenciales inválidas.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error de conexión: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

class Inicio(QFrame):
    def __init__(self, contenedor):
        super().__init__(contenedor)
        self.setStyleSheet("background-color: gray;")
        self.layout = QVBoxLayout(self)

        label = QLabel(self)
        label.setStyleSheet("background-color: gray;")
        self.layout.addWidget(label, alignment=Qt.AlignCenter)

        etiqueta = QLabel("Bienvenido al SIG LAB MANAGER", label)
        etiqueta.setStyleSheet("font: bold 16px Arial; color: blue;")
        self.layout.addWidget(etiqueta, alignment=Qt.AlignCenter)

        etiqueta = QLabel("WORK IN PROGRESS", label)
        etiqueta.setStyleSheet("font: bold 16px Arial; color: blue;")
        self.layout.addWidget(etiqueta, alignment=Qt.AlignCenter)

        etiqueta = QLabel("¡Explora y disfruta de las funcionalidades del sistema!", label)
        etiqueta.setStyleSheet("font: bold 16px Arial; color: blue;")
        self.layout.addWidget(etiqueta, alignment=Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = "JoseDaza"  # Cambia esto por el usuario real
    menu = Menu(user)
    sys.exit(app.exec())