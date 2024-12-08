<?php
// Imprimir un mensaje simple con echo
echo "<h1>¡PHP está funcionando correctamente!</h1>";

// Imprimir la fecha y hora actual del servidor
echo "<p>La fecha y hora actual del servidor es: " . date("Y-m-d H:i:s") . "</p>";

// Imprimir información sobre el entorno PHP
echo "<p>Versión de PHP instalada: " . phpversion() . "</p>";

// Comprobar una variable de entorno
$serverName = $_SERVER['SERVER_NAME'];
echo "<p>El nombre del servidor es: $serverName</p>";

// Realizar una operación matemática simple
$sum = 5 + 3;
echo "<p>5 + 3 = $sum</p>";
?>
