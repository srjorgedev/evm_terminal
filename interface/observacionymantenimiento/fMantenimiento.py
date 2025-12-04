# fMantenimiento.py
from interface.observacionymantenimiento import val
from domain.mantenimiento import crudMantenimiento
from domain.mantenimiento.Mantenimiento import Mantenimiento
from db.conn import conn

# Mapas de conversión
MAPA_TIPO = {"Preventivo": 1, "Correctivo": 2, "Superficial": 3}
MAPA_TIPO_INV = {v: k for k, v in MAPA_TIPO.items()}

MAPA_ESTADO = {"PENDIENTE DE ASIGNACIÓN": 1, "EN PROGRESO": 2, "FINALIZADO": 3}
MAPA_ESTADO_INV = {v: k for k, v in MAPA_ESTADO.items()}


# ----- Crear Mantenimiento -----
def pedirDatos():
    print(" ----- Solicitar Nuevo Mantenimiento -----")
    razon = val.vEmpresa("Razón de la solicitud")
    
    tipo = val.vSeleccion("Tipo de Mantenimiento", list(MAPA_TIPO.keys()))
    tipo_id = MAPA_TIPO[tipo]
    
    importancia = val.vSeleccion("Importancia", ["Alta", "Media", "Baja"])
    vehiculo = pedirVehiculoValido()
    fechaProgramada = val.vFecha("Fecha Programada")
    comentarios = val.Str("Comentarios generales")
    
    estado_id = MAPA_ESTADO["PENDIENTE DE ASIGNACIÓN"]
    
    nuevoMantenimiento = Mantenimiento(
        razon, importancia, fechaProgramada, comentarios,
        tipo_id, vehiculo, estado_id
    )
    
    crudMantenimiento.alta(nuevoMantenimiento)


# ----- Listado Limpio -----
def listaGeneral():
    listado = crudMantenimiento.lista()
    if listado == 0 or listado is None:
        print("No se pudo obtener el listado.")
        return

    print("\n*** Listado de Mantenimientos ***")
    for m in listado:
        tipoTexto = MAPA_TIPO_INV.get(m.get_tipoMantenimiento(), m.get_tipoMantenimiento())
        estadoTexto = MAPA_ESTADO_INV.get(m.get_estadoMantenimiento(), m.get_estadoMantenimiento())

        print(f"Folio: {m.get_folio()}")
        print(f"Razón: {m.get_razon()}")
        print(f"Importancia: {m.get_importancia()}")
        print(f"Fecha Programada: {m.get_fechaProgramada()}")
        print(f"Comentarios: {m.get_comentarios()}")
        print(f"Tipo de Mantenimiento: {tipoTexto}")
        print(f"Vehículo: {m.get_vehiculo()}")
        print(f"Estado Mantenimiento: {estadoTexto}")
        print("-" * 60)


# ----- Actualizar Mantenimiento -----
def actualizarMantenimiento():
    print(" ----- Actualizar Mantenimiento -----")
    folio = val.vInt("Folio del Mantenimiento a modificar")
    tempM = Mantenimiento("", "", "", "", "", "", "", folio)
    
    objM = crudMantenimiento.buscar(tempM)
    if not objM:
        return
    
    estatusOpciones = ["ABIERTO", "ASIGNADO", "CERRADO"]
    nuevoEstatus = val.vSeleccion("Seleccione el Nuevo Estatus", estatusOpciones)
    objM.set_estatus(nuevoEstatus)
    
    # Cambiar Estado Mantenimiento según Estatus
    if nuevoEstatus == "ABIERTO":
        objM.set_estadoMantenimiento(MAPA_ESTADO["PENDIENTE DE ASIGNACIÓN"])
    elif nuevoEstatus == "ASIGNADO":
        objM.set_estadoMantenimiento(MAPA_ESTADO["EN PROGRESO"])
    elif nuevoEstatus == "CERRADO":
        objM.set_estadoMantenimiento(MAPA_ESTADO["FINALIZADO"])
    
    # Pedir actualización de datos adicionales si no es cerrado
    if nuevoEstatus != "CERRADO":
        nuevaImportancia = val.vSeleccion(f"Nueva Importancia (actual: {objM.get_importancia()})", ["Alta", "Media", "Baja"])
        objM.set_importancia(nuevaImportancia)
        
        nuevaFecha = val.vFecha(f"Nueva Fecha Programada (actual: {objM.get_fechaProgramada()})")
        objM.set_fechaProgramada(nuevaFecha)
        
        nuevoComentario = val.Str(f"Nuevos Comentarios (actual: {objM.get_comentarios()})")
        objM.set_comentarios(nuevoComentario)
    
    crudMantenimiento.actualizar(objM)
    print("Actualización completada.")


