<?php
include_once "conexion.php"; 

//verifico que el usuario este logeado
session_start();
if (!isset($_SESSION["usuario"])) {
    http_response_code(401);
    echo json_encode(array("exito" => false, "mensaje" => "Acceso no permitido"));
    exit();
}

//si el usuario esta logeado se ejecuta esto
try {
    $id_usuario = $_SESSION["usuario"];
    //obtengo los datos que necesito mostrar en el template
    $sql = "SELECT rut, nombre_solicitante, telefono, ingresado, agendado, fecha_ingreso 
            FROM solicitudes 
            WHERE usuario_id = :id_usuario";

    //verifico si se enviaron fechas para filtrar
    if (isset($_GET['fechaInicio']) && isset($_GET['fechaFin'])) {
        $fechaInicio = $_GET['fechaInicio'];
        $fechaFin = $_GET['fechaFin'];
        $sql .= " AND fecha_ingreso BETWEEN :fechaInicio AND :fechaFin";
    }
    $sql .= " ORDER BY fecha_ingreso";
    $stmt = $conn->prepare($sql);
    $stmt->bindParam(':id_usuario', $id_usuario);

    //añado los parametros de fecha si es necesario
    if (isset($_GET['fechaInicio']) && isset($_GET['fechaFin'])) {
        $stmt->bindParam(':fechaInicio', $fechaInicio);
        $stmt->bindParam(':fechaFin', $fechaFin);
    }

    //ejecuto
    $stmt->execute();
    $solicitudes = $stmt->fetchAll(PDO::FETCH_ASSOC);

    //preparo la respuesta 
    foreach ($solicitudes as &$solicitud) {
        if ($solicitud['agendado'] === true) {
            $solicitud['estado'] = "Agendado";
        } elseif ($solicitud['agendado'] === null) {
            $solicitud['estado'] = "Ingresado";
        }
        
        unset($solicitud['ingresado']);
        unset($solicitud['agendado']);
    }
    $conn = null;
    echo json_encode($solicitudes);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(array("exito" => false, "mensaje" => "Error en la consulta SQL: " . $e->getMessage()));
}

?>
