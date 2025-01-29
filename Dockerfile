# se usa la imagen de python
FROM python:3.12-slim

# Evitar buffering en la salida de Python para mejores logs en tiempo real
ENV PYTHONUNBUFFERED=1

## establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt (lo crearemos más abajo)
COPY requirements.txt .

# Instala dependencias necesarias para rembg
RUN apt-get update && apt-get install -y --no-install-recommends \
    libomp-dev libgl1-mesa-glx libglib2.0-0 ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
pip install --no-cache-dir -r requirements.txt

## Copiamos los archivos del proyecto en el contenedor
COPY . .

# exponemos el en el que Flask va a correr
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "removeBackgroundApi.py", "--server.port=8501", "--server.address=0.0.0.0"]