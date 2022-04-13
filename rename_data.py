# -*- coding: utf-8 -*-

#%%

unzip -q "/data.zip" -d "/"
#%%

import shutil
import os
import cv2 as cv 
path_raiz = './data'

i_total = 0

with os.scandir(path_raiz) as ficheros:

    for clase in ficheros:
        i = 0
        path_carpeta_clase = './data' + '/' + clase.name
        path_carpeta_clase_new = './data_new' + '/' + clase.name + '/'
        
        with os.scandir(path_carpeta_clase) as ficheros:
          for web in ficheros:
            if os.path.isdir(web):
              path_carpeta_clase_webs = path_carpeta_clase + '/' + web.name
            #print(path_carpeta_clase_webs)

            with os.scandir(path_carpeta_clase_webs) as ficheros:
              for especie in ficheros:
                  path_carpeta_clase_web_especie = path_carpeta_clase_webs + "/" + especie.name
                  #print(path_carpeta_clase_web_especie)
                  #print("Clase " + clase.name + " de la web " + web.name + " de la especie " + especie.name)
                  for item in os.listdir(path_carpeta_clase_web_especie):
                  
                    nombre_absoluto_archivo = path_carpeta_clase_web_especie + "/" + item
                    #nombre_nuevo_archivo = clase.name + "_" + especie.name +  "_" + str(i_total) + ".jpg"
                    #print(nombre_nuevo_archivo)
                    #nombre_nuevo_archivo = path_carpeta_clase + '/' + clase.name + item
                    #os.rename(nombre_absoluto_archivo, nombre_nuevo_archivo)
                    file_name = os.path.join(path_carpeta_clase_web_especie, item)
                    #print(nombre_absoluto_archivo)
                    img = cv.imread(file_name)
                    channels = img.shape[-1] if img.ndim == 3 else 1
                    if (channels == 1):
                      print(file_name)
                    os.makedirs(os.path.dirname(path_carpeta_clase_new), exist_ok=True)
                    shutil.move(file_name, path_carpeta_clase_new)
                    i = i + 1
                    i_total = i_total + 1

        print ("Clase", clase.name, "- número de imágenes de la clase: ", i)
                    
print("Total de imágenes: ", i_total)

#%%
