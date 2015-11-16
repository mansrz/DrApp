import sys
from PyQt4 import QtGui,QtCore, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
from Conexion import *

login = uic.loadUiType('login.ui')[0]
consulta = uic.loadUiType('consulta.ui')[0]
cliente = uic.loadUiType('paciente.ui')[0]
doctor = uic.loadUiType('doctor.ui')[0]
reporte = uic.loadUiType('consulta.ui')[0]
acercade = uic.loadUiType('acercade.ui')[0]
estilo = open('st.stylesheet','r').read()
principal_ui = uic.loadUiType('principal.ui')[0]

class VentanaConsulta(QtGui.QDialog, consulta):
    def __init__(self, parent =  None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)

class VentanaCliente(QtGui.QDialog, cliente):
    def __init__(self, parent =  None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)

class VentanaDoctor(QtGui.QDialog, doctor):
    def __init__(self, parent =  None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)

class VentanaReportes(QtGui.QDialog, reporte):
    def __init__(self, parent =  None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)

class VentanaAcercaDe(QtGui.QDialog, acercade):
    def __init__(self, parent =  None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)

class VentanaPrincipal(QtGui.QMainWindow, principal_ui):
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.frame.move((screen.width()-self.frame.geometry().width())/2, (screen.height()-self.frame.geometry().height())/2)
        self.setStyleSheet(estilo)
        self.inicializar()

    def inicializar(self):
        self.action_cliente.triggered.connect(self.Abrir_cliente)
        self.action_crearconsulta.triggered.connect(self.Abrir_consulta)
        self.action_doctor.triggered.connect(self.Abrir_doctor)
        self.action_reportes.triggered.connect(self.Abrir_reporte)
        self.action_acerca.triggered.connect(self.Abrir_acercade)

    def Abrir_reporte(self):
        reporte = VentanaReportes()
        reporte.exec_()

    def Abrir_doctor(self):
        doctor = VentanaDoctor()
        doctor.exec_()

    def Abrir_consulta(self):
        consulta = VentanaConsulta()
        consulta.exec_()

    def Abrir_cliente(self):
        cliente = VentanaCliente()
        cliente.exec_()

    def Abrir_acercade(self):
        acercade = VentanaAcercaDe()
        acercade.exec_()

class Login(QtGui.QDialog, login):
    conexion = Conexion()
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)
        self.boton_iniciarsesion.clicked.connect(self.login_act)

    def login_act(self):
        self.accept()
        name = str(self.input_usuario.text())
        pwd = str(self.input_pwd.text())
        query = ('SELECT COUNT(*) FROM Usuario WHERE usuario_nick= %s AND usuario_pwd = %s')
        conexion = self.conexion.getConnection()
        cursor= conexion.cursor()
        cursor.execute(query,(name,pwd))
        result=cursor.fetchone()
        if result[0]>0:
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Usuario o contrasena equivocadas', QtGui.QMessageBox.Ok)
        cursor.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    if Login().exec_() == QtGui.QDialog.Accepted:
        principal = VentanaPrincipal()
        principal.showMaximized()
        sys.exit(app.exec_())

