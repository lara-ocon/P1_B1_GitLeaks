# Practica1_bloque1

Hecho por: Lara Ocón Madrid


En esta práctica hemos hecho un buscador de leaks en mensajes de commits de un repositorio de git. Para ello, primero tendremos que instalar los paquetes necesarios especificados en requirements.txt y después lanzar el programa git_leaks.py.

El programa en sí consiste en una ETL que, en primer lugar, clona el siguiente repositorio:
'https://github.com/skalenetwork/skale-manager' dentro de la carpeta skale/skale-manager dentro
del directorio en el que estemos trabajando. (Antes de clonarlo, comprueba que este directorio
no esté ya clonado en nuestro ordenador, pues en caso de estarlo, no hará nada).

En segundo lugar, creamos la lista de las palabras que vamos a buscar en los mensajes de commits del repositorio en cuestión. Tras esto, con la librería tkinter crea una barra de  progreso que iniciará la ETL, mostrando así el avance de este. 

Nuestra ETL consistirá en: 
1) Extracción de datos: Cargamos el repositorio a través de su path. (Una vez completado esto, ya llevaremos 1/3 de nuestra barra de progreso).

2) Transformación de datos: Buscamos, mediante expresiones regulares, dentro de los mensajes de commits del repo las palabras clave y vamos guardando dichos mensajes en una lista. (Finalizado esto, sumamos 1/3 a nuestra barra de progreso).

3) Carga de datos: Cargamos nuestros datos (la lista que nos ha pasado la fase de transformación) imprimiéndolos por pantalla y también agregándolos a un dataframe de pandas. Finalmente guardamos el dataframe en un csv y la barra de progreso habrá finalizado.