# ----- Borrar Mantenimiento -----
def borrarMantenimiento():
    print(" ----- Eliminar Mantenimiento -----")
    folio = val.vInt("Folio del Mantenimiento a eliminar")
    tempM = Mantenimiento("", "", "", "", "", "", "", "", folio)
    
    objM = crudMantenimiento.buscar(tempM)
    if not objM:
        return
    
    confirma = val.vSeleccion("Confirme eliminación", ["si", "no"])
    if confirma.lower() == "si":
        crudMantenimiento.borrar(objM)
        print("Mantenimiento eliminado.")
    else:
        print("Eliminación cancelada.")


# ----- Validar Vehículo -----
def pedirVehiculoValido():
    miConn = conn()
    cursor = miConn.conexion.cursor()
    
    while True:
        vehiculo = val.vEmpresa("Número de Serie del Vehículo").strip()
        cursor.execute("SELECT numSerie FROM vehiculo WHERE numSerie = %s", (vehiculo,))
        resultado = cursor.fetchone()
        if resultado:
            return vehiculo
        print(" El número de serie NO existe, ingresa uno válido.\n")
        input(" Presiona Enter para intentar de nuevo...")

def menuMantenimientos():
    while True:
        print("\n--- MENÚ MANTENIMIENTO ---")
        print("--------------------------------------------")
        print("1. Registrar Mantenimiento")
        print("--------------------------------------------")
        print("2. Listar Mantenimientos")
        print("--------------------------------------------")
        print("3. Actualizar Mantenimiento")
        print("--------------------------------------------")
        print("4. Eliminar Mantenimiento")
        print("--------------------------------------------")
        print("5. Reporte de Mantenimiento de un Vehículo")
        print("--------------------------------------------")
        print("6. Estado de Mantenimientos de Vehículos")
        print("--------------------------------------------")
        print("7. Historial de Mantenimientos y Observaciones")
        print("--------------------------------------------")
        print("8. Regresar al menú principal")
        print("--------------------------------------------")

        opcion = val.vInt("Selecciona una opción")

        if opcion == 1:
            pedirDatos()
        elif opcion == 2:
            listaGeneral()
        elif opcion == 3:
            actualizarMantenimiento()
        elif opcion == 4:
            borrarMantenimiento()
        elif opcion == 5:
            reporteMantenimientoVehiculo()
        elif opcion == 6:
            estadoMantenimientosVehiculos()
        elif opcion == 7:
            historialMantenimientosObservaciones()
        elif opcion == 8:
            break
        else:
            print("Opción inválida, intenta de nuevo.")
            
# --- Funciones de reportes ---

