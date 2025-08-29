class Frecuencia:
    def __init__(self, id_estacion, valor):
        self.id_estacion = id_estacion
        self.valor = valor
    
    def __str__(self):
        return f"Frecuencia - Estación {self.id_estacion}: {self.valor}"