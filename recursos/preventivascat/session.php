<?php

session_start();

// Inicializar la respuesta
$response = ["authenticated" => false];

if (isset($_SESSION['usuario'])) {
    // El usuario está autenticado
    $response["authenticated"] = true;
    $response["usuario"] = $_SESSION['usuario'];

    include_once "conexion.php"; 
    $query = "SELECT nombre,empresa_id,mutualidad_id,utm_id FROM usuario WHERE usuario = :usuario";
    $stmt = $conn->prepare($query);
    $stmt->bindParam(':usuario', $_SESSION['usuario'], PDO::PARAM_STR);
    $stmt->execute();
    
    //verifico a cual organizacion pertenece usuario
    if ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        $response["nombre"] = $row["nombre"];

        if ($row["empresa_id"] != '') {
            $response["pertenece"] = "empresa";
        } elseif ($row["mutualidad_id"] != '') {
            $response["pertenece"] = "mutualidad";
        } elseif ($row["utm_id"] != null) {
            $response["pertenece"] = "utm";
        } else {
            $response["pertenece"] = "ninguna";
        }
    }
}

echo json_encode($response);
?>
