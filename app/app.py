from flask import Flask, render_template, request
import mysql.connector
import redis

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
    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Obtener productos de la base de datos
    cursor.execute("SELECT * FROM TEST")
    products = cursor.fetchall()

    # Devolver los productos al template
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    # Agregar un nuevo producto a la base de datos
    product_name = request.form['product_name']
    product_quantity = request.form['product_quantity']

    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insertar el nuevo producto
    cursor.execute("INSERT INTO TEST (product_name, product_quantity) VALUES (%s, %s)", 
                   (product_name, product_quantity))
    conn.commit()

    # Redirigir a la página principal
    return index()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
