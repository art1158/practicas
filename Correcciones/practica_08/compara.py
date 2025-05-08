import pandas as pd
import os

# Rutas
ruta_base = os.path.dirname(os.path.abspath(__file__))

ruta_tf = os.path.join(ruta_base, "Resultados.txt")
ruta_idf = os.path.join(ruta_base, "ResultadosIDF.txt")

# Leemos los CSV especificando que las columnas están separadas por tabulaciones
tf = pd.read_csv(ruta_tf, sep='\t', skiprows=1, encoding='utf-8', header=None)
idf = pd.read_csv(ruta_idf, sep='\t', skiprows=1, encoding='latin-1', header=None)

# Accedemos a la columna después de la cuarta tabulación (índice 4)
precision_tf = pd.to_numeric(tf.iloc[:, 4], errors='coerce')
precision_idf = pd.to_numeric(idf.iloc[:, 4], errors='coerce')

promedios_tf = precision_tf.mean()
promedios_idf = precision_idf.mean()

diferencia = precision_idf - precision_tf
promedio_diferencia = diferencia.mean()

resultados = pd.DataFrame({
    "Precision TF": precision_tf,
    "Precision IDF": precision_idf,
    "Diferencia (IDF - TF)": diferencia
})

print("Resultados:")
print(resultados)
print(f"\nPromedios: {promedios_tf:.4f}        {promedios_idf:.4f}                   {promedio_diferencia:.2f}")

