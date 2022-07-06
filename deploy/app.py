# Jacobo Casado de Gracia - Archivo app.py 
# Carga del mejor modelo y montaje en una interfaz web sencilla utilizando Flask.

import os
import sys

# Importacion de sublibrerias necesarias de flask 
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from skimage.io import imread

# Importacion de sublibrerias necesarias de Tensorflow y Keras.
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

# Importacion de algunas utilidades necesarias.
import numpy as np
from util import base64_to_pil

#Importacion de la libreria EfficientNet.
import efficientnet.keras as eff

# Declaramos una APP de Flask
app = Flask(__name__)

# PATH DEL MODELO QUE SE CARGARÁ EN LA WEB. Este es el modelo lanzado a producción.
MODEL_PATH = 'models/effnetv2.h5'

# CARGA DE ESTE MODELO.
model = load_model(MODEL_PATH)
model.make_predict_function()

# Para ver que funciona correctamente
print('Model loaded. Start serving...')
print('Model loaded. Check http://127.0.0.1:5000/')

# Si se añade alguna clase más al modelo se tiene que meter en esta lista.
labels = ['Achnanthidium', 'Adlafia', 'Amphora', 'Aulacoseira', 'Brachysira', 'Caloneis', 'Cavinula', 
'Chamaepinnularia', 'Cocconeis', 'Craticula', 'Cyclotella', 'Cymbopleura', 'Diadesmis', 'Diatoma', 'Encyonema', 
'Encyonopsis', 'Eolimna', 'Eunotia', 'Fragilaria', 'Frustulia', 'Geissleria', 'Gomphonema', 'Luticola', 'Mayamaea', 
'Meridion', 'Navicula', 'Neidiopsis', 'Neidium', 'Nitzschia', 'Pinnularia', 'Planothidium', 'Psammothidium', 'Pseudostaurosira', 
'Rossithidium', 'Sellaphora', 'Stauroforma', 'Stauroneis', 'Staurosira', 'Staurosirella', 'Stephanodiscus', 'Surirella', 
'Tabellaria']

print(len(labels), "clases en total.")
# Función que carga la imagen insertada por el usuario en el modelo y devuelve la predicción.
def model_predict(image, model):
    
    # Preprocesamos la imagen, convirtiendola a RGB si es necesario.
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Obtenemos el tamanio del modelo viendo su capa de entrada.
    image_size = model.input_shape[1]
    
    # Modificamos el tamanio de la imagen del usuario para que sea una entrada correcta a la red.
    image = image.resize((image_size, image_size))
    image = tf.keras.utils.img_to_array(image)
    image = np.expand_dims(image, 0)
    
    # Predecimos la clase de la imagen con el modelo
    img_gen = ImageDataGenerator()
    test_gen = img_gen.flow(image)
    preds = model.predict(test_gen, verbose=1)
    
    # Pasamos la salida del modelo a la prediccion.
    diatom_class = np.argmax(preds)
    
    # Obtenemos el top 5 de predicciones para esa imagen.
    top_5_labels = []
    top_5_probabilities = []
    
    top_5_predictions = np.argsort(preds)[:,-5:][0]
    
    for i in top_5_predictions:
        top_5_labels.append(labels[i])
        top_5_probabilities.append(preds[0][i] * 100)
    
    top_5_labels.reverse()
    top_5_probabilities.reverse()
    
    return top_5_labels, top_5_probabilities

# Metodo que se ejecuta cuando se accede a la pagina. Simplemente se carga.
@app.route('/', methods=['GET'])
def index():
    # Carga de la pagina principal. Copiado de tutorial basico de Flask.
    return render_template('index.html')

# Metodo que se ejecuta cuando se le pulsa el boton de prededir
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Cogemos la imagen de la request POST y la pasamos a PIL.
        img = base64_to_pil(request.json)

        # Obtenemos lap rediccion
        labels, probabilities = model_predict(img, model)
        
        # Decimos la prediccion TOP 1.
        result = "La clase predicha por el modelo es <b> " + labels[0] + " </b> <br> "
        result += "Predicciones: <br> "
        
        # Listamos las top 5 predicciones junto con su probabilidad.
        for i in range(len(labels)):
            result = result + str(labels[i]) +  " - probabilidad: " + str(round(probabilities[i], 2)) + " %. <br>"
            
        # Serializamos el resultado. Copiado de tutorial basico de Flask.
        return jsonify(result=result)

    return None

if __name__ == '__main__':
    # Lanzamos la app con Gevent. Copiado de tutorial.
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
