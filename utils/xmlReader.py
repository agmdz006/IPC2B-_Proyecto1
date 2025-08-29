import xml.etree.ElementTree as ET
from entities.Campo import Campo
from entities.EstacionBase import EstacionBase
from entities.SensorSuelo import SensorSuelo
from entities.SensorCultivo import SensorCultivo
from entities.Frecuencia import Frecuencia
from TDA.ListaCampo import ListaCampo

def leer_campos_xml(path):
    campos = ListaCampo()
    
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        
        for campo_elem in root.findall('campo'):
            id_campo = campo_elem.get('id')
            nombre_campo = campo_elem.get('nombre')
            campo = Campo(id_campo, nombre_campo)
            
            print(f"➢ Cargando campo agrícola {id_campo}")
            
            # Cargar estaciones base
            estaciones_elem = campo_elem.find('estacionesBase')
            if estaciones_elem is not None:
                for estacion_elem in estaciones_elem.findall('estacion'):
                    id_estacion = estacion_elem.get('id')
                    nombre_estacion = estacion_elem.get('nombre')
                    estacion = EstacionBase(id_estacion, nombre_estacion)
                    campo.estaciones.insertar(estacion)
                    print(f"➢ Creando estación base {id_estacion}")
            
            # Cargar sensores de suelo
            sensores_suelo_elem = campo_elem.find('sensoresSuelo')
            if sensores_suelo_elem is not None:
                for sensor_elem in sensores_suelo_elem.findall('sensorS'):
                    id_sensor = sensor_elem.get('id')
                    nombre_sensor = sensor_elem.get('nombre')
                    sensor = SensorSuelo(id_sensor, nombre_sensor)
                    
                    # Cargar frecuencias del sensor
                    for freq_elem in sensor_elem.findall('frecuencia'):
                        id_estacion = freq_elem.get('idEstacion')
                        valor = int(freq_elem.text.strip())
                        frecuencia = Frecuencia(id_estacion, valor)
                        sensor.frecuencias.insertar(frecuencia)
                    
                    campo.sensores_suelo.insertar(sensor)
                    print(f"➢ Creando sensor de suelo {id_sensor}")
            
            # Cargar sensores de cultivo
            sensores_cultivo_elem = campo_elem.find('sensoresCultivo')
            if sensores_cultivo_elem is not None:
                for sensor_elem in sensores_cultivo_elem.findall('sensorT'):
                    id_sensor = sensor_elem.get('id')
                    nombre_sensor = sensor_elem.get('nombre')
                    sensor = SensorCultivo(id_sensor, nombre_sensor)
                    
                    # Cargar frecuencias del sensor
                    for freq_elem in sensor_elem.findall('frecuencia'):
                        id_estacion = freq_elem.get('idEstacion')
                        valor = int(freq_elem.text.strip())
                        frecuencia = Frecuencia(id_estacion, valor)
                        sensor.frecuencias.insertar(frecuencia)
                    
                    campo.sensores_cultivo.insertar(sensor)
                    print(f"➢ Creando sensor de cultivo {id_sensor}")
            
            campos.insertar(campo)
        
        return campos
        
    except ET.ParseError as e:
        print(f"Error al parsear el XML: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None