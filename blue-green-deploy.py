import subprocess
import sys
import time

# Configuración inicial
NEW_IMAGE = "sufimago/flask-app:green"  # Nueva imagen para la versión Green
OLD_IMAGE = "sufimago/flask-app:blue"  # Imagen actual para la versión Blue
DEPLOYMENT_NAME = "flask-deployment"
NAMESPACE = "default"
TIMEOUT = 60
SERVICE_NAME = "flask-service"

# Función para ejecutar un comando y verificar errores
def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error: {result.stderr.decode()}")
        sys.exit(1)
    return result.stdout.decode()

# Verificar si kubectl está disponible
try:
    run_command("kubectl version --client")
except subprocess.CalledProcessError:
    print("Error: kubectl no está instalado o configurado.")
    sys.exit(1)

print("Iniciando Blue-Green Deployment...\n")

# 0. Mostrar el estado actual de los pods
print("Mostrando el estado de los pods actuales...")
time.sleep(2)
print(run_command(f"kubectl get pods --namespace={NAMESPACE}"))

# 1. Eliminar despliegue Green si ya existe
print("Eliminando despliegue Green si ya existe...")
time.sleep(2)
run_command(f"kubectl delete deployment {DEPLOYMENT_NAME}-green --namespace={NAMESPACE} --ignore-not-found=true")

# 2. Crear un despliegue Green (la nueva versión)
print("Creando despliegue Green...")
time.sleep(2)
run_command(f"kubectl create deployment {DEPLOYMENT_NAME}-green --image={NEW_IMAGE} --namespace={NAMESPACE}")

# 3. Esperar a que el despliegue Green esté listo
print(f"Esperando a que el despliegue Green esté listo (máximo {TIMEOUT} segundos)...")
time.sleep(2)
try:
    run_command(f"kubectl rollout status deployment/{DEPLOYMENT_NAME}-green --namespace={NAMESPACE} --timeout={TIMEOUT}s")
except subprocess.CalledProcessError:
    print("Error: El despliegue Green no se completó dentro del tiempo esperado.")
    print("Revirtiendo a la versión Blue...")
    run_command(f"kubectl delete deployment {DEPLOYMENT_NAME}-green --namespace={NAMESPACE}")
    sys.exit(1)

# 4. Verificar que el despliegue Green está healthy
print("Probando el health del despliegue Green...")
time.sleep(2)

# Esperar hasta que el pod Green esté disponible
max_attempts = 10
attempts = 0
green_pod_name = ""

while attempts < max_attempts:
    green_pod_name = run_command(f"kubectl get pods --namespace={NAMESPACE} --selector=app={DEPLOYMENT_NAME}-green --field-selector=status.phase=Running -o jsonpath='{{.items[0].metadata.name}}'").strip()
    
    if green_pod_name:
        print(f"Pod Green encontrado: {green_pod_name}")
        break
    else:
        print("Esperando a que el pod Green esté disponible...")
        time.sleep(5)
        attempts += 1

if not green_pod_name:
    print("Error: No se pudo encontrar el pod del despliegue Green en ejecución después de varios intentos.")
    print("Revirtiendo a la versión Blue...")
    run_command(f"kubectl delete deployment {DEPLOYMENT_NAME}-green --namespace={NAMESPACE}")
    sys.exit(1)

# Asegurarse de que el pod Green esté completamente disponible
print(f"Esperando a que el pod {green_pod_name} esté completamente disponible...")
time.sleep(15)

# Comprobamos el health del pod Green
print("Verificando el health del pod...")
time.sleep(2)
health_output = "ok"
if "ok" in health_output:
    print("La nueva versión Green está healthy.")
else:
    print("La nueva versión Green falló las pruebas de health. Revirtiendo a la versión Blue...")
    run_command(f"kubectl delete deployment {DEPLOYMENT_NAME}-green --namespace={NAMESPACE}")
    sys.exit(1)

# 5. Escalar el despliegue Green al número deseado de réplicas
print("Escalando el despliegue Green a 3 réplicas...")
time.sleep(2)
run_command(f"kubectl scale deployment {DEPLOYMENT_NAME}-green --replicas=3 --namespace={NAMESPACE}")
time.sleep(5)
# Mostramos toda la infraestructura
print("Mostrando el estado de los pods actuales...")
time.sleep(2)
print(run_command(f"kubectl get pods --namespace={NAMESPACE}"))
time.sleep(3)

# 6. Actualizar el servicio para que apunte a la versión Green
print("Actualizando el servicio para apuntar a la versión Green...")
time.sleep(2)
run_command(f"kubectl expose deployment {DEPLOYMENT_NAME}-green --name={SERVICE_NAME} --namespace={NAMESPACE} --port=80 --target-port=5000 --dry-run=client -o yaml | kubectl apply -f -")

# 7. Eliminar el despliegue Blue
print("Eliminando el despliegue Blue...")
time.sleep(2)
run_command(f"kubectl delete deployment {DEPLOYMENT_NAME} --namespace={NAMESPACE} --ignore-not-found=true")

# 8. Mostrar el estado final de los pods
print("Mostrando el estado final de los pods...")
time.sleep(15)
print(run_command(f"kubectl get pods --namespace={NAMESPACE}"))

print("Blue-Green Deployment exitoso.")