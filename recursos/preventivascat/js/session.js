document.addEventListener("DOMContentLoaded", function () {
  var apiUrl = "http://localhost/recursos/preventivascat/auth.php";

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
      .then((response) => response.text()) // Obtener la respuesta como texto
      .then((responseText) => {
        console.log(responseText); // Inspecciona la respuesta

        // Intentar convertir la respuesta a JSON
        try {
          const data = JSON.parse(responseText);

          if (data.error) {
            mensajeError.textContent = data.error;
          } else {
            window.location.href = "home.html";
          }
        } catch (error) {
          // Si no es un JSON válido, mostrar un error
          console.error('Error al analizar JSON:', error);
          mensajeError.textContent = "Hubo un problema al procesar la respuesta del servidor.";
        }
      })
      .catch((error) => {
        console.error(error);
        mensajeError.textContent = "Hubo un error al realizar la solicitud.";
      });
  });
});

