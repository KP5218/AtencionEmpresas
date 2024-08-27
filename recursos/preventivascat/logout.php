<?php
//Creado por Barbara Vera

session_start();

// Verifica si hay una sesión activa
if (isset($_SESSION['usuario'])) {
    // Destruye la sesión actual
    session_destroy();
    $response = ["loggedOut" => true];
} else {
    $response = ["loggedOut" => false];
}

// Establece la cabecera Content-Type para JSON
header('Content-Type: application/json');

echo json_encode($response);
?>
