import graphviz
import os
import sys

def generar_grafica(campo, tipo_matriz):
    """
    Genera gráfica usando Graphviz para mostrar las matrices en formato tabular
    tipo_matriz: 'frecuencia', 'patron', 'reducida'
    """
    try:
        dot = graphviz.Digraph(comment=f'Campo {campo.nombre} - Matriz {tipo_matriz}')
        dot.attr(rankdir='TB')
        
        # Configurar el ejecutable de Graphviz si está en una ubicación específica
        if os.name == 'nt':  # Windows
            # Rutas comunes donde se instala Graphviz en Windows
            possible_paths = [
                r"C:\Program Files\Graphviz\bin",
                r"C:\Program Files (x86)\Graphviz\bin",
                r"C:\Graphviz\bin"
            ]
            
            for path in possible_paths:
                if os.path.exists(os.path.join(path, "dot.exe")):
                    os.environ["PATH"] += os.pathsep + path
                    break
        
        if tipo_matriz == 'frecuencia':
            generar_matriz_frecuencia(dot, campo)
        elif tipo_matriz == 'patron':
            generar_matriz_patron(dot, campo)
        elif tipo_matriz == 'reducida':
            generar_matriz_reducida(dot, campo)
        
        # Renderizar y mostrar
        nombre_archivo = f"{campo.id}_{tipo_matriz}"
        dot.render(nombre_archivo, format='png', cleanup=True)
        print(f"Gráfica generada exitosamente: {nombre_archivo}.png")
        
        return dot
        
    except FileNotFoundError as e:
        print("ERROR: No se pudo encontrar el ejecutable de Graphviz.")
        print("Soluciones:")
        print("1. Asegúrate de que Graphviz esté instalado desde: https://graphviz.org/download/")
        print("2. Agrega la carpeta 'bin' de Graphviz a tu PATH del sistema")
        print("3. En Windows, típicamente está en: C:\\Program Files\\Graphviz\\bin")
        return None
    except Exception as e:
        print(f"Error inesperado al generar gráfica: {str(e)}")
        return None

def generar_matriz_frecuencia(dot, campo):
    """Genera matriz de frecuencias en formato tabular"""
    html_content = f'''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD COLSPAN="10" BGCOLOR="lightgray"><B>Matriz completa de Frecuencias</B></TD></TR>
        <TR><TD COLSPAN="10" BGCOLOR="white"><B>--- Campo ID: {campo.id}, Nombre: {campo.nombre} ---</B></TD></TR>
    '''
    
    # Matriz de Sensores de Suelo
    html_content += '''
        <TR><TD COLSPAN="10" BGCOLOR="lightgreen"><B>Matriz de Frecuencia Sensores de Suelo F[n,s]</B></TD></TR>
        <TR><TD BGCOLOR="lightgray"><B>Estación</B></TD>
    '''
    
    # Obtener sensores de suelo para encabezados
    sensores_suelo = []
    actual_sensor = campo.sensores_suelo.primero
    while actual_sensor is not None:
        sensores_suelo.append(actual_sensor.sensor_suelo)
        html_content += f'<TD BGCOLOR="lightgreen"><B>{actual_sensor.sensor_suelo.nombre}</B></TD>'
        actual_sensor = actual_sensor.siguiente
    html_content += '</TR>'
    
    # Filas de estaciones para sensores de suelo
    actual_est = campo.estaciones.primero
    while actual_est is not None:
        estacion = actual_est.estacion
        html_content += f'<TR><TD BGCOLOR="lightgray"><B>{estacion.id}</B></TD>'
        
        for sensor in sensores_suelo:
            valor = obtener_frecuencia(sensor, estacion.id)
            html_content += f'<TD>{valor}</TD>'
        
        html_content += '</TR>'
        actual_est = actual_est.siguiente
    
    # Matriz de Sensores de Cultivo
    html_content += '''
        <TR><TD COLSPAN="10" BGCOLOR="orange"><B>Matriz de Frecuencia Sensores de Cultivo F[n,t]</B></TD></TR>
        <TR><TD BGCOLOR="lightgray"><B>Estación</B></TD>
    '''
    
    # Obtener sensores de cultivo para encabezados
    sensores_cultivo = []
    actual_sensor = campo.sensores_cultivo.primero
    while actual_sensor is not None:
        sensores_cultivo.append(actual_sensor.sensor_cultivo)
        html_content += f'<TD BGCOLOR="orange"><B>{actual_sensor.sensor_cultivo.nombre}</B></TD>'
        actual_sensor = actual_sensor.siguiente
    html_content += '</TR>'
    
    # Filas de estaciones para sensores de cultivo
    actual_est = campo.estaciones.primero
    while actual_est is not None:
        estacion = actual_est.estacion
        html_content += f'<TR><TD BGCOLOR="lightgray"><B>{estacion.id}</B></TD>'
        
        for sensor in sensores_cultivo:
            valor = obtener_frecuencia(sensor, estacion.id)
            html_content += f'<TD>{valor}</TD>'
        
        html_content += '</TR>'
        actual_est = actual_est.siguiente
    
    html_content += '</TABLE>>'
    
    # Crear nodo con tabla HTML
    dot.node('matriz', html_content, shape='plaintext')

