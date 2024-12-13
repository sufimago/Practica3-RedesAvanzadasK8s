@echo off
REM --- Paso 1: Construir la imagen de Docker ---
echo Building Docker image...
docker build -t sufimago/flask-app:latest .

REM --- Paso 2: Pushear la imagen a Docker Hub ---
echo Pushing Docker image to Docker Hub...
docker push sufimago/flask-app:latest

echo Build and pushed complete!
pause
