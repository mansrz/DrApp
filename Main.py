import sys
from PyQt4 import QtGui,QtCore, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
from Conexion import *

login = uic.loadUiType('login.ui')[0]
estilo = open('st.stylesheet','r').read()

class Login(QtGui.QDialog, login):
    conexion = Conexion()
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)

    def login_act(self):
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

