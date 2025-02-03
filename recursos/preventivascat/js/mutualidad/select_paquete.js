// Llamar a la función mostrarEntradas
document.addEventListener("DOMContentLoaded", function() {
    // Llamar a la función mostrarEntradas al cargar la página
    mostrarEntradas();
});

function mostrarEntradas() {
    var opcionSeleccionada = document.getElementById("tipo").value;

    ocultarEntradas();

    // Mostrar el campo de entrada según la opción seleccionada
    if (opcionSeleccionada === "01") {
        resetSelect('tipo_examen');
        document.getElementById("div_examen").style.display = 'none';
        document.getElementById("selectPaquete").style.display = 'block';
        document.getElementById("botonPaquete").style.display = 'block';
        document.getElementById("verDetalles").style.display = 'block';

            fetch('select_paquete.php')
            .then(response => response.json())
            .then(data => {
                llenarSelectPaquete('paquete', data);
            })
            .catch(error => console.error('Error al obtener las opciones:', error));

    } else if (opcionSeleccionada === "02") {
        document.getElementById("div_examen").style.display = 'none';
        document.getElementById("selectPaquete").style.display = 'none';
        document.getElementById("verDetalles").style.display = 'none';
        document.getElementById("botonPaquete").style.display = 'none';
        resetSelect('paquete');
        resetSelect('tipo_examen');
    } else if (opcionSeleccionada === "03") {
        document.getElementById("div_examen").style.display = 'none';
        document.getElementById("selectPaquete").style.display = 'none';
        document.getElementById("verDetalles").style.display = 'none';
        document.getElementById("botonPaquete").style.display = 'none';
        resetSelect('paquete');
        resetSelect('tipo_examen');
    }else if (opcionSeleccionada === "04") {
        document.getElementById("div_examen").style.display = 'none';
        document.getElementById("selectPaquete").style.display = 'none';
        document.getElementById("verDetalles").style.display = 'none';
        document.getElementById("botonPaquete").style.display = 'none';
        resetSelect('paquete');
        resetSelect('tipo_examen');
    } else if (opcionSeleccionada === "05") {
        document.getElementById("selectPaquete").style.display = 'none';
        document.getElementById("verDetalles").style.display = 'none';
        document.getElementById("botonPaquete").style.display = 'none';
        resetSelect('paquete');
        document.getElementById("div_examen").style.display = 'block';
    } else {
        document.getElementById("div_examen").style.display = 'none';
        document.getElementById("selectPaquete").style.display = 'none';
        document.getElementById("verDetalles").style.display = 'none';
        document.getElementById("botonPaquete").style.display = 'none';
        resetSelect('paquete');
        resetSelect('tipo_examen');
    }
}

// Función para ocultar todas las entradas
function ocultarEntradas() {
    // Ocultar todos los campos de entrada
    document.getElementById("paquete").closest('div').style.display = 'none';
    // Ocultar el campo de entrada por defecto
    document.getElementById("selectPaquete").style.display = 'none';
}


function llenarSelectPaquete(idSelect, opciones) {
    var select = document.getElementById(idSelect);
    
    select.innerHTML = "";
    
    var optionDefault = document.createElement("option");
    optionDefault.text = "Seleccione paquete";
    optionDefault.value = "";
    select.appendChild(optionDefault);
    
    opciones.forEach(opcion => {
        var option = document.createElement("option");
        option.text = opcion.nombre_paquete;
        option.value = opcion.cod_paquete;
        select.appendChild(option);
    });
}


function resetSelect(idSelect) {
    document.getElementById(idSelect).selectedIndex = 0;
}