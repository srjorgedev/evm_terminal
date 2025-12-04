import domain.vehiculos.crudVehiculo as crudVehiculo
from domain.vehiculos.ClaseVehiculo import Vehiculo
import interface.vehiculos.val as val
from datetime import datetime

def listarVehiculos():
    print("- - - Listado de Vehiculos - - -")
    crudVehiculo.listarVehiculos()
    
def tipolicencia():
    print("- - - Tiposs de licencia de Vehiculos - - -")
    crudVehiculo.tipolicencia()
    
def SolicitarDatos():

    print("\n{:^40}".format("Marcas y Modelos Disponibles"))
    print("+" + "-"*63 + "+")
    
    crudVehiculo.mostarmarcaymodelo()

    print("+" + "-"*63 + "+\n")
    
    print("\n{:^40}".format("Tipos de licencia"))
    print("+" + "-"*63 + "+")
    crudVehiculo.tipli()
    print("+" + "-"*63 + "+\n")
    
    print("\n" + "+" + "-"*63 + "+")
    print("|{:^63}|".format("AGREGAR VEHÍCULO"))
    print("+" + "-"*63 + "+")

    numSerie = val.vNumSerie("Ingresa el numero de serie del vehiculo: ")
    matricula = val.vMatricula("Ingresa la matricula del vehiculo: ") 
    marca = val.vDatos("Ingresa el codigo de la marca del vehiculo: ") 
    modelo = val.vDatos("Ingresa el codigo del modelo del vehiculo: ") 
    fecha_adquision = val.vFecha()
    tipo_licencia = crudVehiculo.RegistroLicencias()
    proposito =val.vDatos("Utilidad del vehiculo: ")
    nuevoVehiculo = Vehiculo ("", numSerie, matricula, marca, modelo, fecha_adquision,1,  tipo_licencia, proposito)
    crudVehiculo.agregarVehiculo(nuevoVehiculo)
    
def borrarVehiculo():
    print("\n{:^40}".format("Informacion del vehiculo"))
    print("+" + "-"*63 + "+")
    crudVehiculo.numsemoma()
    print("+" + "-"*63 + "+\n")
    print(" - - - Dar de Baja Vehiculo - - - ")
    print("Esta acción marcará el vehículo como NO disponible (disponibilidad = 2).")

    num_serie = input("Ingresa el número de serie del vehiculo a dar de baja: ")

    existeVehiculo = Vehiculo("", num_serie, "", "", "", "", 2, "", "")

    crudVehiculo.borrarVehiculo(existeVehiculo)


            
def modificarMatricula():
    print("\n{:^40}".format("Numero de serie y matricula"))
    print("+" + "-"*63 + "+")
    crudVehiculo.nummat()
    print("+" + "-"*63 + "+\n")
    
    print(" - - - Modificar Matricula del Vehiculo - - - ")
    
    num_serie = input("Ingresa el número de serie del vehículo a modificar: ")
    nueva_matricula = val.vMatricula("Ingresa la nueva matrícula: ")
    existeVehiculo = Vehiculo(
        "",             
        num_serie,       
        nueva_matricula, 
        "", "", "", "", "", ""
    )
    crudVehiculo.modificarVehiculo(existeVehiculo)



    