def generar_matriz_patron(dot, campo):
    """Genera matriz de patrones en formato tabular (0 y 1)"""
    html_content = f'''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD COLSPAN="10" BGCOLOR="lightgray"><B>Matriz de Patrones</B></TD></TR>
        <TR><TD COLSPAN="10" BGCOLOR="white"><B>--- Campo ID: {campo.id}, Nombre: {campo.nombre} ---</B></TD></TR>
    '''
    
    # Matriz de Patrones Sensores de Suelo
    html_content += '''
        <TR><TD COLSPAN="10" BGCOLOR="lightcoral"><B>Matriz de Patrones Sensores de Suelo Fp[n,s]</B></TD></TR>
        <TR><TD BGCOLOR="lightgray"><B>Estación</B></TD>
    '''
    
    # Obtener sensores de suelo para encabezados
    sensores_suelo = []
    actual_sensor = campo.sensores_suelo.primero
    while actual_sensor is not None:
        sensores_suelo.append(actual_sensor.sensor_suelo)
        html_content += f'<TD BGCOLOR="lightcoral"><B>{actual_sensor.sensor_suelo.nombre}</B></TD>'
        actual_sensor = actual_sensor.siguiente
    html_content += '</TR>'
    
    # Filas de estaciones para sensores de suelo (patrones binarios)
    actual_est = campo.estaciones.primero
    while actual_est is not None:
        estacion = actual_est.estacion
        html_content += f'<TR><TD BGCOLOR="lightgray"><B>{estacion.id}</B></TD>'
        
        for sensor in sensores_suelo:
            valor = obtener_frecuencia(sensor, estacion.id)
            patron = "1" if valor > 0 else "0"
            color = "red" if patron == "1" else "white"
            html_content += f'<TD BGCOLOR="{color}"><B>{patron}</B></TD>'
        
        html_content += '</TR>'
        actual_est = actual_est.siguiente
    
    # Matriz de Patrones Sensores de Cultivo
    html_content += '''
        <TR><TD COLSPAN="10" BGCOLOR="yellow"><B>Matriz de Patrones Sensores de Cultivo Fp[n,t]</B></TD></TR>
        <TR><TD BGCOLOR="blue"><B>Estación</B></TD>
    '''
    
    # Obtener sensores de cultivo para encabezados
    sensores_cultivo = []
    actual_sensor = campo.sensores_cultivo.primero
    while actual_sensor is not None:
        sensores_cultivo.append(actual_sensor.sensor_cultivo)
        html_content += f'<TD BGCOLOR="lightyellow"><B>{actual_sensor.sensor_cultivo.nombre}</B></TD>'
        actual_sensor = actual_sensor.siguiente
    html_content += '</TR>'
    
    # Filas de estaciones para sensores de cultivo (patrones binarios)
    actual_est = campo.estaciones.primero
    while actual_est is not None:
        estacion = actual_est.estacion
        html_content += f'<TR><TD BGCOLOR="lightgray"><B>{estacion.id}</B></TD>'
        
        for sensor in sensores_cultivo:
            valor = obtener_frecuencia(sensor, estacion.id)
            patron = "1" if valor > 0 else "0"
            color = "red" if patron == "1" else "white"
            html_content += f'<TD BGCOLOR="{color}"><B>{patron}</B></TD>'
        
        html_content += '</TR>'
        actual_est = actual_est.siguiente
    
    html_content += '</TABLE>>'
    
    # Crear nodo con tabla HTML
    dot.node('matriz', html_content, shape='plaintext')

