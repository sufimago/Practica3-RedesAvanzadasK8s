# Usar una imagen base de PHP con Apache
FROM php:8.1-apache

# Instalar extensiones necesarias para MySQL
RUN docker-php-ext-install mysqli

# Copiar los archivos de la aplicación al contenedor
COPY . /var/www/html/

# Configurar permisos
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Exponer el puerto 80
EXPOSE 80

# Activar el módulo de reescritura de Apache
RUN a2enmod rewrite
