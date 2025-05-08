import pandas as pd
import numpy as np
import os

#Rutas
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_documentos = os.path.join(ruta_base, "matriz_tf.csv")
ruta_qry = os.path.join(ruta_base, "matriz_qry_tf.csv")
ruta_cosenos = os.path.join(ruta_base, "Cosenos.txt")

#Leemos los CSV sin cabecera ni índice para que no se omitan datos
tfidf_documentos = pd.read_csv(ruta_documentos, header=None, index_col=None)
tfidf_qry = pd.read_csv(ruta_qry, header=None, index_col=None)

#Pasar a matrices numpy
matriz_doc = tfidf_documentos.values
matriz_qry = tfidf_qry.values

coseno = np.dot(matriz_doc, matriz_qry.T) / (np.linalg.norm(matriz_doc, axis=1, keepdims=True) * np.linalg.norm(matriz_qry, axis=1, keepdims=True).T)

#Guardar el coseno en archivo
# Recolectar todas las líneas primero
lineas = []

for indice_qry, row in enumerate(coseno):  # Recorremos desde cada consulta
    qryId = indice_qry + 1  # Guardamos como entero

    orden_indices = np.argsort(row)[::-1]  # Ordenar de mayor a menor
    for indice_doc in orden_indices:
        sim = row[indice_doc]
        if sim > 0:
            docId = indice_doc + 1
            lineas.append((docId, qryId, sim))

# Ordenar las líneas por docId (primer valor de cada tupla)
lineas.sort(key=lambda x: x[0])

# Escribir el archivo con el nuevo orden y formato
with open(ruta_cosenos, "w") as f:
    for docId, qryId, sim in lineas:
        f.write(f"{docId} {qryId} {sim:.8f}\n")

