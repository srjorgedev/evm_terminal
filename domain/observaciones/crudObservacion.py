# crudObservacion.py


from db.conn import conn
from domain.observaciones.Observacion import Observacion

# CREATE
def alta(obj):
    miConn = conn()
    comando = "INSERT INTO observacion (descripcion, tipoObservacion, bitacora) VALUES (%s, %s, %s)"
    valores = (obj.get_descripcion(), obj.get_tipoObservacion(), obj.get_bitacoraAsociada())
    miConn.registrar_param(comando, valores)
    

# READ
def lista():
    miConn = conn()
    comando = """
        SELECT o.numero, o.descripcion, t.descripcion AS TipoTexto, o.bitacora
        FROM observacion o
        JOIN tipoobservacion t ON o.tipoObservacion = t.numero
        ORDER BY o.numero
    """
    listado = miConn.lista(comando)
    if listado == 0:
        print("Error: No se puede mostrar el listado o la conexión falló.")
        return

    if len(listado) == 0:
        print("No hay observaciones registradas.")
        return

    print("\n--- Listado de Observaciones ---")
    for fila in listado:
        obj = Observacion(fila[1], fila[2], fila[3], fila[0])
        print(obj)

# UPDATE
def actualizar(obj):
    miConn = conn()
    comando = "UPDATE observacion SET descripcion = %s, bitacora = %s WHERE numero = %s"
    valores = (obj.get_descripcion(), obj.get_bitacoraAsociada(), obj.get_numero())
    miConn.actualizar_param(comando, valores)

# DELETE
def borrar(obj):
    miConn = conn()
    comando = "DELETE FROM observacion WHERE numero = %s"
    valores = (obj.get_numero(),)
    miConn.actualizar_param(comando, valores)

# BUSCAR
def buscar(obj):
    miConn = conn()
    comando = "SELECT numero, descripcion, tipoObservacion, bitacora FROM observacion WHERE numero = %s"
    valores = (obj.get_numero(),)
    listado = miConn.lista_param(comando, valores)
    if listado != 0 and len(listado) == 1:
        fila = listado[0]
        objEncontrado = Observacion(fila[1], fila[2], fila[3], fila[0])
        print("Observación encontrada:")
        print(objEncontrado)
        return objEncontrado
    print("Folio de Observación no encontrado.")
    return False
