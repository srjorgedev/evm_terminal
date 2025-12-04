#fObservacion.py

from interface.observacionymantenimiento import val
from domain.observaciones import crudObservacion
from domain.observaciones.Observacion import Observacion
from interface.observacionymantenimiento import fMantenimiento

# Tipos de Observación disponibles
TIPOS_OBSERVACION = ["General", "Seguridad", "Estetica"]

MAPA_TIPO_OBS = {
    "General": 1,
    "Seguridad": 2,
    "Estetica": 3
}

def pedirDatos():
    print(" ----- Registrar Observación -----")
    
    # Tipo de observación
    tipoSeleccion = val.vSeleccion("Tipo de Observación", TIPOS_OBSERVACION)
    tipoIndice = MAPA_TIPO_OBS[tipoSeleccion]  # FK numérico
    
    # Descripción
    descripcion = val.Str("Descripción de la Observación")
    
    # Bitácora válida
    bitacora = pedirBitacoraValida()
    
    # Crear objeto y registrar
    nuevaObservacion = Observacion(descripcion, tipoIndice, bitacora)
    crudObservacion.alta(nuevaObservacion)

    # Preguntar si se desea registrar mantenimiento
    while True:
        respuesta = val.vSeleccion("¿Desea registrar un nuevo MANTENIMIENTO?", ["si", "no"]).lower()
        if respuesta == "si":
            print("\n** Redirigiendo a registro de Mantenimiento **")
            fMantenimiento.pedirDatos()
            break
        elif respuesta == "no":
            break

def listaGeneral():
    crudObservacion.lista()

def actualizarObservacion():
    print(" ----- Modificar Observación -----")
    numero = val.vInt("Folio de la Observación a modificar")
    temp = Observacion("", 0, 0, numero)
    
    obj = crudObservacion.buscar(temp)
    if not obj:
        return

    print("\n-- Ingrese nuevos datos --")
    # Actualizar descripción
    nuevaDescripcion = val.Str(f"Nueva Descripción (actual: {obj.get_descripcion()})")
    obj.set_descripcion(nuevaDescripcion)

    # Actualizar bitácora con validación
    bitacora = pedirBitacoraValida(f"Nueva Bitácora asociada (actual: {obj.get_bitacoraAsociada()})")
    obj.set_bitacoraAsociada(bitacora)

    # Actualizar en BD
    crudObservacion.actualizar(obj)

def borrarObservacion():
    print(" ----- Eliminar Observación -----")
    numero = val.vInt("Folio de la Observación a eliminar")
    temp = Observacion("", 0, 0, numero)

    obj = crudObservacion.buscar(temp)
    if not obj:
        return

    confirma = val.vSeleccion("Confirme eliminación", ["si", "no"])
    if confirma.lower() == "si":
        crudObservacion.borrar(obj)
    else:
        print("Eliminación cancelada.")

def pedirBitacoraValida(mensaje="Bitácora asociada"):
    miConn = crudObservacion.conn()
    while True:
        bit = val.vInt(mensaje)
        cursor = miConn.conexion.cursor()
        cursor.execute("SELECT numero FROM bitacora WHERE numero = %s", (bit,))
        if cursor.fetchone():
            return bit
        print("  La bitácora NO existe. Ingresa un número válido.\n")

def menuObservaciones():
    while True:
        print("\n--- MENÚ OBSERVACIONES ---")
        print("--------------------------------------------")
        print("1. Registrar Observación")
        print("--------------------------------------------")
        print("2. Listar Observaciones")
        print("--------------------------------------------")
        print("3. Actualizar Observación")
        print("--------------------------------------------")
        print("4. Eliminar Observación")
        print("--------------------------------------------")
        print("5. Consultar Observaciones por Bitácora")
        print("--------------------------------------------")
        print("6. Regresar al menú principal")
        print("--------------------------------------------")

        opcion = val.vInt("Selecciona una opción")

        if opcion == 1:
            pedirDatos()
        elif opcion == 2:
            listaGeneral()
        elif opcion == 3:
            actualizarObservacion()
        elif opcion == 4:
            borrarObservacion()
        elif opcion == 5:
            consultarObservacionesBitacora()
        elif opcion == 6:
            break
        else:
            print("Opción inválida, intenta de nuevo.")


def consultarObservacionesBitacora():
    bitacora = pedirBitacoraValida("Número de bitácora a consultar")
    miConn = crudObservacion.conn()
    cursor = miConn.conexion.cursor()
    cursor.execute("""
        SELECT o.numero, o.descripcion, t.descripcion 
        FROM observacion o
        JOIN tipoObservacion t ON o.tipoObservacion = t.numero
        WHERE o.bitacora = %s
        ORDER BY o.numero
    """, (bitacora,))
    resultados = cursor.fetchall()

    if resultados:
        print(f"\n--- Observaciones de la Bitácora {bitacora} ---")
        for fila in resultados:
            print(f"Folio: {fila[0]} | Tipo: {fila[2]} | Descripción: {fila[1]}")
    else:
        print("No se encontraron observaciones para esta bitácora.")