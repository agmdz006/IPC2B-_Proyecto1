import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def procesar_campos(campos):
    """
    Procesa los campos agrícolas para optimizar las estaciones base
    mediante el algoritmo de agrupamiento de patrones
    """
    print("Iniciando procesamiento de campos agrícolas...")
    
    actual_campo = campos.primero
    while actual_campo is not None:
        campo = actual_campo.campo
        print(f"Procesando campo: {campo.nombre}")
        
        # Crear matrices de frecuencias
        print("➢ Creando matrices de frecuencias F[n,s] y F[n,t]")
        matriz_suelo, matriz_cultivo = crear_matrices_frecuencia(campo)
        
        # Convertir a matrices de patrones
        print("➢ Convirtiendo a matrices de patrones Fp[n,s] y Fp[n,t]")
        matriz_patron_suelo, matriz_patron_cultivo = crear_matrices_patron(matriz_suelo, matriz_cultivo)
        
        # Agrupar estaciones con patrones idénticos
        print("➢ Agrupando estaciones con patrones idénticos")
        estaciones_agrupadas = agrupar_estaciones_por_patron(campo, matriz_patron_suelo, matriz_patron_cultivo)
        
        # Crear matrices reducidas
        print("➢ Creando matrices reducidas Fr[n,s] y Fr[n,t]")
        actualizar_campo_con_agrupamiento(campo, estaciones_agrupadas)
        
        print(f"✓ Campo {campo.nombre} procesado exitosamente")
        actual_campo = actual_campo.siguiente
    
    print("Procesamiento completado.")

class MatrizFrecuencia:
    def __init__(self):
        self.filas = ListaFilas()
    
    def establecer_valor(self, estacion_id, sensor_id, valor):
        # Buscar fila existente
        actual_fila = self.filas.primero
        while actual_fila is not None:
            if actual_fila.fila.estacion_id == estacion_id:
                actual_fila.fila.establecer_celda(sensor_id, valor)
                return
            actual_fila = actual_fila.siguiente
        
        # Crear nueva fila
        nueva_fila = FilaMatriz(estacion_id)
        nueva_fila.establecer_celda(sensor_id, valor)
        self.filas.insertar(nueva_fila)
    
    def comparar_filas(self, id1, id2):
        fila1 = self.obtener_fila(id1)
        fila2 = self.obtener_fila(id2)
        if fila1 is None or fila2 is None:
            return False
        return fila1.comparar_con(fila2)
    
    def obtener_fila(self, estacion_id):
        actual = self.filas.primero
        while actual is not None:
            if actual.fila.estacion_id == estacion_id:
                return actual.fila
            actual = actual.siguiente
        return None

class ListaFilas:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def insertar(self, fila):
        nuevo_nodo = NodoFila(fila)
        if self.primero is None:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        self.size += 1

class NodoFila:
    def __init__(self, fila, siguiente=None):
        self.fila = fila
        self.siguiente = siguiente

class FilaMatriz:
    def __init__(self, estacion_id):
        self.estacion_id = estacion_id
        self.celdas = ListaCeldas()
    
    def establecer_celda(self, sensor_id, valor):
        nueva_celda = CeldaMatriz(sensor_id, valor)
        self.celdas.insertar(nueva_celda)
    
    def comparar_con(self, otra_fila):
        # Comparar patrones de ambas filas
        actual1 = self.celdas.primero
        actual2 = otra_fila.celdas.primero
        
        while actual1 is not None and actual2 is not None:
            if actual1.celda.valor != actual2.celda.valor:
                return False
            actual1 = actual1.siguiente
            actual2 = actual2.siguiente
        
        return actual1 is None and actual2 is None

class ListaCeldas:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def insertar(self, celda):
        nuevo_nodo = NodoCelda(celda)
        if self.primero is None:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        self.size += 1

class NodoCelda:
    def __init__(self, celda, siguiente=None):
        self.celda = celda
        self.siguiente = siguiente

class CeldaMatriz:
    def __init__(self, sensor_id, valor):
        self.sensor_id = sensor_id
        self.valor = valor

class GrupoEstaciones:
    def __init__(self):
        self.grupos = ListaGrupos()
    
    def agregar_grupo(self, id_representante, estaciones, nombre):
        nuevo_grupo = Grupo(id_representante, estaciones, nombre)
        self.grupos.insertar(nuevo_grupo)

class ListaGrupos:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def insertar(self, grupo):
        nuevo_nodo = NodoGrupo(grupo)
        if self.primero is None:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        self.size += 1

class NodoGrupo:
    def __init__(self, grupo, siguiente=None):
        self.grupo = grupo
        self.siguiente = siguiente

class Grupo:
    def __init__(self, id_representante, estaciones, nombre):
        self.id_representante = id_representante
        self.estaciones = estaciones
        self.nombre = nombre

