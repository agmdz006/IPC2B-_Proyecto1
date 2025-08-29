from TDA.NodoSensorCultivo import NodoSensorCultivo

class ListaSensorCultivo:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def insertar(self, sensor_cultivo):
        nuevo_nodo = NodoSensorCultivo(sensor_cultivo)
        if self.primero is None:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        self.size += 1

    def __str__(self):
        resultado = ""
        actual = self.primero
        while actual is not None:
            sensor = actual.sensor_cultivo
            if resultado != "":
                resultado += "\n"
            resultado += f"{sensor.id} - {sensor.nombre}"
            actual = actual.siguiente
        return resultado
