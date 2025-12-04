import domain.bitacoras.crudBitacora as CRUD
from domain.bitacoras.Bitacora import Bitacora
import interface.bitacoras.Val as Val
from utils.limpiar import limpiar


def mostrar_tabla_resumen(datos):
    lista_id = []

    titulo = "Listado de bitacoras"
    espacios = int((64 - len(titulo)) / 2)
    print("-" * espacios + titulo + "-" * espacios)
    print()

    print(
        f"{'  N°':<6}{'Asunto':<15}{'Destino':<15}{'Fecha Salida':<15}{'Fecha Entrada':<15}\n"
    )

    if not datos:
        print("No hay bitacoras.")
        return []

    for fila in datos:
        id_bit, asunto, destino, salida, entrada, fechaSalida, fechaEntrada = fila
        lista_id.append(id_bit)

        # Formato visual
        asunto_fmt = asunto[0:8] + ("." *
                                    (12 - 8)) if len(asunto) > 8 else asunto
        destino_fmt = destino[0:8] + ("." * (12 - 8)) if len(
            destino) > 8 else destino
        fecha_ent_str = str(
            fechaEntrada) if fechaEntrada is not None else "---"
        fecha_sal_str = str(fechaSalida) if fechaSalida is not None else "---"

        print(
            f"  {id_bit:<4}{asunto_fmt:<15}{destino_fmt:<15}{fecha_sal_str:<15}{fecha_ent_str:<15}"
        )

    print()
    print("-" * 64)
    return lista_id


def ver_bitacora_completa(lista_id):
    titulo = "Buscar bitacora"
    espacios = int((64 - len(titulo)) / 2)
    print("-" * espacios + titulo + "-" * espacios)

    elec = Val.IntListRange("Numero de bitacora: ", lista_id)
    bit = CRUD.leerCompleta(elec)

    print()

    if bit:
        row = bit[0]

        empleados_lista = []
        for fila in bit:
            nombre_empleado = fila[12]
            if nombre_empleado:
                empleados_lista.append(nombre_empleado)

        titulo = f"Informacion bitacora N.{elec}"
        espacios = int((64 - len(titulo)) / 2)
        print("-" * espacios + titulo + "-" * espacios)

        print(f" Asunto:      {row[3]}")
        print(f" Destino:     {row[2]}")
        print("-" * 64)
        print(f" Solicitante: {row[0]}")
        print(f" Autorizado por:    {row[1]}")
        print(f" Vehículo:    {row[14]}, {row[15]} (Matrícula: {row[13]})")

        print("-" * 64)
        print("[Acompañantes]:")
        if empleados_lista:
            for emp in empleados_lista:
                print(f"> {emp}")
        else:
            print("   (Sin acompañantes registrados)")

        print("-" * 64)

        print(" [SALIDA]:")
        print(f" Fecha y hora de salida:  {row[4]} - {row[5]}")
        print(f" Kilometraje: {row[6]} km")
        print(f" Gasolina:    {row[7]} L")

        print("-" * 64)

        print(" [ENTRADA]")
        if row[8] is not None:
            print(f" Fecha y hora de entrada:  {row[8]} - {row[9]}")
            print(f" Kilometraje: {row[10]} km")
            print(f" Gasolina:    {row[11]} L")
        else:
            print(" Fecha y hora de entrada:  Pendiente....")
            print(" Kilometraje: Pendiente....")
            print(" Gasolina:    Pendiente....")

    print("-" * 64)
    input("Presione ENTER para continuar...")


def archivar_bitacora(lista_id):
    titulo = "Archivar bitacora"
    espacios = int((64 - len(titulo)) / 2)
    print("-" * espacios + titulo + "-" * espacios)

    elec = Val.IntListRange("Numero de bitacora: ", lista_id)

    archivar_decision = Val.Decision("Archivar bitacora? (S / N): ")

    if archivar_decision:
        r = CRUD.baja(elec)
        if r == -1:
            print("No se pudo archivar la bitacora.")
        else:
            print("Bitacora archivada.")
    else:
        print("Bitacora no archivada.")

    print("-" * 64)
    input("Presione enter para continuar...")


