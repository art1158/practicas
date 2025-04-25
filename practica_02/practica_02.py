#stemming 

import re
import string
#librerias para stemming y palabras vacias
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import nltk

#por si no estan ya listas las stopwords de nltk
nltk.download('stopwords')

#cargamos el archivo
with open('PRACTICAS/practica_02/fairytales.txt', encoding='utf-8') as archivo:
    contenido = archivo.read()

#lo pasamos a minusculas
contenido = contenido.lower()

#Separamos las palabras con espacios y mostramos las primeras 100
print("\n\n\nPalabras separadas")
words = contenido.split()
print(words[0:100])  

#Cargamos las palabras vacias
stop_words = set(stopwords.words('english'))

#Expresion regular para eliminar signos de puntuacion
re_punc = re.compile(f'[{re.escape(string.punctuation)}]')
#Reemplazamos signos por espacio vacio
stripped = [re_punc.sub("", w) for w in words]

#Filtramos para eliminar las palabras vacias
filtered_words = [word for word in stripped if word not in stop_words]


#Aplicamos Stemmer
porter = PorterStemmer()
stemmed_words = [porter.stem(stripped_word) for stripped_word in filtered_words]
print("\n\nPalabras después del stemming con Porter")
print(stemmed_words[0:100])

#Aplicamos Snowball para comparar resultados
snowball = SnowballStemmer('english')
snowball_words = [snowball.stem(stripped_word) for stripped_word in filtered_words]
print("\n\nPalabras después del stemming con Snowball")
print(snowball_words[0:100])
