import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from TDA.ListaEstacion import ListaEstacion
from TDA.ListaSensorSuelo import ListaSensorSuelo
from TDA.ListaSensorCultivo import ListaSensorCultivo

class Campo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.estaciones = ListaEstacion()
        self.sensores_suelo = ListaSensorSuelo()
        self.sensores_cultivo = ListaSensorCultivo()
    
    def __str__(self):
        return f"Campo {self.id}: {self.nombre}"