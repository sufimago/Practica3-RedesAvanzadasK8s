<?php
session_start(); // Inicia la sesión
$is_pro_env = true;  // Cambiar a true para producción
$connection_status = "";
$insert_status = "";
$result = null;
$cache_result = null;
$cache_key = 'productos_cache'; // Clave de Redis
$cache_duration = 600; // Duración de la caché en segundos (600 = 10 minutos)

$config = require 'config.php';


// Conectar con la base de datos según el entorno
if ($is_pro_env) {
    // Conectar con Redis solo en producción
    $redis = new Redis();
    $redis->connect('my_redis_pro', 6379);

    $servername = $config['db2']['host'];
    $username = $config['db2']['user'];
    $password = $config['db2']['password'];
    $dbname = $config['db2']['dbname'];
} else {
    $servername = $config['db']['host'];
    $username = $config['db']['user'];
    $password = $config['db']['password'];
    $dbname = $config['db']['dbname'];
}

// Inicializar el contador de sesión
if (!isset($_SESSION['contador'])) {
    $_SESSION['contador'] = 1;
} else {
    $_SESSION['contador']++;
}

// Conexión a la base de datos
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

$connection_status = "Conectado por la '{$_SESSION['contador']}' vez.";
$insert_status = "";

// Procesar inserción de nuevos productos
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $product_name = $_POST['product_name'];
    $product_quantity = $_POST['product_quantity'];

    // Comprobar si el producto ya existe
    $check_sql = "SELECT * FROM TEST WHERE product_name = '$product_name'";
    $check_result = $conn->query($check_sql);

    if ($check_result->num_rows == 0) {
        // Si no existe, insertamos
        $insert_sql = "INSERT INTO TEST (product_name, product_quantity) VALUES ('$product_name', '$product_quantity')";
        
        if ($conn->query($insert_sql) === TRUE) {
            $insert_status = "Nuevo producto agregado: $product_name.";
        } else {
            $insert_status = "Error al agregar producto: " . $conn->error;
        }

        // Limpiar la caché en Redis al agregar un nuevo producto (solo si estamos en producción)
        if ($is_pro_env) {
            $redis->del($cache_key);
        }
    }
}

// Intentar cargar los productos de la caché en Redis solo si es entorno de producción
if ($is_pro_env) {
    $cache_result = $redis->get($cache_key);

    if ($cache_result) {
        // Si los productos están en caché, los decodificamos
        $result = json_decode($cache_result, true);
        // print_r($result);
    } else {
        // Si no hay caché, obtener productos de la base de datos
        $sql = "SELECT * FROM TEST";
        $db_result = $conn->query($sql);

        if ($db_result->num_rows > 0) {
            // Extraer resultados de la base de datos y almacenarlos en un array
            $result = [];
            while ($row = $db_result->fetch_assoc()) {
                $result[] = $row;
            }

            // Guardar los productos en la caché de Redis y establecer el tiempo de expiración
            $redis->set($cache_key, json_encode($result), $cache_duration);
        } else {
            $result = null; // No hay productos
        }
    }
} else {
    // Si no estamos en producción, obtenemos directamente de la base de datos
    $sql = "SELECT * FROM TEST";
    $db_result = $conn->query($sql);

    if ($db_result->num_rows > 0) {
        $result = [];
        while ($row = $db_result->fetch_assoc()) {
            $result[] = $row;
        }
    } else {
        $result = null; // No hay productos
    }
}

// Cerrar conexión a la base de datos
$conn->close();

echo "<script></script>";

// Retornar las variables para que puedan ser usadas en index.php
return [
    'connection_status' => $connection_status,
    'insert_status' => $insert_status,
    'result' => $result
];