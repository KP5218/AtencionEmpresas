<?php
include_once "conexion.php"; 

//verifico si esta logeado
session_start();
if (!isset($_SESSION["usuario"])) {
    http_response_code(401);
    echo json_encode(array("exito" => false, "mensaje" => "Acceso no permitido"));
    exit();
}

try {
     //obtengo los paquetes desde bd y los envio como respuesta
    $sql ="SELECT cod_paquete, nombre_paquete FROM paquete";
    $stmt = $conn->prepare($sql);
    $stmt->execute();
    $opciones = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($opciones as &$opcion) {
        $opcion['nombre_paquete'] = htmlspecialchars($opcion['nombre_paquete']);
    }
    $conn = null;
    echo json_encode($opciones);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(array("exito" => false, "mensaje" => "Error en la consulta SQL: " . $e->getMessage()));
}
?>
