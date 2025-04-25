import nltk
import re
import string
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

#Esto es para obtener la direccion actual de los directorios para que no haya problemas al generar los archivos
import os


#Funcion reutilizable para preprocesamiento y guardado en: extraccion y limpieza
def procesar_archivo_entrada(ruta_entrada, ruta_salida_bruto):
    snow = SnowballStemmer("english")
    index = None
    content = []
    formatted_lines = []


    # Leer el archivo convertido a minusculas línea por línea
    with open(ruta_entrada,"r", encoding="utf-8") as archivo:
        contenido = [line.lower().strip() for line in archivo.readlines()]


    for line in contenido:
        if line.startswith(".i"):  # Si la línea indica un nuevo índice
            if index is not None and content:
                formatted_lines.append(f"{index} | {' '.join(content)}")  # Guardamos el anterior

            index = line.split()[1]  # Extraemos el número después de ".i"
            content = []  # Reiniciamos el contenido

        elif line.startswith(".w"):  # Si la línea es ".w", la ignoramos
            continue

        else:  # Si es contenido, lo agregamos a la lista `content`
            content.append(line)

    # Agregar la última entrada al resultado
    if index is not None and content:
        formatted_lines.append(f"{index} | {' '.join(content)}")



    with open(ruta_salida_bruto,"w") as salida:
        for cadaLinea in formatted_lines:
            print(cadaLinea)
            salida.write(cadaLinea+"\n")

def preprocesar_texto(ruta_entrada, ruta_salida_preprocesado):
    snow = SnowballStemmer("english")
    # instancia para cargar als palabras vacias que vamos a eliminar
    stop_w = set(stopwords.words("English"))
    # Crear la expresión regular para eliminar puntuación, signos y números, donde la expresion regular [0-9] quita numeros y la funcion punctutation quita todos los signos
    # Quitamos puntuación (excepto el guion "-") y números
    re_punc = re.compile('[%s0-9]' % re.escape(string.punctuation.replace("-", "")))

    with open(ruta_entrada, "r", encoding="utf-8") as nuevoCargaDocumento, open(ruta_salida_preprocesado, "w",encoding="utf-8") as salidaDocumento:
        for linea in nuevoCargaDocumento:
            partes = linea.strip().split("|",1) # con esto esperamos eliminar espacios y saltos con strip y con split la creacion de una lista de palabras siguiendo el formato
            if len(partes) == 2:
                index, texto = partes # extraemos los valores diferentes

                #Tokenizar palabras (separarlas en una lista)
                palabras = texto.split()
                #Aqui hacemos uso de nuestra expresion regular y el escape de signos que cambiamos por espacios vacios
                palabras_limpias = [re_punc.sub("", word.replace("-"," ")) for word in palabras] #se cambian guiones por espacios

                #quitamos las palabras vacias y aplicamos snowball
                palabrasproceso = [snow.stem(word) for word in palabras_limpias if word not in stop_w]

                #ordenamos
                texto_ordenado_modificado = " ".join(palabrasproceso)

                #volvemos a guardar en el mismo formato
                salidaDocumento.write(f"{index} | {texto_ordenado_modificado}\n")

# Rutas base
ruta_base = os.path.dirname(os.path.abspath(__file__))

# Rutas de entrada
ruta_med = os.path.join(ruta_base, "med", "MED.ALL")
ruta_qry = os.path.join(ruta_base, "med", "MED.QRY")

# Rutas de salida
ruta_guardar_med = os.path.join(ruta_base, "Documentos.txt")
ruta_guardar_qry = os.path.join(ruta_base, "Consultas.txt")

ruta_salida_med = os.path.join(ruta_base, "DocumentosPreProcesados.txt")
ruta_salida_qry = os.path.join(ruta_base, "ConsultasPreProcesadas.txt")

# Procesamiento
procesar_archivo_entrada(ruta_med, ruta_guardar_med)
procesar_archivo_entrada(ruta_qry, ruta_guardar_qry)

preprocesar_texto(ruta_guardar_med, ruta_salida_med)
preprocesar_texto(ruta_guardar_qry, ruta_salida_qry)  