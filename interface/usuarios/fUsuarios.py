import mysql
from domain.usuarios.ClaseUsuarios import Usuario, TipoEmpleado, Telefono, Licencia, TipoLicencia
import domain.usuarios.crudUsers as crudUsers
from interface.usuarios.Menu import _Tipos, _Usuarios
from interface.usuarios.Menu import licencias
from interface.usuarios.Menu import datos
from interface.usuarios import val
import random
import bcrypt

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="evm_db"
)


def createUser():
    print("    --REGISTRAR USUARIO--")
    while True:
        nombrePila = input("   Ingrese su(s) nombre(s): ")
        if val.vNombre(nombrePila):
            print(" Nombre válido:", nombrePila)
            break
        else:
            print(
                "   Nombre inválido. Solo se permiten letras y espacios (sin números ni símbolos)."
            )
            print(" Por favor, intente de nuevo.\n")
    while True:
        apdPaterno = input("   Ingrese su primer apellido: ")
        if val.vNombre(apdPaterno):
            print(" Apellido válido:", apdPaterno)
            break
        else:
            print(
                "   Nombre inválido. Solo se permiten letras y espacios (sin números ni símbolos)."
            )
            print(" Por favor, intente de nuevo.\n")
            print()
    desMod3 = input("         Cuenta con segundo apellido?   (s/n): ").strip().lower()
    if desMod3 != 's':
        apdMaterno = None
        nombre2 = nombrePila + " " + apdPaterno
        print("     Nombre: " + nombre2)
        telefono = val.valTelefono()
        _Tipos()
        opcEmpleado = val.vInt("  Seleccion una opcion:  ")
        match opcEmpleado:
            case 1:
                codigo = str(random.randint(10000, 99999))
                descripcion = "Administrador"
                print("Tipo de empleado: " + descripcion)
                while True:
                    password = input("Cree una contraseña: ")
                    if val.validate_password(password):
                        password = password.encode('utf-8')
                        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                        print("     Contraseña Valida")
                        break
                    else:
                        print(" Contraseña Invalida. Intente de nuevo")
                        print(" La contraseña debe cumplir con los siguientes requisitos para ser válida:")
                        print(" 1. Tener al menos 8 caracteres.")
                        print(" 2. Incluir al menos una letra mayúscula (A-Z).")
                        print(" 3. Incluir al menos una letra minúscula (a-z).")
                        print(" 4. Incluir al menos un número (0-9).")
                email = val.vEmail("Ingrese su Correo Electronico: ")
                newTipo = TipoEmpleado(codigo, descripcion)
                newUser = Usuario(None, nombrePila, apdPaterno, apdMaterno, newTipo.get_codigo(), 1, hashed, email)
                newTel = Telefono(None, telefono ,None)
                crudUsers.Create2(newUser, newTipo, newTel)
                return
            case 2:
                codigo = str(random.randint(10000, 99999))
                descripcion = "Chofer"
                print("Tipo de empleado: " + descripcion)
                licencias()
                opclicencia = val._IntRange("   Ingrese una opcion de Licencia: ", 1, 5)
                match opclicencia:
                    case 1:
                        codigoLic = "A"
                        print("    Eligio la opcion de licencia " + codigoLic + ".")
                        descripcionLic = "Automovilista"
                        desMod5 = input("         Es la opcion de licencia correcta?   (s/n): ").strip().lower()
                        if desMod5 != 's':
                            licencias()
                            opclicencia = val._IntRange("   Ingrese una la opcion de Licencia correcta: ", 1, 5)
                            match opclicencia:
                                case 1:
                                    codigoLic = "A"
                                    print("    Eligio la opcion de licencia " + codigoLic + ".")
                                    descripcionLic = "Automovilista"
                                case 2:
                                    codigoLic = "B"
                                    print("    Eligio la opcion de licencia " + codigoLic + ".")
                                    descripcionLic = "Taxis y Aplicaciones"
                                case 3:
                                    codigoLic = "C"
                                    print("    Eligio la opcion de licencia " + codigoLic + ".")
                                    descripcionLic = "Transporte público"
                                case 4:
                                    codigoLic = "D"
                                    print("    Eligio la opcion de licencia " + codigoLic + ".")
                                    descripcionLic = "Transporte de carga"
                                case 5:
                                    codigoLic = "E"
                                    print("    Eligio la opcion de licencia " + codigoLic + ".")
                                    descripcionLic = "Servicios especializados y carga"
                                    print()
                                    while True:
                                        numeroLicencia = input("   Ingrese su numero de licencia: ")
                                        if val.valLicencia(numeroLicencia):
                                            print("  Número de licencia válido.")
                                            break
                                        else:
                                            print(
                                                "    Licencia inválida. Debe tener el formato: BC + 9 dígitos. Ejemplo: BC060759162"
                                            )
                                    exp = val.val_exp()
                                    ven = val.val_ven(exp)
                                    while True:
                                        password = input("Cree una contraseña: ")
                                        if val.validate_password(password):
                                            password = password.encode('utf-8')
                                            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                                            print(" Contraseña Valida")
                                            break
                                        else:
                                            print(" Contraseña Invalida. Intente de nuevo")
                                            print(" La contraseña debe cumplir con los siguientes requisitos para ser válida:")
                                            print(" 1. Tener al menos 8 caracteres.")
                                            print(" 2. Incluir al menos una letra mayúscula (A-Z).")
                                            print(" 3. Incluir al menos una letra minúscula (a-z).")
                                            print(" 4. Incluir al menos un número (0-9).")
                                    email = val.vEmail("Ingrese su Correo Electronico: ")
                                    newTipo = TipoEmpleado(codigo, descripcion)
                                    newUser = Usuario(None, nombrePila, apdPaterno, apdMaterno, newTipo.get_codigo(), 1, hashed, email)
                                    newTel = Telefono(None, telefono ,None)
                                    newTLic = TipoLicencia(None, codigoLic, descripcionLic)
                                    newLic = Licencia(numeroLicencia, exp, ven, None, newTLic.get_codigoLic())
                                    crudUsers.Create(newUser, newTipo, newTel, newTLic, newLic)
                                    return
                    case 2:
                        codigoLic = "B"
                        print("    Eligio la opcion de licencia " + codigoLic + ".")
                        descripcionLic = "Taxis y Aplicaciones"
                    case 3:
                        codigoLic = "C"
                        print("    Eligio la opcion de licencia " + codigoLic + ".")
                        descripcionLic = "Transporte público"
                    case 4:
                        codigoLic = "D"
                        print("    Eligio la opcion de licencia " + codigoLic + ".")
                        descripcionLic = "Transporte de carga"
                    case 5:
                        codigoLic = "E"
                        print("    Eligio la opcion de licencia " + codigoLic + ".")
                        descripcionLic = "Servicios especializados y carga"
                print()
                while True:
                    numeroLicencia = input("   Ingrese su numero de licencia: ")
                    if val.valLicencia(numeroLicencia):
                        print("  Número de licencia válido.")
                        break
                    else:
                        print(
                            "    Licencia inválida. Debe tener el formato: BC + 9 dígitos. Ejemplo: BC060759162"
                        )
                exp = val.val_exp()
                ven = val.val_ven(exp)
                while True:
                    password = input("Cree una contraseña: ")
                    if val.validate_password(password):
                        password = password.encode('utf-8')
                        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                        print(" Contraseña Valida")
                        break
                    else:
                        print(" Contraseña Invalida. Intente de nuevo")
                        print(" La contraseña debe cumplir con los siguientes requisitos para ser válida:")
                        print(" 1. Tener al menos 8 caracteres.")
                        print(" 2. Incluir al menos una letra mayúscula (A-Z).")
                        print(" 3. Incluir al menos una letra minúscula (a-z).")
                        print(" 4. Incluir al menos un número (0-9).")
                email = val.vEmail("Ingrese su Correo Electronico: ")
                newTipo = TipoEmpleado(codigo, descripcion)
                newUser = Usuario(None, nombrePila, apdPaterno, apdMaterno, newTipo.get_codigo(), 1, hashed, email)
                newTel = Telefono(None, telefono ,None)
                newTLic = TipoLicencia(None, codigoLic, descripcionLic)
                newLic = Licencia(numeroLicencia, exp, ven, None, newTLic.get_codigoLic())
                crudUsers.Create(newUser, newTipo, newTel, newTLic, newLic)
                return
            case 3:
                codigo = str(random.randint(10000, 99999))
                descripcion = "Vigilante"
                print("Tipo de empleado: " + descripcion)
                while True:
                    password = input("  Cree una contraseña: ")
                    if val.validate_password(password):
                        password = password.encode('utf-8')
                        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                        print(" Contraseña Valida")
                        break
                    else:
                        print(" Contraseña Invalida. Intente de nuevo")
                        print(" La contraseña debe cumplir con los siguientes requisitos para ser válida:")
                        print(" 1. Tener al menos 8 caracteres.")
                        print(" 2. Incluir al menos una letra mayúscula (A-Z).")
                        print(" 3. Incluir al menos una letra minúscula (a-z).")
                        print(" 4. Incluir al menos un número (0-9).")
                email = val.vEmail("Ingrese su Correo Electronico: ")
                newTipo = TipoEmpleado(codigo, descripcion)
                newUser = Usuario(None, nombrePila, apdPaterno, apdMaterno, newTipo.get_codigo(), 1, hashed, email)
                newTel = Telefono(None, telefono ,None)
                crudUsers.Create2(newUser, newTipo, newTel)
                return
            case 4:
                codigo = str(random.randint(10000, 99999))
                descripcion = "Empleado-User"
                print("Tipo de empleado: " + descripcion)
                while True:
                    password = input("  Cree una contraseña: ")
                    if val.validate_password(password):
                        password = password.encode('utf-8')
                        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                        print(" Contraseña Valida")
                        break
                    else:
                        print(" Contraseña Invalida. Intente de nuevo")
                        print("La contraseña debe cumplir con los siguientes requisitos para ser válida:")
                        print(" 1. Tener al menos 8 caracteres.")
                        print(" 2. Incluir al menos una letra mayúscula (A-Z).")
                        print(" 3. Incluir al menos una letra minúscula (a-z).")
                        print(" 4. Incluir al menos un número (0-9).")
                email = val.vEmail("Ingrese su Correo Electronico: ")
                newTipo = TipoEmpleado(codigo, descripcion)
                newUser = Usuario(None, nombrePila, apdPaterno, apdMaterno, newTipo.get_codigo(), 1, hashed, email)
                newTel = Telefono(None, telefono ,None)
                crudUsers.Create2(newUser, newTipo, newTel)
                return
    while True:
        apdMaterno = input("  Ingrese su segundo apellido: ")
        if val.vNombre(apdMaterno):
            print(" Apellido válido:", apdMaterno)
            break
        else:
            print(
                "   Nombre inválido. Solo se permiten letras y espacios (sin números ni símbolos)."
            )
            print(" Por favor, intente de nuevo.\n")
    nombre = nombrePila + " " + apdPaterno + " " + apdMaterno
    print("         Nombre: " + nombre)
    print()
    telefono = val.valTelefono()
    _Tipos()
    opcEmpleado = val.vInt("  Seleccion una opcion:  ")
    match opcEmpleado:
        case 1:
            codigo = str(random.randint(10000, 99999))
            descripcion = "     Administrador"
            print("Tipo de empleado: " + descripcion)
            while True:
                password = input("Cree una contraseña: ")
                if val.validate_password(password):
                    password = password.encode('utf-8')
                    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                    print("     Contraseña Valida")
                    break
                else:
                    print(" Contraseña Invalida. Intente de nuevo")
                    print(" La contraseña debe cumplir con los siguientes requisitos para ser válida:")
                    print(" 1. Tener al menos 8 caracteres.")
                    print(" 2. Incluir al menos una letra mayúscula (A-Z).")
                    print(" 3. Incluir al menos una letra minúscula (a-z).")
                    print(" 4. Incluir al menos un número (0-9).")
            email = val.vEmail("Ingrese su Correo Electronico: ")
            newTipo = TipoEmpleado(codigo, descripcion)
            newUser = Usuario(None, nombrePila, apdPaterno, apdMaterno, newTipo.get_codigo(), 1, hashed, email)
            newTel = Telefono(None, telefono ,None)
            crudUsers.Create2(newUser, newTipo, newTel)
        case 2:
            codigo = str(random.randint(10000, 99999))
            descripcion = "Chofer"
            print("Tipo de empleado: " + descripcion)
            licencias()
            opclicencia = val._IntRange("   Ingrese una opcion de Licencia: ", 1, 5)
            match opclicencia:
                case 1:
                    codigoLic = "A"
                    print("    Eligio la opcion de licencia " + codigoLic + ".")
                    descripcionLic = "Automovilista"
                case 2:
                    codigoLic = "B"
                    print("    Eligio la opcion de licencia " + codigoLic + ".")
                    descripcionLic = "Taxis y Aplicaciones"
                case 3:
                    codigoLic = "C"
                    print("    Eligio la opcion de licencia " + codigoLic + ".")
                    descripcionLic = "Transporte público"
                case 4:
                    codigoLic = "D"
                    print("    Eligio la opcion de licencia " + codigoLic + ".")
                    descripcionLic = "Transporte de carga"
                case 5:
                    codigoLic = "E"
                    print("    Eligio la opcion de licencia " + codigoLic + ".")
                    descripcionLic = "Servicios especializados  y carga"
            print()
            while True:
                numeroLicencia = input("   Ingrese su numero de licencia: ")
                if val.valLicencia(numeroLicencia):
                    print("  Número de licencia válido.")
                    break
                else:
                    print(
                        "    Licencia inválida. Debe tener el formato: BC + 9 dígitos. Ejemplo: BC060759162"
                    )
            exp = val.val_exp()
            ven = val.val_ven(exp)
            while True:
                password = input("Cree una contraseña: ")
                if val.validate_password(password):
                    password = password.encode('utf-8')
                    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                    print(" Contraseña Valida")
                    break
                else:
                    print(" Contraseña Invalida. Intente de nuevo")
                    print(" La contraseña debe cumplir con los siguientes requisitos para ser válida:")
                    print(" 1. Tener al menos 8 caracteres.")
                    print(" 2. Incluir al menos una letra mayúscula (A-Z).")
                    print(" 3. Incluir al menos una letra minúscula (a-z).")
                    print(" 4. Incluir al menos un número (0-9).")
            email = val.vEmail("Ingrese su Correo Electronico: ")
            newTipo = TipoEmpleado(codigo, descripcion)
            newUser = Usuario(None, nombrePila, apdPaterno, apdMaterno, newTipo.get_codigo(), 1, hashed, email)
            newTel = Telefono(None, telefono ,None)
            newTLic = TipoLicencia(None, codigoLic, descripcionLic)
            newLic = Licencia(numeroLicencia, exp, ven, None, newTLic.get_codigoLic())
            crudUsers.Create(newUser, newTipo, newTel, newTLic, newLic)
        case 3:
            codigo = str(random.randint(10000, 99999))
            descripcion = "Vigilante"
            print("Tipo de empleado: " + descripcion)
            while True:
                password = input("  Cree una contraseña: ")
                if val.validate_password(password):
                    password = password.encode('utf-8')
                    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                    print(" Contraseña Valida")
                    break
                else:
                    print(" Contraseña Invalida. Intente de nuevo")
                    print(" La contraseña debe cumplir con los siguientes requisitos para ser válida:")
                    print(" 1. Tener al menos 8 caracteres.")
                    print(" 2. Incluir al menos una letra mayúscula (A-Z).")
                    print(" 3. Incluir al menos una letra minúscula (a-z).")
                    print(" 4. Incluir al menos un número (0-9).")
            email = val.vEmail("Ingrese su Correo Electronico: ")
            newTipo = TipoEmpleado(codigo, descripcion)
            newUser = Usuario(None, nombrePila, apdPaterno, apdMaterno, newTipo.get_codigo(), 1, hashed, email)
            newTel = Telefono(None, telefono ,None)
            crudUsers.Create2(newUser, newTipo, newTel)
        case 4:
            codigo = str(random.randint(10000, 99999))
            descripcion = "Empleado-User"
            print("Tipo de empleado: " + descripcion)
            while True:
                password = input("  Cree una contraseña: ")
                if val.validate_password(password):
                    password = password.encode('utf-8')
                    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                    print(" Contraseña Valida")
                    break
                else:
                    print(" Contraseña Invalida. Intente de nuevo")
                    print("La contraseña debe cumplir con los siguientes requisitos para ser válida:")
                    print(" 1. Tener al menos 8 caracteres.")
                    print(" 2. Incluir al menos una letra mayúscula (A-Z).")
                    print(" 3. Incluir al menos una letra minúscula (a-z).")
                    print(" 4. Incluir al menos un número (0-9).")
            email = val.vEmail("Ingrese su Correo Electronico: ")
            newTipo = TipoEmpleado(codigo, descripcion)
            newUser = Usuario(None, nombrePila, apdPaterno, apdMaterno, newTipo.get_codigo(), 1, hashed, email)
            newTel = Telefono(None, telefono ,None)
            crudUsers.Create2(newUser, newTipo, newTel)


