<?php
include_once "conexion.php"; 

//verifico si el usuario esta logeado
session_start();
if (!isset($_SESSION["usuario"])) {
    http_response_code(401);
    echo json_encode(array("exito" => false, "mensaje" => "Acceso no permitido"));
    exit();
}

//si esta logeaod se ejecuta
try {
    //busco en bd los tipos de examen y los envio como respuesta
    $sql = "SELECT cod_examen, descripcion FROM tipo_examen";
    $stmt = $conn->prepare($sql);
    $stmt->execute();
    $opciones = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($opciones as &$opcion) {
        $opcion['descripcion'] = htmlspecialchars($opcion['descripcion']);
    }
    $conn = null;
    echo json_encode($opciones);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(array("exito" => false, "mensaje" => "Error en la consulta SQL: " . $e->getMessage()));
}
?>
