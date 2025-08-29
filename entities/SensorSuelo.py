from TDA.ListaFrecuencia import ListaFrecuencia

class SensorSuelo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaFrecuencia()
    
    def __str__(self):
        return f"Sensor Suelo {self.id}: {self.nombre}"