def crear_matrices_frecuencia(campo):
    """Crea las matrices de frecuencias F[n,s] y F[n,t]"""
    from TDA.ListaEstacion import ListaEstacion
    
    # Obtener listas de estaciones usando estructura propia
    estaciones_lista = ListaEstacion()
    actual_est = campo.estaciones.primero
    while actual_est is not None:
        estaciones_lista.insertar(actual_est.estacion)
        actual_est = actual_est.siguiente
    
    # Matriz para sensores de suelo usando estructura propia
    matriz_suelo = MatrizFrecuencia()
    actual_sensor = campo.sensores_suelo.primero
    while actual_sensor is not None:
        sensor = actual_sensor.sensor_suelo
        actual_est = estaciones_lista.primero
        while actual_est is not None:
            estacion_id = actual_est.estacion.id
            matriz_suelo.establecer_valor(estacion_id, sensor.id, 0)
            
            # Buscar frecuencia para esta estación
            actual_freq = sensor.frecuencias.primero
            while actual_freq is not None:
                freq = actual_freq.frecuencia
                if freq.id_estacion == estacion_id:
                    matriz_suelo.establecer_valor(estacion_id, sensor.id, freq.valor)
                    break
                actual_freq = actual_freq.siguiente
            
            actual_est = actual_est.siguiente
        actual_sensor = actual_sensor.siguiente
    
    # Matriz para sensores de cultivo usando estructura propia
    matriz_cultivo = MatrizFrecuencia()
    actual_sensor = campo.sensores_cultivo.primero
    while actual_sensor is not None:
        sensor = actual_sensor.sensor_cultivo
        actual_est = estaciones_lista.primero
        while actual_est is not None:
            estacion_id = actual_est.estacion.id
            matriz_cultivo.establecer_valor(estacion_id, sensor.id, 0)
            
            # Buscar frecuencia para esta estación
            actual_freq = sensor.frecuencias.primero
            while actual_freq is not None:
                freq = actual_freq.frecuencia
                if freq.id_estacion == estacion_id:
                    matriz_cultivo.establecer_valor(estacion_id, sensor.id, freq.valor)
                    break
                actual_freq = actual_freq.siguiente
            
            actual_est = actual_est.siguiente
        actual_sensor = actual_sensor.siguiente
    
    return matriz_suelo, matriz_cultivo

def crear_matrices_patron(matriz_suelo, matriz_cultivo):
    """Convierte matrices de frecuencias a matrices de patrones (0 o 1)"""
    matriz_patron_suelo = MatrizFrecuencia()
    matriz_patron_cultivo = MatrizFrecuencia()
    
    # Convertir matriz de suelo a patrones
    actual_fila = matriz_suelo.filas.primero
    while actual_fila is not None:
        estacion_id = actual_fila.fila.estacion_id
        actual_celda = actual_fila.fila.celdas.primero
        while actual_celda is not None:
            sensor_id = actual_celda.celda.sensor_id
            frecuencia = actual_celda.celda.valor
            patron = 1 if frecuencia > 0 else 0
            matriz_patron_suelo.establecer_valor(estacion_id, sensor_id, patron)
            actual_celda = actual_celda.siguiente
        actual_fila = actual_fila.siguiente
    
    # Convertir matriz de cultivo a patrones
    actual_fila = matriz_cultivo.filas.primero
    while actual_fila is not None:
        estacion_id = actual_fila.fila.estacion_id
        actual_celda = actual_fila.fila.celdas.primero
        while actual_celda is not None:
            sensor_id = actual_celda.celda.sensor_id
            frecuencia = actual_celda.celda.valor
            patron = 1 if frecuencia > 0 else 0
            matriz_patron_cultivo.establecer_valor(estacion_id, sensor_id, patron)
            actual_celda = actual_celda.siguiente
        actual_fila = actual_fila.siguiente
    
    return matriz_patron_suelo, matriz_patron_cultivo

def agrupar_estaciones_por_patron(campo, matriz_patron_suelo, matriz_patron_cultivo):
    """Agrupa estaciones que tienen el mismo patrón"""
    from TDA.ListaEstacion import ListaEstacion
    
    grupos = GrupoEstaciones()
    estaciones_procesadas = ListaEstacion()
    
    # Obtener todas las estaciones usando estructura propia
    estaciones = ListaEstacion()
    actual_est = campo.estaciones.primero
    while actual_est is not None:
        estaciones.insertar(actual_est.estacion)
        actual_est = actual_est.siguiente
    
    actual_est1 = estaciones.primero
    while actual_est1 is not None:
        estacion1 = actual_est1.estacion
        
        # Verificar si ya fue procesada
        if esta_procesada(estaciones_procesadas, estacion1.id):
            actual_est1 = actual_est1.siguiente
            continue
        
        # Crear nuevo grupo
        grupo_estaciones = ListaEstacion()
        grupo_estaciones.insertar(estacion1)
        estaciones_procesadas.insertar(estacion1)
        
        # Buscar estaciones con el mismo patrón
        actual_est2 = actual_est1.siguiente
        while actual_est2 is not None:
            estacion2 = actual_est2.estacion
            
            if not esta_procesada(estaciones_procesadas, estacion2.id):
                # Comparar patrones
                if patrones_iguales(matriz_patron_suelo, matriz_patron_cultivo, estacion1.id, estacion2.id):
                    grupo_estaciones.insertar(estacion2)
                    estaciones_procesadas.insertar(estacion2)
            
            actual_est2 = actual_est2.siguiente
        
        # Crear nombre del grupo
        nombre_grupo = crear_nombre_grupo(grupo_estaciones)
        grupos.agregar_grupo(estacion1.id, grupo_estaciones, nombre_grupo)
        
        actual_est1 = actual_est1.siguiente
    
    return grupos

