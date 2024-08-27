<?php
require_once('conexion.php');

//obtengo el codigo de la url
$codigo = filter_input(INPUT_GET, 'id', FILTER_SANITIZE_STRING);

$codigo = pg_escape_string($conn, $codigo);

//busco si el codigo es valido
$sql = "SELECT valido FROM qr_solicitudes WHERE cod_encrip = $1";
$stmt = pg_prepare($conn, "get_valido", $sql);
$result = pg_execute($conn, "get_valido", array($codigo));

if (pg_num_rows($result) > 0) {
    $row = pg_fetch_assoc($result);
    $valido = $row['valido'];

    //si no es valido
    if($valido == 'f'){
        $valido = FALSE;
    }else{
        //si es valido obtengo los datos para usarlos en el template
        $num = substr($codigo, 20);
        $sql_solicitudes = "SELECT * FROM solicitudes WHERE n_solicitud = $1";
        $stmt_solicitudes = pg_prepare($conn, "get_solicitudes", $sql_solicitudes);
        $result_solicitudes = pg_execute($conn, "get_solicitudes", array($num));

        if (pg_num_rows($result_solicitudes) > 0) {
            $solicitudes = array();
            while ($row_solicitudes = pg_fetch_assoc($result_solicitudes)) {
                $solicitudes[] = $row_solicitudes;
            }
        } else {
            $solicitudes = array();
        }
    }
} else {
    $valido = FALSE;

}
pg_free_result($result);

pg_close($conn);

require_once('resultado.html');
?>