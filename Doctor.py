from Conexion import Conexion
from Objeto import Objeto

class Doctor(Objeto):
    headernames = [ 'Username', 'Nombres', 'Apellidos', 'Telefono','Cedula', 'Direccion', 'Email']
    atributos = ['doctor_id', 'doctor_nombres', 'doctor_apellidos', 'doctor_telefono', 'doctor_username', 'doctor_password', 'doctor_cedula', 'doctor_direccion', 'doctor_mail' ]
    tabla = ' doctor'

    def __init__(self):
        self.inicializar()
        self.id = ''
        self.nombres =''
        self.apellidos =''
        self.telefono =''
        self.username =''
        self.password =''
        self.cedula = ''
        self.direccion = ''
        self.mail = ''

    def mapeardatos(self, datarow):
        self.id = datarow[0]
        self.nombres = datarow[1]
        self.apellidos = datarow[2]
        self.telefono = datarow[3]
        self.username = datarow[4]
        self.password = datarow[5]
        self.cedula = datarow[6]
        self.direccion = datarow[7]
        self.mail = datarow[8]

    def getNombre(self):
        return self.nombres + ' ' + self.apellidos

    def enlistar(self, listas):
        lista=[]
        for r in listas:
            doctor = Doctor()
            doctor.mapeardatos(r)
            lista.append(doctor)
        return lista

    def guardar(self):
        consulta = 'SELECT * FROM Doctor WHERE doctor_id = ?;'
        conexion = self.conexion.getConnection()
        cursor = conexion.cursor()
        cursor.execute(consulta, (str(self.id),))
        print(self.id)
        if cursor.fetchone() is None:
            query = self.query_insert + '?,?,?,?,?,?,?,?,?' + self.query_insert_end
            try:
                cursor.execute(query, (str(self.contar()), self.nombres, self.apellidos, self.telefono, self.username, self.password, self.cedula, self.direccion, self.mail))
                conexion.commit()
                cursor.close()
            except:
                return False
            return True
        else:
            cursor.close()
            return self.modificar()

    def modificar(self):
        query = (self.query_update+' doctor_nombres = ? , \
           doctor_apellidos =?, doctor_telefono =?, doctor_username = ?, \
           doctor_password = ?, doctor_cedula = ?, doctor_direccion = ?, \
           doctor_mail = ?'+self.query_update_end)
        conexion = self.conexion.getConnection()
        cursor= conexion.cursor()
        try:
            cursor.execute(query,(self.nombres, self.apellidos, self.telefono, self.username, self.password,self.cedula, self.direccion, self.mail, self.id))
            conexion.commit()
            cursor.close()
        except:
            return False
        return True

    def login(self):
        query = 'SELECT *  FROM doctor  WHERE doctor_username= ? AND doctor_password = ?'
        conexion = self.conexion.getConnection()
        cursor= conexion.cursor()
        cursor.execute(query,(self.username, self.password))
        result=cursor.fetchone()
        cursor.close()
        if (result is not None):
            print(result)
            self.mapeardatos(result)
            return True;
        else:
            return False;
