
# Proyecto Flask con Kubernetes, MySQL, Redis y Prometheus
Este proyecto es una aplicación web desarrollada con Flask, que interactúa con MySQL y Redis para almacenar productos y almacenar datos en caché. Además, expone métricas para ser recolectadas por Prometheus. El despliegue se realiza en Kubernetes, utilizando estrategias de despliegue como Blue-Green y Canary. Este proyecto está configurado para CI/CD con GitHub Actions.

## Requisitos
Antes de comenzar, asegúrate de tener las siguientes herramientas instaladas y configuradas:

**Kubernetes**: Para el despliegue de la aplicación.

**Docker**: Para la creación de imágenes de contenedor.

**Kubectl**: Para interactuar con tu clúster de Kubernetes.

**Helm** (opcional): Para gestionar despliegues más complejos.

**Prometheus**: Para la recolección de métricas.

**Git**: Para gestionar el código fuente.

## Diagrama/ Estructura del Proyecto
/project-root  
│  
├── /app                    --> Código fuente de la aplicación Flask  
│   ├── app.py              --> Código principal de la aplicación Flask  
│   ├── test_app.py         --> Pruebas unitarias de la aplicación  
│   ├── /static             --> Archivos estáticos (imágenes, CSS, JS)  
│   │   └── mago.jpg        --> Imagen de ejemplo  
│   └── /templates          --> Plantillas HTML para renderizar las vistas  
│       └── index.html      --> Plantilla principal  
│  
├── /k8s                            --> Archivos de Kubernetes para el despliegue  
│   ├── blue-green-deploy.py        --> Script para el despliegue Blue-Green  
│   ├── canary-deploy.py            --> Script para el despliegue Canary  
│   ├── comandosk8s.txt             --> Comandos útiles para interactuar con Kubernetes  
│   ├── deployment-flask.yaml       --> Despliegue de la aplicación Flask  
│   ├── deployment-mysql.yaml       --> Despliegue de MySQL  
│   ├── deployment-phpmyadmin.yaml  --> Despliegue de PHPMyAdmin  
│   ├── deployment-redis.yaml       --> Despliegue de Redis  
│   ├── mysql-pvc.yaml              --> Configuración del PVC para MySQL  
│   ├── prometheus-config.yaml      --> Configuración de Prometheus  
│   ├── prometheus-deployment.yaml  --> Despliegue de Prometheus  
│   ├── prometheus-rbac.yaml        --> RBAC para Prometheus  
│   └── prometheus-service.yaml     --> Servicio de Prometheus  
│  
├── /ci-cd                  --> Configuración de CI/CD  
│   └── .github/workflows/ci-cd-pipeline.yml # Pipeline de GitHub Actions  
│  
├── Dockerfile              --> Dockerfile para construir la imagen  
├── .gitignore              --> Archivos a ignorar por Git  
├── requirements.txt        --> Dependencias de Python  
├── secret.yaml             --> Archivos secretos (como contraseñas)  
├── practica3.pdf           --> Documento de la práctica  
└── README.md               --> Este archivo

## Installation

### 1. Clona el Repositorio

```bash
  git clone https://github.com//Practica3-RedesAvanzadasK8s/
  cd proyecto-flask
```
    
### 2. Construir y Subir la Imagen Docker    
Una vez tengas el código en tu máquina local, construye la imagen Docker de la aplicación:
```bash
docker build -t tu_usuario/flask-app .

```
Después, sube la imagen al repositorio de Docker (asegúrate de tener la sesión iniciada en Docker):
```bash
docker push tu_usuario/flask-app
```
### 3. Desplegar en Kubernetes
Una vez la imagen está subida al repositorio, puedes proceder con el despliegue en Kubernetes. Asegúrate de tener acceso al clúster de Kubernetes y de haber configurado kubectl.

Para aplicar los archivos de configuración de Kubernetes, utiliza el siguiente comando:
```bash
kubectl apply -f .
```
Esto aplicará todos los archivos de configuración en el directorio actual, que incluyen:

Despliegue de la aplicación Flask (deployment-flask.yaml).
Despliegue de Redis (deployment-redis.yaml).
Despliegue de MySQL (deployment-mysql.yaml).
Despliegue de PHPMyAdmin (deployment-phpmyadmin.yaml).
Configuración de Prometheus para la recolección de métricas (prometheus-config.yaml, prometheus-deployment.yaml, prometheus-rbac.yaml, prometheus-service.yaml).

### 4. Verificar el Despliegue
Una vez que se haya aplicado la configuración, puedes verificar que los servicios están corriendo correctamente con los siguientes comandos:
```bash
kubectl get pods
kubectl get svc
```

### 5. Acceder a la Aplicación
La aplicación Flask estará disponible en el servicio de Kubernetes configurado. Dependiendo de la configuración de tu clúster, puedes acceder a la aplicación a través de un LoadBalancer, NodePort o Ingress.

Lo que hago yo, es un minikube tunnel, y mediante el servicio de flask, accedes a tu ip/5000
```bash
minikube tunnel
http://<ip-de-flask-service>:5000
```

## CI/CD con GitHub Actions
Este proyecto está configurado con un pipeline de CI/CD utilizando GitHub Actions. El archivo de configuración se encuentra en:
```bash
.github/workflows/ci-cd-pipeline.yml
```
El pipeline se ejecuta en cada push al repositorio y realiza los siguientes pasos:

Instalación de dependencias: Se instalan las dependencias de Python y Docker.
Build de la imagen: Se construye la imagen Docker de la aplicación.
Push al repositorio Docker: Se sube la imagen construida a Docker Hub.
Despliegue en Kubernetes: Se despliega la aplicación en el clúster de Kubernetes.
Para configurar el pipeline, asegúrate de tener configurados los secretos en GitHub (como tus credenciales de Docker Hub).

## Estrategias de Despliegue
Este proyecto soporta dos estrategias de despliegue avanzadas en Kubernetes:

### 1. Despliegue Blue-Green(simulación)
El script:
```bash
blue-green-deploy.py 
```
automatiza el proceso de despliegue Blue-Green en Kubernetes. Esta estrategia permite tener dos versiones de la aplicación corriendo (una "verde" y una "azul") para facilitar el proceso de actualización sin tiempos de inactividad.

### 2. Despliegue Canary(simulación)
El script:
```bash
canary-deploy.py
```
permite realizar un despliegue "Canary", donde una pequeña porción del tráfico se dirige a la nueva versión de la aplicación, lo que permite probarla con un tráfico real antes de hacer el cambio completo.

## Kubernetes RBAC
El archivo prometheus-rbac.yaml configura los permisos necesarios para que Prometheus pueda acceder a los recursos de Kubernetes y recolectar métricas desde los servicios desplegados.

## Prometheus
Prometheus se encarga de recolectar métricas de la aplicación Flask. La configuración de Prometheus se encuentra en los siguientes archivos:

Configuración de scraping para Prometheus.
```bash 
prometheus-config.yaml
```

Despliegue de Prometheus en el clúster.
```bash 
prometheus-deployment.yaml
``` 

Servicio de Kubernetes para exponer Prometheus.
```bash 
prometheus-service.yaml
```

## Endpoints
**/**: Página principal que muestra los productos de la base de datos y los productos almacenados en el caché de Redis.

**/add** (POST): Permite agregar un nuevo producto a la base de datos.

**/health** (GET): Endpoint de comprobación de salud que verifica la conexión con MySQL y Redis.

**/metrics** (GET): Endpoint que expone las métricas para Prometheus.




