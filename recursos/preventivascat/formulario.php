<?php
include_once "conexion.php";
include_once "respuesta.php";
require_once __DIR__ . '/vendor/autoload.php';
include "lib/barcode.php";

use Dompdf\Dompdf;

//dominios
$dominios = array("http://localhost");

//verifico dominio
if (isset($_SERVER['HTTP_ORIGIN']) && in_array($_SERVER['HTTP_ORIGIN'], $dominios)) {
    header("Access-Control-Allow-Origin: " . $_SERVER['HTTP_ORIGIN']);
} else {
    http_response_code(403);
    exit();
}

//aqui recibo la info del js
$inputJSON = file_get_contents('php://input');
$datos_tabla = json_decode($inputJSON, true);

//usuario autenticado
if ($response["authenticated"]) {
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        try {
            if ($datos_tabla === null) {
                throw new Exception("Error al decodificar los datos JSON: " . json_last_error_msg(), 400);
            }

            //obtengo el usuario y la fecha actual
            $usuario_logeado = $response["usuario"];
            $fecha_actual = new DateTime('now', new DateTimeZone('UTC'));
            $fecha_actual_str = $fecha_actual->format('Y-m-d H:i:s');

            //ultimo n de solicitucd (el general) para crear el siguiente
            $stmt = $conn->query("SELECT MAX(n_solicitud) AS max_solicitud FROM solicitudes");
            $max_solicitud = $stmt->fetch(PDO::FETCH_ASSOC)["max_solicitud"];
            $num_solicitud = ($max_solicitud !== null) ? $max_solicitud + 1 : 1;

            //obtengo el ultimo codigo de la tabla de solicitudes (son los individuales) para crear los siguientes
            $stmt2 = $conn->query("SELECT MAX(cod_solicitud) AS max_codsolicitud FROM solicitudes");
            $max_codsolicitud = $stmt2->fetch(PDO::FETCH_ASSOC)["max_codsolicitud"];
            $num_codsolicitud = ($max_codsolicitud !== null) ? $max_codsolicitud + 1 : 1;

            $errores = [];

            //esto es para construir una encriptacion para el qr
            $letras = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
            $numeros = '0123456789';

            $caracteres = $letras . $numeros;
            $longitud = 20;

            $cadena = '';
            for ($i = 0; $i < $longitud; $i++) {
                $cadena .= $caracteres[rand(0, strlen($caracteres) - 1)];
            }
            
            $cadena .= strval($num_solicitud);

            //for de lo recibido desde js
            foreach ($datos_tabla as $fila) {
                $paquete = $fila["paquete"];
                $rut = $fila["rut"];
                $nombre = $fila["nombre"];
                $telefono = $fila["telefono"];
                $comentario = $fila["comentario"];
                $tipo = $fila["tipo"];
                $examen = $fila["examen"];

                $ingresado = 'true';
                $valido = 'true';

                if(empty($paquete)){
                    $paquete = null;
                }
                if(empty($examen)){
                    $examen = null;
                }

                //ingreso a bd
                $stmt = $conn->prepare("INSERT INTO solicitudes (rut, nombre_solicitante, usuario_id, fecha_ingreso, telefono, comentario, paquete_id, tipo_solicitud_id, n_solicitud,
                ingresado,valido,tipo_examen_id,cod_solicitud) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?)");
                $stmt->bindParam(1, $rut, PDO::PARAM_STR);
                $stmt->bindParam(2, $nombre, PDO::PARAM_STR);
                $stmt->bindParam(3, $usuario_logeado, PDO::PARAM_STR);
                $stmt->bindParam(4, $fecha_actual_str, PDO::PARAM_STR);
                $stmt->bindParam(5, $telefono, PDO::PARAM_STR);
                $stmt->bindParam(6, $comentario, PDO::PARAM_STR);
                $stmt->bindParam(7, $paquete, PDO::PARAM_STR);
                $stmt->bindParam(8, $tipo, PDO::PARAM_STR);
                $stmt->bindParam(9, $num_solicitud, PDO::PARAM_INT);
                $stmt->bindParam(10, $ingresado, PDO::PARAM_STR);
                $stmt->bindParam(11, $valido, PDO::PARAM_STR);
                $stmt->bindParam(12, $examen, PDO::PARAM_STR);
                $stmt->bindParam(13, $num_codsolicitud, PDO::PARAM_STR);
                
                if (!$stmt->execute()) {
                    $errores[] = "Error al insertar registro: " . implode(", ", $stmt->errorInfo());
                }
                //aumento el codigo de solcitud individual
                $num_codsolicitud ++;
            }

            if (!empty($errores)) {
                throw new Exception("Hubo errores al insertar algunos registros", 500);
            }

            //inserto en tabla de qr
            $stmt2 = $conn->prepare("INSERT INTO qr_solicitudes (cod_encrip, valido, n_solicitud) VALUES (?, ?, ?)");
            $stmt2->bindParam(1, $cadena, PDO::PARAM_STR); 
            $stmt2->bindParam(2, $valido, PDO::PARAM_STR);
            $stmt2->bindParam(3, $num_solicitud, PDO::PARAM_INT);

            if (!$stmt2->execute()) {
                $errores[] = "Error al insertar registro en qr_solicitudes: " . implode(", ", $stmt2->errorInfo());
            }

            //instancio el objeto de pdf
            $dompdf = new Dompdf();

            $template_html = file_get_contents(__DIR__ . '/pdf.html');
            $template_html = str_replace('{titulo}', 'Solicitud ingresada', $template_html);

            $num_solicitud_str = strval($num_solicitud);
            $template_html = str_replace('{num_solicitud}', $num_solicitud_str, $template_html);

            $ruta_logo = 'img/Home.png';

            //creo la imagen
            $logo_base64 = 'data:image/png;base64,' . base64_encode(file_get_contents($ruta_logo));
            $template_html = str_replace('{logo}', '<img src="' . $logo_base64 . '" class="logo" alt="Logo">', $template_html);

            $tabla_data = '';
            //creo los registros de la tabla del pdf
            foreach ($datos_tabla as $fila) {
                $tabla_data .= '<tr>
                                    <td>' . $fila["rut"] . '</td>
                                    <td>' . $fila["nombre"] . '</td>
                                    <td>' . $fila["telefono"] . '</td>
                                    <td>' . $fila["comentario"] . '</td>
                                </tr>';
            }

            $template_html = str_replace('{tabla_data}', $tabla_data, $template_html);

            //creo el qr y su informacion
            $url = 'http://192.168.1.84:80/qr_preventivas/datosqr.php?id=' . $cadena;
            $generator = new barcode_generator();
            $svg = $generator->render_svg("qr", $url, "");

            $template_html = str_replace('{codigo_qr}', '<img src="data:image/svg+xml;base64,' . base64_encode($svg) . '" class="qr-code" />', $template_html);
            
            //creo el pdf
            $dompdf->loadHtml($template_html);

            $dompdf->render();

            $pdf_content = $dompdf->output();

            //devuelvo el pdf como respuesta
            echo $pdf_content;

            $conn = null;

            echo json_encode(array("exito" => true, "mensaje" => "Todos los registros insertados correctamente"));
        } catch (Exception $e) {
            http_response_code($e->getCode());
            echo json_encode(array("exito" => false, "mensaje" => $e->getMessage()));
        }
    } else {
        http_response_code(405); 
        echo json_encode(array("exito" => false, "mensaje" => "Acceso no permitido"));
    }
} else {
    http_response_code(401); 
    echo json_encode(array("exito" => false, "mensaje" => "Acceso no permitido"));
}
?>
