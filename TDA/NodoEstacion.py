from TDA.Nodo import Nodo

class NodoEstacion(Nodo):
    def __init__(self, estacion, siguiente=None):
        super().__init__(siguiente)
        self.estacion = estacion
    
    def __str__(self):
        return f"NodoEstacion: {self.estacion}"