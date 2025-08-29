from TDA.Nodo import Nodo

class NodoSensorSuelo(Nodo):
    def __init__(self, sensor_suelo, siguiente=None):
        super().__init__(siguiente)
        self.sensor_suelo = sensor_suelo
    
    def __str__(self):
        return f"NodoSensorSuelo: {self.sensor_suelo}"