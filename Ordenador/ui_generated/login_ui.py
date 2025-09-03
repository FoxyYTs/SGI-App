# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_SGI_Login(object):
    def setupUi(self, SGI_Login):
        if not SGI_Login.objectName():
            SGI_Login.setObjectName(u"SGI_Login")
        SGI_Login.resize(900, 700)
        self.centralwidget = QWidget(SGI_Login)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMaximumSize(QSize(500, 1000))
        self.stackedWidget.setLayoutDirection(Qt.LeftToRight)
        self.stackedWidget.setAutoFillBackground(False)
        self.inicio = QWidget()
        self.inicio.setObjectName(u"inicio")
        self.verticalLayout_2 = QVBoxLayout(self.inicio)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(50, 50, 50, 50)
        self.line_inicio_usuario = QLineEdit(self.inicio)
        self.line_inicio_usuario.setObjectName(u"line_inicio_usuario")

        self.verticalLayout_2.addWidget(self.line_inicio_usuario)

        self.line_inicio_clave = QLineEdit(self.inicio)
        self.line_inicio_clave.setObjectName(u"line_inicio_clave")
        self.line_inicio_clave.setEchoMode(QLineEdit.Password)

        self.verticalLayout_2.addWidget(self.line_inicio_clave)

        self.btn_inicio_iniciar = QPushButton(self.inicio)
        self.btn_inicio_iniciar.setObjectName(u"btn_inicio_iniciar")

        self.verticalLayout_2.addWidget(self.btn_inicio_iniciar)

        self.btn_inicio_registrar = QPushButton(self.inicio)
        self.btn_inicio_registrar.setObjectName(u"btn_inicio_registrar")

        self.verticalLayout_2.addWidget(self.btn_inicio_registrar)

        self.btn_inicio_recuperar = QPushButton(self.inicio)
        self.btn_inicio_recuperar.setObjectName(u"btn_inicio_recuperar")

        self.verticalLayout_2.addWidget(self.btn_inicio_recuperar)

        self.stackedWidget.addWidget(self.inicio)
        self.registro = QWidget()
        self.registro.setObjectName(u"registro")
        self.verticalLayout = QVBoxLayout(self.registro)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(50, 50, 50, 50)
        self.line_registro_usuario = QLineEdit(self.registro)
        self.line_registro_usuario.setObjectName(u"line_registro_usuario")

        self.verticalLayout.addWidget(self.line_registro_usuario)

        self.line_registro_correo = QLineEdit(self.registro)
        self.line_registro_correo.setObjectName(u"line_registro_correo")

        self.verticalLayout.addWidget(self.line_registro_correo)

        self.line_registro_clave = QLineEdit(self.registro)
        self.line_registro_clave.setObjectName(u"line_registro_clave")
        self.line_registro_clave.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.line_registro_clave)

        self.line_registro_reclave = QLineEdit(self.registro)
        self.line_registro_reclave.setObjectName(u"line_registro_reclave")

        self.verticalLayout.addWidget(self.line_registro_reclave)

        self.btn_registro_registrar = QPushButton(self.registro)
        self.btn_registro_registrar.setObjectName(u"btn_registro_registrar")

        self.verticalLayout.addWidget(self.btn_registro_registrar)

        self.btn_registro_iniciar = QPushButton(self.registro)
        self.btn_registro_iniciar.setObjectName(u"btn_registro_iniciar")

        self.verticalLayout.addWidget(self.btn_registro_iniciar)

        self.stackedWidget.addWidget(self.registro)
        self.recupero = QWidget()
        self.recupero.setObjectName(u"recupero")
        self.verticalLayout_4 = QVBoxLayout(self.recupero)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(50, 50, 50, 50)
        self.line_recupero_correo = QLineEdit(self.recupero)
        self.line_recupero_correo.setObjectName(u"line_recupero_correo")

        self.verticalLayout_4.addWidget(self.line_recupero_correo)

        self.btn_recupero_recuperar = QPushButton(self.recupero)
        self.btn_recupero_recuperar.setObjectName(u"btn_recupero_recuperar")

        self.verticalLayout_4.addWidget(self.btn_recupero_recuperar)

        self.btn_recupero_iniciar = QPushButton(self.recupero)
        self.btn_recupero_iniciar.setObjectName(u"btn_recupero_iniciar")

        self.verticalLayout_4.addWidget(self.btn_recupero_iniciar)

        self.stackedWidget.addWidget(self.recupero)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

        SGI_Login.setCentralWidget(self.centralwidget)

        self.retranslateUi(SGI_Login)

        QMetaObject.connectSlotsByName(SGI_Login)
    # setupUi

    def retranslateUi(self, SGI_Login):
        SGI_Login.setWindowTitle(QCoreApplication.translate("SGI_Login", u"MainWindow", None))
        self.line_inicio_usuario.setPlaceholderText(QCoreApplication.translate("SGI_Login", u"Usuario", None))
        self.line_inicio_clave.setPlaceholderText(QCoreApplication.translate("SGI_Login", u"Contrase\u00f1a", None))
        self.btn_inicio_iniciar.setText(QCoreApplication.translate("SGI_Login", u"Iniciar Sesion", None))
        self.btn_inicio_registrar.setText(QCoreApplication.translate("SGI_Login", u"Crear Cuenta", None))
        self.btn_inicio_recuperar.setText(QCoreApplication.translate("SGI_Login", u"Olvide Mi Contrase\u00f1a", None))
        self.line_registro_usuario.setPlaceholderText(QCoreApplication.translate("SGI_Login", u"Usuario", None))
        self.line_registro_correo.setPlaceholderText(QCoreApplication.translate("SGI_Login", u"Correo", None))
        self.line_registro_clave.setPlaceholderText(QCoreApplication.translate("SGI_Login", u"Contrase\u00f1a", None))
        self.line_registro_reclave.setPlaceholderText(QCoreApplication.translate("SGI_Login", u"Confirmar Contrase\u00f1a", None))
        self.btn_registro_registrar.setText(QCoreApplication.translate("SGI_Login", u"Registrar Cuenta", None))
        self.btn_registro_iniciar.setText(QCoreApplication.translate("SGI_Login", u"Ya Tengo una Cuenta", None))
        self.line_recupero_correo.setPlaceholderText(QCoreApplication.translate("SGI_Login", u"Correo", None))
        self.btn_recupero_recuperar.setText(QCoreApplication.translate("SGI_Login", u"Enviar Correo de Recuperacion", None))
        self.btn_recupero_iniciar.setText(QCoreApplication.translate("SGI_Login", u"Iniciar Sesion", None))
    # retranslateUi

