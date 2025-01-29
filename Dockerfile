# se usa la imagen de python
FROM python:3.12-slim

## establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt (lo crearemos más abajo)
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

## Instala las dependencias del proyecto 
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

## Copiamos los archivos del proyecto en el contenedor
COPY . .

# Instala dependencias necesarias para rembg
RUN --mount=type=cache,target=/var/cache/apt \
apt-get update && apt install -y --no-install-recommends libomp-dev \ 
&& apt clean \
&& rm -rf /var/lib/apt/lists/*

# exponemos el en el que Flask va a correr
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "removeBackgroundApi.py", "--server.port=8501", "--server.address=0.0.0.0"]