#! user/bin/python3 

# Buscador de leaks en commits de git - Adquisición de Datos - iMat
# Lara Ocón Madrid - 202115710


# Importamos las librerías necesarias
from git import Repo

import re, signal, sys , time, os

import pandas as pd

from tkinter import *
from tkinter import ttk



def handler_signal(signal, frame):
    # Controlamos la señal de control C, para salir correctamente del programa

    print("\n\n [!] Out .......\n")
    sys.exit(1)


def step():
    # Esta funcion muestra el progreso del programa, imprimiendo
    # dicho progreso en una barra que se va actualizando a medida
    # que superamos las fases de la ETL

    my_progress['value'] += 0
    my_label.config(text= "Iniciando ETL")
    root.update()
    time.sleep(1)

    # EXTRACCIÓN DE DATOS ======================================#
    # extraemos los datos del directorio y actualizamos la barra 
    # de progreso un 33%
    commit_messages = extract(REPO_DIR)
    my_progress['value'] += 100 / 3
    my_label.config(text= "Datos extraídos")
    root.update()
    time.sleep(1)

    # TRANSFORMACIÓN DE LOS DATOS ==============================#
    # Transformamos los datos obteniendo los leaks en los mensajes 
    # de commits que contengan las palabras clave. Una vez hecho esto
    # actualizamos la barra de progreso sumando un 33%
    leaks_encontrados = transform(commit_messages, kwords)
    my_progress['value'] += 100 / 3
    my_label.config(text= "Datos transformados")
    root.update()
    time.sleep(1)

    # CARGA DE DATOS ==========================================#
    # Cargamos los datos imprimiéndolos por pantalla y una vez hecho
    # esto, actualizamos la barra de progreso y esperamos 3 segundos
    # para cerra la ventana de dicha barra
    load(leaks_encontrados)
    my_progress['value'] += 100 / 3
    my_label.config(text= "Finalizada carga de datos")
    root.update()
    time.sleep(3)

    sys.exit(1)
    

def extract(url):
    # Función de extracción: creamos el repositorio para trabajar
    # y devolvemos una lista con los commits en la rama develop

    repo = Repo(url)
    lista = list(repo.iter_commits('develop'))

    return lista


def transform(lista_commits, kwords):
    # Finción transformación: Recorremos los mensaje de commits en 
    # busca de las palabras clave y guardamos los mensajes que 
    # contengan dichas palabras en una lista que devolveremos como 
    # output

    leaks_encontrados = []

    for commit in lista_commits:
        for kword in kwords:
            if re.search(kword, commit.message, re.I):
                leaks_encontrados.append(commit.message)

    return leaks_encontrados 


def load(leaks_encontrados):
    # Función carga: cargamos los datos imprimiéndolos por pantalla
    # y guardandolos en un dataframe para después pasarlo a csv
    df = pd.DataFrame()
    print("\n"+"\033[1;31m"+"Leaks encontrados:"+"\033[0;m"+"\n")
    i = 0
    for leak in leaks_encontrados:
        i += 1
        print(f"{i}) {leak}")
        df.loc[len(df.index), 'Leaks'] = [leak]
    
    # exportamos el dataframe a un csv
    df.to_csv("leaks_encontrados.csv")


if __name__ == "__main__":

    # Controlamos la señal de control C, para salir correctamente del programa
    signal.signal(signal.SIGINT, handler_signal)


    url = 'https://github.com/skalenetwork/skale-manager'

    # Clonamos el repositorio (si no existe) dentro de la carpeta skale
    REPO_DIR = "./skale/skale-manager"
    if not os.path.exists(REPO_DIR):
        Repo.clone_from(url, 'skale/skale-manager')


    # Introducimos las palabras clave que queremos buscar en los mensajes de commits
    kwords = ['credentials', 'password','key']

    # Creamos la ventana de progreso
    root = Tk()
    root.title('ETL leaks en commits')
    root.geometry("500x200")
    
    # Barra de progreso, esta se irá actualizando a medida que superamos
    # las distintas fases de la ETL
    my_progress = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
    my_progress.pack(pady=20)

    my_label = Label(root, text=" ")
    my_label.pack(pady=20)

    # Botón para iniciar la ETL
    my_button = Button(root, text = "Iniciar ETL", command=step)
    my_button.pack(pady=20)

    
    root.mainloop()
