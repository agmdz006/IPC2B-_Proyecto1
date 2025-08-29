from TDA.NodoFrecuencia import NodoFrecuencia

class ListaFrecuencia:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def insertar(self, frecuencia):
        nuevo_nodo = NodoFrecuencia(frecuencia)
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
            freq = actual.frecuencia
            if resultado != "":
                resultado += "\n"
            resultado += f"Estación {freq.id_estacion}: {freq.valor}"
            actual = actual.siguiente
        return resultado