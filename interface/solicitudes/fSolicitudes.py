from domain.solicitudes import crudSolicitudes
from interface.solicitudes import valSolicitudes as val
from db.connV import conn
from domain.solicitudes.ClaseSolicitudes import Solicitud

def listarSolicitudes():
    crudSolicitudes.listarSolicitudes()

def VerEstado():
    crudSolicitudes.listarEstado()

def SolicitarDatos():
    print("\nInformación del Vehículo")
    crudSolicitudes.numsemoma()

    print("\nInformación del Empleado")
    crudSolicitudes.empleados()

    miConn = conn()
    print("Crear una solicitud de vehículo:")
    asunto = val.vAsunto("Asunto: ")
    hora = val.vHora("Hora solicitada (HH:MM): ")
    fecha = val.vFecha("Fecha solicitada (AAAA-MM-DD): ")
    vehiculo = val.vVehiculo(miConn, "Número de serie del vehículo: ")
    solicitante = val.vEmpleado(miConn, "ID del solicitante: ")

    nueva = Solicitud("", asunto, hora, fecha, vehiculo, 1, solicitante, 3)

    crudSolicitudes.agregarSolicitud(nueva)


def modificarEstadoSolicitud():
    crudSolicitudes.listarSolicitudes()
    crudSolicitudes.edosoli()
    print(" - - - Modificar estado de la solicitud - - - ")
    print("ADVERTENCIA: Esta acción es irreversible y puede afectar otros datos")
    

    numero = input("Ingresa el ID de la solicitud a modificar: ")

    miConn = conn()
    nuevo_estado = val.vEstado(miConn, "Nuevo estado (1/2/3): ")

    existeSolicitud = Solicitud(
        numero,
        "", "", "", "", 
        nuevo_estado, 
        "", ""
    )

    crudSolicitudes.modificarEstado(existeSolicitud)




def modificarAsuntoSolicitud():
    print(" - - - Modificar asunto de la solicitud - - - ")
    crudSolicitudes.listarSolicitudes()
    id_solicitud = input("ID de solicitud: ")
    nuevo_asunto = val.vAsunto("Nuevo asunto: ")
    crudSolicitudes.modificarAsunto(id_solicitud, nuevo_asunto)


def eliminarSolicitud():
    print(" - - - Eliminar solicitud - - - ")
    crudSolicitudes.listarSolicitudes()
    numero = input("Número de solicitud a eliminar: ")
    crudSolicitudes.eliminarSolicitud(numero)
