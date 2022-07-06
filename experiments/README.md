# Manual de usuario 
## Scripts utilizados para el manejo de los datasets, entrenamiento y validación de modelos y evaluación del mejor modelo en test.

Este directorio contiene los 4 scripts de Python con las funciones respectivas para cada una de las fases del proyecto \textbf{previas al desarrollo en web}: preparación de datos, división en entrenamiento/validación/test, entrenamiento de modelos y evaluación y reentrenamiento del mejor modelo para el lanzamiento a la web. Cada uno de estos los archivos dedicados a la primera parte del proyecto contienen una celda dedicada a la personalización de los parámetros como la \textbf{ruta de los directorios donde se ubican las imágenes y los ficheros de trabajo}, el \textbf{número de imágenes} con el que aplicar el balanceo de datos vía \textit{data augmentation} o \textbf{hiperparámetros} de los modelos a utilizar. 

Estas celdas se comentan en el código para facilitar su búsqueda y edición por parte del usuario. 
A continuación se procede a explicar brevemente el funcionamiento de cada uno de los scripts ya que cada script está comentado celda a celda, explicando todo lo que se va haciendo. 

## ```rename_data.py```

Este script de Python se creó inicialmente debido a que las imágenes de cada diatomea se almacenaron en un subdirectorio por cada página web de la que se han obtenido.

El modelo necesitaba disponer de todas las imágenes de cada clase dentro de un único directorio, por lo que se diseñó este pequeño script para fusionar los subdirectorios de las webs. De esta manera todas las imágenes de la clase se sitúan en el directorio raíz de la diatomea correspondiente. \textbf{No es necesario utilizar este script de nuevo} si especificamos que las imágenes se deben insertar de la manera comentada anteriormente y no creando un directorio por cada página web y especie.

## ```train_test_val_creation.py```
En este notebook de Python se crean los dataframes de entrenamiento, validación y test y se utiliza la técnica de data augmentation para realizar balanceo de datos almacenando las imágenes aumentadas, en caso de ser especificada por el usuario con una variable de tipo bool llamada balance. Mediante las variables min_samples y max_samples se especifican el mínimo y máximo número de imágenes por clase. También se puede personalizar el tamaño de las imágenes generadas por aumento de datos con la variable img_size}. Por defecto, las imágenes generadas por el aumento de datos se almacenarán en el directorio aug, generado automáticamente.

Todos los dataframes se guardan automáticamente en un directorio llamado folds en un archivo de extensión .pkl para cargarlos en la fase de entrenamiento.

## ```model_training_and_evaluation.py```

En este archivo se realiza el proceso de entrenamiento y validación de modelos utilizando validación cruzada en 3 folds. Se ha dejado una celda situada antes de la ejecución del entrenamiento para permitir la personalización rápida de los parámetros e hiperparámetros (tamaño de batch, learning rate, tamaño de imagen...) a la hora de hacer comparativas. Los callbacks utilizados se pueden modificar en la variable callbacks. Por defecto, los modelos que se entrenan en el archivo son los modelos de AlexNet y de EfficientNetV2B0 pero se pueden personalizar cambiando una línea de código dentro del bloque de entrenamiento cuando se carga la variable model. En la parte final de este archivo se exportan los resultados de los modelos en los 3 folds correspondientes a un archivo en formato xlsx.

## ```best_model_analysis_and_retrain.py```
En este archivo se carga el modelo con mejores resultados y se analiza el comportamiento en el conjunto de test con métricas como la matriz de confusión o el reporte de clasificación. También se ha añadido un apartado usando LIME con una imagen bien clasificada del dataset y otro pequeño apartado dedicado a graficar una imagen mal clasificada junto a la etiqueta real y la predicha por el modelo. Por último, el modelo se reentrena con todos los datos para tener el modelo que se llevará a producción.
