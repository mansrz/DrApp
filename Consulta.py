from Conexion import Conexion
from Objeto import Objeto
from Paciente import Paciente
from Doctor import Doctor

class Consulta(Objeto):
    fecha = Date()
    paciente = Paciente()
    doctor = Doctor()
    observaciones = ''
    extra = ''
    extra2 = ''

    headernames = ['Fecha', 'Paciente', 'Doctor', 'Observaciones', 'Extra']
    atributos = 'consulta_id, consulta_fecha, consulta_paciente, consulta_doctor, consulta_observaciones, consulta_extra, consulta_extra2'
    tabla = 'consulta'

    def __init__(self):
        self.inicializar()

