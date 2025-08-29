from utils.xmlReader import leer_campos_xml
from utils.xmlWritter import escribir_campos_xml
from utils.procesador import procesar_campos
from utils.graphviz_generator import generar_grafica
import os
import sys  # Added sys import for proper exit

campos = None

def mostrar_datos_estudiante():
    print("\n--- Datos del Estudiante ---")
    print("➢ Erwin Alejandro Giron Menéndez")
    print("➢ 202405935")
    print("➢ Introducción a la Programación y Computación 2")
    print("➢ B-")
    print("➢ 4to. Semestre")
    print("➢ [Enlace a tu documentación]")

def seleccionar_campo_para_grafica():
    if campos is None or campos.primero is None:
        print("No hay campos cargados. Por favor, cargue el archivo XML primero.")
        return None
    
    print("\n--- Campos Disponibles ---")
    actual = campos.primero
    contador = 1
    while actual is not None:
        campo = actual.campo
        print(f"{contador}. {campo.nombre} (ID: {campo.id})")
        actual = actual.siguiente
        contador += 1
    
    try:
        opcion = int(input("Seleccione el número del campo: "))
        actual = campos.primero
        contador = 1
        while actual is not None:
            if contador == opcion:
                return actual.campo
            actual = actual.siguiente
            contador += 1
        print("Opción no válida.")
        return None
    except ValueError:
        print("Por favor ingrese un número válido.")
        return None

def showMenu():
    global campos
    
    while True:  # Changed to infinite loop with explicit break
        print("\n==== SISTEMA DE AGRICULTURA DE PRECISIÓN ====")
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar gráfica")
        print("6. Salida")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("Opción cargar archivo")
            archivo_completo = input("Ingrese la ruta completa del archivo (ej: ./archivoPrueba.xml o C:\\ruta\\archivo.xml): ")
            
            print(f"Cargando datos desde {archivo_completo}...")
            campos = leer_campos_xml(archivo_completo)
            if campos:
                print("Datos cargados exitosamente.")
            else:
                print("Error al cargar los datos.")
        
        elif opcion == '2':
            if campos is None:
                print("No hay datos cargados. Por favor, cargue el archivo XML primero.")
            else:
                print("Procesando archivo...")
                procesar_campos(campos)
                print("Procesamiento completado exitosamente.")
        
        elif opcion == '3':
            if campos is None:
                print("No hay datos procesados. Por favor, cargue y procese el archivo primero.")
            else:
                print("Opción generar archivo de salida")
                archivo_salida = input("Ingrese la ruta completa del archivo de salida: ")
                ruta = os.path.dirname(archivo_salida)
                nombre_archivo = os.path.basename(archivo_salida)
                if not nombre_archivo:
                    nombre_archivo = "salida.xml"
                escribir_campos_xml(campos, ruta, nombre_archivo)
        
        elif opcion == '4':
            mostrar_datos_estudiante()
        
        elif opcion == '5':
            campo_seleccionado = seleccionar_campo_para_grafica()
            if campo_seleccionado:
                print("\nTipos de matriz disponibles:")
                print("1. Matriz de frecuencias")
                print("2. Matriz de patrones")
                print("3. Matriz reducida")
                
                try:
                    tipo_opcion = int(input("Seleccione el tipo de matriz: "))
                    tipo_matriz = ""
                    if tipo_opcion == 1:
                        tipo_matriz = "frecuencia"
                    elif tipo_opcion == 2:
                        tipo_matriz = "patron"
                    elif tipo_opcion == 3:
                        tipo_matriz = "reducida"
                    
                    if tipo_matriz != "":
                        print(f"Generando gráfica de {tipo_matriz} para {campo_seleccionado.nombre}...")
                        generar_grafica(campo_seleccionado, tipo_matriz)
                    else:
                        print("Opción no válida.")
                except ValueError:
                    print("Por favor ingrese un número válido.")
        
        elif opcion == '6':
            print("¡Gracias por usar el Sistema de Agricultura de Precisión!")
            print("Saliendo del programa...")
            sys.exit(0)
        
        else:
            print("Opción no válida. Intente de nuevo.")