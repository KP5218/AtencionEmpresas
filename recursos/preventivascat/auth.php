<?php
//Creado por Barbara Vera

// realizo la conexion
include_once "conexion.php";

// Verifico si es post
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    header('Content-Type: application/json');

    // paso los datos del formulario a un json
    $data = json_decode(file_get_contents("php://input"));

    //aqui compruebo que los campos no esten vacios
    if (empty($data->usuario) || empty($data->clave)) {
        http_response_code(400);
        echo json_encode(["error" => "Complete los campos"]);
        exit;
    }

    $usuario = $data->usuario;
    $clave = $data->clave;

    // busco al usuario primero
    $query = "SELECT * FROM usuario WHERE usuario = :usuario";
    $stmt = $conn->prepare($query);
    $stmt->bindParam(':usuario', $usuario, PDO::PARAM_STR);
    $stmt->execute();

    //si se encontro al usuario entra
    if ($stmt->rowCount() == 1) {
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        //tomo la clave encriptada
        $clave_hash = $row['clave'];

        //la contra en bd es igual a la ingresada
        if (password_verify($clave, $clave_hash)) {
            session_start();
            //inicio la sesion y guardo el nombre del usuario logeado
            $_SESSION['usuario'] = $usuario;
            $response = ["mensaje" => "Inicio de sesión exitoso"];
        } else {
            // no son iguales las contras
            http_response_code(401);
            $response = ["error" => "Usuario o contraseña incorrectos"];
        }
    } else {
        // aqui se entra si el usuario no es valido
        http_response_code(401);
        $response = ["error" => "Usuario o contraseña incorrectos"];
    }

    echo json_encode($response);
} else {
    // esto se ejecuta si se intenta por otra forma que no sea post
    http_response_code(405);
    echo json_encode(["error" => "Método no permitido"]);
}
?>
