from db.connU import conn
from domain.usuarios.ClaseUsuarios import Usuario, TipoEmpleado, Telefono, Licencia, TipoLicencia
from mysql.connector import Error, IntegrityError
from interface.usuarios import val
from interface.usuarios.Menu import datos, licencias
import mysql.connector

#Create
#Read
#Update
#Delete
#Buscar
'''
#def __init__(self, numEmpleado, nombre, tipo_empleado, activo):
def __init__(self, codigo, descripcion):
)
'''

'''
#Create insert
def Create(newUser, newTipo):
    objUser = Usuario(0, "", "", 0, "", "")
    objUser = newUser
    objTipo = TipoEmpleado("", "")
    objTipo = newTipo
    miConn = conn()
    aux2 = "INSERT INTO tipo_empleado(codigo, descripcion) VALUES ('{0}','{1}')"
    comando2 = aux2.format(objTipo.get_codigo(), objTipo.get_descripcion())
    miConn.register2(comando2)
    aux = "INSERT INTO empleado(nombre, tipo_empleado, activo, password_hash, email) VALUES ('{0}','{1}','{2}','{3}','{4}')"
    comando = aux.format(objUser.get_nombre(), objTipo.get_codigo(), objUser.get_activo(), objUser.get_password(), objUser.get_email())
    miConn.register(comando)
'''

def Create(newUser, newTipo, newTel, newTLic, newLic):
    miConn = conn()

    cursor = miConn.conexion.cursor()

    # INSERT tipo_empleado
    comando2 = """
    INSERT INTO tipo_empleado (codigo, descripcion)
    VALUES (%s, %s)
    """
    cursor.execute(comando2, (
        newTipo.get_codigo(),
        newTipo.get_descripcion()
    ))

    # INSERT empleado
    comando = """
    INSERT INTO empleado (nombrePila, apdPaterno, apdMaterno, tipo_empleado, activo, password_hash, email)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(comando, (
        newUser.get_nombrePila(),
        newUser.get_apdPaterno(),
        newUser.get_apdMaterno(),
        newTipo.get_codigo(),
        newUser.get_activo(),
        newUser.get_password(),
        newUser.get_email()
    ))

    idEmpleado = cursor.lastrowid
    print("Numero de Empleado:", idEmpleado)
    newTel.set_empleado(idEmpleado)
    newLic.set_empleado(idEmpleado)
    
    #INSERT telefono
    comando3 = """
    INSERT INTO telefono (numTelefono, empleado)
    VALUES (%s, %s)
    """
    cursor.execute(comando3, (
        newTel.get_numTelefono(),
        newTel.get_empleado()
    ))
    
    idTelefono = cursor.lastrowid
    
    comando4 = """
    INSERT INTO tipo_licencia (codigo, descripcion)
    VALUES (%s, %s)
    """
    cursor.execute(comando4, (
        newTLic.get_codigoLic(),
        newTLic.get_descripcionLic()
    ))
    
    idTipoLic = cursor.lastrowid
    newLic.set_tipoLicencia(idTipoLic)
    comando5 = """
    INSERT INTO licencia (numero, fechaExpedicion, fechaVencimiento, empleado, tipo_licencia)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(comando5, (
        newLic.get_num(),
        newLic.get_fechaExpedicion(),
        newLic.get_fechaVencimiento(),
        newLic.get_empleado(),
        newLic.get_tipoLicencia()
    ))

    miConn.conexion.commit()
    print("     ID Telefono", idTelefono)
    print("     Empleado Resgistrado con Exito")


