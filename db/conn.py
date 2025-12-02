# conn.py
import mysql.connector
from mysql.connector import Error

class conn:
    def __init__(self):
        self.conexion = None
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="",
                database="evm")
            print("Conectado a Enterprise Vehicle Manager")
        except Error as variable:
            print("Error en conexion")
            print(variable)
            
    def lista(self, comando):
        if self.conexion and self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando)
                resultados = cursor.fetchall()
                # print("Listado correcto")
                return resultados
            except Error as valError:
                print("Error al listar:")
                print(valError)
        return 0
    
    def lista_param(self, comando, valores):
        if self.conexion and self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando, valores)
                return cursor.fetchall()
            except Error as valError:
                print("Error al listar:")
                print(valError)
        return 0
    
    def registrar(self, comando):
        if self.conexion and self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando)
                self.conexion.commit()
                print("Registrado correctamente")
                return cursor.rowcount
            except Error as valError:
                print("Error en el registro:")
                print(valError)
        return -1
    
    def registrar_param(self, comando, valores):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(comando, valores)
            self.conexion.commit()
            return True
        except Error as variable:
            print("Error en conexión o registro:")
            print(variable)
            return False
                
    def actualizar(self, comando):
        contador = -1
        if self.conexion and self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando)
                self.conexion.commit()
                contador = cursor.rowcount
            except Error as valError:
                print("Error en conexión o actualización:")
                print(valError)
                contador = -1
            
            return contador
        return contador
    
    def actualizar_param(self, comando, valores):
        if self.conexion and self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando, valores)
                self.conexion.commit()
                return cursor.rowcount
            except Error as valError:
                print("Error en actualización:")
                print(valError)
                return -1
        return -1