import os

def leer_relevancia(ruta_med_rel):
    relevancia = {} # Diccionario para almacenar la relevancia
    with open(ruta_med_rel, 'r') as f: 
        for linea in f:
            consulta, _, documento, _ = map(int, linea.split()) # Leer la línea y separar los valores, valores se convierten a enteros
            if consulta not in relevancia: # Si la consulta no está en el diccionario, inicializarla
                relevancia[consulta] = set()
            relevancia[consulta].add(documento) # Agregar el documento a la lista de documentos relevantes
    return relevancia

def leer_cosenos(ruta_cosenos):
    cosenos = {} #Los cosenos estan en formato consulta documento similitud
    with open(ruta_cosenos, 'r') as f:
        for linea in f:
            consulta, documento, similitud = linea.split()
            consulta, documento = int(consulta), int(documento)
            similitud = float(similitud)
            if consulta not in cosenos: # Si la consulta no está en el diccionario, se inicializa
                cosenos[consulta] = []
            cosenos[consulta].append((documento, similitud)) # Agregar el documento y su similitud a la lista de documentos similares
    return cosenos

def calcular_metricas(relevancia, cosenos, z): #Recibe la relevancia, los cosenos y el valor de Z
    resultados = {} # Diccionario para almacenar los resultados
    for consulta, documentos_similares in cosenos.items(): #Para cada consulta en los cosenos
        documentos_similares.sort(key=lambda x: x[1], reverse=True)  # Ordenar por similitud descendente
        documentos_recuperados = [doc for doc, _ in documentos_similares[:z]] # Recuperar los Z documentos más similares
        documentos_relevantes = relevancia.get(consulta, set()) # Obtener documentos relevantes para la consulta

        # Calcular métricas
        tp = len(set(documentos_recuperados) & documentos_relevantes)  # Verdaderos positivos - Documentos relevantes recuperados
        
        #Precision: Documentos relevantes recuperados / Total de documentos recuperados
        precision = tp / len(documentos_recuperados) if documentos_recuperados else 0
        #Recuerdo: Documentos relevantes recuperados / Total de documentos relevantes
        recuerdo = tp / len(documentos_relevantes) if documentos_relevantes else 0
        #Media F: 2 * (Precision * Recuerdo) / (Precision + Recuerdo)
        media_f = (2 * precision * recuerdo / (precision + recuerdo)) if (precision + recuerdo) > 0 else 0
        #Precisión R a Z: Documentos relevantes recuperados / Total de documentos consultados
        precision_r_a_z = tp / z if z > 0 else 0
        
        #Diccionartio para almacenar los resultados de cada consulta
        resultados[consulta] = {
            'Precisión': precision,
            'Recuerdo': recuerdo,
            'Media F': media_f,
            'Precisión R a Z': precision_r_a_z
        }
    return resultados

# Main
# Definir rutas de archivos
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_med_rel = os.path.join(ruta_base, "MED.REL")
ruta_cosenos = os.path.join(ruta_base, "Cosenos.txt")
z = int(input("Ingrese el valor de Z: "))

# Leer archivos
relevancia = leer_relevancia(ruta_med_rel)
cosenos = leer_cosenos(ruta_cosenos)
resultados = calcular_metricas(relevancia, cosenos, z)

# Mostrar resultados a consola
# for consulta, metricas in resultados.items():
#     print(f"Consulta {consulta}:")
#     for metrica, valor in metricas.items():
#         print(f"  {metrica}: {valor:.4f}")

# Guardar resultados en un archivo en formato tabular
ruta_resultados = os.path.join(ruta_base, "Resultados.txt")
with open(ruta_resultados, 'w') as f:
    # Escribir encabezados
    f.write("Consulta\tPrecisión\tRecuerdo\tMedia F\tPrecisión R a Z\n")
    for consulta, metricas in resultados.items():
        f.write(f"{consulta:02}\t\t\t\t{metricas['Precisión']:.4f}\t\t{metricas['Recuerdo']:.4f}\t"
                f"{metricas['Media F']:.4f}\t{metricas['Precisión R a Z']:.4f}\n")