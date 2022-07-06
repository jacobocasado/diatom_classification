# Manual de usuario para el lanzamiento de la herramienta web

## Pasos principales para ejecutar la herramienta usando Docker y Python

Instalar **[Docker](https://www.docker.com)** y **[Python](https://www.python.org/downloads/)** (clickear)

Una vez instalados seguir los siguientes pasos:

```
# 1. Clonar este repositorio de GitHub
$ git clone https://github.com/jacobocasado/diatom_classification.git
$ o descargarlo como archivo .zip (clone, descargar como zip)

# 2. Cargar la imagen Docker
$ cd diatom_classification/deploy
$ docker build -t project .

# 3. Lanzar la imagen Docker
$ docker run -it --rm -p 5000:5000 project
```

Abrir http://localhost:5000 cuando el proceso de carga y lanzamiento haya finalizado.

El nombre del contenedor Docker (project) puede modificarse si se desea.
