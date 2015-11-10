from Conexion import Conexion
from Objeto import Objeto
from Consulta import Consulta

class Documento(Objeto):
    data = ''
    consulta = Consulta()
    headernames = ['Data', 'Consulta']
    atributos = ['documento_id', 'documento_data', 'documento_consulta']
    tabla = ' documentos'

    def __init__(self):
        self.inicializar()

    def mapeardatos(self, datarow):
        self.id = datarow[0]
        self.data = datarow[1]
        self.consulta.id = datarow[2]
        self.consulta.consultar()

    def enlistar(self, listas):
        lista = []
        for r in listas:
            documento = Documento()
            documento.mapeardatos(r)
            lista.append(documento)
        return lista

