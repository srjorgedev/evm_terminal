from db.connV import conn

# ---------------------------------------------------------
# LISTAR SOLICITUDES
# ---------------------------------------------------------

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
        es.descripcion AS Estado,

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
        print("No hay solicitudes.")
        return []

    print(f"{'ID':<5} {'Asunto':<30} {'Hora':<10} {'Fecha':<12} "
          f"{'Vehiculo':<15} {'Matricula':<12} {'Estado':<15} "
          f"{'ID Sol':<7} {'Solicitante':<25} {'ID Aut':<7} {'Autorizador':<25}")
    print("-" * 160)

    for fila in lista:
        print(f"{fila[0]:<5} {fila[1]:<30} {str(fila[2]):<10} {str(fila[3]):<12} "
              f"{fila[4]:<15} {fila[5]:<12} {fila[6]:<15} "
              f"{fila[7]:<7} {fila[8]:<25} {fila[9]:<7} {fila[10]:<25}")

    print("-" * 160)
    return lista


# ---------------------------------------------------------
# LISTAR ESTADO
# ---------------------------------------------------------

def listarEstado():
    miConn = conn()

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

    print("\n--- ESTADO DE SOLICITUDES ---")

    if not lista:
        print("No hay solicitudes.")
        return []

    print(f"{'ID':<5} {'Solicitante':<25} {'Asunto':<30} {'Fecha':<12} {'Hora':<10} {'Estado':<20}")
    print("-" * 110)

    for fila in lista:
        print(f"{fila[0]:<5} {fila[1]:<25} {fila[2]:<30} "
              f"{str(fila[3]):<12} {str(fila[4]):<10} {fila[5]:<20}")

    print("-" * 110)
    return lista


# ---------------------------------------------------------
# AGREGAR SOLICITUD
# ---------------------------------------------------------

def agregarSolicitud(obj):
    miConn = conn()

    comando = f"""
    INSERT INTO solicitud
        (asunto, fechaSolicitada, horaSolicitada, vehiculo, edo_solicitud, solicitante, autorizador)
    VALUES (
        '{obj.get_asunto()}',
        '{obj.get_fechaSolicitud()}',
        '{obj.get_horaSolicitud()}',
        '{obj.get_vehiculo()}',
        1,                   
        {obj.get_solicitante()},
        3                    
    );
    """

    lastid = miConn.registrar(comando)

    if lastid:
        print(f"\nSolicitud agregada con ID: {lastid}\n")
    else:
        print("\nERROR al agregar la solicitud.\n")


# ---------------------------------------------------------
# MODIFICAR ASUNTO
# ---------------------------------------------------------

def modificarAsunto(id_solicitud, nuevo_asunto):
    miConn = conn()

    comando = f"""
    UPDATE solicitud
    SET asunto = '{nuevo_asunto}'
    WHERE numero = {id_solicitud};
    """

    res = miConn.actualizar(comando)

    if res == 1:
        print("\nAsunto modificado correctamente.\n")
    else:
        print("\nERROR: No se pudo modificar el asunto.\n")


# ---------------------------------------------------------
# MODIFICAR ESTADO
# ---------------------------------------------------------

def modificarEstado(existeSolicitud):
    id_solicitud = existeSolicitud.get_numero()
    nuevo_estado = existeSolicitud.get_edoSolicitud()
    miConn = conn()



    comando = f"""
    UPDATE solicitud
    SET edo_solicitud = {nuevo_estado}
    WHERE numero = {id_solicitud};
    """

    res = miConn.actualizar(comando)

    if res == 1:
        print("\nEstado actualizado correctamente.\n")
    else:
        print("\nERROR actualizando estado.\n")


# ---------------------------------------------------------
# ELIMINAR
# ---------------------------------------------------------

def eliminarSolicitud(numero):
    miConn = conn()
    comando = f"DELETE FROM solicitud WHERE numero = {numero};"

    res = miConn.actualizar(comando)

    if res == 1:
        print("\nSolicitud eliminada correctamente.\n")
    else:
        print("\nERROR eliminando la solicitud.\n")


# ---------------------------------------------------------
# VEHÍCULOS
# ---------------------------------------------------------

def numsemoma():
    miConn = conn()
    comando = "SELECT numSerie, marca, modelo FROM vehiculo;"

    lista = miConn.lista(comando)

    print(f"{'NumSerie':<20} {'Marca':<20} {'Modelo':<20}")
    print("-" * 60)

    for fila in lista:
        print(f"{fila[0]:<20} {fila[1]:<20} {fila[2]:<20}")

    print("-" * 60)


# ---------------------------------------------------------
# EMPLEADOS
# ---------------------------------------------------------

def empleados():
    miConn = conn()
    comando = """
        SELECT 
            numero AS ID,
            CONCAT(nombrePila, ' ', apdPaterno, ' ', apdMaterno) AS Empleado
        FROM empleado;
    """

    lista = miConn.lista(comando)

    print(f"{'ID Empleado':<15} {'Empleado':<40}")
    print("-" * 65)

    for fila in lista:
        print(f"{fila[0]:<15} {fila[1]:<40}")

    print("-" * 65)
    
def edosoli():
    miConn = conn()
    comando = """
        SELECT ed.numero as Num, ed.descripcion as Descripcion FROM edo_solicitud as ed;
    """

    lista = miConn.lista(comando)

    print(f"{'Numero':<15} {'Descripcion':<40}")
    print("-" * 65)

    for fila in lista:
        print(f"{fila[0]:<15} {fila[1]:<40}")

    print("-" * 65)
        
