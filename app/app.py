from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import redis
import json

app = Flask(__name__)

# Configuración de MySQL
db_config = {
    'host': 'mysql-service',  # Nombre del servicio MySQL en Kubernetes
    'user': 'root',
    'password': 'pro-pass',  # Asegúrate de usar las credenciales correctas
    'database': 'pro.db',
}

# Configuración de Redis
redis_client = redis.StrictRedis(host='redis-service', port=6379, db=0)

@app.route('/')
def index():
    print("inicio")
    conn = None  # Inicializar la variable conn
    try:
        # Conectar a la base de datos MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # Obtener productos de la base de datos
        cursor.execute("SELECT * FROM TEST")
        products = cursor.fetchall()
        # Intentar obtener productos desde Redis si están en caché
        cached_data = redis_client.get('products')
        cached_products = []
        if cached_data:
            try:
                raw_products = json.loads(cached_data)  # Recupera la lista de listas
                print(f"Datos sin procesar del caché: {raw_products}")
                # Convertir a una lista de diccionarios
                cached_products = [
                    {"product_name": item[0], "product_quantity": item[1]} for item in raw_products
                ]
                print(f"Productos decodificados desde el caché: {cached_products}")
            except json.JSONDecodeError as e:
                print(f"Error al decodificar los productos desde el caché: {str(e)}")
                print(f"Datos recibidos de Redis: {cached_data}")

        # Retornamos los productos y el estado de conexión al template
        return render_template('index.html', products=products, cached_products=cached_products,
                               connection_status="conexión con éxito", insert_status=None, is_pro_env=True)
    except mysql.connector.Error as e:
        # En caso de error con MySQL
        return render_template('index.html', products=[], cached_products=[], 
                               connection_status=f"Error con la base de datos: {str(e)}",
                               insert_status=None, is_pro_env=False)
    except redis.exceptions.ConnectionError as e:
        # En caso de error con Redis
        return render_template('index.html', products=[], cached_products=[], 
                               connection_status="Conexión con Redis fallida.",
                               insert_status=None, is_pro_env=False)
    finally:
        if conn and conn.is_connected():  # Verificar si conn está inicializado y conectado
            cursor.close()
            conn.close()

@app.route('/add', methods=['POST'])
def add_product():
    product_name = request.form['product_name']
    product_quantity = request.form['product_quantity']
    try:
        # Conectar a la base de datos MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insertar el nuevo producto en la base de datos
        cursor.execute("INSERT INTO TEST (product_name, product_quantity) VALUES (%s, %s)", 
                       (product_name, product_quantity))
        conn.commit()

        # Obtener todos los productos de la base de datos actualizada
        cursor.execute("SELECT * FROM TEST")
        products = cursor.fetchall()

        # Guardar los productos en Redis como JSON
        redis_client.set('products', json.dumps(products))

    except mysql.connector.Error as e:
        return render_template('index.html', products=[], cached_products=[], 
                               connection_status="Conexión exitosa pero",
                               insert_status=f"Error al agregar producto: {str(e)}",
                               is_pro_env=True)
    except redis.exceptions.ConnectionError as e:
        return render_template('index.html', products=[], cached_products=[], 
                               connection_status="Error al conectar con Redis.",
                               insert_status=f"Error al agregar producto: {str(e)}",
                               is_pro_env=True)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    # Redirigir a la página principal después de agregar el producto
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
index()