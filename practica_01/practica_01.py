#signos de puntuacion 

import re
import string

with open('fairytales.txt') as archivo:
    contenido = archivo.read()

print("\nPalabras separadas:")
words = contenido.split()
print(words[3000:3100])

#print(string.punctuation)

re_punc = re.compile('[%s]' % re.escape(string.punctuation))
stripped = [re_punc.sub("",w) for w in words]

print("\nPalabras sin puntuacion:")
print(stripped[3000:3100])

stripped = [re_punc.sub("",w) for w in words]

print("\nPalabras con guiones en lugar de puntuacion:")
stripped = [re_punc.sub("----",w) for w in words]
print(stripped[3000:3100])

print("\nTexto en minusculas y sin puntuacion:")
stripped = [re_punc.sub("",w).lower() for w in words]
print(stripped[3000:3100])