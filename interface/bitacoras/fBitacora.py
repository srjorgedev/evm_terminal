import domain.bitacoras.crudBitacora as CRUD
from domain.bitacoras.Bitacora import Bitacora
import interface.bitacoras.Val as Val
from utils.limpiar import limpiar

def lista():
    while True:
        limpiar()

        titulo = "Listado de bitacoras"
        espacios = int((64 - len(titulo)) / 2)
        print("-"*espacios + titulo + "-"*espacios)
        print()

        print(f"{'  N°':<6}{'Asunto':<15}{'Destino':<15}{'Fecha Salida':<15}{'Fecha Entrada':<15}\n")

        datos = CRUD.listaGeneral()
        if datos == []:
            print("No hay bitacoras.")

        lista_id = []
        if len(datos) > 0:
            for fila in datos:
                id, asunto, destino, salida, entrada, fechaSalida, fechaEntrada = fila
                lista_id.append(id)

                asunto = asunto[0:8] + ("." * (12 - 8))
                destino = destino = destino[0:8] + ("." * (12 - 8))
                fechaEntrada = fechaEntrada if fechaEntrada is not None  else "---"
                fechaSalida = fechaSalida if fechaSalida is not None else "---"

                print(f"  {id:<4}{asunto:<15}{destino:<15}{fechaSalida:<15}{fechaEntrada:<15}")

        print()
        print("-"*64)

        opc = None

        if opc == None:
            print("Acciones:")
            print("1. Ver bitacora completa")
            print("2. Archivar bitacora")
            print("0. Salir")

            opc = Val.IntRange("Opcion: ", 0, 2)

            if opc == 0: break;
        if opc == 1:
            elec = Val.IntListRange("Numero de bitacora: ", lista_id)
            bit = CRUD.leerCompleta(elec)
            print("-"*64)
            
            print("Solicitante: ", bit[0][0])
            print("Autorizado por: ", bit[0][1])
            
            print("-"*64)
            print("Acciones:")
            print("1. Archivar")
            print("2. Modificar")
            print("0. Salir")

            opc = Val.IntRange("Opcion: ", 0, 2)
        if opc == 2:
            pass            
            
    

def registrarSalida():
    print("\n-- Registrar salida --")

    asunto = Val.Str("Asunto: ")
    destino = Val.Str("Destino: ")
    kilometraje = Val.Float("Kilometraje: ")
    gasolina = Val.Float("Gasolina: ")

    bitacora = Bitacora()
    bitacora.set_asunto(asunto)
    bitacora.set_destino(destino)
    bitacora.registrar_salida(kilometraje, gasolina)

    lastid = CRUD.crearSalida(bitacora)

    if (lastid == -1):
        print("No se pudo registrar.")
        return
    else:
        print("Bitacora registrada.")
    print()

    bitacora.set_numControl(lastid)

    print(bitacora)


def registrarEntrada():
    print("\n-- Registrar entrada --")

    print("Bitacoras sin entrada:")
    bitacoras_sin_entrada = CRUD.bitacoraSinEntrada()
    print()

    if bitacoras_sin_entrada == 0:
        print("No hay bitacoras.")
        return

    numControl = Val.Int("Numero de control: ")

    bitacora = Bitacora()
    bitacora.set_numControl(numControl)

    existe = CRUD.existe(bitacora)
    if len(existe) == 0:
        print(
            f"No existe la bitacora con el numero de control {numControl}.\n")
        return

    bitacora = completar_objeto(bitacora, existe[0])

    kilometraje = Val.KMEntrada("Kilometraje: ",
                                bitacora.get_salida().get_kilometraje())
    gasolina = Val.GasEntrada("Gasolina: ",
                              bitacora.get_salida().get_gasolina())

    bitacora.registrar_entrada(kilometraje, gasolina)
    bitacora.calcular_gasolinaConsumida()
    bitacora.calcular_kilometrajeTotal()
    bitacora.calcular_gasolinaRendimiento()

    rowcount = CRUD.crearEntrada(bitacora)
    if rowcount == -1:
        print("No se pudo registrar la entrada.")
        return

    print(bitacora)


def eliminar():
    print("\n-- Eliminar --")
    print("Bitacoras:")
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

    elegir = Val.Decision("Borrar la bitacora? (Si / No): ")
    if elegir:
        rowcount = CRUD.baja(bitacora)
        if rowcount == -1:
            print("No se pudo eliminar la bitacora.")
            return

        print("Bitacora eliminada.")
    else:
        print("Eliminacion cancelada.")
    print()


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
