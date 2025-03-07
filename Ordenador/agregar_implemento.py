from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QMessageBox
import mysql.connector
import conexion

class AgregarImplemento(QWidget):
    def __init__(self, contenedor):
        super().__init__(contenedor)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: gray;")
        layout = QVBoxLayout(self)

        label_agregar = QLabel("Agregar Implemento", self)
        label_agregar.setStyleSheet("font: bold 16px; color: blue;")
        layout.addWidget(label_agregar)

        nombre = QWidget(self)
        nombre_layout = QVBoxLayout(nombre)
        label_nombre = QLabel("Nombre del implemento:", nombre)
        nombre_layout.addWidget(label_nombre)
        self.entry_nombre = QLineEdit(nombre)
        nombre_layout.addWidget(self.entry_nombre)
        layout.addWidget(nombre)

        stock = QWidget(self)
        stock_layout = QVBoxLayout(stock)
        label_stock = QLabel("Stock:", stock)
        stock_layout.addWidget(label_stock)
        self.entry_stock = QLineEdit(stock)
        stock_layout.addWidget(self.entry_stock)
        layout.addWidget(stock)

        ubicacion = QWidget(self)
        ubicacion_layout = QVBoxLayout(ubicacion)
        label_ubicacion = QLabel("Ubicacion:", ubicacion)
        ubicacion_layout.addWidget(label_ubicacion)
        self.combo_ubicacion = QComboBox(ubicacion)
        self.combo_ubicacion.addItems(["Ubicacion 1", "Ubicacion 2", "Ubicacion 3"])
        ubicacion_layout.addWidget(self.combo_ubicacion)
        layout.addWidget(ubicacion)

        unidad_medida = QWidget(self)
        unidad_medida_layout = QVBoxLayout(unidad_medida)
        label_unidad_medida = QLabel("Unidad de Medida:", unidad_medida)
        unidad_medida_layout.addWidget(label_unidad_medida)
        self.combo_unidad_medida = QComboBox(unidad_medida)
        self.combo_unidad_medida.addItems(["Unidad 1", "Unidad 2", "Unidad 3"])
        unidad_medida_layout.addWidget(self.combo_unidad_medida)
        layout.addWidget(unidad_medida)

        tecnica = QWidget(self)
        tecnica_layout = QVBoxLayout(tecnica)
        label_tecnica = QLabel("Tecnica:", tecnica)
        tecnica_layout.addWidget(label_tecnica)
        self.entry_tecnica = QLineEdit(tecnica)
        tecnica_layout.addWidget(self.entry_tecnica)
        layout.addWidget(tecnica)

        guia_uso = QWidget(self)
        guia_uso_layout = QVBoxLayout(guia_uso)
        label_guia_uso = QLabel("Guia de Uso:", guia_uso)
        guia_uso_layout.addWidget(label_guia_uso)
        self.text_guia_uso = QLineEdit(guia_uso)
        guia_uso_layout.addWidget(self.text_guia_uso)
        layout.addWidget(guia_uso)

        button_registrar = QPushButton("Registrar", self)
        button_registrar.clicked.connect(self.registrar)
        layout.addWidget(button_registrar)

        self.consulta()

    def consulta(self):
        try:
            mydb = conexion.conectar()
            mycursor = mydb.cursor()

            sql = "SELECT * FROM implemento JOIN unidad_medida ON unidad_medida.id_medida=implemento.und_medida_fk ORDER BY id_implemento ASC"
            mycursor.execute(sql)
            self.resultado = mycursor.fetchall()

            if not self.resultado:
                QMessageBox.critical(self, "Error", "Credenciales inválidas.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error de conexión: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def registrar(self):
        # Aquí puedes agregar la lógica para registrar el implemento
        pass