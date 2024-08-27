 var checksData = [];
 document.addEventListener("DOMContentLoaded", function() {
        mostrarEntradas();
    });

 // Función para mostrar todas las entradas
 function mostrarEntradas() {
        var opcionSeleccionada = document.getElementById("busqueda").value;

        ocultarEntradas();

        switch (opcionSeleccionada) {
            case "codigo1":
                document.getElementById("busquedaCodigo").closest('div').style.display = 'block';
                break;
            case "codigo2":
                document.getElementById("busquedaRut").closest('div').style.display = 'block';
                break;
            case "codigo3":
                document.getElementById("busquedaNomUtm").closest('div').style.display = 'block';
                break;
            case "codigo4":
                document.getElementById("busquedaNexamen").closest('div').style.display = 'block';
                break;
            case "codigo5":
                document.getElementById("busquedafecha1").closest('div').style.display = 'block';
                document.getElementById("busquedafecha2").closest('div').style.display = 'block';
                break;

        }


        document.getElementById("botonbusqueda").closest('div').style.display = 'block';

    }


// Función para ocultar todas las entradas
function ocultarEntradas() {
    document.getElementById("busquedaCodigo").closest('div').style.display = 'none';
    document.getElementById("busquedaRut").closest('div').style.display = 'none';
    document.getElementById("busquedaNomUtm").closest('div').style.display = 'none';
    document.getElementById("busquedafecha1").closest('div').style.display = 'none';
    document.getElementById("busquedafecha2").closest('div').style.display = 'none';
    document.getElementById("busquedaNexamen").closest('div').style.display = 'none'
    document.getElementById("mensaje1").closest('div').style.display = 'none';
    document.getElementById("mensaje2").closest('div').style.display = 'none';
    document.getElementById("mensaje3").closest('div').style.display = 'none';
    document.getElementById("mensaje4").closest('div').style.display = 'none';
    document.getElementById("mensaje5").closest('div').style.display = 'none';


    // Ocultar el campo de entrada por defecto
    document.getElementById("busquedaRutDiv").style.display = 'none';

    $('#table-body').empty();
    $('#pagination').empty();
}


///////////////////////////////---------------Filtro Codigo------------/////////////////////////////////
$(document).ready(function() {
    $('#filtro').click(function() {
        $('#table-body').empty();
        var codigo = $('#busquedaCodigo').val().trim();
        $('#busquedaCodigo').val("");
        var mensajeElement = $('#mensaje1');
        if (!codigo || isNaN(codigo)) {
         mostrarMensaje("Por favor ingrese un código válido.");
        return;
        }

        $.ajax({
            url: 'filtroCodigo/',
            method: 'POST',
            data: {
                'busquedaCodigo': codigo,
            },
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    mostrarMensaje("");
                } else {
                    mostrarMensaje("No se encontró código.");
                }
            }
        });
    });
    function mostrarMensaje(mensaje) {
        if (mensaje.includes("No se encontró codigo.")) {
            $('#mensaje1').text(mensaje).addClass('error').show();
        } else {
            $('#mensaje1').text(mensaje).removeClass('error').show();
        }
    }
    function mostrarPagina(data, numeroPagina, filasPorPagina) {
        $('#table-body').empty();
        var inicio = (numeroPagina - 1) * filasPorPagina;
        var fin = Math.min(inicio + filasPorPagina, data.length);
        for (var i = inicio; i < fin; i++) {
            var examen = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(examen.codigo),
                $('<td>').text(examen.rut),
                $('<td>').text(examen.nombre_solicitante),
                $('<td>').text(examen.telefono),
                $('<td>').text(examen.tipo_examen),
                $('<td>').text(examen.fecha),
                $('<td>').text(examen.solicitante),
                $('<td>').append(
                 $('<input>').attr('type', 'checkbox').click(function() {
                        var ischecked = $(this).is(':checked');
                        var examenCodigo = $(this).closest('tr').find('td:first').text();
                        var checkData = {
                            isChecked: ischecked,
                            examenCodigo: examenCodigo
                        };
                        // Verifica si ya existe un código en el array
                        var index = checksData.findIndex(function(item) {
                            return item.examenCodigo === examenCodigo;
                        });
                        if (index !== -1) {
                            // Si existe actualizar su estado
                            checksData[index].isChecked = ischecked;
                        } else {
                            // Si no existe agregarlo al array
                            checksData.push(checkData);
                        }
                        var jsonData = JSON.stringify(checksData);
                        document.getElementById('checkbox').value = JSON.stringify(checksData);
                    })
                )
            );
            $('#table-body').append(fila);
        }
        if (data.length > filasPorPagina) {
            var totalPaginas = Math.ceil(data.length / filasPorPagina);
            $('#pagination').empty();
            for (var i = 1; i <= totalPaginas; i++) {
                var btnPagina = $('<button>').text(i).addClass('btn pagination-btn').attr('type', 'button');
                if (i === numeroPagina) {
                    btnPagina.addClass('active');
                }
                btnPagina.click((function(pagina) {
                    return function() {
                        mostrarPagina(data, pagina, filasPorPagina);
                    };
                })(i)).mouseenter(function() {
                    $(this).css('background-color', 'rgba(255, 255, 255, 0.2)');
                }).mouseleave(function() {
                    $(this).css('background-color', '');
                }).css('border', 'none');
                $('#pagination').append(btnPagina);
            }
        }
        else {
            $('#pagination').empty();
        }
    }
});