def actualizar_campo_con_agrupamiento(campo, estaciones_agrupadas):
    """Actualiza el campo con las estaciones agrupadas y frecuencias sumadas"""
    from TDA.ListaEstacion import ListaEstacion
    from TDA.ListaFrecuencia import ListaFrecuencia
    from entities.EstacionBase import EstacionBase
    from entities.Frecuencia import Frecuencia
    
    # Crear nueva lista de estaciones reducidas
    nuevas_estaciones = ListaEstacion()
    
    actual_grupo = estaciones_agrupadas.grupos.primero
    while actual_grupo is not None:
        grupo = actual_grupo.grupo
        # Crear nueva estación representante del grupo
        estacion_reducida = EstacionBase(grupo.id_representante, grupo.nombre)
        nuevas_estaciones.insertar(estacion_reducida)
        actual_grupo = actual_grupo.siguiente
    
    # Actualizar estaciones del campo
    campo.estaciones = nuevas_estaciones
    
    # Actualizar frecuencias de sensores de suelo
    actual_sensor = campo.sensores_suelo.primero
    while actual_sensor is not None:
        sensor = actual_sensor.sensor_suelo
        nuevas_frecuencias = ListaFrecuencia()
        
        actual_grupo = estaciones_agrupadas.grupos.primero
        while actual_grupo is not None:
            grupo = actual_grupo.grupo
            suma_frecuencias = calcular_suma_frecuencias(sensor.frecuencias, grupo.estaciones)
            
            if suma_frecuencias > 0:
                nueva_freq = Frecuencia(grupo.id_representante, suma_frecuencias)
                nuevas_frecuencias.insertar(nueva_freq)
            
            actual_grupo = actual_grupo.siguiente
        
        sensor.frecuencias = nuevas_frecuencias
        actual_sensor = actual_sensor.siguiente
    
    # Actualizar frecuencias de sensores de cultivo
    actual_sensor = campo.sensores_cultivo.primero
    while actual_sensor is not None:
        sensor = actual_sensor.sensor_cultivo
        nuevas_frecuencias = ListaFrecuencia()
        
        actual_grupo = estaciones_agrupadas.grupos.primero
        while actual_grupo is not None:
            grupo = actual_grupo.grupo
            suma_frecuencias = calcular_suma_frecuencias(sensor.frecuencias, grupo.estaciones)
            
            if suma_frecuencias > 0:
                nueva_freq = Frecuencia(grupo.id_representante, suma_frecuencias)
                nuevas_frecuencias.insertar(nueva_freq)
            
            actual_grupo = actual_grupo.siguiente
        
        sensor.frecuencias = nuevas_frecuencias
        actual_sensor = actual_sensor.siguiente

def esta_procesada(lista_procesadas, estacion_id):
    """Verifica si una estación ya fue procesada"""
    actual = lista_procesadas.primero
    while actual is not None:
        if actual.estacion.id == estacion_id:
            return True
        actual = actual.siguiente
    return False

def patrones_iguales(matriz_suelo, matriz_cultivo, id1, id2):
    """Compara si dos estaciones tienen el mismo patrón"""
    return (matriz_suelo.comparar_filas(id1, id2) and 
            matriz_cultivo.comparar_filas(id1, id2))

def crear_nombre_grupo(grupo_estaciones):
    """Crea el nombre del grupo concatenando nombres de estaciones"""
    nombre = ""
    actual = grupo_estaciones.primero
    primera = True
    while actual is not None:
        if not primera:
            nombre += ", "
        nombre += actual.estacion.nombre
        primera = False
        actual = actual.siguiente
    return nombre

def calcular_suma_frecuencias(frecuencias_originales, estaciones_grupo):
    """Calcula la suma de frecuencias para un grupo de estaciones"""
    suma = 0
    actual_est = estaciones_grupo.primero
    while actual_est is not None:
        estacion = actual_est.estacion
        actual_freq = frecuencias_originales.primero
        while actual_freq is not None:
            if actual_freq.frecuencia.id_estacion == estacion.id:
                suma += actual_freq.frecuencia.valor
                break
            actual_freq = actual_freq.siguiente
        actual_est = actual_est.siguiente
    return suma

