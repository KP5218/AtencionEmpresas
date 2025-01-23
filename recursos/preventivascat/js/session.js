
//esto sirve para saber si las credenciales del usuario son correctas
//si lo son se inicia sesion y redirige al home
document.addEventListener("DOMContentLoaded", function () {
  var apiUrl = "http://localhost/preventivascat/auth.php";

  var usuarioInput = document.getElementById("usuario");
  var claveInput = document.getElementById("clave");
  var loginButton = document.getElementById("loginButton"); 
  var mensajeError = document.getElementById("mensajeError");

  loginButton.addEventListener("click", function (e) {
    e.preventDefault();

    var usuario = usuarioInput.value;
    var clave = claveInput.value;

    fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ usuario, clave }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          mensajeError.textContent = data.error;
        } else {
          window.location.href = "home.html";
        }
      })
      .catch((error) => {
        console.error(error);
      });
  });
});
