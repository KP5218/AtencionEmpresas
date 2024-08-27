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

            //ultimo n de examen (el general) para crear el siguiente
            $stmt = $conn->query("SELECT MAX(n_examen) AS max_examen FROM examenes");
            $max_examen = $stmt->fetch(PDO::FETCH_ASSOC)["max_examen"];
            $num_examen = ($max_examen !== null) ? $max_examen + 1 : 1;

            //obtengo el ultimo codigo de la tabla de examenes (son los individuales) para crear los siguientes
            $stmt2 = $conn->query("SELECT MAX(cod_examen) AS max_codexamen FROM examenes");
            $max_codexamen = $stmt2->fetch(PDO::FETCH_ASSOC)["max_codexamen"];
            $num_cod_examen = ($max_codexamen !== null) ? $max_codexamen + 1 : 1;

            $errores = [];

            //esto es para construir una encriptacion para el qr
            $letras = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
            $numeros = '0123456789';

            $caracteres = $letras . $numeros;
            $longitud = 20;

            $cadena = '';
            $cadena2 = '';
            for ($i = 0; $i < $longitud; $i++) {
                $cadena .= $caracteres[rand(0, strlen($caracteres) - 1)];
                $cadena2 .= $caracteres[rand(0, strlen($caracteres) - 1)];
            }
            
            $cadena .= strval($num_examen);

            //aqui instancio la funcion para crear pdfs
            $dompdf = new Dompdf();

            //paso el template al que le pasare los datos a convertir en pdf
            $template_html = file_get_contents(__DIR__ . '/pdf2.html');
            $template_html = str_replace('{titulo}', 'Examenes', $template_html);

            //Numero del documento
            $num_examen_str = strval($num_examen);
            $template_html = str_replace('{num_examen}', $num_examen_str, $template_html);

            $ruta_logo = 'img/Home.png';

            //qr para escanear los estados de todos registros 
            $logo_base64 = 'data:image/png;base64,' . base64_encode(file_get_contents($ruta_logo));
            $template_html = str_replace('{logo}', '<img src="' . $logo_base64 . '" class="logo" alt="Logo">', $template_html);

            $tabla_data = '';


            //for de lo recibido desde js
            foreach ($datos_tabla as $fila) {
                $rut = $fila["rut"];
                $nombre = $fila["nombre"];
                $telefono = $fila["telefono"];
                $comentario = $fila["comentario"];
                $examen = '01';

                $recepcionado = 'false';
                $valido = 'true';

                //ingreso a bd
                $stmt = $conn->prepare("INSERT INTO examenes (rut, nombre_paciente, usuario_id, fecha_ingreso, telefono, comentario, n_examen,
                valido,tipo_examen_id,cod_examen,recepcionado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)");
                $stmt->bindParam(1, $rut, PDO::PARAM_STR);
                $stmt->bindParam(2, $nombre, PDO::PARAM_STR);
                $stmt->bindParam(3, $usuario_logeado, PDO::PARAM_STR);
                $stmt->bindParam(4, $fecha_actual_str, PDO::PARAM_STR);
                $stmt->bindParam(5, $telefono, PDO::PARAM_STR);
                $stmt->bindParam(6, $comentario, PDO::PARAM_STR);
                $stmt->bindParam(7, $num_examen, PDO::PARAM_INT);
                $stmt->bindParam(8, $valido, PDO::PARAM_STR);
                $stmt->bindParam(9, $examen, PDO::PARAM_STR);
                $stmt->bindParam(10, $num_cod_examen, PDO::PARAM_STR);
                $stmt->bindParam(11, $recepcionado, PDO::PARAM_STR);
                
                if (!$stmt->execute()) {
                    $errores[] = "Error al insertar registro: " . implode(", ", $stmt->errorInfo());
                }

                //encriptacion para cada uno de los qr individuales
                $cadena3 = $cadena2 . strval($num_cod_examen);

                //genero el qr para cada uno
                $url = 'http://192.168.1.84:80/qr_preventivas/detalle_examen.php?id=' . $cadena3;
                $generator = new barcode_generator();
                $svg = $generator->render_svg("qr", $url, "");

                $tabla_data .= '<tr>
                                    <td style=" text-align: center;">' . $num_cod_examen . '</td>
                                    <td style=" text-align: center;">' . $fila["rut"] . '</td>
                                    <td style=" text-align: center;">' . $fila["nombre"] . '</td>
                                    <td style=" text-align: center;">' . $fila["telefono"] . '</td>
                                    <td style=" text-align: center;">' . '<img src="data:image/svg+xml;base64,' . base64_encode($svg) . '" style="width:100px "/>' . '</td>
                                </tr>';

                //inserto en bd los datos de los qr
                $stmt3 = $conn->prepare("INSERT INTO qr_examen (cod_encrip, valido, cod_examen) VALUES (?, ?, ?)");
                $stmt3->bindParam(1, $cadena3, PDO::PARAM_STR); 
                $stmt3->bindParam(2, $valido, PDO::PARAM_STR);
                $stmt3->bindParam(3, $num_cod_examen, PDO::PARAM_INT);
    
                if (!$stmt3->execute()) {
                    $errores[] = "Error al insertar registro en qr_examen: " . implode(", ", $stmt3->errorInfo());
                }
                //aumento el codigo de examen individual
                $num_cod_examen ++;

            }

            if (!empty($errores)) {
                throw new Exception("Hubo errores al insertar algunos registros", 500);
            }

            //guardo en bd el n de examen (el general)
            $stmt2 = $conn->prepare("INSERT INTO qr_examen (cod_encrip, valido, n_examen) VALUES (?, ?, ?)");
            $stmt2->bindParam(1, $cadena, PDO::PARAM_STR); 
            $stmt2->bindParam(2, $valido, PDO::PARAM_STR);
            $stmt2->bindParam(3, $num_examen, PDO::PARAM_INT);

            if (!$stmt2->execute()) {
                $errores[] = "Error al insertar registro en qr_solicitudes: " . implode(", ", $stmt2->errorInfo());
            }
            //////////////////////////////////////
            //obtengo datos importantes para la creacion del pdf

            $query = "SELECT u.usuario, u.nombre, u.utm_id, ut.nombre_utms
                FROM usuario u
                INNER JOIN utms ut ON u.utm_id = ut.cod_utms
                WHERE u.usuario = :usuario";
            $stmt = $conn->prepare($query);
            $stmt->bindParam(':usuario', $_SESSION['usuario'], PDO::PARAM_STR);
            $stmt->execute();

            if ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                $usuario = $row['usuario'];
                $responsable = $row['nombre'];
                $utm_id = $row['utm_id'];
                $nombre_utms = $row['nombre_utms'];
                

                $template_html = str_replace('{utm}', $nombre_utms, $template_html);
                $template_html = str_replace('{responsable}', $responsable, $template_html);
            }

            $template_html = str_replace('{fecha}', $fecha_actual->format('d-m-Y '), $template_html);
            $template_html = str_replace('{tabla_data}', $tabla_data, $template_html);

            //creo el qr general
            $url = 'http://192.168.1.84:80/qr_preventivas/examenqr.php?id=' . $cadena;
            $generator = new barcode_generator();
            $svg = $generator->render_svg("qr", $url, "");

            $template_html = str_replace('{codigo_qr}', '<img src="data:image/svg+xml;base64,' . base64_encode($svg) . '" class="qr-code" />', $template_html);
            
            //creo el pdf
            $dompdf->loadHtml($template_html);

            $dompdf->render();

            $pdf_content = $dompdf->output();

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
