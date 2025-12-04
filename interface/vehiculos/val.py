import datetime

def vOpciones(msg,inf,sup, funcion):
    while True:
        funcion()
        valor=input(msg)
        if valor.isdigit() != True:
            print("Solo ingresa números enteros")
        else:
            valor = int(valor)
            if (valor>=inf and valor<=sup):
                return valor
            else:
                print("Esta fuera de rango")
                
def vNumSerie(msg):
    while True:
        valor=input(msg)
        if len(valor) != 17:
            print("El numero de serie debe tener 17 caracteres")
        else: 
            return valor

def vMatricula(matricula): 
    while True: 
        valor=input(matricula) 
        if len(valor) < 6 or len(valor) >10: 
            print("La matricula debe tener entre 6 y 10 caracteres") 
        else:
            return valor
        

def vDatos(msg):
    while True:
        valor=input(msg)
        if len(valor) ==0:
            print("Este campo no puede estar vacio")
        else:
            if len(valor)<2 or len(valor) >20:
                print("Lo solicitado debe tener entre 2 y 20 caracteres")
            else:
                return valor
        
def vFecha():
    while True:
        fechastr = input("Fecha de adquisición formato (aaaa/mm/dd): ")
        try:
            fecha=datetime.datetime.strptime(fechastr, "%Y/%m/%d").date()
            return fecha
        except ValueError:
            print("Fecha invalida")


def vTipoLicencia(tipo_licencia):
    while True:
        valor=input(tipo_licencia)
        if len(valor) <1 or len(valor) >2:
            print("El tipo de licencia solo requiere de 1 o 2 caracteres")
        else:
            return valor

def vCapacidad(capacidad_pasajeros):
    while True:
        valor=input(capacidad_pasajeros)
        if not valor.isdigit():
            print("La capacidad de pasajeros debe ser un número entero")
        else:
            return (valor)
