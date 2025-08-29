import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def escribir_campos_xml(campos, ruta, nombre_archivo):
    root = ET.Element('camposAgricolas')
    
    actual_campo = campos.primero
    while actual_campo is not None:
        campo = actual_campo.campo
        campo_elem = ET.SubElement(root, 'campo', {'id': str(campo.id), 'nombre': campo.nombre})
        
        # Estaciones base reducidas
        estaciones_elem = ET.SubElement(campo_elem, 'estacionesBaseReducidas')
        actual_estacion = campo.estaciones.primero
        while actual_estacion is not None:
            estacion = actual_estacion.estacion
            estacion_elem = ET.SubElement(estaciones_elem, 'estacion', {'id': str(estacion.id), 'nombre': estacion.nombre})
            actual_estacion = actual_estacion.siguiente
        
        # Sensores de suelo
        sensores_suelo_elem = ET.SubElement(campo_elem, 'sensoresSuelo')
        actual_sensor_s = campo.sensores_suelo.primero
        while actual_sensor_s is not None:
            sensor = actual_sensor_s.sensor_suelo
            sensor_elem = ET.SubElement(sensores_suelo_elem, 'sensorS', {'id': str(sensor.id), 'nombre': sensor.nombre})
            
            actual_freq = sensor.frecuencias.primero
            while actual_freq is not None:
                freq = actual_freq.frecuencia
                freq_elem = ET.SubElement(sensor_elem, 'frecuencia', {'idEstacion': str(freq.id_estacion)})
                freq_elem.text = str(freq.valor)
                actual_freq = actual_freq.siguiente
            
            actual_sensor_s = actual_sensor_s.siguiente
        
        # Sensores de cultivo
        sensores_cultivo_elem = ET.SubElement(campo_elem, 'sensoresCultivo')
        actual_sensor_c = campo.sensores_cultivo.primero
        while actual_sensor_c is not None:
            sensor = actual_sensor_c.sensor_cultivo
            sensor_elem = ET.SubElement(sensores_cultivo_elem, 'sensorT', {'id': str(sensor.id), 'nombre': sensor.nombre})
            
            actual_freq = sensor.frecuencias.primero
            while actual_freq is not None:
                freq = actual_freq.frecuencia
                freq_elem = ET.SubElement(sensor_elem, 'frecuencia', {'idEstacion': str(freq.id_estacion)})
                freq_elem.text = str(freq.valor)
                actual_freq = actual_freq.siguiente
            
            actual_sensor_c = actual_sensor_c.siguiente
        
        actual_campo = actual_campo.siguiente
    
    # Escribir archivo
    xml_str = ET.tostring(root, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")
    
    # Construir ruta completa del archivo correctamente
    if ruta and nombre_archivo:
        archivo_completo = os.path.join(ruta, nombre_archivo)
    elif ruta:
        # Si solo se proporciona ruta, usar nombre por defecto
        archivo_completo = os.path.join(ruta, "salida.xml")
    else:
        archivo_completo = nombre_archivo if nombre_archivo else "salida.xml"
    
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(archivo_completo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        with open(archivo_completo, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        print(f"Archivo guardado exitosamente en: {archivo_completo}")
    except PermissionError:
        print(f"Error: No tienes permisos para escribir en la ruta: {archivo_completo}")
        print("Intenta con una ruta diferente o ejecuta como administrador.")
    except Exception as e:
        print(f"Error al guardar el archivo: {str(e)}")

