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
                database="evm_db"
            )
        except Error as variable:
            print(" Error en conexion")
            print(variable)

    #Create
    def register(self, comando):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando)
                self.conexion.commit()
                print("   registrado")
                print("Nuevo ID:", cursor.lastrowid)

            except Error as valError:
                print(valError)

    def register2(self, comando):
            if self.conexion.is_connected():
                try:
                    cursor = self.conexion.cursor()
                    cursor.execute(comando)
                    self.conexion.commit()
                    print("Registro Exitoso")

                except Error as valError:
                    print(valError)

    #READ - Select
    def lista(self, comando):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando)
                resultados = cursor.fetchall()
                return resultados

            except Error as valError:
                print(valError)
        return 0

    def lista_param(self, comando, params):
        try:
            if self.conexion.is_connected():
                cursor = self.conexion.cursor()
                cursor.execute(comando, params)
                resultados = cursor.fetchall()
                return resultados
        except Error as e:
            print(e)
            return []


    #Update
    def actualizar(self, comando):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(comando)
                self.conexion.commit()
                contador = cursor.rowcount
                print("   Actualizado")
                print()

            except Error as valError:
                print(valError)
                contador = -1
        return contador

import mysql.connector
from mysql.connector import Error
from utils.log import log

import mysql.connector
from mysql.connector import Error

class Conn:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sistema_evm"
            )
        except Error as e:
            print("Error al conectar:", e)
            self.conn = None

    def cursor(self):
        if self.conn:
            return self.conn.cursor()
        return None

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
