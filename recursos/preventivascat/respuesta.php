<?php

session_start();

// Inicializar la respuesta
$response = ["authenticated" => false];

if (isset($_SESSION['usuario'])) {
    // El usuario está autenticado
    $response["authenticated"] = true;
    $response["usuario"] = $_SESSION['usuario'];

    include_once "conexion.php"; 
    $query = "SELECT nombre FROM usuario WHERE usuario = :usuario";
    $stmt = $conn->prepare($query);
    $stmt->bindParam(':usuario', $_SESSION['usuario'], PDO::PARAM_STR);
    $stmt->execute();

    if ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        $response["nombre"] = $row["nombre"];
    }
}

return json_encode($response);
?>