def lista():
    while True:
        limpiar()

        datos = CRUD.listaGeneral()
        ids_disponibles = mostrar_tabla_resumen(datos)

        print("Acciones:")
        print("1. Ver bitacora completa")
        print("2. Archivar bitacora")
        print("0. Salir")

        opc = Val.IntRange("\nOpcion: ", 0, 2)
        print()

        if opc == 0:
            break

        elif opc == 1:
            if not ids_disponibles:
                input("No hay registros para ver...")
            else:
                ver_bitacora_completa(ids_disponibles)

        elif opc == 2:
            if not ids_disponibles:
                input("No hay registros para archivar...")
            else:
                archivar_bitacora(ids_disponibles)


def registrarSalida():
    limpiar()
    print("\n-- Registrar salida --")

    print("\nSeleccione el Solicitante:")
    empleados = CRUD.listaEmpleados()
    lista_emp_ids = []

    if empleados:
        print(f"{'ID':<4}{'Nombre':<30}")
        print("-" * 34)
        for emp in empleados:
            id_emp, nombre, paterno, materno = emp[0], emp[1], emp[2], emp[3]
            lista_emp_ids.append(id_emp)
            nombre_completo = f"{nombre} {paterno} {materno}"
            print(f"{id_emp:<4}{nombre_completo:<30}")
        print("-" * 34)
    else:
        print("No hay empleados registrados.")
        input("Presione enter para continuar...")
        return

    solicitante = Val.IntListRange("ID Solicitante: ", lista_emp_ids)

    print("\nSeleccione el Autorizador:")
    autorizador = Val.IntListRange("ID Autorizador: ", lista_emp_ids)

    print("\nSeleccione el Vehiculo:")
    vehiculos = CRUD.listaVehiculos()
    lista_veh_ids = []

    if vehiculos:
        print(f"{'ID':<4}{'Vehiculo':<20}{'Matricula':<10}")
        print("-" * 34)
        for i, veh in enumerate(vehiculos, start=1):
            id_veh, marca, modelo, matricula = veh[0], veh[1], veh[2], veh[3]
            lista_veh_ids.append(i)
            desc = f"{marca} {modelo}"
            print(f"{i}, {id_veh:<4}, {desc:<20}, {matricula:<10}")
        print("-" * 34)
    else:
        print("No hay vehiculos disponibles.")
        input("Presione enter para continuar...")
        return

    vehiculo = Val.IntListRange("ID Vehiculo: ", lista_veh_ids)

    acompanantes = []
    while True:
        print()
        agregar = Val.Decision("¿Agregar acompañante? (S/N): ")
        if not agregar:
            break

        id_acomp = Val.IntListRange("ID Acompañante: ", lista_emp_ids)
        if id_acomp not in acompanantes:
            acompanantes.append(id_acomp)
            print("Acompañante agregado.")
        else:
            print("El empleado ya está en la lista.")

    print("\n-- Datos del viaje --")
    asunto = Val.Str("Asunto: ")
    destino = Val.Str("Destino: ")
    kilometraje = Val.Float("Kilometraje actual: ")
    gasolina = Val.Float("Nivel de gasolina: ")

    bitacora = Bitacora()
    #bitacora.set_solicitante(solicitante)
    bitacora.set_autorizador(autorizador)
    bitacora.set_vehiculo(vehiculos[vehiculo - 1][0])
    #bitacora.set_acompanantes(acompanantes)
    bitacora.set_asunto(asunto)
    bitacora.set_destino(destino)
    bitacora.registrar_salida(kilometraje, gasolina)

    lastid = CRUD.crearSalida(bitacora)

    if lastid == -1:
        print("\nNo se pudo registrar la salida.")
    else:
        print(f"\nSalida registrada con exito. Folio: {lastid}")

    input("Presione enter para continuar...")


