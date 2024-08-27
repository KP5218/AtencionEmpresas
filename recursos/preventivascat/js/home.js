//Creado por Barbara Vera
//aqui verifico si el usuario esta logeado y si lo está el boton del home debe estar configurado para redireccionarlo
document.addEventListener("DOMContentLoaded", function () {
    var nombreUsuarioSpan = document.getElementById("nombreUsuario");

    fetch("session.php")
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            if (data.authenticated) {
                nombreUsuarioSpan.textContent = data.nombre;
                console.log(data.pertenece);
                if (data.pertenece == 'mutualidad') {
                    console.log('entroa  mutuL')
                    document.getElementById("solicitudButton").onclick = function() {
                        window.location.href = "formulario_mutual.html";
                    };
                }else if (data.pertenece == 'utm') {
                    console.log('entro a utm')
                    document.getElementById("solicitudButton").onclick = function() {
                        window.location.href = "formulario_utms.html";
                    };
                } else {
                    console.log('entro a empresa')
                    document.getElementById("solicitudButton").onclick = function() {
                        window.location.href = "formulario.html";
                    };
                }
                
            } 
        })
        .catch((error) => {
            console.error(error);
        });
});
