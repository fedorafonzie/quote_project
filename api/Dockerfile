# /api/Dockerfile

# Gebruik een officiële Python runtime als basisimage
FROM python:3.9-slim

# Voorkom dat Python output buffert, zodat logs direct in de Docker logs verschijnen
ENV PYTHONUNBUFFERED 1

# Stel de werkdirectory in binnen de container
WORKDIR /code

# Kopieer de requirements en installeer de dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de rest van je Django project (de '.' verwijst naar de build context, oftewel de 'api' map)
COPY . /code/