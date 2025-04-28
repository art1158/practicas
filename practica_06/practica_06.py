import pandas as pd
import numpy as np
import os

#Rutas
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_documentos = os.path.join(ruta_base, "matriz_tf_idf.csv")
ruta_qry = os.path.join(ruta_base, "matriz_qry_tf_idf.csv")
ruta_cosenos = os.path.join(ruta_base, "Cosenos.txt")

#Leemos los CSV sin cabecera ni índice para que no se omitan datos
tfidf_documentos = pd.read_csv(ruta_documentos, header=None, index_col=None)
tfidf_qry = pd.read_csv(ruta_qry, header=None, index_col=None)

#Pasar a matrices numpy
matriz_doc = tfidf_documentos.values
matriz_qry = tfidf_qry.values

coseno = np.dot(matriz_doc, matriz_qry.T) / (np.linalg.norm(matriz_doc, axis=1, keepdims=True) * np.linalg.norm(matriz_qry, axis=1, keepdims=True).T)

#Guardar el coseno en archivo
with open(ruta_cosenos, "w") as f:
    for indice_qry, row in enumerate(coseno): #Recorremos desde cada consulta
        qryId = f"{indice_qry+1:02}"
        
        # Ordenar las similitudes y sus índices de documento de mayor a menor
        orden_indices = np.argsort(row)[::-1]  # Devuelve los índices ordenados de mayor a menor
        
        for indice_doc in orden_indices: #Para revisar todas las similitudes que tenga en cada documento
            sim = row[indice_doc] #Accedemos a las filas de similitud pero ya ordenadas

            if sim > 0:
                docId = f"{indice_doc+1}"
                f.write(f"{qryId:02} {docId} {sim:.4f}\n")
