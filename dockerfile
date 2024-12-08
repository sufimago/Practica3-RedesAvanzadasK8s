FROM nginx:latest

RUN apt-get update && apt-get install -y \
    php-fpm \
    php-mysql

# Copia los archivos de configuración de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copia el código fuente de la web
COPY . /usr/share/nginx/html/

# Exponer el puerto 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
