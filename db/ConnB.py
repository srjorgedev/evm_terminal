import mysql.connector
from mysql.connector import Error
from utils.log import log

class Conn:
    def __init__(self):
        self.__config = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "",
            "db": "evm_db",
            "use_pure": True
        }

    def conectar(self):
        return mysql.connector.connect(**self.__config)
        
    def comprobarConexion(self) -> bool:
        try:
            cnx = self.conectar()
            is_connected = cnx.is_connected()
            cnx.close()
            
            return is_connected
        except Error:
            return False

    def lista(self, query, params=None):
        cnx = None
        cursor = None
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            res = cursor.fetchall()
            return res
            
        except Error as error:
            log(f"[BD ERROR - LISTA]: {error.errno}")
            log(f"[BD ERROR - LISTA]: {error.msg}")
            return []
            
        finally:
            if cursor: cursor.close()
            if cnx and cnx.is_connected(): cnx.close()
            
    def registrar(self, query, params=None) -> int:
        cnx = None
        cursor = None
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            cnx.commit()
            lastid = cursor.lastrowid
            return lastid
            
        except Error as error:
            log(f"[BD ERROR - REGISTRAR]: {error}")
            input("Presione Enter para continuar...")
            return -1
            
        finally:
            if cursor: cursor.close()
            if cnx and cnx.is_connected(): cnx.close()

    def actualizar(self, query, params=None):
        cnx = None
        cursor = None
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            cnx.commit()
            count = cursor.rowcount
            return count
            
        except Error as error:
            log(f"[BD ERROR - ACTUALIZAR]: {error}")
            return 0
            
        finally:
            if cursor: cursor.close()
            if cnx and cnx.is_connected(): cnx.close()
            
    def cerrar(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
