//Creado por Barbara Vera
document.addEventListener("DOMContentLoaded", function () {
    // Agrega un evento de clic al botón "Cerrar Sesión"
    document.getElementById("cerrarSesion").addEventListener("click", function () {
        // Realiza una solicitud para destruir la sesión actual
        fetch("logout.php")
            .then((response) => response.json())
            .then((data) => {
                if (data.loggedOut) {
                    // Si la sesión se cerró correctamente, redirige a la página de inicio de sesión
                    window.location.href = "login.html";
                }
            })
            .catch((error) => {
                console.error(error);
            });
    });
});