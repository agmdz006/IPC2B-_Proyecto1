from TDA.Nodo import Nodo

class NodoCampo(Nodo):
    def __init__(self, campo, siguiente=None):
        super().__init__(siguiente)
        self.campo = campo
    
    def __str__(self):
        return f"NodoCampo: {self.campo}"