def reporteMantenimientoVehiculo():
    vehiculo = val.Str("Número de matrícula del vehículo")
    miConn = crudMantenimiento.conn()
    cursor = miConn.conexion.cursor()
    cursor.execute("""
        SELECT v.matricula, ma.nombre, mo.nombre, mt.fechaProgramada, mt.razon,
               mt.comentarios, tm.comentario, tobs.descripcion, em.descripcion
        FROM mantenimiento mt
        JOIN vehiculo v ON mt.vehiculo = v.numSerie
        JOIN marca ma ON v.marca = ma.codigo
        JOIN modelo mo ON v.modelo = mo.codigo
        JOIN tipo_mantenimiento tm ON mt.tipoMantenimiento = tm.numero
        JOIN edo_mantenimiento em ON mt.estadoMantenimiento = em.numero
        LEFT JOIN mantenimiento_bitacora mb ON mt.folio = mb.mantenimiento
        LEFT JOIN observacion o ON mb.bitacora = o.bitacora
        LEFT JOIN tipoObservacion tobs ON o.tipoObservacion = tobs.numero
        WHERE v.matricula = %s
        ORDER BY mt.fechaProgramada DESC
    """, (vehiculo,))
    resultados = cursor.fetchall()

    if resultados:
        print(f"\n--- Reporte de Mantenimiento del Vehículo {vehiculo} ---")
        for fila in resultados:
            print(f"Matrícula: {fila[0]} | Marca: {fila[1]} | Modelo: {fila[2]} | Fecha: {fila[3]}")
            print(f"Razón: {fila[4]} | Comentarios: {fila[5]} | Tipo: {fila[6]} | Observación: {fila[7]} | Estado: {fila[8]}")
            print("-"*60)
    else:
        print("No se encontraron mantenimientos para este vehículo.")


def estadoMantenimientosVehiculos():
    miConn = crudMantenimiento.conn()
    cursor = miConn.conexion.cursor()
    cursor.execute("""
        SELECT mt.folio, v.matricula, ma.nombre, mo.nombre, mt.fechaProgramada,
               mt.razon, tm.comentario, em.descripcion
        FROM mantenimiento mt
        JOIN vehiculo v ON mt.vehiculo = v.numSerie
        JOIN marca ma ON v.marca = ma.codigo
        JOIN modelo mo ON v.modelo = mo.codigo
        JOIN tipo_mantenimiento tm ON mt.tipoMantenimiento = tm.numero
        JOIN edo_mantenimiento em ON mt.estadoMantenimiento = em.numero
        ORDER BY mt.fechaProgramada DESC
    """)
    resultados = cursor.fetchall()

    if resultados:
        print("\n--- Estado de Mantenimientos de Vehículos ---")
        for fila in resultados:
            print(f"Folio: {fila[0]} | Matrícula: {fila[1]} | Marca: {fila[2]} | Modelo: {fila[3]}")
            print(f"Fecha: {fila[4]} | Razón: {fila[5]} | Tipo: {fila[6]} | Estado: {fila[7]}")
            print("-"*60)
    else:
        print("No hay mantenimientos registrados.")


def historialMantenimientosObservaciones():
    vehiculo = val.Str("Número de matrícula del vehículo")
    miConn = crudMantenimiento.conn()
    cursor = miConn.conexion.cursor()
    cursor.execute("""
        SELECT v.matricula, ma.nombre, mo.nombre, mt.folio, mt.fechaProgramada, mt.razon,
               tm.comentario, tobs.descripcion
        FROM mantenimiento mt
        JOIN vehiculo v ON mt.vehiculo = v.numSerie
        JOIN marca ma ON v.marca = ma.codigo
        JOIN modelo mo ON v.modelo = mo.codigo
        JOIN tipo_mantenimiento tm ON mt.tipoMantenimiento = tm.numero
        LEFT JOIN mantenimiento_bitacora mb ON mt.folio = mb.mantenimiento
        LEFT JOIN observacion o ON mb.bitacora = o.bitacora
        LEFT JOIN tipoObservacion tobs ON o.tipoObservacion = tobs.numero
        WHERE v.matricula = %s
        ORDER BY mt.fechaProgramada DESC
    """, (vehiculo,))
    resultados = cursor.fetchall()

    if resultados:
        print(f"\n--- Historial de Mantenimientos y Observaciones del Vehículo {vehiculo} ---")
        for fila in resultados:
            print(f"Folio: {fila[3]} | Fecha: {fila[4]} | Razón: {fila[5]} | Tipo: {fila[6]} | Observación: {fila[7]}")
            print("-"*60)
    else:
        print("No se encontraron registros para este vehículo.")