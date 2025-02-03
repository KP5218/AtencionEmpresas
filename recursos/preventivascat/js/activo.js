document.addEventListener("DOMContentLoaded", function () {
    // Verificar si la sesión del usuario existe
    fetch("session.php")
        .then((response) => response.json())
        .then((data) => {
            if (data.authenticated) {
                window.location.href = "home.html";
            } else {
                
            }
        })
        .catch((error) => {
            console.error(error);
        });
});
