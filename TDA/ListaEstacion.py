from TDA.NodoEstacion import NodoEstacion

class ListaEstacion:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def insertar(self, estacion):
        nuevo_nodo = NodoEstacion(estacion)
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
            estacion = actual.estacion
            if resultado != "":
                resultado += "\n"
            resultado += f"{estacion.id} - {estacion.nombre}"
            actual = actual.siguiente
        return resultado