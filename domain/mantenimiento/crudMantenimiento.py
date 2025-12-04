# crudMantenimiento.py
from db.conn import conn
from db.ConnB import Conn
from domain.mantenimiento.Mantenimiento import Mantenimiento

'''
Columnas tabla mantenimiento:
    folio INT PRIMARY KEY AUTO_INCREMENT,
    razon VARCHAR(200) NOT NULL,
    estatus VARCHAR(50) NOT NULL,
    importancia VARCHAR(50) NOT NULL,
    fechaProgramada DATE NOT NULL,
    comentarios VARCHAR(300),
    tipo_Mantenimiento INT NOT NULL,
    vehiculo VARCHAR(17) NOT NULL,
    estadoMantenimiento INT NOT NULL,
'''

# ----- CREATE -----
def alta(objMantenimiento):
    miConn = conn()
    comando = """
        INSERT INTO mantenimiento 
        (razon, importancia, fechaProgramada, comentarios, tipoMantenimiento, vehiculo, estadoMantenimiento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        objMantenimiento.get_razon(),
        objMantenimiento.get_importancia(),
        objMantenimiento.get_fechaProgramada(),
        objMantenimiento.get_comentarios(),
        objMantenimiento.get_tipoMantenimiento(),
        objMantenimiento.get_vehiculo(),
        objMantenimiento.get_estadoMantenimiento()
    )
    try:
        cursor = miConn.conexion.cursor()
        cursor.execute(comando, valores)
        miConn.conexion.commit()
        print("Mantenimiento registrado correctamente.")
    except Exception as e:
        print("Error en el registro:")
        print(e)


# ----- READ -----
def lista():
    miConn = Conn()
    
    try:
        comando = "SELECT folio, razon, importancia, fechaProgramada, comentarios, tipoMantenimiento, vehiculo, estadoMantenimiento FROM MANTENIMIENTO"
        listado = miConn.lista(comando)
        lista = []
        for fila in listado:
            m = Mantenimiento(
                fila[1],  # Razon
                0,  # Importancia
                str(fila[2]),  # FechaProgramada
                fila[3],  # Comentarios
                fila[4],  # TipoMantenimiento (ID)
                fila[5],  # Vehiculo
                fila[6],  # EstadoMantenimiento (ID)
                fila[0]   # Folio
            )
            lista.append(m)
        return lista
    except Exception as e:
        print("Error al listar:")
        print(e)
        return []


# ----- UPDATE -----
def actualizar(objMantenimiento):
    miConn = conn()
    comando = """
        UPDATE mantenimiento SET
        Importancia=%s,
        FechaProgramada=%s,
        Comentarios=%s,
        TipoMantenimiento=%s,
        EstadoMantenimiento=%s
        WHERE Folio=%s
    """
    valores = (
        objMantenimiento.get_importancia(),
        objMantenimiento.get_fechaProgramada(),
        objMantenimiento.get_comentarios(),
        objMantenimiento.get_tipoMantenimiento(),
        objMantenimiento.get_estadoMantenimiento(),
        objMantenimiento.get_folio()
    )
    try:
        cursor = miConn.conexion.cursor()
        cursor.execute(comando, valores)
        miConn.conexion.commit()
        if cursor.rowcount == 1:
            print("Actualización de mantenimiento realizada.")
            input("Presione Enter para continuar...")
        else:
            print("Actualización no realizada o folio no encontrado.")
            input("Presione Enter para continuar...")
    except Exception as e:
        print("Error en conexión o actualización:")
        input("Presione Enter para continuar...")
        print(e)


# ----- DELETE -----
def borrar(objMantenimiento):
    miConn = conn()
    comando = "DELETE FROM mantenimiento WHERE Folio=%s"
    valores = (objMantenimiento.get_folio(),)
    try:
        cursor = miConn.conexion.cursor()
        cursor.execute(comando, valores)
        miConn.conexion.commit()
        if cursor.rowcount == 1:
            print("Mantenimiento eliminado correctamente.")
            input("Presione Enter para continuar...")
        else:
            print("El folio del mantenimiento no existe.")
            input("Presione Enter para continuar...")
    except Exception as e:
        print("Error al eliminar mantenimiento:")
        input("Presione Enter para continuar...")
        print(e)


# ----- BUSCAR POR FOLIO -----
def buscar(objMantenimiento):
    miConn = conn()
    comando = "SELECT Folio, Razon, Importancia, FechaProgramada, Comentarios, tipoMantenimiento, Vehiculo, estadoMantenimiento FROM mantenimiento WHERE Folio=%s"
    valores = (objMantenimiento.get_folio(),)
    try:
        cursor = miConn.conexion.cursor()
        cursor.execute(comando, valores)
        fila = cursor.fetchone()
        if fila:
            m = Mantenimiento(
                fila[1],
                fila[2],
                fila[3],
                str(fila[4]),
                fila[5],
                fila[6],
                fila[7],
                fila[0]
            )
            return m
        else:
            print("Folio de mantenimiento no encontrado.")
            return False
    except Exception as e:
        print("Error al buscar mantenimiento:")
        print(e)
        return False
