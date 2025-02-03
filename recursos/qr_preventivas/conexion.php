<?php
require_once('config.php');

$conn = pg_connect("host=" . DB_HOST . " port=" . DB_PORT . " dbname=" . DB_NAME . " user=" . DB_USER . " password=" . DB_PASSWORD);

if (!$conn) {
    die("Conexión fallida: " . pg_last_error());
} else {

}

?>