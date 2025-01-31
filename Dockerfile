# Se usa la imagen de Python
FROM python:3.12-slim

# Evitar buffering en la salida de Python para mejores logs en tiempo real
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt
COPY requirements.txt .

# Instalar dependencias del sistema y Python en una sola capa optimizada
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libomp-dev \
        libsm6 \
        libxext6 && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiamos los archivos del proyecto en el contenedor
COPY . .

# Exponer el puerto en el que Flask/Streamlit va a correr
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "removeBackgroundApi.py", "--server.port=8501", "--server.address=0.0.0.0"]
