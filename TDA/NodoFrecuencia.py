from TDA.Nodo import Nodo

class NodoFrecuencia(Nodo):
    def __init__(self, frecuencia, siguiente=None):
        super().__init__(siguiente)
        self.frecuencia = frecuencia
    
    def __str__(self):
        return f"NodoFrecuencia: {self.frecuencia}"