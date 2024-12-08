<?php
// Incluir el archivo db.php y recibir las variables
$data = include 'db.php';

// Extraer las variables desde el array $data
$connection_status = $data['connection_status'];
$insert_status = $data['insert_status'];
$result = $data['result'];
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Practica 1 - Gestión de Productos</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <h1>Practica 1 - Gestión de Productos</h1>
    <div class="container">
        <h2>Estado de Conexión</h2>
        <div class="status"><?php echo $connection_status; ?></div>
        <?php if ($insert_status) { echo "<div class='status'>$insert_status</div>"; } ?>

        <h2>Agregar Producto</h2>
        <form method="POST" action="" class="product-form">
            <div class="form-group">
                <input type="text" name="product_name" placeholder="Nombre del producto" required>
            </div>
            <div class="form-group">
                <input type="number" name="product_quantity" placeholder="Cantidad" required>
            </div>
            <button type="submit">Agregar</button>
        </form>

        <h2>Lista de Productos</h2>
        <div class="product-list">
            <?php
            if ($result) {
                echo "<table>";
                echo "<thead>";
                echo "<tr>
                <th>Nombre del producto</th>
                <th>Cantidad</th>
                </tr>";
                echo "</thead>";
                echo "<tbody>";
                foreach ($result as $row) {
                    echo "<tr>";
                    echo "<td>" . htmlspecialchars($row["product_name"]) . "</td>";
                    echo "<td>" . htmlspecialchars($row["product_quantity"]) . "</td>";
                    echo "</tr>";
                }
                echo "</tbody>";
                echo "</table>";
            } else {
                echo "<p>No hay productos en la base de datos.</p>";
            }
            ?>
        </div>

        <?php if ($is_pro_env && !empty($result)) : ?>
        <h2>Productos en Caché</h2>
        <div class="product-list">
            <?php
            // Aquí mostraríamos los productos que están en la caché
            echo "<table>";
            echo "<thead>";
            echo "<tr><th>Nombre del producto (Caché)</th><th>Cantidad (Caché)</th></tr>";
            echo "</thead>";
            echo "<tbody>";
            foreach ($result as $row) {
                echo "<tr>";
                echo "<td>" . htmlspecialchars($row["product_name"]) . "</td>";
                echo "<td>" . htmlspecialchars($row["product_quantity"]) . "</td>";
                echo "</tr>";
            }
            echo "</tbody>";
            echo "</table>";
            ?>
        </div>
        <?php endif; ?>
    </div>
</body>
</html>