///////////////////////////////---------------Filtro fecha------------/////////////////////////////////
$('#filtro').click(function() {
    $('#table-body').empty();
    if ($('#busquedafecha1').css('display') !== 'none' && $('#busquedafecha2').css('display') !== 'none') {

        var fechaInicio = $('#fechaInicio').val();
        var fechaFin = $('#fechaFin').val();

        if (fechaInicio === '' || fechaFin === '') {
            mostrarMensaje("Por favor ingrese una fecha de inicio y una fecha de fin.");
            return;
        }

        if (!isValidDate(fechaInicio) || !isValidDate(fechaFin)) {
            mostrarMensaje("Formato de fecha no válido. Utilice el formato YYYY-MM-DD.");
            return;
        }

        var fechaActual = new Date().toISOString().split('T')[0];
        if (fechaInicio > fechaActual) {
            mostrarMensaje("Las fechas de búsqueda no pueden ser posteriores a la fecha actual.");
            return;
        }

        if (fechaInicio > fechaFin) {
            mostrarMensaje("La fecha de inicio no puede ser posterior a la fecha de fin.");
            return;
        }

        $.ajax({
            url: 'filtroFecha/',
            method: 'POST',
            data: {
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
            },
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    mostrarMensaje("");
                } else {
                    mostrarMensaje("No se encontraron solicitudes para estas fechas.");
                }
            }
        });

        $('#busquedafecha1').show();
        $('#busquedafecha2').show();
    }
});

function mostrarMensaje(mensaje) {

$('#mensaje5').text(mensaje).addClass('error').show();
}
function isValidDate(dateString) {
    var regexDate = /^\d{4}-\d{2}-\d{2}$/;
    return dateString.match(regexDate);
}
function mostrarPagina(data, numeroPagina, filasPorPagina) {
    $('#table-body').empty();

    var inicio = (numeroPagina - 1) * filasPorPagina;
    var fin = inicio + filasPorPagina;
    for (var i = inicio; i < fin && i < data.length; i++) {
         var examen = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(examen.codigo),
                $('<td>').text(examen.rut),
                $('<td>').text(examen.nombre_solicitante),
                $('<td>').text(examen.telefono),
                $('<td>').text(examen.Examen),
                $('<td>').text(examen.fecha),
                $('<td>').text(examen.solicitante),
                $('<td>').append(
                    $('<input>').attr('type', 'checkbox').click(function() {
                        var ischecked = $(this).is(':checked');
                        var examenCodigo = $(this).closest('tr').find('td:first').text();
                        var checkData = {
                            isChecked: ischecked,
                            examenCodigo: examenCodigo
                        };
                        // Verifica si ya existe un código en el array
                        var index = checksData.findIndex(function(item) {
                            return item.examenCodigo === examenCodigo;
                        });
                        if (index !== -1) {
                            // Si existe actualizar su estado
                            checksData[index].isChecked = ischecked;
                        } else {
                            // Si no existe agregarlo al array
                            checksData.push(checkData);
                        }
                        var jsonData = JSON.stringify(checksData);
                        document.getElementById('checkbox').value = JSON.stringify(checksData);
                    })
                )
            );
            $('#table-body').append(fila);
    }

    if (data.length > filasPorPagina) {
            var totalPaginas = Math.ceil(data.length / filasPorPagina);
            $('#pagination').empty();
            for (var i = 1; i <= totalPaginas; i++) {
                var btnPagina = $('<button>').text(i).addClass('btn pagination-btn').attr('type', 'button');
                if (i === numeroPagina) {
                    btnPagina.addClass('active');
                }
                btnPagina.click((function(pagina) {
                    return function() {
                        mostrarPagina(data, pagina, filasPorPagina);
                    };
                })(i)).mouseenter(function() {
                    $(this).css('background-color', 'rgba(255, 255, 255, 0.2)');
                }).mouseleave(function() {
                    $(this).css('background-color', '');
                }).css('border', 'none');
                $('#pagination').append(btnPagina);
            }
        } else {
            $('#pagination').empty();
        }

}

