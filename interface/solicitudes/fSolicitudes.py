from domain.solicitudes import crudSolicitudes 
from domain.solicitudes.ClaseSolicitudes import Solicitud
from interface.solicitudes import valSolicitudes as val
from db.connV import conn


def listarSolicitudes():
    print("- - - Listado de Solicitudes - - -")
    crudSolicitudes.listarSolicitudes()
    
def VerEstado():
    print("- - - Listado de Solicitudes - - -")
    crudSolicitudes.listarEstado()

    
    
def SolicitarDatos():
    print(" - - - Agregar Solicitud - - - ")

    miConn = conn()  

    asunto = val.vAsunto("Asunto: ")
    hora = val.vHora("Hora solicitada (HH:MM): ")
    fecha = val.vFecha("Fecha solicitada (AAAA-MM-DD): ")
    vehiculo = val.vVehiculo(miConn, "Número de serie del vehículo: ")
    estado = val.vEstado(miConn, "ID de estado: ")        
    solicitante = val.vEmpleado(miConn, "ID del solicitante: ") 
    autorizador = val.vEmpleado(miConn, "ID del autorizador: ")  

    nueva = Solicitud("", asunto, hora, fecha,
                      vehiculo, estado, solicitante, autorizador)

    crudSolicitudes.agregarSolicitud(nueva)

    
def modificarEstadoSolicitud():
    print(" - - - Modificar estado de la solicitud - - - ")
    print("ADVERTENCIA: Esta acción es irreversible y puede afectar otros datos")
    numero = input("Ingresa el ID de la solicitud a modificar: ")
    nuevo_estado = val.vEstado("Ingresa el nuevo estado (Pendiente / Aprobada / Rechazada): ")
    existeSolicitud = Solicitud(numero, "", "", "", "", nuevo_estado, "", "")
    crudSolicitudes.estadoSolicitud(existeSolicitud)
    
            
def modificarAsuntoSolicitud():
    print(" - - - Modificar asunto de la solicitud - - - ")
    id_solicitud = input("Ingresa el ID de la solicitud a modificar: ")
    nuevo_asunto = val.vAsunto("Ingresa el nuevo asunto: ")
    existeSolicitud = Solicitud(id_solicitud, nuevo_asunto, "", "", "", "", "", "")
    crudSolicitudes.modificarSolicitud(existeSolicitud)