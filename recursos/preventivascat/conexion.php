<?php
//busco que el archivo de config exista
$configPath = __DIR__ . "/config.php";
if (file_exists($configPath)) {
    require_once $configPath;
} else {
    die("Error: El archivo de configuración no existe.");
}

try {
    // hago la conexion
    $conn = new PDO("pgsql:host=$host;port=$port;dbname=$dbname", $user, $password);

    // aqui se establece el modo de error
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

} catch (PDOException $e) {
    die("Error en la conexión a la base de datos: " . $e->getMessage());
}
?>

