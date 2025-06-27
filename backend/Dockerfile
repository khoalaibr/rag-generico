# backend/Dockerfile

# Usar una imagen oficial de Python como imagen base.
# 'slim' es una versión ligera que reduce el tamaño de nuestra imagen final.
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor.
# Todos los comandos siguientes se ejecutarán desde esta ruta.
WORKDIR /app

# Copiar el archivo de dependencias primero.
# Docker aprovecha el sistema de capas; si requirements.txt no cambia,
# no volverá a instalar las dependencias, acelerando la construcción.
COPY requirements.txt .

# Instalar las dependencias de Python.
# --no-cache-dir para no guardar el cache y mantener la imagen ligera.
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al directorio de trabajo.
COPY . .