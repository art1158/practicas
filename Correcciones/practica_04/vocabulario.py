#Rutas
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_vocabulario = os.path.join(ruta_base, "Vocabulario.txt")
ruta_documentos = os.path.join(ruta_base, "DocumentosPreProcesados.txt")

# Abrir el archivo de entrada
with open(ruta_documentos, 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Obtener todas las palabras únicas de la colección (de 2 o más letras)
vocabulario = set()
for linea in lineas:
    partes = linea.split('|')
    if len(partes) < 2:
        continue  # Saltar líneas mal formateadas
    
    palabras = partes[1].strip().lower().split()
    palabras_filtradas = [p for p in palabras if len(p) >= 2]  # Filtrar palabras con 2 o más letras
    vocabulario.update(palabras_filtradas)

# Ordenar el vocabulario y obtener su longitud
vocabulario_ordenado = sorted(vocabulario)
longitud_vocabulario = len(vocabulario_ordenado)

with open(ruta_vocabulario, 'w', encoding='utf-8') as f:
    f.write('\n'.join(vocabulario_ordenado) + '\n')

print("Longitud del vocabulario:", longitud_vocabulario)

