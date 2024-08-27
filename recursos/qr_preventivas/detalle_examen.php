<?php
require_once('conexion.php');

//obtengo el codigo de la url
$solicitud = filter_input(INPUT_GET, 'id', FILTER_SANITIZE_STRING);
$redirectUrl = '';

//si el codigo no es vacio creo la redireccion en una variable
if ($solicitud !== null) {
    $redirectUrl = "http://192.168.1.84/qr_preventivas/detalle_examen.php?id=" . urlencode($solicitud);
}

//si la solicitud es POST es porque se esta enviando info desde la pagina
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST['seleccion'])) {
    $fecha_actual = new DateTime('now', new DateTimeZone('UTC'));
    $fecha_actual_str = $fecha_actual->format('Y-m-d H:i:s');
    foreach ($_POST['seleccion'] as $idExamen) {
        $sql_update = "UPDATE examenes SET recepcionado = $2, fecha_recepcion = $3 WHERE cod_examen = $1";
        $stmt_update = pg_prepare($conn, "update_examen", $sql_update);

        $result_update = pg_execute($conn, "update_examen", array($idExamen, 'true',$fecha_actual_str));

        if (!$result_update) {
            die("Error al actualizar el examen: " . pg_last_error($conn));
        }
    }

    pg_close($conn);

    header("Location: " . $redirectUrl);
    exit(); 
}

//Busco la informacion del codigo para poder usarla desde el template
if ($solicitud !== null) {
    $valor = $solicitud;
    $codigo = pg_escape_string($conn, $solicitud);
    $num = substr($codigo, 20);

    $sql = "SELECT valido,cod_examen FROM qr_examen WHERE cod_encrip = $1";
    $stmt = pg_prepare($conn, "get_valido", $sql);
    $result = pg_execute($conn, "get_valido", array($codigo));

    if (pg_num_rows($result) > 0) {
        $row = pg_fetch_assoc($result);
        $valido = $row['valido'];
        $is_cod = $row['cod_examen'];

        if($valido == 'f' || $is_cod == null || $is_cod == '' ){
            $valido = FALSE;
        }else{
            
            $sql_examen = "SELECT * FROM examenes WHERE cod_examen = $1";
            $stmt_examen = pg_prepare($conn, "get_examen", $sql_examen);
            $result_examen = pg_execute($conn, "get_examen", array($num));

            if (pg_num_rows($result_examen) > 0) {
                $examen = array();
                while ($row_examen = pg_fetch_assoc($result_examen)) {
                    $examen[] = $row_examen;
                }
            } else {
                $examen = array();
            }
        }
    } else {
        $valido = FALSE;

    }
    pg_free_result($result);

    pg_close($conn);

} else{
    $valido = FALSE;
}



require_once('detalle_examen.html');
?>