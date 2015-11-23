from Conexion import Conexion
from Objeto import Objeto

class Paciente(Objeto):
    headernames = ['Nombres', 'Apellidos', 'Direccion', 'Telefono', 'Cedula']
    atributos = ['paciente_id', 'paciente_nombres', 'paciente_apellidos', 'paciente_direccion', 'paciente_telefono', 'paciente_cedula' ]
    tabla = ' paciente'

    def __init__(self):
        self.inicializar()
        self.id = ''
        self.nombres = ''
        self.apellidos = ''
        self.direccion = ''
        self.telefono = ''
        self.cedula = ''

    def mapeardatos(self, datarow):
        self.id = datarow[0]
        self.nombres = datarow[1]
        self.apellidos = datarow[2]
        self.direccion = datarow[3]
        self.telefono= datarow[3]
        self.cedula= datarow[4]

    def getPacientes(self, id):
        consulta = 'SELECT DISTINCT * FROM paciente WHERE paciente_id in (SELECT consulta_paciente\
                FROM consulta WHERE consulta_doctor=?);'
        conexion = self.conexion.getConnection()
        cursor = conexion.cursor()
        cursor.execute(consulta, (str(id),))
        result = cursor.fetchall()
        lista = self.enlistar(result)
        cursor.close()
        return lista


    def getNombre(self):
        return self.nombres + ' ' + self.apellidos

    def enlistar(self, listas):
        lista=[]
        for r in listas:
            paciente = Paciente()
            paciente.mapeardatos(r)
            lista.append(paciente)
        return lista

    def guardar(self):
        consulta = 'SELECT * FROM paciente WHERE paciente_id = ?;'
        conexion = self.conexion.getConnection()
        cursor = conexion.cursor()
        cursor.execute(consulta, (str(self.id),))
        if cursor.fetchone() is None:
            query = self.query_insert + '?,?,?,?,?,?' + self.query_insert_end
            try:
                cursor.execute(query, (str(self.contar()), self.nombres, self.apellidos, self.direccion, self.telefono, self.cedula))
                conexion.commit()
                cursor.close()
                return True
            except:
                cursor.close()
                return False
        else:
            cursor.close()
            return self.modificar()

    def modificar(self):
        query = (self.query_update+' paciente_nombres = ? , \
           paciente_apellidos =?, paciente_direccion=?, paciente_telefono =?,\
           paciente_cedula = ?'+self.query_update_end)
        conexion = self.conexion.getConnection()
        cursor= conexion.cursor()
        try:
            cursor.execute(query,(self.nombres, self.apellidos, self.direccion, self.telefono, self.cedula, self.id))
            conexion.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False
