@echo off
REM --- Paso 1: Construir la imagen de Docker ---
echo Building Docker image...
docker build -t sufimago/flask-app:latest .

REM --- Paso 2: Pushear la imagen a Docker Hub ---
echo Pushing Docker image to Docker Hub...
docker push sufimago/flask-app:latest

REM --- Paso 3: Verificar los deployments en el namespace 'monitoring' ---
echo Verifying deployments in the 'monitoring' namespace...

REM Obtener los nombres de los deployments en el namespace 'monitoring' y reiniciarlos
kubectl get deployments -n monitoring --no-headers -o custom-columns=":metadata.name" | for /f "tokens=*" %%a in ('more') do (
    echo Restarting deployment %%a in namespace monitoring...
    kubectl rollout restart deployment %%a -n monitoring
)

REM --- Paso 4: Verificar los deployments en el namespace 'default' (u otros sin especificar namespace) ---
echo Verifying deployments in the 'default' namespace...

REM Obtener los nombres de los deployments en el namespace 'default' y reiniciarlos
kubectl get deployments -n default --no-headers -o custom-columns=":metadata.name" | for /f "tokens=*" %%a in ('more') do (
    echo Restarting deployment %%a in namespace default...
    kubectl rollout restart deployment %%a -n default
)

echo Deployment complete!
pause
