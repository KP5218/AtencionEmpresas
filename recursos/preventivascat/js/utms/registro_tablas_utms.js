//funcion para agregar a la tabla del template los registros
document.getElementById("agregar").addEventListener("click", function() {
    
    var rut = document.getElementById("rut_paciente").value;
    var nombre = document.getElementById("nombre_paciente").value;
    var telefono = document.getElementById("telefono_paciente").value;
    var comentario = document.getElementById("comentario").value;

    
    if (rut && nombre && telefono && comentario) {
        
        var fila = "<tr><td>" + rut + "</td><td>" + nombre + "</td><td>" + telefono + "</td><td>" + comentario + "</td></tr>";

        document.getElementById("tablaBody").innerHTML += fila;

        document.getElementById("rut_paciente").value = "";
        document.getElementById("nombre_paciente").value = "";
        document.getElementById("telefono_paciente").value = "";
        document.getElementById("comentario").value = "";

        document.getElementById('caracteres_restantes').textContent = 160;

        document.getElementById("enviar").disabled = false;
        document.getElementById("borrar").disabled = false;
        document.getElementById("agregar").disabled = true;

        var alertaContainer = document.getElementById("alert-container");
        if (alertaContainer.classList.contains("show")) {
            alertaContainer.classList.remove("show");
        }
    } else {
        var alertaHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                Por favor complete todos los campos antes de agregar a la tabla.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        document.getElementById("alert-container").innerHTML = alertaHTML;
    }
});

//funcion para eliminar el ultimo registro de la tabla del template
document.getElementById("borrar").addEventListener("click", function() {
    var tabla = document.getElementById("tablaBody");
    var filas = tabla.getElementsByTagName("tr");

    if (filas.length > 0) {
        tabla.deleteRow(filas.length - 1);

        
        if (filas.length < 1) {
            document.getElementById("enviar").disabled = true;
            document.getElementById("borrar").disabled = true;
        }
    }
});
