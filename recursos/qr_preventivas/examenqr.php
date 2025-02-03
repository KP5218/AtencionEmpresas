<?php
require_once('conexion.php');

//obtengo el codigo de la url
$examen = filter_input(INPUT_GET, 'id', FILTER_SANITIZE_STRING);

$valido = false;

//si el codigo no es nulo, busco toda la info en bd para usarla en el template
if ($examen !== null) {
    $codigo = pg_escape_string($conn, $examen);

    $sql = "SELECT valido, n_examen, cod_examen FROM qr_examen WHERE cod_encrip = $1";
    $stmt = pg_prepare($conn, "get_valido", $sql);

    $result = pg_execute($conn, "get_valido", array($codigo));

    if (pg_num_rows($result) > 0) {
        $row = pg_fetch_assoc($result);
        $valido = ($row['valido'] == 't'); 

        $n_examen = $row['n_examen'];
        $cod_examen = $row['cod_examen'];

        if (!empty($n_examen)) {
            $num = substr($codigo, 20);
            $sql_examen = "SELECT * FROM examenes WHERE n_examen = $1";
        } else {
            $valido = false;
        }

        if (isset($sql_examen)) {
            $stmt_examen = pg_prepare($conn, "get_examen", $sql_examen);
            $result_examen = pg_execute($conn, "get_examen", array($num));

            $examen = pg_fetch_all($result_examen) ?: [];
        }
    }

    pg_free_result($result);
    pg_close($conn);
} else {
    $valido = false;
}

require_once('examenqr.html');
?>
