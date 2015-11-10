import sqlite3

class Conexion():
    database = 'dr_help'
    def getConnection(self):
        conexion =  sqlite3.connect(self.database)
        return conexion
