//Funcion para tomar los datos de la tabla de registros y enviarlos a la bd
//y recibir una respuesta y el pdf

document.getElementById("idForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var tabla = document.getElementById("tablaBody");
    var filas = tabla.getElementsByTagName("tr");
    var datos = [];

    for (var i = 0; i < filas.length; i++) {
        var fila = filas[i];
        var celdas = fila.getElementsByTagName("td");
        var filaDatos = {};

        filaDatos.rut = celdas[0].textContent;
        filaDatos.nombre = celdas[1].textContent;
        filaDatos.telefono = celdas[2].textContent;
        filaDatos.comentario = celdas[3].textContent;

        datos.push(filaDatos);
    }

    fetch('http://localhost/preventivascat/formulario_utms.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(datos),
    })
    .then(response => {
        console.log("este es el response",response);
        if (!response.ok) {
            throw new Error('Hubo un problema con la solicitud: ' + response.statusText);
        }
        // Enviar el contenido del PDF al navegador para descargar
        return response.blob();
    })
    .then(blob => {
        // Crear una URL local para el blob del PDF
        var url = window.URL.createObjectURL(blob);
        // Crear un enlace y simular un clic para descargar el PDF
        var a = document.createElement('a');
        a.href = url;
        a.download = 'Solicitudes.pdf';
        a.click();
        // Liberar el objeto URL
        window.URL.revokeObjectURL(url);
        mostrarMensajeExito("Datos insertados correctamente");
            document.getElementById("rut_paciente").value = "";
            document.getElementById("nombre_paciente").value = "";
            document.getElementById("telefono_paciente").value = "";
            document.getElementById("comentario").value = "";
            tabla.innerHTML = ""; 
    })
    .catch((error) => {
        console.error('Error:', error);
        mostrarMensajeError(error);
    });
});
function mostrarMensajeExito(mensaje) {
    var alertContainer = document.getElementById("alert-container");
    var alertHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    alertContainer.innerHTML = alertHTML;
    document.getElementById("enviar").disabled = true;
    document.getElementById("borrar").disabled = true;
}

function mostrarMensajeError(mensaje) {
    var alertContainer = document.getElementById("alert-container");
    var alertHTML = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    alertContainer.innerHTML = alertHTML;
}
