//Creado por Barbara Vera
document.addEventListener("DOMContentLoaded", function () {
    // Verificar si la sesión del usuario existe
    fetch("session.php")
        .then((response) => response.json())
        .then((data) => {
            if (data.authenticated) {
                //si esta logeado verifico si pertence a una de estas empresa pero si no es porque es de mutualidad
                if (data.pertenece == 'empresa') {
                    window.location.href = "formulario.html";
                }if (data.pertenece == 'utm') {
                    window.location.href = "formulario_utms.html";
                }
            } else {
                
                window.location.href = "login.html";
            }
        })
        .catch((error) => {
            console.error(error);
        });
});
