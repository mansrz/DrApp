import sys
from PyQt5 import QtGui,QtCore, uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import re
#CLASES
from Conexion import *
from Doctor import *
from Paciente import *
from Consulta import *

login = uic.loadUiType('login.ui')[0]
consulta = uic.loadUiType('consulta.ui')[0]
cliente = uic.loadUiType('paciente.ui')[0]
doctor = uic.loadUiType('doctor.ui')[0]
reporte = uic.loadUiType('reporte.ui')[0]
acercade = uic.loadUiType('acercade.ui')[0]
estilo = open('st.stylesheet','r').read()
principal_ui = uic.loadUiType('principal.ui')[0]

class VentanaDoctor(QDialog, doctor):
    doctor_user = Doctor()

    def __init__(self, parent =  None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)
        self.inicializar()

    def inicializar(self):
        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_eliminar_todo.clicked.connect(self.eliminar)
        self.todos = self.doctor_user.consultar_todos()
        self.btn_cerrar.clicked.connect(self.closeEvent)
        self.tb_doctores.doubleClicked.connect(self.elegir_dobleclick)
        self.actualizarGrids()

    def actualizarGrids(self):
        self.todos = self.doctor_user.consultar_todos()
        self.fillDataGrid(self.todos, self.tb_doctores)
        self.fillDataGrid(self.todos, self.tb_eliminar)

    def elegir_dobleclick(self):
        rst = QMessageBox.warning(self,"Alerta","¿Esta seguro que desea editar?", QMessageBox.Cancel, QMessageBox.Ok)
        if rst != QMessageBox.Ok:
            self.doctor_user = Doctor()
            return
        selected = self.tb_doctores.selectedIndexes()
        self.selected_index = selected.__getitem__(0)
        select = self.todos[self.selected_index.row()]
        self.doctor_user.id = select.id
        self.tabWidget.setCurrentWidget(self.tab_1)
        self.txt_username.setText(select.username)
        self.txt_nombre.setText(select.nombres)
        self.txt_apellido.setText(select.apellidos)
        self.txt_telefono.setText(select.telefono)
        self.txt_password.setText(select.password)
        self.txt_cedula.setText(select.cedula)
        self.txt_direccion.setText(select.direccion)
        self.txt_mail.setText(select.mail)

    def guardar(self):
        if self.doctor_user.id is None or self.doctor_user.id == 0:
            self.doctor_user = Doctor()
        self.doctor_user.username = self.txt_username.text()
        self.doctor_user.nombres = self.txt_nombre.text()
        self.doctor_user.apellidos = self.txt_apellido.text()
        self.doctor_user.telefono = self.txt_telefono.text()
        self.doctor_user.password = self.txt_password.text()
        self.doctor_user.cedula = self.txt_cedula.text()
        self.doctor_user.direccion = self.txt_direccion.text()
        self.doctor_user.mail = self.txt_mail.text()
        if(self.doctor_user.guardar()):
            self.txt_username.setText('')
            self.txt_nombre.setText('')
            self.txt_apellido.setText('')
            self.txt_telefono.setText('')
            self.txt_password.setText('')
            self.txt_cedula.setText('')
            self.txt_direccion.setText('')
            self.txt_mail.setText('')
            self.doctor_user = Doctor()
            QtGui.QMessageBox.information(self, '¡Enhorabuena!', 'Se ha registrado el doctor', QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Revisa los datos', QtGui.QMessageBox.Ok)
        self.actualizarGrids()

    def eliminar(self):
        try:
            selected = self.tb_eliminar.selectedIndexes()
            self.selected_index = selected.__getitem__(0)
            select = self.todos[self.selected_index.row()]
            doctor_user = Doctor()
            doctor_user.id = select.id
            rst=QMessageBox.warning(self,"Alerta","Esta seguro que desea eliminar", QMessageBox.Cancel, QMessageBox.Ok)
            if rst == QMessageBox.Ok:
                if(doctor_user.eliminar()):
                    QMessageBox.about(self,"¡Enhorabuena!", "Se ha eliminado al Doctor")
                else:
                    print('dd')
                    QMessageBox.warning(self,"Error", "Ha ocurrido un error")
        except:
            QMessageBox.about(self,"Error", "Ha ocurrido un error")
        self.actualizarGrids()

    def fillDataGrid(self, result, tb):
        model = QStandardItemModel()
        model.setColumnCount(len(self.doctor_user.headernames))
        model.setHorizontalHeaderLabels(self.doctor_user.headernames)
        doctors = []
        for doctor_result in result:
          li = [doctor_result.username, doctor_result.nombres, doctor_result.apellidos, doctor_result.telefono, doctor_result.cedula, doctor_result.direccion, doctor_result.mail]
          doctors.append(li)
          row = []
          for name in li:
            item = QStandardItem(str(name))
            item.setEditable(False)
            row.append(item)
          model.appendRow(row)
        tb.setModel(model)
        return doctors

    def buscar(self):
        texto = self.txt_buscar.text()
        if len(texto) < 1:
            QMessageBox.about(self,"Error", "No encontramos nada")
            self.actualizarGrids()
        result = []
        if self.radioButton_nombre.isChecked():
           result = self.doctor_user.consultar_By_Atribute(texto, 'nombres')
        elif self.radioButton_apellido.isChecked():
           result = self.doctor_user.consultar_By_Atribute(texto, 'apellidos')
        elif self.radioButton_cedula.isChecked():
           result = self.doctor_user.consultar_By_Atribute(texto, 'cedula')
        self.fillDataGrid(result, self.tb_doctores)

    def closeEvent(self):
        self.hide()

class VentanaCliente(QDialog, cliente):
    paciente_user = Paciente()

    def __init__(self, parent =  None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)
        self.inicializar()

    def inicializar(self):
        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_eliminar_todo.clicked.connect(self.eliminar)
        self.todos = self.paciente_user.consultar_todos()
        self.tb_pacientes.doubleClicked.connect(self.elegir_dobleclick)
        self.btn_cerrar.clicked.connect(self.closeEvent)
        self.actualizarGrids()

    def actualizarGrids(self):
        self.todos = self.paciente_user.consultar_todos()
        self.fillDataGrid(self.todos, self.tb_pacientes)
        self.fillDataGrid(self.todos, self.tb_eliminar)

    def elegir_dobleclick(self):
        rst = QMessageBox.warning(self,"Alerta","¿Esta seguro que desea editar?", QMessageBox.Cancel, QMessageBox.Ok)
        if rst != QMessageBox.Ok:
            self.paciente_user = Paciente()
            return
        selected = self.tb_pacientes.selectedIndexes()
        self.selected_index = selected.__getitem__(0)
        select = self.todos[self.selected_index.row()]
        self.paciente_user.id = select.id
        self.tabWidget.setCurrentWidget(self.tab_1)
        self.txt_nombre.setText(select.nombres)
        self.txt_apellido.setText(select.apellidos)
        self.txt_telefono.setText(select.telefono)
        self.txt_cedula.setText(select.cedula)
        self.txt_direccion.setText(select.direccion)

    def guardar(self):
        if self.paciente_user.id is None or self.paciente_user.id == 0:
            self.paciente_user = Paciente()
        self.paciente_user.nombres = self.txt_nombre.text()
        self.paciente_user.apellidos = self.txt_apellido.text()
        self.paciente_user.telefono = self.txt_telefono.text()
        self.paciente_user.cedula = self.txt_cedula.text()
        self.paciente_user.direccion = self.txt_direccion.text()
        if(self.paciente_user.guardar()):
            self.txt_nombre.setText('')
            self.txt_apellido.setText('')
            self.txt_telefono.setText('')
            self.txt_cedula.setText('')
            self.txt_direccion.setText('')
            QtGui.QMessageBox.information(self, '¡Enhorabuena!', 'Se ha registrado el doctor', QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Revisa los datos', QtGui.QMessageBox.Ok)
        self.actualizarGrids()

    def eliminar(self):
        try:
            selected = self.tb_eliminar.selectedIndexes()
            self.selected_index = selected.__getitem__(0)
            select = self.todos[self.selected_index.row()]
            paciente_user = Paciente()
            paciente_user.id = select.id
            rst=QMessageBox.warning(self,"Alerta","Esta seguro que desea eliminar", QMessageBox.Cancel, QMessageBox.Ok)
            if rst == QMessageBox.Ok:
                if(paciente_user.eliminar()):
                    QMessageBox.about(self,"¡Enhorabuena!", "Se ha eliminado al Paciente")
                else:
                    print('dd')
                    QMessageBox.warning(self,"Error", "Ha ocurrido un error")
        except:
            QMessageBox.about(self,"Error", "Ha ocurrido un error")
        self.actualizarGrids()

    def fillDataGrid(self, result, tb):
        model = QStandardItemModel()
        model.setColumnCount(len(self.paciente_user.headernames))
        model.setHorizontalHeaderLabels(self.paciente_user.headernames)
        pacientes = []
        for paciente_result in result:
          li = [paciente_result.nombres, paciente_result.apellidos, paciente_result.direccion, paciente_result.telefono, paciente_result.cedula]
          pacientes.append(li)
          row = []
          for name in li:
            item = QStandardItem(str(name))
            item.setEditable(False)
            row.append(item)
          model.appendRow(row)
        tb.setModel(model)
        return pacientes

    def buscar(self):
        texto = self.txt_buscar.text()
        if len(texto) < 1:
            self.actualizarGrids()
            QMessageBox.about(self,"Error", "No encontramos nada")
            return
        result = []
        if self.radioButton_nombre.isChecked():
           result = self.paciente_user.consultar_By_Atribute(texto, 'nombres')
        elif self.radioButton_apellido.isChecked():
           result = self.paciente_user.consultar_By_Atribute(texto, 'apellidos')
        elif self.radioButton_cedula.isChecked():
           result = self.paciente_user.consultar_By_Atribute(texto, 'cedula')
        self.fillDataGrid(result, self.tb_pacientes)

    def closeEvent(self):
        self.hide()

class VentanaConsulta(QDialog, consulta):
    consulta_user = Consulta()
    doctor_user = Doctor()

    def __init__(self, parent =  None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)
        self.inicializar()

    def inicializar(self):
        self.btn_documento.clicked.connect(self.subirDocumento)
        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_eliminar_todo.clicked.connect(self.eliminar)
        self.todos = self.consulta_user.consultar_todos()
        self.tb_consultas.doubleClicked.connect(self.elegir_dobleclick)
        self.btn_cerrar.clicked.connect(self.closeEvent)
        self.tb_documentos.doubleClicked.connect(self.preview_dobleclick)
        for p in Paciente().consultar_todos():
            self.cbo_paciente.addItem(p.nombres+' '+p.apellidos, p.id)
        self.actualizarGrids()

    def actualizarGrids(self):
        self.todos = self.consulta_user.consultar_todos()
        self.fillDataGrid(self.todos, self.tb_consultas)
        self.fillDataGrid(self.todos, self.tb_eliminar)

    def preview_dobleclick(self):
        selected = self.tb_documentos.selectedIndexes()
        self.selected_index = selected.__getitem__(0)
        doc = self.consulta_user.documentos[self.selected_index.row()]
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Guardar",
        '', "All Files (*)")
        spl =doc.nombre.split('/')
        name = spl[len(spl)-1]
        with open(fileName, 'wb') as file_:
                file_.write(doc.data)


    def elegir_dobleclick(self):
        rst = QMessageBox.warning(self,"Alerta","¿Esta seguro que desea editar?", QMessageBox.Cancel, QMessageBox.Ok)
        if rst != QMessageBox.Ok:
            self.consulta_user = Paciente()
            return
        selected = self.tb_consultas.selectedIndexes()
        self.selected_index = selected.__getitem__(0)
        select = self.todos[self.selected_index.row()]
        self.consulta_user.id = select.id
        self.consulta_user.consultar()
        self.tabWidget.setCurrentWidget(self.tab_1)
        self.cbo_paciente.setCurrentIndex(self.cbo_paciente.findText(self.consulta_user.paciente.nombres+ ' ' + self.consulta_user.paciente.apellidos))
        self.txt_observacion.setPlainText(self.consulta_user.observaciones)
        self.fillDocumentos()

    def guardar(self):
        if self.consulta_user.id is None or self.consulta_user.id == 0:
            self.consulta_user = Consulta()
        self.consulta_user.paciente.id =  self.cbo_paciente.itemData(self.cbo_paciente.currentIndex())
        self.consulta_user.doctor = self.doctor_user
        self.consulta_user.observaciones = self.txt_observacion.toPlainText()
        if(self.consulta_user.guardar()):
            QtGui.QMessageBox.information(self, '¡Enhorabuena!', 'Se ha registrado el consulta', QtGui.QMessageBox.Ok)
            self.consulta_user = Consulta()
            model = QStandardItemModel()
            model.setColumnCount(len(Documento().headernames))
            model.setHorizontalHeaderLabels(Documento().headernames)
            self.tb_documentos.setModel(model)
            self.txt_observacion.setPlainText('')
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Revisa los datos', QtGui.QMessageBox.Ok)
        self.actualizarGrids()

    def eliminar(self):
        try:
            selected = self.tb_eliminar.selectedIndexes()
            self.selected_index = selected.__getitem__(0)
            select = self.todos[self.selected_index.row()]
            consulta_user = Consulta()
            consulta_user.id = select.id
            rst = QMessageBox.warning(self,"Alerta","Esta seguro que desea eliminar", QMessageBox.Cancel, QMessageBox.Ok)
            if rst == QMessageBox.Ok:
                if(consulta_user.eliminar()):
                    QMessageBox.about(self,"¡Enhorabuena!", "Se ha eliminado al Paciente")
                else:
                    QMessageBox.warning(self,"Error", "Ha ocurrido un error")
        except:
            QMessageBox.about(self,"Error", "Ha ocurrido un error")
        self.actualizarGrids()

    def fillDataGrid(self, result, tb):
        model = QStandardItemModel()
        model.setColumnCount(len(self.consulta_user.headernames))
        model.setHorizontalHeaderLabels(self.consulta_user.headernames)
        consultas = []
        for consulta_result in result:
          li = [consulta_result.paciente.getNombre(), consulta_result.doctor.getNombre(), consulta_result.observaciones]
          consultas.append(li)
          row = []
          for name in li:
            item = QStandardItem(str(name))
            item.setEditable(False)
            row.append(item)
          model.appendRow(row)
        tb.setModel(model)
        return consultas

    def subirDocumento (self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        nuevo_documento = Documento()
        nuevo_documento.nombre = filename
        with open(filename, 'rb') as f:
            nuevo_documento.data = f.read()
        self.consulta_user.documentos.append(nuevo_documento)
        self.fillDocumentos()

    def fillDocumentos(self):
        lista = self.consulta_user.documentos
        model = QStandardItemModel()
        model.setColumnCount(len(Documento().headernames))
        model.setHorizontalHeaderLabels(Documento().headernames)
        for documento in lista:
          li = [documento.nombre]
          row = []
          for name in li:
            item = QStandardItem(str(name))
            item.setEditable(False)
            row.append(item)
          model.appendRow(row)
        self.tb_documentos.setModel(model)

    def buscar(self):
        texto = self.txt_buscar.text()
        if len(texto) < 1:
            self.actualizarGrids()
            QMessageBox.about(self,"Error", "No encontramos nada")
            return
        result = []
        if self.radioButton_nombre.isChecked():
           result = self.consulta_user.consultar_By_Atribute(texto, 'nombres')
        elif self.radioButton_apellido.isChecked():
           result = self.consulta_user.consultar_By_Atribute(texto, 'apellidos')
        elif self.radioButton_cedula.isChecked():
           result = self.consulta_user.consultar_By_Atribute(texto, 'cedula')
        self.fillDataGrid(result, self.tb_consultas)


    def closeEvent(self):
        self.hide()

class VentanaReportes(QDialog, reporte):
    doctor_user = Doctor()

    def __init__(self, parent =  None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)
        self.inicializar()

    def inicializar(self):
        self.cbo_reporte.addItem('Consultas por doctor')
        self.cbo_reporte.addItem('Pacientes atendidos')
        self.btn_generar.clicked.connect(self.generar)

    def fillDataGrid(self, result, tb):
        model = QStandardItemModel()
        model.setColumnCount(len(Consulta().headernames))
        model.setHorizontalHeaderLabels(Consulta().headernames)
        consultas = []
        for consulta_result in result:
            li = [consulta_result.paciente.getNombre(), consulta_result.doctor.getNombre(), consulta_result.observaciones]
            consultas.append(li)
            row = []
            for name in li:
                item = QStandardItem(str(name))
                item.setEditable(False)
                row.append(item)
        model.appendRow(row)
        tb.setModel(model)
        return consultas

    def fillDataGrid_2(self, result, tb):
        model = QStandardItemModel()
        model.setColumnCount(len(Paciente().headernames))
        model.setHorizontalHeaderLabels(Paciente().headernames)
        pacientes = []
        for paciente_result in result:
            li = [paciente_result.nombres, paciente_result.apellidos, paciente_result.direccion, paciente_result.telefono, paciente_result.cedula]
            pacientes.append(li)
            row = []
            for name in li:
                item = QStandardItem(str(name))
                item.setEditable(False)
                row.append(item)
        model.appendRow(row)
        tb.setModel(model)
        return pacientes

    def generar(self):
        opcion =  self.cbo_reporte.currentIndex()
        if opcion == 0:
            self.fillDataGrid(Consulta().consultar_By_Atribute(self.doctor_user.id,'doctor'), self.tb_reporte)
        elif opcion == 1:
            self.fillDataGrid_2(Paciente().getPacientes(self.doctor_user.id), self.tb_reporte)

class VentanaAcercaDe(QDialog, acercade):
    def __init__(self, parent =  None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)

class VentanaPrincipal(QtWidgets.QMainWindow, principal_ui):
    doctor_user = ''

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.frame.move((screen.width()-self.frame.geometry().width())/2, (screen.height()-self.frame.geometry().height())/2)
        self.setStyleSheet(estilo)
        self.inicializar()

    def setUser(self, doctor_user):
        self.doctor_user = doctor_user
        self.txt_nombre.setText(self.doctor_user.nombres)
        self.txt_apellido.setText(self.doctor_user.apellidos)

    def inicializar(self):
        self.action_cliente.triggered.connect(self.Abrir_cliente)
        self.action_crearconsulta.triggered.connect(self.Abrir_consulta)
        self.action_doctor.triggered.connect(self.Abrir_doctor)
        self.action_reportes.triggered.connect(self.Abrir_reporte)
        self.action_acerca.triggered.connect(self.Abrir_acercade)

    def Abrir_reporte(self):
        reporte = VentanaReportes()
        reporte.doctor_user = self.doctor_user
        reporte.exec_()

    def Abrir_doctor(self):
        doctor = VentanaDoctor()
        doctor.exec_()

    def Abrir_consulta(self):
        consulta = VentanaConsulta()
        consulta.doctor_user = self.doctor_user
        consulta.exec_()

    def Abrir_cliente(self):
        cliente = VentanaCliente()
        cliente.exec_()

    def Abrir_acercade(self):
        acercade = VentanaAcercaDe()
        acercade.exec_()

class Login(QDialog, login):
    conexion = Conexion()
    doctor_user = Doctor()

    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.setStyleSheet(estilo)
        self.boton_iniciarsesion.clicked.connect(self.login_act)

    def login_act(self):
        name = str(self.input_usuario.text())
        pwd = str(self.input_pwd.text())
        self.doctor_user.username = name
        self.doctor_user.password = pwd
        result = self.doctor_user.login()
        if result:
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Usuario o contrasena equivocadas', QtGui.QMessageBox.Ok)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    if login.exec_() == QDialog.Accepted:
        principal = VentanaPrincipal()
        principal.setUser(login.doctor_user)
        principal.showMaximized()
        sys.exit(app.exec_())