def selectChofer():
    crudUsers.mostrar_choferes(conexion)
    desMod = input(" Desea modificar algun chofer? (s/n): ").strip().lower()
    if desMod == "s":
        updateUser()
    else:
        print("   Saliendo del Menu de Choferes...")

def empleados_contactos():
    crudUsers.empleados_contactos(conexion)
    desMod2 = input(" Desea modificar algun contacto? (s/n): ").strip().lower()
    if desMod2 == "s":
        updateUser()
    else:
        print("   Saliendo del Menu de Contactos...")

def updateUser():
    print("   Actualizar Usuario: ")
    # buscar3 ya pide el número e imprime los datos
    oldUser = crudUsers.buscar3() 
    # preparar objetos relacionados
    oldTel = Telefono("", "", oldUser.get_numEmpleado())
    datos()
    opcMod = int(input("   Seleccione el dato del usuario que desea modificar: "))
    match opcMod:
        case 1:
            nombrePila = input("Ingrese su nombre de pila: ")
            apdPaterno = input("Ingrese su apellido paterno: ")
            apdMaterno = input("Ingrese su apellido materno: ")
            val.vNombre(nombrePila)
            val.vNombre(apdPaterno)
            val.vNombre(apdMaterno)
            oldUser.set_nombrePila(nombrePila)
            oldUser.set_apdPaterno(apdPaterno)
            oldUser.set_apdMaterno(apdMaterno)
            crudUsers.UpdateNombre(oldUser)
        case 2:
            telefono = val.valTelefono()
            oldTel.set_numTelefono(telefono)
            crudUsers.UpdateTelefono(oldTel)
        case 3:
            oldTipo = crudUsers.buscarTipoEmpleado()
            _Tipos()

            opcEmpleado = val.vInt("Seleccion el nuevo tipo de empleado: ")

            match opcEmpleado:
                case 1:
                    descripcion = "Administrador"
                case 2:
                    crudUsers.registrarLicencia(oldUser.get_numEmpleado())
                    descripcion = "Chofer"
                case 3:
                    descripcion = "Vigilante"
                case 4:
                    descripcion = "Empleado-User"

            oldTipo.set_descripcion(descripcion)
            crudUsers.UpdateTipoEmpleado(oldTipo)
        case 4:
            email = val.vEmail("Ingrese su Correo Electronico: ")
            oldUser.set_email(email)
            crudUsers.UpdateEmail(oldUser)
        case 5:
            _Usuarios()

def deleteUser():
    print("\n   Inhabilitar Empleado \n")

    numEmpleado = val.vInt("   Ingrese el número de empleado que desea inhabilitar: ")

    oldUser = Usuario(numEmpleado, "", "", "", "", 0, "", "")

    existe = crudUsers.Deactive(oldUser)

    if not existe:
        print("   ERROR: El empleado no existe.\n")
        return False

    confirmar = input("\n   ¿Seguro que desea inhabilitar este empleado? (s/n): ").strip().lower()

    if confirmar != "s":
        print("   Operación cancelada. No se realizaron cambios.\n")
        return False
    
    crudUsers.Delete(oldUser)