///////////////////////////////---------------Filtro rut------------/////////////////////////////////
$(document).ready(function() {
    $('#filtro').click(function() {
        $('#table-body').empty();
        var rut = $('#busquedaRut').val().trim();
        $('#busquedaRut').val("");
        var mensajeElement = $('#mensaje2');

        if (!validarRut(rut)) {
            mostrarMensaje("Por favor ingrese un RUT válido.");
            return;
        }
        $.ajax({
            url: 'filtroRut/',
            method: 'POST',
            data: {
                'busquedaRut': rut,
            },
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    mostrarMensaje("");
                } else {
                    mostrarMensaje("No se encontró rut.");
                }
            }
        });
    });
    // Función para validar el RUT
    function validarRut(rut) {
        return /^0*(\d{1,3}(\.?\d{3})*)\-?([\dkK])$/.test(rut);
    }
    // Función para mostrar un mensaje
    function mostrarMensaje(mensaje) {
        if (mensaje === "No se encontró rut.") {
            $('#mensaje2').text(mensaje).addClass('error').show();
        } else {
            $('#mensaje2').text(mensaje).removeClass('error').show();
        }
    }
    function mostrarPagina(data, numeroPagina, filasPorPagina) {
        $('#table-body').empty();
        var inicio = (numeroPagina - 1) * filasPorPagina;
        var fin = inicio + filasPorPagina;
        for (var i = inicio; i < fin && i < data.length; i++) {
            var examen = data[i];
           var fila = $('<tr>').append(
                $('<td>').text(examen.codigo),
                $('<td>').text(examen.rut),
                $('<td>').text(examen.nombre_solicitante),
                $('<td>').text(examen.telefono),
                $('<td>').text(examen.tipo_examen),
                $('<td>').text(examen.fecha),
                $('<td>').text(examen.solicitante),
                $('<td>').append(
                    $('<input>').attr('type', 'checkbox').click(function() {
                        var ischecked = $(this).is(':checked');
                        var examenCodigo = $(this).closest('tr').find('td:first').text();
                        var checkData = {
                            isChecked: ischecked,
                            examenCodigo: examenCodigo
                        };
                        // Verifica si ya existe un código en el array
                        var index = checksData.findIndex(function(item) {
                            return item.examenCodigo === examenCodigo;
                        });
                        if (index !== -1) {
                            // Si existe actualizar su estado
                            checksData[index].isChecked = ischecked;
                        } else {
                            // Si no existe agregarlo al array
                            checksData.push(checkData);
                        }
                        var jsonData = JSON.stringify(checksData);
                        document.getElementById('checkbox').value = JSON.stringify(checksData);
                    })
                )
            );
            $('#table-body').append(fila);
        }
        if (data.length > filasPorPagina) {
            var totalPaginas = Math.ceil(data.length / filasPorPagina);
            $('#pagination').empty();
            for (var i = 1; i <= totalPaginas; i++) {
                var btnPagina = $('<button>').text(i).addClass('btn pagination-btn').attr('type', 'button');
                if (i === numeroPagina) {
                    btnPagina.addClass('active');
                }
                btnPagina.click((function(pagina) {
                    return function() {
                        mostrarPagina(data, pagina, filasPorPagina);
                    };
                })(i)).mouseenter(function() {
                  $(this).css('background-color', 'rgba(255, 255, 255, 0.2)');
                }).mouseleave(function() {
                    $(this).css('background-color', '');
                }).css('border', 'none');
                $('#pagination').append(btnPagina);
            }
        }
    }
});


