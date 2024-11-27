FROM php:8.0-fpm

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    libpng-dev libjpeg-dev libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd mysqli

# Comprobar si la extensión Redis ya está instalada, si no, instalarla
RUN if ! php -m | grep -q 'redis'; then \
      pecl install redis && docker-php-ext-enable redis; \
    else \
      echo "Redis ya está instalado"; \
    fi
