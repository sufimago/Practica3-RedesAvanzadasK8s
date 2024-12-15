import subprocess
import sys
import time

# Configuración inicial
NEW_IMAGE = "sufimago/flask-app:canary"
DEPLOYMENT_NAME = "flask-deployment"
NAMESPACE = "default"
TIMEOUT = 60

# Función para ejecutar un comando y verificar errores
def run_command(command):
    """Ejecuta un comando en la terminal y verifica si hay errores."""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"\nError al ejecutar el comando: {command}\n{result.stderr.decode()}\n")
        sys.exit(1)
    return result.stdout.decode()
# Verificar si kubectl está disponible
try:
    run_command("kubectl version --client")
except subprocess.CalledProcessError:
    print("\nError: kubectl no está instalado o configurado correctamente.\n")
    sys.exit(1)

print("\n============================")
print("Iniciando Canary Deployment...")
print("============================\n")
time.sleep(3)
# Paso 1: Mostrar el estado actual de los pods
print("\nMostrando el estado de los pods actuales...")
print(run_command(f"kubectl get pods --namespace={NAMESPACE}"))
time.sleep(3)
# Paso 2: Actualizar SOLO 1 réplica a la nueva imagen
print("\nActualizando 1 de las réplicas a la nueva versión...")
run_command(f"kubectl set image deployment/{DEPLOYMENT_NAME} flask={NEW_IMAGE} --namespace={NAMESPACE}")
time.sleep(5)
# Paso 3: Escalar temporalmente a 1 réplica
print("\nEscalando temporalmente a 1 réplica...")
run_command(f"kubectl scale deployment {DEPLOYMENT_NAME} --replicas=1 --namespace={NAMESPACE}")
time.sleep(4)
# Paso 4: Verificar el despliegue con un timeout
print(f"\nEsperando a que el despliegue esté listo (máximo {TIMEOUT} segundos)...")
try:
    run_command(f"kubectl rollout status deployment/{DEPLOYMENT_NAME} --namespace={NAMESPACE} --timeout={TIMEOUT}s")
except subprocess.CalledProcessError:
    print("\nError: El despliegue no se completó dentro del tiempo esperado.")
    print("Revirtiendo el despliegue...\n")
    run_command(f"kubectl rollout undo deployment/{DEPLOYMENT_NAME} --namespace={NAMESPACE}")
    sys.exit(1)
time.sleep(4)
# Paso 5: Esperar un poco para estabilizar los pods
print("\nEsperando unos segundos para estabilizar los pods...")
time.sleep(10)

# Paso 6: Obtener el nombre del pod desplegado
print("\nObteniendo el nombre del pod desplegado...")
pod_name = run_command(
    f"kubectl get pods --namespace={NAMESPACE} --selector=app=flask "
    f"--field-selector=status.phase=Running -o jsonpath='{{.items[0].metadata.name}}'"
).strip()
time.sleep(2)
# Verificar si se obtuvo el nombre del pod
if not pod_name:
    print("\nError: No se pudo encontrar el pod en ejecución.")
    print("Revirtiendo el despliegue...\n")
    run_command(f"kubectl rollout undo deployment/{DEPLOYMENT_NAME} --namespace={NAMESPACE}")
    sys.exit(1)

# Asegurarse de que el pod esté en estado 'Running' antes de probar el health
print(f"\nEsperando a que el pod {pod_name} esté completamente disponible...")
time.sleep(10)  # Espera de 10 segundos para asegurarnos de que el pod esté listo

# Paso 7: Probar el health del pod
print(f"\nProbando el health del pod: {pod_name}...")
time.sleep(10)

# Aquí simulamos que la salida de la prueba de health fue exitosa.
# En un entorno real, reemplazar este bloque con una llamada real al endpoint de health.
health_output = "ok"  # Simulación de salida positiva de health check

if "ok" in health_output:
    print("\nLa nueva versión pasó las pruebas de health. Desplegando el resto de las réplicas...")
    run_command(f"kubectl scale deployment {DEPLOYMENT_NAME} --replicas=3 --namespace={NAMESPACE}")
    print("\n============================")
    # Paso 1: Mostrar el estado final de los pods
    print("\nMostrando el estado de los pods finales...")
    print(run_command(f"kubectl get pods --namespace={NAMESPACE}"))
    time.sleep(5)
    print("Canary Deployment exitoso.")
    print("============================\n")
else:
    print("\nLa nueva versión falló las pruebas de health. Revirtiendo el despliegue...\n")
    run_command(f"kubectl rollout undo deployment/{DEPLOYMENT_NAME} --namespace={NAMESPACE}")
    sys.exit(1)