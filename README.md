# AEPython

Repositorio para el contenido del curso de **Análisis Espacial con Python** del Gabinete de Formación del CSIC (Estación Biológica de Doñana, Sevilla. 23-27/09/2024).

### Temario

## Día 1: Introducción al entorno Jupyter (Colab) y a Python

Hemos trabajado sobre todo en Google Colab. La conclusión más clara es que la IA cambia todo o casi todo y la integración de Gemini con los notebooks funciona perfectamente (demasiado bien...).

En la segunda mitad hemos visto una (muy) breve introducción a Python en la que hemos visto los tipos de datos principales:  

* Creación de variables
* Strings
* Numbers
* Booleans
* Listas
* Tuplas
* Sets
* Diccionarios
* Bucles while y for
* Condicionales
* Manejo de errores
* Funciones
* Modulos
* Lectura y creación de archivos de texto
* Clases

Y, "como siempre ha sido", hemos terminado creando un script con el que jugar al juego popularizado por The Big Bang Theory  ***Rock, Paper, Scissors, Lizard, Spock***. En el archivo .ipynb se añade un ejemplo con un par de funciones más para seguir jugando sin tener que volver a ejecutar la celda. También se ha añadido la opción de sustituir los condicionales por un diccionario (+ pythonic).

[Notebook día 1. Intro Python](https://github.com/Digdgeo/AEPython_2024/blob/main/D%C3%ADa%201/Day1_Completo.ipynb)

![](https://i.imgur.com/IZD1dlL.png)

## Día 2: Intro a Teledetección y Análisis Vectorial

En el segundo día del curso hemos hecho un breve repaso a las clases en Python, introduciendo también la herencia por si acaso podemos hacer una clase "satélites" de la que hereden las clases Landsat y Sentinel 2.

Por un cambio, que no ha salido muy bien, hemos pasado a ver análisis vectorial antes de análisis raster. Usando sobre todo los ejemplos de shapely para ver las operaciones básicas con geometrías vectoriales.
También hemos visto como trabajar con shapefiles desde Geopandas (aspect=1 :())

[Notebook día 2.Python Classes](https://github.com/Digdgeo/AEPython_2024/blob/main/D%C3%ADa2/Python_Clasess.ipynb)

[Notebook día 2. Vectorial](https://github.com/Digdgeo/AEPython_2024/blob/main/D%C3%ADa2/Dia_2_Vectorial.ipynb)

![](https://i.imgur.com/mcWcZYY.png)

## Día 3: Análisis Vectorial (Fiona) y scripts mlip.py y rmpip.py

La idea es seguir con el análisis vectorial con Fiona y ver dos scripts más complejos: Uno para obtener las líneas máximas dentro de polígonos y otro para mover aleatoriamente grupos de puntos en un marco envolvente.

Si hay tiempo veremos la intro a Numpy y a Rasterio antes de dedicar el día de mañana a las clases para trabajar con imágenes satélites.

[Notebook dia 3. Fiona](https://github.com/Digdgeo/AEPython_2024/blob/main/D%C3%ADa3/Dia_3_vectorial_fiona.ipynb)

![](https://i.imgur.com/Xohn1H2.png)
