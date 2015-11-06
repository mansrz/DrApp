from MySQLdb import connect

class Conexion():
   user = 'root'
   pwd = '1234'
   host = '127.0.0.1'
   database = 'bd'
   def getConnection(self):
      conexion= mysql.connector.connect(user=self.user, password=self.pwd,host=self.host,database=self.database)
      return conexion
