import pandas as pd
import os

def leer_relevancia(ruta_med_rel):
    relevancia = {}
    with open(ruta_med_rel, 'r') as f:
        for linea in f:
            consulta, _, documento, _ = map(int, linea.split())
            if consulta not in relevancia:
                relevancia[consulta] = set()
            relevancia[consulta].add(documento)
    return relevancia

def leer_cosenos(ruta_cosenos):
    cosenos = {}
    with open(ruta_cosenos, 'r') as f:
        for linea in f:
            consulta, documento, similitud = linea.split()
            consulta, documento = int(consulta), int(documento)
            similitud = float(similitud)
            if consulta not in cosenos:
                cosenos[consulta] = []
            cosenos[consulta].append((documento, similitud))
    return cosenos

def calcular_metricas(relevancia, cosenos, z):
    resultados = {}
    for consulta, documentos_similares in cosenos.items():
        documentos_similares.sort(key=lambda x: x[1], reverse=True)  # Ordenar por similitud
        documentos_recuperados = [doc for doc, _ in documentos_similares[:z]]
        documentos_relevantes = relevancia.get(consulta, set())

        # Calcular métricas
        tp = len(set(documentos_recuperados) & documentos_relevantes)  # Verdaderos positivos
        fp = len(documentos_recuperados) - tp  # Falsos positivos
        fn = len(documentos_relevantes) - tp  # Falsos negativos

        precision = tp / len(documentos_recuperados) if documentos_recuperados else 0
        recuerdo = tp / len(documentos_relevantes) if documentos_relevantes else 0
        media_f = (2 * precision * recuerdo / (precision + recuerdo)) if (precision + recuerdo) > 0 else 0

        resultados[consulta] = {
            'Precisión': precision,
            'Recuerdo': recuerdo,
            'Media F': media_f,
            'Precisión R a Z': precision
        }
    return resultados

# Main
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_med_rel = os.path.join(ruta_base, "MED.REL")
ruta_cosenos = os.path.join(ruta_base, "Cosenos.txt")
z = int(input("Ingrese el valor de Z: "))

relevancia = leer_relevancia(ruta_med_rel)
cosenos = leer_cosenos(ruta_cosenos)
resultados = calcular_metricas(relevancia, cosenos, z)

# Mostrar resultados
for consulta, metricas in resultados.items():
    print(f"Consulta {consulta}:")
    for metrica, valor in metricas.items():
        print(f"  {metrica}: {valor:.4f}")