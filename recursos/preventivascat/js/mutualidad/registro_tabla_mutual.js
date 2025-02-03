//funcion que agrega a la tabla del template los registros 

document.getElementById("agregar").addEventListener("click", function() {
    
    var rut = document.getElementById("rut_paciente").value;
    var nombre = document.getElementById("nombre_paciente").value;
    var telefono = document.getElementById("telefono_paciente").value;
    var paquete = document.getElementById("paquete").value;
    var comentario = document.getElementById("comentario").value;
    var tipo = document.getElementById("tipo").value;
    var tipo_formulario = ""; 
    var edad = document.getElementById("edad").value;
    var tipo_examen = document.getElementById("tipo_examen").value;
    var direccion = document.getElementById("direccion").value;
    var genero = document.getElementById("genero").value;

    if (document.getElementById("diep_check").checked) {
        tipo_formulario = "DIEP";
    } else if (document.getElementById("diat_check").checked) {
        tipo_formulario = "DIAT";
    }
    
    if (rut && nombre && telefono && comentario && tipo && genero && edad && direccion) {
        
        var fila = "<tr><td>" + rut + "</td><td>" + nombre + "</td><td>" + genero + "</td><td>" + edad + "</td><td>" + direccion + "</td><td>" + telefono + "</td><td>"+ tipo + "</td><td>" + tipo_formulario + "</td><td>" + tipo_examen + "</td><td>" + paquete + "</td><td>" + comentario + "</td></tr>";

        document.getElementById("tablaBody").innerHTML += fila;

        document.getElementById("rut_paciente").value = "";
        document.getElementById("nombre_paciente").value = "";
        document.getElementById("telefono_paciente").value = "";
        document.getElementById("paquete").value = "";
        document.getElementById("comentario").value = "";
        document.getElementById("tipo").value = "";
        document.getElementById("edad").value = "";
        document.getElementById("tipo_examen").value = "";
        document.getElementById("direccion").value = "";
        document.getElementById("genero").value = "";
        document.getElementById("selectPaquete").style.display = 'none';
        resetSelect('paquete');
        resetSelect('tipo_examen');
        document.getElementById("div_examen").style.display = 'none';
        document.getElementById("verDetalles").style.display = 'none';
        document.getElementById("botonPaquete").style.display = 'none';

        document.getElementById('caracteres_restantes').textContent = 160;

        document.getElementById("diep_check").checked = false;
        document.getElementById("diat_check").checked = false;

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


//funcion para borrar la ultima fila de la tabla de registros
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
