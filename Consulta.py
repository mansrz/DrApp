from Conexion import Conexion
from Objeto import Objeto
from Paciente import Paciente
from Doctor import Doctor
from Documento import *

class Consulta(Objeto):
    fecha = ''
    paciente = Paciente()
    doctor = Doctor()
    documentos = []
    observaciones = ''
    extra = ''
    extra2 = ''

    headernames = ['Fecha','Paciente', 'Doctor', 'Observaciones']
    atributos = '[consulta_id, consulta_fecha, consulta_paciente, consulta_doctor, consulta_observaciones, consulta_extra, consulta_extra2]'
    tabla = 'consulta'

    def __init__(self):
        self.inicializar()
        self.id = ''
        self.fecha = ''
        self.observaciones = ''
        self.extra = ''
        self.extra2 = ''

    def mapeardatos(self, datarow):
        self.id = datarow[0]
        self.fecha = datarow[1]
        self.paciente.id = datarow[2]
        self.doctor.id = datarow[3]
        self.observaciones = datarow[4]
        self.extra = datarow[5]
        self.extra2 = datarow[6]
        self.paciente.consultar()
        self.doctor.consultar()
        self.getDocumentos()

    def getDocumentos(self):
        documento = Documento()
        self.documentos = documento.consultar_By_Atribute(self.id, 'consulta')

    def enlistar(self, listas):
        lista=[]
        for r in listas:
            consulta = Consulta()
            consulta.mapeardatos(r)
            lista.append(consulta)
        return lista

    def guardar(self):
        import datetime
        consulta = 'SELECT * FROM consulta WHERE consulta_id = ?;'
        conexion = self.conexion.getConnection()
        cursor = conexion.cursor()
        cursor.execute(consulta, (str(self.id),))
        if cursor.fetchone() is None:
            pk = str(self.contar())
            query = self.query_insert + '?,?,?,?,?,?,?' + self.query_insert_end
            try:
                cursor.execute(query, (pk, str(datetime.datetime.now().date())
, self.paciente.id, self.doctor.id, self.observaciones, self.extra, self.extra2))
                conexion.commit()
                cursor.close()
                print(query)
                for documento in self.documentos:
                    documento.consulta = pk
                    documento.guardar()
                return True
            except:
                cursor.close()
                return False
        else:
            cursor.close()
            return self.modificar()

    def modificar(self):
        query = (self.query_update+' consulta_fecha = ? , \
           consulta_paciente =?, consulta_doctor =?, consulta_observaciones = ?,\
           consulta_extra = ?, consulta_extra2 = ?'+self.query_update_end)
        conexion = self.conexion.getConnection()
        cursor= conexion.cursor()
        try:
            cursor.execute(query, (self.fecha, self.paciente.id, self.doctor.id, self.observaciones, self.extra, self.extra2, self.id))
            conexion.commit()
            for documento in self.documentos:
                documento.consulta = self.id
                if documento.nuevo:
                    documento.guardar()
            cursor.close()
            return True
        except:
            cursor.close()
            return False
