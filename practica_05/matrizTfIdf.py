import numpy as np
import os
import pandas as pd
ruta_base = os.path.dirname(os.path.abspath(__file__))
#Documentos de salida
ruta_salida_tf = os.path.join(ruta_base, "matriz_tf.csv")
ruta_salida_tf_idf = os.path.join(ruta_base, "matriz_tf_idf.csv")
ruta_salida_qry_tf = os.path.join(ruta_base, "matriz_qry_tf.csv")
ruta_salida_qry_tf_idf = os.path.join(ruta_base, "matriz_qry_tf_idf.csv")
#Documentos de entrada
ruta_vocabulario = os.path.join(ruta_base, "Vocabulario.txt")
ruta_consultas = os.path.join(ruta_base, "ConsultasPreProcesadas.txt")
ruta_documentos = os.path.join(ruta_base, "DocumentosPreProcesados.txt")

# Cargar vocabulario (una palabra por línea)
def cargar_vocabulario(path):
    with open(path, 'r', encoding='utf-8') as f:
        vocabulario = [line.strip().lower() for line in f]
    return vocabulario

# Leer documentos desde archivo con formato: id | texto
def cargar_documentos(path):
    documentos = []
    with open(path, 'r', encoding='utf-8') as f:
        for linea in f:
            _, texto = linea.strip().split('|', 1)
            palabras = texto.lower().split()  # Tokenización
            documentos.append(palabras)
    return documentos

# Calcular matriz TF
def calcular_tf_por_vocabulario(documentos, vocabulario):
    num_docs = len(documentos)
    num_palabras = len(vocabulario)
    matriz_tf = np.zeros((num_docs, num_palabras), dtype=int)

    for j, palabra in enumerate(vocabulario):  # por cada palabra del vocabulario
        for i, doc in enumerate(documentos):   # por cada documento
            matriz_tf[i][j] = doc.count(palabra)  # cuántas veces aparece esa palabra en ese documento
    return matriz_tf

# Calcular IDF para cada palabra del vocabulario
def calcular_idf(documentos, vocabulario):
    num_docs = len(documentos)
    idf = np.zeros(len(vocabulario))

    for j, palabra in enumerate(vocabulario):
        df = sum(1 for doc in documentos if palabra in doc) #documentos que contienen la palabra
        if df > 0:
            idf[j] = np.log(num_docs / df) + 1 #si es mayor a 0 se calcula el idf - es el num de documentos / df
        
        else:
            idf[j] = 0.0  # o np.log(num_docs), pero depende del tratamiento de palabras ausentes
            
        if palabra == "abdomen":
            print(f"DF de 'abdomen': {df}")
            print(f"IDF de 'abdomen': {idf[j]}")
    return idf

# Guardar matriz TF
def guardar_matriz_tf(matriz, salida):
    np.savetxt(salida, matriz, fmt='%d', delimiter=',')

# Guardar matriz TF-IDF
def guardar_matriz_idf(matriz, salida):
    np.savetxt(salida, matriz, fmt='%.6f', delimiter=',')
    
# Calcular matriz TF-IDF
def calcular_tfidf(matriz_tf, idf):
    return matriz_tf * idf  # broadcasting de NumPy


# Main
#Carga de documentos
vocabulario = cargar_vocabulario(ruta_vocabulario)
documentos = cargar_documentos(ruta_documentos)
consultas = cargar_documentos(ruta_consultas)

#Matices tf
matriz_tf = calcular_tf_por_vocabulario(documentos, vocabulario)
matriz_qry_tf = calcular_tf_por_vocabulario(consultas, vocabulario)

#Matrices tf-idf
idf = calcular_idf(documentos, vocabulario)
idf_qry = calcular_idf(consultas, vocabulario)
matriz_tfidf = calcular_tfidf(matriz_tf, idf)
matriz_qry_tfidf = calcular_tfidf(matriz_qry_tf, idf)

#Guardar matrices
guardar_matriz_tf(matriz_tf, ruta_salida_tf) #Documentos
guardar_matriz_idf(matriz_tfidf, ruta_salida_tf_idf)
guardar_matriz_tf(matriz_qry_tf, ruta_salida_qry_tf) #Consultas
guardar_matriz_idf(matriz_qry_tfidf, ruta_salida_qry_tf_idf)
