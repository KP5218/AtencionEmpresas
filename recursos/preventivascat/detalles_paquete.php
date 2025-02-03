<?php
include_once "conexion.php"; 

//compruebo que la sesion esté iniciada
session_start();
if (!isset($_SESSION["usuario"])) {
    http_response_code(401);
    echo json_encode(array("exito" => false, "mensaje" => "Acceso no permitido"));
    exit();
}

//compruebo que el codigo venga en la url
if (!isset($_GET['codigo'])) {
    http_response_code(400);
    echo json_encode(array("exito" => false, "mensaje" => "Falta el parámetro 'codigo'"));
    exit();
}

//obtengo el codigo
$cod_paquete = $_GET['codigo'];

try {
    //busco la info en bd
    $sql ="SELECT p.cod_prestacion, p.prestacion
            FROM paquete_prestacion pp
            INNER JOIN prestacion p ON pp.cod_prestacion_id = p.cod_prestacion
            WHERE pp.cod_paquete_id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->execute([$cod_paquete]);
    $detalles_prestaciones = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $conn = null;
    echo json_encode($detalles_prestaciones);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(array("exito" => false, "mensaje" => "Error en la consulta SQL: " . $e->getMessage()));
}

?>