def Create2(newUser, newTipo, newTel):
    miConn = conn()

    cursor = miConn.conexion.cursor()

    # INSERT tipo_empleado
    comando2 = """
    INSERT INTO tipo_empleado (codigo, descripcion)
    VALUES (%s, %s)
    """
    cursor.execute(comando2, (
        newTipo.get_codigo(),
        newTipo.get_descripcion()
    ))

   # INSERT empleado
    comando = """
    INSERT INTO empleado (nombrePila, apdPaterno, apdMaterno, tipo_empleado, activo, password_hash, email)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(comando, (
        newUser.get_nombrePila(),
        newUser.get_apdPaterno(),
        newUser.get_apdMaterno(),
        newTipo.get_codigo(),
        newUser.get_activo(),
        newUser.get_password(),
        newUser.get_email()
    ))

    idEmpleado = cursor.lastrowid
    print("     Numero de Empleado:", idEmpleado)
    newTel.set_empleado(idEmpleado)
    
    #INSERT telefono
    comando3 = """
    INSERT INTO telefono (numTelefono, empleado)
    VALUES (%s, %s)
    """
    while True:
        try:
            cursor.execute(comando3, (
                newTel.get_numTelefono(),
                newTel.get_empleado()
            ))
            break
        except IntegrityError as e:
            if e.errno == 1062:
                print("\n   ERROR: El número de teléfono ya está registrado. Intente otro.")
                nuevoTel = val.valTelefono()
                newTel.set_numTelefono(nuevoTel)
    idTelefono = cursor.lastrowid
    miConn.conexion.commit()
    print("     ID Telefono", idTelefono)
    print("     Empleado Resgistrado con Exito")


#Read select
def Select():
    miConn = conn()
    comando = "select * from usuario"
    listado = miConn.lista(comando)

    if listado == 0:
        print("   No se puede mostrar")
    else:
        if len(listado) > 0:
            for fila in listado:
                objUser = Usuario(fila[0], fila[1], fila[2], fila[3], fila[4],
                                  fila[5], fila[6])
                print(objUser)
                print()


def selectInd(oldUser):
    objUser = Usuario("", "", "", "", "", 0, "", "")
    objUser = oldUser
    miConn = conn()
    aux = "select * from usuario where numEmpleado = {0}"
    comando = aux.format(objUser.get_numEmpleado())
    listado = miConn.lista(comando)
    if len(listado) == 1:
        print("   Datos de Usuario:")
        print()
        for fila in listado:
            obj = Usuario(
                fila[0],  # customerID
                fila[1],  # storeID
                fila[2],  # first_name
                fila[3],  # last_name
                fila[4],  # email
                fila[5],  # addressID
                fila[6],
                fila[7])
            print(obj)

        return True
    else:
        return False

#def __init__(self, numEmpleado, nombre, tipo_empleado, activo, password, email):
#Update
def UpdateNombre(oldUser):
    objUser = Usuario("", "", "", "", "", 0, "", "")
    objUser = oldUser
    miConn = conn()
    aux = "UPDATE empleado SET nombrePila = '{0}', apdPaterno = '{1}', apdMaterno = '{2}' WHERE numero = {3}"
    comando = aux.format(objUser.get_nombrePila(), objUser.get_apdPaterno(), objUser.get_apdMaterno(), objUser.get_numEmpleado())
    miConn.actualizar(comando)

#class Telefono:
    #def __init__(self, num, numTelefono, empleado):
def UpdateTelefono(oldUser):
    objTel = Telefono("", "", "")
    objTel = oldUser
    miConn = conn()
    aux = "UPDATE telefono SET numTelefono = '{0}' WHERE empleado = {1}"
    comando = aux.format(objTel.get_numTelefono(), objTel.get_empleado())
    miConn.actualizar(comando)


def UpdateTipoEmpleado(oldTipo):
    objTipo = TipoEmpleado("", "")
    objTipo = oldTipo
    miConn = conn()
    aux = "UPDATE tipo_empleado SET descripcion = '{0}' WHERE codigo = {1}"
    comando = aux.format(objTipo.get_descripcion(), objTipo.get_codigo())
    miConn.actualizar(comando)

def UpdateEmail(oldUser):
    objUser = Usuario("", "", "", "", "", 0, "", "")
    objUser = oldUser
    miConn = conn()
    aux = "UPDATE empleado SET email = '{0}' WHERE numero = {1}"
    comando = aux.format(objUser.get_email(), objUser.get_numEmpleado())
    miConn.actualizar(comando)


#Delete
def Delete(oldUser):
    objUser = Usuario("", "", "", "", "", 0, "", "")
    objUser = oldUser
    try:
        miConn = conn()
        cursor = miConn.conexion.cursor()
        cursor.execute(
        "UPDATE empleado SET activo = %s WHERE numero = %s",
            (objUser.get_activo(), objUser.get_numEmpleado())
        )
        miConn.conexion.commit()
        if cursor.rowcount > 0:
            print(f"Empleado {objUser.get_numEmpleado()} desactivado correctamente.")
            return True
        else:
            print(f"No se encontró empleado {objUser.get_numEmpleado()}.")
            return False
    except Exception as e:
        print("Error:", e)
        return False







def Deactive(oldUser):
    miConn = conn()
    comando = "SELECT * FROM empleado WHERE numero = %s"
    listado = miConn.lista_param(comando, (oldUser.get_numEmpleado(),))

    if len(listado) == 1:
        fila = listado[0]

        obj = Usuario(
            fila[0],  # numero
            fila[1],  # nombre
            fila[2],  # apellido
            fila[3],  # tipoEmpleado
            fila[4],  # email
            fila[5],  # activo
            fila[6],
            fila[7]
        )

        print("\n   Datos a Inhabilitar: ")
        print(obj)

        return obj     # <── REGRESAMOS EL OBJETO COMPLETO
    else:
        return None



#Buscar
def buscar(oldUser):
    objUser = Usuario("", "", "", "", "", 0, "", "")
    objUser = oldUser
    miConn = conn()
    aux = "select * from empleado where numero = {0}"
    comando = aux.format(objUser.get_numEmpleado())
    listado = miConn.lista(comando)
    if len(listado) == 1:
        print("   Datos a modificar: ")
        for fila in listado:
            obj = Usuario(
                fila[0],  # customerID
                fila[1],  # storeID
                fila[2],  # first_name
                fila[3],  # last_name
                fila[4],  # email
                fila[5],
                fila[6],
                fila[7])  # addressID
            print(obj)
        return True
    else:
        return False
    
def buscarTipoEmpleado():
    miConn = conn()

    while True:
        tipoCod = val.vInt("Ingrese el código del Tipo de Empleado: ")

        comando = "SELECT * FROM tipo_empleado WHERE codigo = %s"
        listado = miConn.lista_param(comando, (tipoCod,))

        if len(listado) == 1:
            print("\n   Tipo de empleado encontrado:\n")
            fila = listado[0]

            obj = TipoEmpleado(
                fila[0],  # código
                fila[1]   # descripción
            )

            print(f"Código: {obj.get_codigo()} - Descripción: {obj.get_descripcion()}")

            return obj   # regresamos el tipo encontrado

        else:
            print("\n   ERROR: Ese Tipo de Empleado NO existe. Intente nuevamente.\n")


def buscar3():
    miConn = conn()

    while True:
        numEmpleado = val.vInt("Ingrese el número de Empleado que desea modificar: ")

        comando = "SELECT * FROM empleado WHERE numero = %s"
        listado = miConn.lista_param(comando, (numEmpleado,))

        if len(listado) == 1:
            print("\n   Empleado encontrado:\n")
            fila = listado[0]

            obj = Usuario(
                fila[0],  # numero
                fila[1],  # nombre
                fila[2],
                fila[3],
                fila[4],
                fila[5],
                fila[6],
                fila[7]
            )

            print(obj)
            return obj   
        else:
            print("\n   ERROR: Ese empleado NO existe. Intente nuevamente.\n")

def registrarLicencia(numEmpleado):
    miConn = conn()
    cursor = miConn.conexion.cursor()

    print("\n  Registro de Licencia de Chofer ")

    licencias()
    opcLic = val._IntRange("   Ingrese una opción de Licencia: ", 1, 5)

    match opcLic:
        case 1:
            codigoLic = "A"
            descripcionLic = "Automovilista"
        case 2:
            codigoLic = "B"
            descripcionLic = "Taxis y Aplicaciones"
        case 3:
            codigoLic = "C"
            descripcionLic = "Transporte público"
        case 4:
            codigoLic = "D"
            descripcionLic = "Transporte de carga"
        case 5:
            codigoLic = "E"
            descripcionLic = "Servicios especializados y carga"

    print(f"   Seleccionó la licencia {codigoLic} ({descripcionLic})\n")

    while True:
        numeroLic = input("   Ingrese el número de licencia: ")
        if val.valLicencia(numeroLic):
            break
        print("   ERROR: Número de licencia inválido.\n")

    exp = val.val_exp()
    ven = val.val_ven(exp)

    cursor.execute("SELECT numero FROM tipo_licencia WHERE codigo = %s", (codigoLic,))
    resultado = cursor.fetchone()

    if resultado:
        id_tipoLic = resultado[0]  
    else:
      
        cursor.execute(
            "INSERT INTO tipo_licencia (codigo, descripcion) VALUES (%s, %s)",
            (codigoLic, descripcionLic)
        )
        miConn.conexion.commit()

        id_tipoLic = cursor.lastrowid

    comandoLic = """
        INSERT INTO licencia (numero, fechaExpedicion, fechaVencimiento, empleado, tipo_licencia)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(comandoLic, (
        numeroLic,
        exp,
        ven,
        numEmpleado,
        id_tipoLic
    ))

    miConn.conexion.commit()

    print("\n   Licencia de chofer registrada correctamente.\n")
    return True



