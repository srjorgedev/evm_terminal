from db.connV import conn
from domain.vehiculos import ClaseVehiculo as Vehiculo

def listarVehiculos():
    miConn = conn()
    comando = """
        SELECT numSerie, matricula, proposito, fechaAdquisicion, disponibilidad, 
               marca, modelo, licencia_requerida 
        FROM vehiculo
    """
    lista = miConn.lista(comando)
    
    print("\n--- LISTADO DE VEHÍCULOS ---")

    if not lista:
        print("No hay vehículos registrados.")
        input("\n   Presione ENTER para continuar...")
        return []

    # Encabezado formateado
    print(f"{'NumSerie':<18} {'Matrícula':<12} {'Propósito':<25} {'Fecha Adq.':<12} "
          f"{'Disponibilidad':<15} {'Marca':<12} {'Modelo':<12} {'Licencia Req.':<15}")
    print("-" * 120)

    # Filas
    for numSerie, matricula, proposito, fecha, disponibilidad, marca, modelo, lic_req in lista:
        
        # Convertir fecha a string
        fecha = str(fecha)

        print(f"{numSerie:<18} {matricula:<12} {proposito:<25} {fecha:<12} "
              f"{disponibilidad:<15} {marca:<12} {modelo:<12} {lic_req:<15}")

    print("-" * 120)
    input("\n   Presione ENTER para continuar...")

    return lista

                
def agregarVehiculo(nuevoVehiculo):
    miConn = conn()

    aux = """
        INSERT INTO vehiculo 
        (numSerie, matricula, proposito, fechaAdquisicion, disponibilidad,
         marca, modelo, licencia_requerida)
        VALUES ('{0}', '{1}', '{2}', '{3}', 1, '{4}', '{5}', '{6}')
    """

    comando = aux.format(
        nuevoVehiculo.get_num_serie(),   
        nuevoVehiculo.get_matricula(),       
        nuevoVehiculo.get_proposito(),       
        nuevoVehiculo.get_fecha_adquision(), 
        nuevoVehiculo.get_marca(),           
        nuevoVehiculo.get_modelo(),          
        nuevoVehiculo.get_tipo_licencia(),   
    )

    lastid = miConn.registrar(comando)
    if lastid:
        print(" Error al guardar el vehículo.")
        input("\n   Presione ENTER para continuar...")
    else:
        print(" Vehículo guardado exitosamente.")
        input("\n   Presione ENTER para continuar...")


    return lastid

def tipolicencia():
    miConn = conn()  
#consulta 3
    comando = """
    SELECT 
        v.matricula AS Matricula, 
        m.nombre AS Marca, 
        md.nombre AS Modelo, 
        v.proposito AS Proposito, 
        tl.descripcion AS TipoLicencia
    FROM vehiculo AS v
    INNER JOIN tipo_licencia AS tl ON v.licencia_requerida = tl.codigo
    INNER JOIN marca AS m ON m.codigo = v.marca
    INNER JOIN modelo AS md ON md.codigo = v.modelo;
    """

    lista = miConn.lista(comando)

    print("\n--- LISTADO DE VEHÍCULOS CON TIPO DE LICENCIA ---")

    if not lista:
        print("No hay vehículos registrados.")
        input("\n   Presione ENTER para continuar...")
        return []

    # Encabezado
    print(f"{'Matrícula':<12} {'Marca':<15} {'Modelo':<15} {'Propósito':<25} {'Tipo Licencia':<20}")
    print("-" * 90)
    input("\n   Presione ENTER para continuar...")

    # Filas
    for fila in lista:
        matricula, marca, modelo, proposito, tipo_licencia = fila
        print(f"{matricula:<12} {marca:<15} {modelo:<15} {proposito:<25} {tipo_licencia:<20}")

    print("-" * 90)

    return lista



def borrarVehiculo(existeVehiculo):
    miConn = conn()

    comando = f"""
        UPDATE vehiculo
        SET disponibilidad = 2
        WHERE numSerie = '{existeVehiculo.get_num_serie()}'
    """

    contador = miConn.actualizar(comando)

    if contador == 1:
        print("Vehículo dado de baja correctamente (disponibilidad = 2).")
        input("\n   Presione ENTER para continuar...")
    elif contador == 0:
        print("Vehículo no encontrado.")
        input("\n   Presione ENTER para continuar...")
    else:
        print("Error al actualizar la disponibilidad.")
        input("\n   Presione ENTER para continuar...")





        
        
def modificarVehiculo(existeVehiculo):
    miConn = conn()

    comando = """
        UPDATE vehiculo
        SET matricula = '{0}'
        WHERE numSerie = '{1}'
    """.format(
        existeVehiculo.get_matricula(),
        existeVehiculo.get_num_serie()
    )

    contador = miConn.actualizar(comando)

    if contador == 1:
        print("Vehículo modificado correctamente")
        input("\n   Presione ENTER para continuar...")
    elif contador == 0:
        print("Vehículo no encontrado")
        input("\n   Presione ENTER para continuar...")
    else:
        print("Error al modificar el vehículo")
        input("\n   Presione ENTER para continuar...")

 
def mostarmarcaymodelo():
    miConn = conn()

    comando = """
        SELECT m.codigo AS CodigoMarca,
               m.nombre AS Marca,
               md.codigo AS CodigoModelo,
               md.nombre AS Modelo
        FROM marca AS m
        INNER JOIN modelo AS md ON md.marca = m.codigo
    """
    lista = miConn.lista(comando)

    if not lista:
        print("No hay registros")
        return

    print(f"{'Codigo':<10} {'Marca':<20} {'Codigo':<12} {'Modelo':<20}")
    print("-"*65)
    input("\n   Presione ENTER para continuar...")

    for fila in lista:
        cod_marca, marca, cod_modelo, modelo = fila
        print(f"{cod_marca:<10} {marca:<20} {cod_modelo:<12} {modelo:<20}")

    print("-"*65)
    
def tipli():
    miConn = conn()
    comando = "SELECT tl.codigo, tl.descripcion FROM tipo_licencia AS tl;"
    
    lista = miConn.lista(comando)

    if not lista:
        print("No hay registros")
        input("\n   Presione ENTER para continuar...")
        return

    print(f"{'Codigo':<10} {'Descripcion':<30}")
    print("-"*45)
    input("\n   Presione ENTER para continuar...")

    for codigo, descripcion in lista:
        print(f"{codigo:<10} {descripcion:<30}")

    print("-"*45)
    
def numsemoma():
    miConn = conn()
    comando = "SELECT v.numSerie, v.marca, v.modelo FROM vehiculo AS v;"
    
    lista = miConn.lista(comando)

    if not lista:
        print("No hay registros")
        input("\n   Presione ENTER para continuar...")
        return

    print(f"{'NumSerie':<20} {'Marca':<20} {'Modelo':<20}")
    print("-" * 60)
    input("\n   Presione ENTER para continuar...")
    
    for numSerie, marca, modelo in lista:
        print(f"{numSerie:<20} {marca:<20} {modelo:<20}")

    print("-" * 60)

    
def nummat():
    miConn = conn()
    comando = """
        SELECT v.numSerie, v.matricula 
        FROM vehiculo AS v;
    """

    lista = miConn.lista(comando)

    if not lista:
        print("No hay registros")
        input("\n   Presione ENTER para continuar...")
        return

    print(f"{'NumSerie':<20} {'Matrícula':<20}")
    print("-" * 40)
    input("\n   Presione ENTER para continuar...")

    for numSerie, matricula in lista:
        print(f"{numSerie:<20} {matricula:<20}")

    print("-" * 40)

    




    


    