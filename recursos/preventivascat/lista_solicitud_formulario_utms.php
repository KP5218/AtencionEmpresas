<?php
include_once "conexion.php"; 

//compruebo que se haya iniciado sesion
session_start();
if (!isset($_SESSION["usuario"])) {
    http_response_code(401);
    echo json_encode(array("exito" => false, "mensaje" => "Acceso no permitido"));
    exit();
}

try {
    //obtengo el usuario
    $id_usuario = $_SESSION["usuario"];

    //lo busco en bd
    $sql = "SELECT rut, nombre_paciente, telefono, recepcionado, fecha_ingreso,fecha_recepcion 
            FROM examenes 
            WHERE usuario_id = :id_usuario";

    //compruebo si es una busqueda por fecha y se lo agrego a la sentencia sql
    if (isset($_GET['fechaInicio']) && isset($_GET['fechaFin'])) {
        $fechaInicio = $_GET['fechaInicio'];
        $fechaFin = $_GET['fechaFin'];
        $sql .= " AND fecha_ingreso BETWEEN :fechaInicio AND :fechaFin";
    }
    $sql .= " ORDER BY fecha_ingreso";
    $stmt = $conn->prepare($sql);
    $stmt->bindParam(':id_usuario', $id_usuario);

    //paso los parametros si es que son necesarios para la sentencia
    if (isset($_GET['fechaInicio']) && isset($_GET['fechaFin'])) {
        $stmt->bindParam(':fechaInicio', $fechaInicio);
        $stmt->bindParam(':fechaFin', $fechaFin);
    }

    $stmt->execute();
    $solicitudes = $stmt->fetchAll(PDO::FETCH_ASSOC);

    //envio la respuesta correspondiente
    foreach ($solicitudes as &$solicitud) {
        if ($solicitud['recepcionado'] === false) {
            $solicitud['estado'] = "Aún no encuentra recepcionado";
        }
        elseif ($solicitud['recepcionado'] === true) {
            $solicitud['estado'] = "Recepcionado;
        }
        
        unset($solicitud['recepcionado']);
        
    }
    $conn = null;
    echo json_encode($solicitudes);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(array("exito" => false, "mensaje" => "Error en la consulta SQL: " . $e->getMessage()));
}

?>
