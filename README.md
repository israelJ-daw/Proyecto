# Despliegue del proyecto con Docker

1. Creación del Dockerfile:

El archivo Dockerfile se creo en la raíz del proyecto, este archivo indica a Docker cómo construir la imagen del proyecto

2. Explicación breve del Dockerfile

    FROM python:3.12-slim

    Imagen base de Python 3.12 ligera

    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1

    Evita que se generen archivos .pyc y permite que los logs se muestren en tiempo real

    WORKDIR /app

    Define la carpeta de trabajo dentro del contenedor

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    Copia las dependencias y las instala
    La opcion --no-cache-dir evita que pip guarde archivos temporales en el contenedor, dejando la imagen más ligera

    COPY . .

    Copia todo el proyecto al contenedor

    EXPOSE 8000

    Expone el puerto 8000 dentro del contenedor

    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

    Arranca el servidor de Django escuchando en todas las interfaces en el puerto 8000

3. Construcción de la imagen

    docker build -t organiza .

    Construye la imagen del proyecto con el nombre organiza, el punto al final indica que se debe construir la imagen en el directorio actual

4. Ejecución del contenedor

    docker run -p 8080:8000 organiza

    Ejecuta el contenedor con el nombre organiza y mapea el puerto 8000 del contenedor al puerto 8080 del host, permitiendo acceder a la app en el navegador a través de http://localhost:8080