///////////////////////////////---------------Filtro número de examen------------/////////////////////////////////
$(document).ready(function() {
    $('#filtro').click(function() {
        $('#table-body').empty();
        var nExamen = $('#busquedaNexamen').val().trim();
        $('#busquedaNexamen').val("");
        var mensajeElement = $('#mensaje4');
        if (!nExamen || isNaN(nExamen))  {
            mostrarMensaje("Por favor ingrese un número de examen valido.");
            return;
        }
        $.ajax({
            url: 'filtro_n_examen/',
            method: 'POST',
            data: {
                'busquedaNexamen': nExamen ,
            },
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    mostrarMensaje("");
                } else {
                    mostrarMensaje("No se encontró número de examen.");
                }
            }
        });
    });
    function mostrarMensaje(mensaje) {
        if (mensaje.includes("No se encontró número de examen.")) {
            $('#mensaje4').text(mensaje).addClass('error').show();
        } else {
            $('#mensaje4').text(mensaje).removeClass('error').show();
        }
    }
    function mostrarPagina(data, numeroPagina, filasPorPagina) {
        $('#table-body').empty();
        var inicio = (numeroPagina - 1) * filasPorPagina;
        var fin = Math.min(inicio + filasPorPagina, data.length);
        for (var i = inicio; i < fin; i++) {
            var examen = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(examen.codigo),
                $('<td>').text(examen.rut),
                $('<td>').text(examen.nombre_solicitante),
                $('<td>').text(examen.telefono),
                $('<td>').text(examen.tipo_examen),
                $('<td>').text(examen.fecha),
                $('<td>').text(examen.solicitante),
                $('<td>').append(
                    $('<input>').attr('type', 'checkbox').click(function() {
                        var ischecked = $(this).is(':checked');
                        var examenCodigo = $(this).closest('tr').find('td:first').text();
                        var checkData = {
                            isChecked: ischecked,
                            examenCodigo: examenCodigo
                        };
                        // Verifica si ya existe un código en el array
                        var index = checksData.findIndex(function(item) {
                            return item.examenCodigo === examenCodigo;
                        });
                        if (index !== -1) {
                            // Si existe actualizar su estado
                            checksData[index].isChecked = ischecked;
                        } else {
                            // Si no existe agregarlo al array
                            checksData.push(checkData);
                        }
                        var jsonData = JSON.stringify(checksData);
                        document.getElementById('checkbox').value = JSON.stringify(checksData);
                    })
                )
            );
            $('#table-body').append(fila);
        }
        if (data.length > filasPorPagina) {
            var totalPaginas = Math.ceil(data.length / filasPorPagina);
            $('#pagination').empty();
            for (var i = 1; i <= totalPaginas; i++) {
                var btnPagina = $('<button>').text(i).addClass('btn pagination-btn').attr('type', 'button');
                if (i === numeroPagina) {
                    btnPagina.addClass('active');
                }
                btnPagina.click((function(pagina) {
                    return function() {
                        mostrarPagina(data, pagina, filasPorPagina);
                    };
                })(i)).mouseenter(function() {
                    $(this).css('background-color', 'rgba(255, 255, 255, 0.2)');
                }).mouseleave(function() {
                    $(this).css('background-color', '');
                }).css('border', 'none');
                $('#pagination').append(btnPagina);
            }
        }
        else {
            $('#pagination').empty();
        }
    }
});


