//Creado por Barbara Vera
document.addEventListener("DOMContentLoaded", function () {
    // Verificar si la sesión del usuario existe
    fetch("session.php")
        .then((response) => response.json())
        .then((data) => {
            if (data.authenticated) {
                //si el usuario esta si pertenece a  alguno de estas organizaciones, si no lo es PERTENECE A EMPRESA asi que no redirigo
                if (data.pertenece == 'mutualidad') {
                    window.location.href = "formulario_mutual.html";
                }if (data.pertenece == 'utm') {
                    window.location.href = "formulario_utms.html";
                }
            } else {
                //si no esta logeado redirigo al login
                window.location.href = "login.html";
            }
        })
        .catch((error) => {
            console.error(error);
        });
});
