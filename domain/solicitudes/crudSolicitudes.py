from db.connV import conn
from domain.solicitudes.ClaseSolicitudes import Solicitud
from domain.solicitudes import crudSolicitudes
from datetime import timedelta


def listarSolicitudes():

    miConn = conn()  

    comando = """
    SELECT 
        s.numero AS ID, 
        s.asunto AS Asunto, 
        s.horaSolicitada AS Hora, 
        s.fechaSolicitada AS Fecha,
        s.vehiculo AS Vehiculo, 
        ve.matricula,
        es.descripcion AS edo_solicitud,

        eso.numero AS id_solicitante,
        CONCAT(eso.nombrePila, ' ', eso.apdPaterno) AS solicitante,

        ea.numero AS id_autorizador,
        CONCAT(ea.nombrePila, ' ', ea.apdPaterno) AS autorizador

    FROM solicitud AS s
    INNER JOIN edo_solicitud AS es ON s.edo_solicitud = es.numero
    INNER JOIN empleado AS eso ON s.solicitante = eso.numero
    INNER JOIN empleado AS ea ON s.autorizador = ea.numero
    INNER JOIN vehiculo AS ve ON s.vehiculo = ve.numSerie
    ORDER BY ID;
    """

    lista = miConn.lista(comando)

    print("\n--- LISTADO DE SOLICITUDES ---")

    if not lista:
        print("No hay solicitudes registradas.")
        return []

    print(f"{'ID':<5} {'Asunto':<30} {'Hora':<10} {'Fecha':<12} {'Vehículo':<15} {'Matrícula':<12} {'Estado':<15} {'ID Sol':<7} {'Solicitante':<22} {'ID Aut':<7} {'Autorizador':<22}")
    print("-" * 160)

    for fila in lista:
        (ID, asunto, hora, fecha, vehiculo, matricula,
         edo_desc, id_sol, solicitante, id_aut, autorizador) = fila

        print(f"{ID:<5} {asunto:<30} {str(hora):<10} {str(fecha):<12} {vehiculo:<15} {matricula:<12} {edo_desc:<15} "
              f"{id_sol:<7} {solicitante:<22} {id_aut:<7} {autorizador:<22}")

    print("-" * 160)

    return lista



def listarEstado():
    miConn = conn()  
#consulta 7
    comando = """
    SELECT 
        s.numero AS ID, 
        CONCAT(e.nombrePila, ' ', e.apdPaterno) AS Solicitante, 
        s.asunto AS Asunto, 
        s.fechaSolicitada AS Fecha, 
        s.horaSolicitada AS Hora, 
        ed.descripcion AS Estado
    FROM solicitud AS s
    INNER JOIN empleado AS e ON s.solicitante = e.numero
    INNER JOIN edo_solicitud AS ed ON s.edo_solicitud = ed.numero
    ORDER BY s.numero;
    """

    lista = miConn.lista(comando)

    print("\n--- LISTADO DE SOLICITUDES ---")

    if not lista:
        print("No hay solicitudes registradas.")
        return []

    # Encabezado
    print(f"{'ID':<5} {'Solicitante':<25} {'Asunto':<30} {'Fecha':<12} {'Hora':<10} {'Estado':<20}")
    print("-" * 110)

    # Filas
    for fila in lista:
        ID, solicitante, asunto, fecha, hora, estado = fila
        print(f"{ID:<5} {solicitante:<25} {asunto:<30} {str(fecha):<12} {str(hora):<10} {estado:<20}")

    print("-" * 110)

    return lista


def agregarSolicitud(nuevaSolicitud):
    obj = nuevaSolicitud
    miConn = conn()

    comando = f"""
    INSERT INTO solicitud 
    (asunto, fechaSolicitada, horaSolicitada, vehiculo, solicitante)
    VALUES (
        '{obj.get_asunto()}',
        '{obj.get_fechaSolicitud()}',
        '{obj.get_horaSolicitud()}',
        '{obj.get_vehiculo()}',
        '{obj.get_solicitante()}'
    );
    """

    lastid = miConn.registrar(comando)

    if lastid:
        print(f"\nSolicitud agregada correctamente con ID: {lastid}\n")
    else:
        print("\nERROR: No se pudo agregar la solicitud.\n")

    return lastid


def estadoSolicitud(existeSolicitud):
    obj = existeSolicitud
    miConn = conn()

    comando = f"""
    UPDATE solicitud 
    SET edo_solicitud = '{obj.get_edoSolicitud()}'
    WHERE numero = {obj.get_numero()};
    """

    contador = miConn.actualizar(comando)

    if contador == 1:
        print("\nEstado actualizado correctamente.\n")
    elif contador == 0:
        print("\nLa solicitud no existe.\n")
    else:
        print("\nERROR actualizando estado de solicitud.\n")


def actualizar_matricula(id_vehiculo, nueva_matricula):
    print(f"\nActualizando id={id_vehiculo} con matrícula={nueva_matricula}")
    # Aquí va tu update real si lo deseas


def eliminarSolicitud(numero):
    miConn = conn()
    comando = f"DELETE FROM solicitud WHERE numero = {numero};"

    contador = miConn.actualizar(comando)

    if contador == 1:
        print("\nSolicitud eliminada correctamente.\n")
    elif contador == 0:
        print("\nSolicitud no encontrada.\n")
    else:
        print("\nERROR eliminando la solicitud.\n")
