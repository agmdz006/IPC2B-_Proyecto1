from TDA.NodoCampo import NodoCampo

class ListaCampo:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def insertar(self, campo):
        nuevo_nodo = NodoCampo(campo)
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
            campo = actual.campo
            if resultado != "":
                resultado += "\n"
            resultado += f"{campo.id} - {campo.nombre}"
            actual = actual.siguiente
        return resultado