def registrarEntrada():
    limpiar()
    print("\n-- Registrar entrada --")

    print("Bitacoras pendientes:")
    bitacoras_sin_entrada = CRUD.bitacoraSinEntrada()

    lista_ids = []

    if not bitacoras_sin_entrada:
        print("\nNo hay bitacoras pendientes.")
        input("Presione enter para continuar...")
        return

    print()
    print(f"{'N°':<4}{'Asunto':<15}{'Destino':<15}{'Fecha Salida':<15}")
    print("-" * 50)

    for fila in bitacoras_sin_entrada:
        id_bit, asunto, destino, fecha = fila[0], fila[1], fila[2], fila[3]
        lista_ids.append(id_bit)

        asunto_fmt = asunto[0:12]
        destino_fmt = destino[0:12]
        fecha_fmt = str(fecha)

        print(f"{id_bit:<4}{asunto_fmt:<15}{destino_fmt:<15}{fecha_fmt:<15}")

    print("-" * 50)
    print()

    numControl = Val.IntListRange("Numero de bitacora a cerrar: ", lista_ids)

    datos_previos = CRUD.leerCompleta(numControl)

    if not datos_previos:
        print("Error al recuperar datos.")
        input("Presione enter para continuar...")
        return

    km_salida = float(datos_previos[0][6])
    gas_salida = float(datos_previos[0][7])

    print(f"\nDatos de salida -> KM: {km_salida} | Gasolina: {gas_salida}")

    bitacora = Bitacora()
    bitacora.set_numControl(numControl)

    bitacora.registrar_salida(km_salida, gas_salida)

    kilometraje = Val.KMEntrada("Kilometraje de llegada: ", km_salida)
    gasolina = Val.GasEntrada("Gasolina de llegada: ", gas_salida)

    bitacora.registrar_entrada(kilometraje, gasolina)

    bitacora.calcular_gasolinaConsumida()
    bitacora.calcular_kilometrajeTotal()
    bitacora.calcular_gasolinaRendimiento()

    rowcount = CRUD.crearEntrada(bitacora)

    if rowcount == -1:
        print("\nNo se pudo registrar la entrada.")
    else:
        print("\nEntrada registrada correctamente.")
        print(f"Recorrido: {bitacora.get_kilometrajeTotal()} km")

    input("Presione enter para continuar...")


def eliminar():
    titulo = "Archivar bitacora"
    espacios = int((64 - len(titulo)) / 2)
    print("-" * espacios + titulo + "-" * espacios)

    lista_id = mostrar_tabla_resumen(CRUD.listaGeneral())

    if not lista_id:
        input("No hay registros para archivar...")

    archivar_bitacora(lista_id)


def modificar():
    print("\n-- Modificar destino --")
    bitacoras = CRUD.listaGeneral()
    print()

    numControl = Val.Int("Numero de control: ")

    bitacora = Bitacora()
    bitacora.set_numControl(numControl)

    existe = CRUD.existe(bitacora)
    if len(existe) == 0:
        print(
            f"No existe la bitacora con el numero de control {numControl}.\n")
        return

    nuevoDestino = Val.Str("Nuevo destino: ")

    bitacora.set_destino(nuevoDestino)

    elegir = Val.Decision("Modificar la bitacora? (Si / No): ")
    if elegir:
        rowcount = CRUD.actualizarDestino(bitacora)
        if rowcount == -1:
            print("No se pudo actualizar la bitacora.")
            return

        print("Destino actualizado.")
    else:
        print("Actualizacion cancelada.")
    print()


def completar_objeto(bitacora: Bitacora, tupla):
    bitacora.set_asunto(tupla[0])
    bitacora.set_destino(tupla[1])
    bitacora.set_responsable(tupla[2])
    bitacora.set_autorizador(tupla[3])
    bitacora.set_vehiculo(tupla[4])
    bitacora.registrar_salida(tupla[5], tupla[6])
    bitacora.get_salida().set_fecha(tupla[7])
    bitacora.get_salida().set_hora(tupla[7])

    return bitacora
