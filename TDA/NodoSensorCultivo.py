from TDA.Nodo import Nodo

class NodoSensorCultivo(Nodo):
    def __init__(self, sensor_cultivo, siguiente=None):
        super().__init__(siguiente)
        self.sensor_cultivo = sensor_cultivo
    
    def __str__(self):
        return f"NodoSensorCultivo: {self.sensor_cultivo}"