///////////////////////////////---------------Filtro Nombre utm------------/////////////////////////////////
$(document).ready(function() {
    $('#filtro').click(function() {
        $('#table-body').empty();
        var NombreUtm = $('#busquedaNomUtm').val().trim();
        $('#busquedaNomUtm').val("");
        var mensajeElement = $('#mensaje3');
        if (!NombreUtm) {
            mostrarMensaje("Por favor ingrese un nombre de utm valido.");
            return;
        }
        $.ajax({
            url: 'filtro_nombre_Utm/',
            method: 'POST',
            data: {
                'busquedaNomUtm': NombreUtm,
            },
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    mostrarMensaje("");
                } else {
                    mostrarMensaje("No se encontró utm.");
                }
            }
        });
    });

    function mostrarMensaje(mensaje) {
        if (mensaje.includes("No se encontró utm.")) {
            $('#mensaje3').text(mensaje).addClass('error').show();
        } else {
            $('#mensaje3').text(mensaje).removeClass('error').show();
        }
    }

    function mostrarPagina(data, numeroPagina, filasPorPagina) {
        $('#table-body').empty();
        var inicio = (numeroPagina - 1) * filasPorPagina;
        var fin = Math.min(inicio + filasPorPagina, data.length);
        for (var i = inicio; i < fin; i++) {
            var examen = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(examen.codigo),
                $('<td>').text(examen.rut),
                $('<td>').text(examen.nombre_solicitante),
                $('<td>').text(examen.telefono),
                $('<td>').text(examen.tipo_examen),
                $('<td>').text(examen.fecha),
                $('<td>').text(examen.solicitante),
                $('<td>').append(
                    $('<input>').attr('type', 'checkbox').click(function() {
                        var ischecked = $(this).is(':checked');
                        var examenCodigo = $(this).closest('tr').find('td:first').text();
                        var checkData = {
                            isChecked: ischecked,
                            examenCodigo: examenCodigo
                        };
                        // Verifica si ya existe un código en el array
                        var index = checksData.findIndex(function(item) {
                            return item.examenCodigo === examenCodigo;
                        });
                        if (index !== -1) {
                            // Si existe actualizar su estado
                            checksData[index].isChecked = ischecked;
                        } else {
                            // Si no existe agregarlo al array
                            checksData.push(checkData);
                        }
                        var jsonData = JSON.stringify(checksData);
                        document.getElementById('checkbox').value = JSON.stringify(checksData);
                    })
                )
            );
            $('#table-body').append(fila);
        }
        if (data.length > filasPorPagina) {
            var totalPaginas = Math.ceil(data.length / filasPorPagina);
            $('#pagination').empty();
            for (var i = 1; i <= totalPaginas; i++) {
                var btnPagina = $('<button>').text(i).addClass('btn pagination-btn').attr('type', 'button');
                if (i === numeroPagina) {
                    btnPagina.addClass('active');
                }
                btnPagina.click((function(pagina) {
                    return function() {
                        mostrarPagina(data, pagina, filasPorPagina);
                    };
                })(i)).mouseenter(function() {
                    $(this).css('background-color', 'rgba(255, 255, 255, 0.2)');
                }).mouseleave(function() {
                    $(this).css('background-color', '');
                }).css('border', 'none');
                $('#pagination').append(btnPagina);
            }
        } else {
            $('#pagination').empty();
        }
    }
});


///////////////////////////////---------------Orden alfabetico de select------------/////////////////////////////////
document.addEventListener("DOMContentLoaded", function(event) {
        var select = document.getElementById("busqueda");
        var options = select.getElementsByTagName("option");
        var arrOptions = Array.from(options).sort((a, b) => a.text.localeCompare(b.text));
        for (var i = 0; i < arrOptions.length; i++) {
            select.appendChild(arrOptions[i]);
        }
    });



///////////////////////////////---------------Boton enviar validaciones y prevenir envio------------/////////////////////////////////
 document.addEventListener("DOMContentLoaded", function() {
        var enviarBtn = document.getElementById('Enviar');
        enviarBtn.addEventListener('click', function(event) {
            if (checksData.length === 0) {
                event.preventDefault();
                alert("No hay datos para enviar.");
            }

        });
 document.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
            event.preventDefault();
            }
        });

    });