def generar_matriz_reducida(dot, campo):
    """Genera matriz reducida con estaciones agrupadas"""
    html_content = f'''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD COLSPAN="10" BGCOLOR="lightgray"><B>Matriz Reducida</B></TD></TR>
        <TR><TD COLSPAN="10" BGCOLOR="white"><B>--- Campo ID: {campo.id}, Nombre: {campo.nombre} ---</B></TD></TR>
    '''
    
    # Matriz Reducida Sensores de Suelo
    html_content += '''
        <TR><TD COLSPAN="10" BGCOLOR="darkgreen"><B>Matriz Reducida Sensores de Suelo Fr[n,s]</B></TD></TR>
        <TR><TD BGCOLOR="lightgray"><B>Estación Agrupada</B></TD>
    '''
    
    # Obtener sensores de suelo para encabezados
    sensores_suelo = []
    actual_sensor = campo.sensores_suelo.primero
    while actual_sensor is not None:
        sensores_suelo.append(actual_sensor.sensor_suelo)
        html_content += f'<TD BGCOLOR="darkgreen"><B>{actual_sensor.sensor_suelo.nombre}</B></TD>'
        actual_sensor = actual_sensor.siguiente
    html_content += '</TR>'
    
    # Filas de estaciones agrupadas para sensores de suelo
    actual_est = campo.estaciones.primero
    while actual_est is not None:
        estacion = actual_est.estacion
        html_content += f'<TR><TD BGCOLOR="lightgray"><B>{estacion.nombre}</B></TD>'
        
        for sensor in sensores_suelo:
            valor = obtener_frecuencia(sensor, estacion.id)
            html_content += f'<TD BGCOLOR="lightsteelblue"><B>{valor}</B></TD>'
        
        html_content += '</TR>'
        actual_est = actual_est.siguiente
    
    # Matriz Reducida Sensores de Cultivo
    html_content += '''
        <TR><TD COLSPAN="10" BGCOLOR="gold"><B>Matriz Reducida Sensores de Cultivo Fr[n,t]</B></TD></TR>
        <TR><TD BGCOLOR="lightgray"><B>Estación Agrupada</B></TD>
    '''
    
    # Obtener sensores de cultivo para encabezados
    sensores_cultivo = []
    actual_sensor = campo.sensores_cultivo.primero
    while actual_sensor is not None:
        sensores_cultivo.append(actual_sensor.sensor_cultivo)
        html_content += f'<TD BGCOLOR="gold"><B>{actual_sensor.sensor_cultivo.nombre}</B></TD>'
        actual_sensor = actual_sensor.siguiente
    html_content += '</TR>'
    
    # Filas de estaciones agrupadas para sensores de cultivo
    actual_est = campo.estaciones.primero
    while actual_est is not None:
        estacion = actual_est.estacion
        html_content += f'<TR><TD BGCOLOR="lightgray"><B>{estacion.nombre}</B></TD>'
        
        for sensor in sensores_cultivo:
            valor = obtener_frecuencia(sensor, estacion.id)
            html_content += f'<TD BGCOLOR="lightsteelblue"><B>{valor}</B></TD>'
        
        html_content += '</TR>'
        actual_est = actual_est.siguiente
    
    html_content += '</TABLE>>'
    
    # Crear nodo con tabla HTML
    dot.node('matriz', html_content, shape='plaintext')

def obtener_frecuencia(sensor, id_estacion):
    """Función auxiliar para obtener el valor de frecuencia de un sensor para una estación específica"""
    actual_freq = sensor.frecuencias.primero
    while actual_freq is not None:
        freq = actual_freq.frecuencia
        if freq.id_estacion == id_estacion:
            return freq.valor
        actual_freq = actual_freq.siguiente
    return 0