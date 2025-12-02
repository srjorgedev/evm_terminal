##import sys
##sys.dont_write_bytecode = True estos dos solo los puse para que no me genere el pycache
import interface.usuarios.Menu as _Usuarios
from interface.usuarios import fUsuarios

import interface.bitacoras.Menu as _Bitacoras
import interface.bitacoras.fBitacora as Fbitacoras

import interface.vehiculos.Menu as _Vehiculos
#from controllers import fVehiculo

from db.conn import conn
miConn = conn()
#from interface.observacionymantenimiento import menu
from interface.observacionymantenimiento import fMantenimiento
from interface.observacionymantenimiento import fObservacion
#from interface.observacionymantenimiento import val

import interface.Menu as Menu
import interface.Val as Val

from utils.limpiar import limpiar

limpiar()

opc1 = 100
while True and opc1 != 9:
    opc1 = Val._SelectMenu("    Seleccione una opción: ", Menu.pricipal, 1, 9)

    match opc1:
        case 1:
            opc11 = 100

            while opc11 != 6:
                opc11 = Val._SelectMenu("    Opcion: ", _Bitacoras.principal, 1, 6)
                match opc11:
                    case 1:
                        Fbitacoras.lista()
                    case 2:
                        Fbitacoras.registrarSalida()
                    case 3:
                        Fbitacoras.registrarEntrada()
                    case 4:
                        Fbitacoras.modificar()
                    case 5:
                        Fbitacoras.eliminar()
                    case 6:
                        print("   Saliendo...")
                        break

    #    case 2:
    #        opc12 = 100
#
 #           while opc12 != 5:
  #              opc12 = Val._SelectMenu("    Opcion: ", _Vehiculos.menuVehiculos,
   #                                     1, 6)
    #            match opc12:
     #               case 1:
      #                  fVehiculo.listarVehiculos()
       #             case 2:
        #                fVehiculo.SolicitarDatos()
         #           case 3:
          #              fVehiculo.modificarMatricula()
          #          case 4:
          #              fVehiculo.borrarVehiculo()
          #          case 5:
          #              print("   Saliendo...")
          #              break


        case 3:
            opc13 = 100

            while opc13 != 6:
                opc13 = Val._SelectMenu("    Seleccione una opción: ", _Usuarios._Usuarios, 1, 6)
                match opc13:
                    case 1:
                        fUsuarios.createUser()
                    case 2:
                        fUsuarios.selectChofer()
                    case 3:
                        fUsuarios.empleados_contactos()
                    case 4:
                        fUsuarios.updateUser()
                    case 5:
                        fUsuarios.deleteUser()
                    case 6:
                        print("   Saliendo del Menu de Usuarios...")

        case 4: # MANTENIMIENTO
    # Llama al submenú completo de mantenimiento
            fMantenimiento.menuMantenimientos()
        case 5: # OBSERVACIONES
    # Llama al submenú completo de observaciones
            fObservacion.menuObservaciones()
        
        case 9:
            print("   Saliendo...")
            break
