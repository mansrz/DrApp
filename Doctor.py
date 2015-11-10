from Conexion import Conexion
from Objeto import Objeto

class Doctor(Objeto):
    headernames = ['Nombres', 'Apellidos', 'Telefono', ]
    atributos = ['doctor_id', 'doctor_nombres', 'doctor_apellidos', 'doctor_telefono', 'doctor_username', 'doctor_password' ]
    tabla = ' doctor'

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
            doctor = Doctor()
            doctor.mapeardatos(r)
            lista.append(doctor)
        return lista

    def guardar(self):
        consulta = 'SELECT * FROM Doctor WHERE doctor_id = %s;'
        conexion = self.conexion.getConnection()
        cursor = conexion.cursor()
        cursor.execute(consulta, (str(self.id),))

        if cursor.fetchone() is None:
            query = self.query_insert + '%s,%s,%s,%s,%s,%s' + self.query_insert_end
            cursor.execute(query, (str(self.contar)), self.nombres, self.apellidos, self.telefono, self.username, self.password)
            conexion.commit()
            cursor.close()
            print query
        else:
            cursor.close()
            self.modificar()

    def modificar(self):
        query = (self.query_update+' doctor_nombres = %s , \
           doctor_apellidos =%s, doctor_telefono =%s, doctor_username = %s \
           doctor_password '+self.query_update_end)
        print query
        conexion = self.conexion.getConnection()
        cursor= conexion.cursor()
        cursor.execute(query,(self.nombres, self.apellidos, self.telefono, self.username, self.password))
        conexion.commit()
        cursor.close()

    
