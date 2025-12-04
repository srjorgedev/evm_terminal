import mysql.connector
from mysql.connector import Error


class Conn:

    def __init__(self):
        self.cnx = mysql.connector.connect(host="localhost",
                                           port=3306,
                                           user="root",
                                           password="",
                                           db="evm_db")
        self.cursor = self.cnx.cursor()

    def lista(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []

    def registrar(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.cnx.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error: {e}")
            return -1

    def actualizar(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.cnx.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(f"Error: {e}")
            return 0

    def cerrar(self):
        self.cursor.close()
        self.cnx.close()
