# se usa la imagen de python
FROM python:3.12-slim


## establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt (lo crearemos más abajo)
COPY requirements.txt requirements.txt

## Instala las dependencias del proyecto 
RUN pip install --no-cache-dir -r requirements.txt

## Copiamos los archivos del proyecto en el contenedor
COPY . .

# Instala dependencias necesarias para rembg
RUN apt-get update && apt-get install -y libomp-dev

# exponemos el en el que Flask va a correr
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "removeBackgroundApi.py", "--server.port=8501", "--server.address=0.0.0.0"]