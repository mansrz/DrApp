from Conexion import Conexion
from Objeto import Objeto

class Paciente(Objeto):
    headernames = ['Nombres', 'Apellidos', 'Direccion', 'Telefono', ]
    atributos = ['paciente_id', 'paciente_nombres', 'paciente_apellidos', 'paciente_direccion', 'paciente_telefono' ]
    tabla = ' paciente'

    def __init__(self):
        self.inicializar()

    def mapeardatos(self, datarow):
        self.id = datarow[0]
        self.nombres = datarow[1]
        self.apellidos = datarow[2]
        self.telefono = datarow[3]
        self.username = datarow[4]
        self.password = datarow[5]

    def enlistar(self, listas):
        lista=[]
        for r in listas:
            paciente = Paciente()
            paciente.mapeardatos(r)
            lista.append(paciente)
        return lista

    def guardar(self):
        consulta = 'SELECT * FROM paciente WHERE paciente_id = %s;'
        conexion = self.conexion.getConnection()
        cursor = conexion.cursor()
        cursor.execute(consulta, (str(self.id),))

        if cursor.fetchone() is None:
            query = self.query_insert + '%s,%s,%s,%s,%s,%s' + self.query_insert_end
            cursor.execute(query, (str(self.contar)), self.nombres, self.apellidos, self.direccion, self.telefono,)
            conexion.commit()
            cursor.close()
            print query
        else:
            cursor.close()
            self.modificar()

    def modificar(self):
        query = (self.query_update+' paciente_nombres = %s , \
           paciente_apellidos =%s, paciente_direccion=%s, paciente_telefono =%s\
           '+self.query_update_end)

        print query
        conexion = self.conexion.getConnection()
        cursor= conexion.cursor()
        cursor.execute(query,(self.nombres, self.apellidos, self.direccion, self.telefono))
        conexion.commit()
        cursor.close()