def mostrar_choferes(conexion):
    cursor = conexion.cursor()

    query = """
    SELECT CONCAT_WS(' ', e.nombrePila, e.apdPaterno, e.apdMaterno) as Nombre,
    te.descripcion as "Tipo de empleado", -- "
    l.numero as "Numero de licencia", -- "
    tl.codigo as "Clase de licencia", -- "
    l.fechaExpedicion as "Fecha de expedicion", -- "
    l.fechaVencimiento as "Fecha de vencimiento" -- "
    from empleado as e
    inner join tipo_empleado as te on e.tipo_empleado = te.codigo
    inner join licencia as l on e.numero = l.empleado
    inner join tipo_licencia as tl on l.tipo_licencia = tl.numero
    """

    cursor.execute(query)
    resultados = cursor.fetchall()

    print("\n=== LISTA DE CHOFERES ===\n")

    if len(resultados) == 0:
        print(" No hay choferes registrados.")
    else:
        for fila in resultados:
            print(f"Nombre: {fila[0]}")
            print(f"Tipo de empleado: {fila[1]}")
            print(f"Número de licencia: {fila[2]}")
            print(f"Clase de licencia: {fila[3]}")
            print(f"Fecha de expedición: {fila[4]}")
            print(f"Fecha de vencimiento: {fila[5]}")
            print("-" * 40)  # separador limpio

    cursor.close()



def empleados_contactos(conexion):
    cursor = conexion.cursor()

    query = """
    SELECT e.numero as Numero,
    CONCAT_WS(' ', e.nombrePila, e.apdPaterno, e.apdMaterno) as Nombre,
    e.email as "Correo Electronico", -- "
    t.numTelefono as "Numero Telefonico" -- "
    from empleado as e
    inner join telefono as t on t.empleado = e.numero
    """

    cursor.execute(query)
    resultados = cursor.fetchall()

    print("\n=== LISTA DE EMPLEADOS Y SUS CONTACTOS ===\n")

    if len(resultados) == 0:
        print(" No hay empleados registrados.")
    else:
        for fila in resultados:
            print(f"Numero de Empleado: {fila[0]}")
            print(f"Nombre: {fila[1]}")
            print(f"Correo Electronico: {fila[2]}")
            print(f"Numero Telefonico: {fila[3]}")
            print("-" * 40)

    cursor.close()