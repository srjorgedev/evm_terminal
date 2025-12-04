# Clase Mantenimiento.py
class Mantenimiento:

    def __init__(self, razon, importancia, fechaProgramada, comentarios, tipoMantenimiento, vehiculo, estadoMantenimiento, folio=0):
        self.__folio = folio
        self.__razon = razon
        self.__importancia = importancia
        self.__fechaProgramada = fechaProgramada
        self.__comentarios = comentarios
        self.__tipoMantenimiento = tipoMantenimiento
        self.__vehiculo = vehiculo
        self.__estadoMantenimiento = estadoMantenimiento

    def __str__(self):
        msg = f"Folio: {self.__folio} | Razón: {self.__razon[:30]}... | Estatus: {self.__estatus} | Importancia: {self.__importancia}"
        msg += f"\n  Tipo: {self.__tipoMantenimiento} | Vehículo: {self.__vehiculo} | Programado: {self.__fechaProgramada} | Estado Mantenimiento: {self.__estadoMantenimiento}"
        return msg

    # Getters
    def get_folio(self):
        return self.__folio
    def get_razon(self):
        return self.__razon
    def get_estatus(self):
        return self.__estatus
    def get_importancia(self):
        return self.__importancia
    def get_fechaProgramada(self):
        return self.__fechaProgramada
    def get_comentarios(self):
        return self.__comentarios
    def get_tipoMantenimiento(self):
        return self.__tipoMantenimiento
    def get_vehiculo(self):
        return self.__vehiculo
    def get_estadoMantenimiento(self):
        return self.__estadoMantenimiento

    # Setters
    def set_folio(self, folio):
        self.__folio = folio
    def set_razon(self, razon):
        self.__razon = razon
    def set_estatus(self, estatus):
        self.__estatus = estatus
    def set_importancia(self, importancia):
        self.__importancia = importancia
    def set_fechaProgramada(self, fechaProgramada):
        self.__fechaProgramada = fechaProgramada
    def set_comentarios(self, comentarios):
        self.__comentarios = comentarios
    def set_tipoMantenimiento(self, tipoMantenimiento):
        self.__tipoMantenimiento = tipoMantenimiento
    def set_vehiculo(self, vehiculo):
        self.__vehiculo = vehiculo
    def set_estadoMantenimiento(self, estadoMantenimiento):
        self.__estadoMantenimiento = estadoMantenimiento