import mysql.connector
from mysql.connector import Error


class conn:

    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            db="evm_db")
            
        except Error as variable:
            print("error en conexion")
            print(variable)

    #READ - SELECT
    def lista(self, comando):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando)
                resultados = cursor.fetchall()
               
                return resultados
            except Error as valError:
                print("   Error al leer datos")
                print(valError)
        return 0

    #CREATE - INSERT
    def registrar(self, comando):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando)
                self.conexion.commit()
                lastid = cursor.lastrowid
            except Error as valError:
                print("   Error de conexion")
                lastid = -1
                print(valError)
        return lastid

    #DELETE - delete
    def borrar(self, comando):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando)
                self.conexion.commit()
                print("   Borrado")
            except Error as valError:
                print("   Error de conexion")
                print(valError)

    #UPDATE
    def actualizar(self, comando):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando)
                self.conexion.commit()
                contador = cursor.rowcount
            except Error as valError:
                print("   Error de conexion")
                print(valError)
                contador = -1

        return contador
