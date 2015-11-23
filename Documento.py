from Conexion import Conexion
from Objeto import Objeto

class Documento(Objeto):
    data = ''
    headernames = ['Nombre']
    atributos = ['documento_id', 'documento_data', 'documento_consulta', 'documento_nombre']
    tabla = ' documento'
    nuevo = True

    def __init__(self):
        self.inicializar()

    def mapeardatos(self, datarow):
        self.id = datarow[0]
        self.data = datarow[1]
        self.consulta = datarow[2]
        self.nombre = datarow[3]
        self.nuevo = False

    def enlistar(self, listas):
        lista = []
        for r in listas:
            documento = Documento()
            documento.mapeardatos(r)
            lista.append(documento)
        return lista

    def guardar(self):
        consulta = 'SELECT * FROM Documento WHERE documento_id = ?;'
        if not self.nuevo:
            return
        conexion = self.conexion.getConnection()
        cursor = conexion.cursor()
        cursor.execute(consulta, (str(self.id),))
        if cursor.fetchone() is None:
            query = self.query_insert + '?,?,?,?' + self.query_insert_end
            try:
                cursor.execute(query, (str(self.contar()), self.data, self.consulta, self.nombre))
                conexion.commit()
                cursor.close()
            except:
                return False
            return True
        else:
            return False
