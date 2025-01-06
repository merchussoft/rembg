# se usa la imagen de python
FROM python:3.12-slim


## establecemos el directorio de trabajo en el contenedor
WORKDIR /app

## Copiamos los archivos del proyecto en el contenedor
COPY . /app

## Instala las dependencias del proyecto 
RUN pip install --no-cache-dir -r requirements.txt

# exponemos el en el que Flask va a correr
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "removeBackgroundApi.py"]