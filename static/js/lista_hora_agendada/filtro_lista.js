  document.addEventListener("DOMContentLoaded", function() {
        mostrarEntradas();
    });

 // Función para mostrar todas las entradas
 function mostrarEntradas() {
        var opcionSeleccionada = document.getElementById("busqueda").value;

        ocultarEntradas();

        switch (opcionSeleccionada) {
            case "codigo1":
                document.getElementById("busquedaRut").closest('div').style.display = 'block';
                break;
            case "codigo2":
                document.getElementById("busquedaPreventivo").closest('div').style.display = 'block';
                break;
            case "codigo3":
                document.getElementById("busquedaEmpresa").closest('div').style.display = 'block';
                break;
            case "codigo4":
                document.getElementById("botonurgencia").style.display = 'block';
                break;
            case "codigo5":
                document.getElementById("botonhospitalario").style.display = 'block';
                break;
            case "codigo6":
                document.getElementById("busquedafecha1").closest('div').style.display = 'block';
                document.getElementById("busquedafecha2").closest('div').style.display = 'block';
                break;
            case "codigo7":
                document.getElementById("busquedaExamen").closest('div').style.display = 'block';
                break;
            case "codigo8":
                document.getElementById("botonConsulta").closest('div').style.display = 'block';
                break;
             case "codigo9":
                document.getElementById("busquedaUtms").closest('div').style.display = 'block';
                break;
            default:
                document.getElementById("botonhospitalario").style.display = 'none';
                document.getElementById("botonurgencia").style.display = 'none';
                document.getElementById("botonConsulta").style.display = 'none';
                break;
        }

        if (opcionSeleccionada !== "codigo4" && opcionSeleccionada !== "codigo5" && opcionSeleccionada !== "codigo8") {
            document.getElementById("botonbusqueda").closest('div').style.display = 'block';
        }
    }


// Función para ocultar todas las entradas
function ocultarEntradas() {
    document.getElementById("busquedaRut").closest('div').style.display = 'none';
    document.getElementById("busquedaPreventivo").closest('div').style.display = 'none';
    document.getElementById("busquedaEmpresa").closest('div').style.display = 'none';
    document.getElementById("busquedafecha1").closest('div').style.display = 'none';
    document.getElementById("busquedafecha2").closest('div').style.display = 'none';
    document.getElementById("botonbusqueda").closest('div').style.display = 'none';
    document.getElementById("busquedaExamen").closest('div').style.display = 'none'
    document.getElementById("busquedaUtms").closest('div').style.display = 'none'
    document.getElementById("mensaje1").closest('div').style.display = 'none';
    document.getElementById("mensaje2").closest('div').style.display = 'none';
    document.getElementById("mensaje3").closest('div').style.display = 'none';
    document.getElementById("mensaje4").closest('div').style.display = 'none';
    document.getElementById("mensaje5").closest('div').style.display = 'none';
    document.getElementById("mensaje6").closest('div').style.display = 'none';
    document.getElementById("mensaje7").closest('div').style.display = 'none';
    document.getElementById("mensaje8").closest('div').style.display = 'none';

    document.getElementById("botonurgencia").style.display = 'none';
    document.getElementById("botonhospitalario").style.display = 'none';
    document.getElementById("botonConsulta").style.display = 'none';

    // Ocultar el campo de entrada por defecto
    document.getElementById("busquedaRutDiv").style.display = 'none';

    $('#table-body').empty();
    $('#pagination').empty();
}

///////////////////////////////---------------Filtro rut------------/////////////////////////////////
$(document).ready(function() {
    $('#filtro').click(function() {
        $('#table-body').empty();
        var rut = $('#busquedaRut').val().trim();
        $('#busquedaRut').val("");
        var mensajeElement = $('#mensaje1');

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
            $('#mensaje1').text(mensaje).addClass('error').show();
        } else {
            $('#mensaje1').text(mensaje).removeClass('error').show();
        }
    }
    function mostrarPagina(data, numeroPagina, filasPorPagina) {
        $('#table-body').empty();
        var inicio = (numeroPagina - 1) * filasPorPagina;
        var fin = inicio + filasPorPagina;
        for (var i = inicio; i < fin && i < data.length; i++) {
            var solicitud = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(solicitud.rut),
                $('<td>').text(solicitud.nombre_solicitante),
                $('<td>').text(solicitud.telefono),
                $('.table-striped').find('thead').find('tr').find('th:contains("Paquete")').length > 0 ? $('<td>').text(solicitud.paquete) : null,
                $('<td>').text(solicitud.empresa),
                $('<td>').text(solicitud.mutualidad),
                $('<td>').text(solicitud.responsable),
                $('<td>').append(
                        $('<button>').text('Ver').addClass('btn btn-dark').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#exampleModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#exampleModal').data('persona-id', personaId);
                            verDetalle(personaId);
                        })
                    ),
                    $('<td>').append(
                        $('<button>').text('Anular').addClass('btn').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#AnulacionModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#AnulacionModal').data('persona-id', personaId);
                            anularRegistro(personaId);
                        })
                        .css('background-color', '#FFA000')
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

///////////////////////////////---------------Filtro preventiva------------/////////////////////////////////
$(document).ready(function() {
    $('#filtro').click(function() {
        $('#table-body').empty();
        var paquete = $('#busquedaPreventivo').val().trim();
        $('#busquedaPreventivo').val("");
        var mensajeElement = $('#mensaje2');
        if (!paquete) {
            mostrarMensaje("Por favor ingrese un nombre de paquete.");
            return;
        }
        $.ajax({
            url: 'filtroPreventiva/',
            method: 'POST',
            data: {
                'busquedaPreventivo': paquete,
            },
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    mostrarMensaje("");
                } else {
                    mostrarMensaje("No se encontró paquete.");
                }
            }
        });
    });
    function mostrarMensaje(mensaje) {
        if (mensaje.includes("No se encontró paquete.")) {
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
            var solicitud = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(solicitud.rut),
                $('<td>').text(solicitud.nombre_solicitante),
                $('<td>').text(solicitud.telefono),
                $('.table-striped').find('thead').find('tr').find('th:contains("Paquete")').length > 0 ? $('<td>').text(solicitud.paquete) : null,
                $('<td>').text(solicitud.empresa),
                $('<td>').text(solicitud.mutualidad),
                $('<td>').text(solicitud.responsable),
                $('<td>').append(
                        $('<button>').text('Ver').addClass('btn btn-primary').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#exampleModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#exampleModal').data('persona-id', personaId);
                            verDetalle(personaId);
                        })
                    ),
                    $('<td>').append(
                        $('<button>').text('Anular').addClass('btn').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#AnulacionModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#AnulacionModal').data('persona-id', personaId);
                            anularRegistro(personaId);
                        })
                        .css('background-color', '#FFA000')
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


///////////////////////////////---------------Filtro empresa------------/////////////////////////////////
$(document).ready(function() {
    $('#filtro').click(function() {
        $('#table-body').empty();
        var empresa = $('#busquedaEmpresa').val().trim();
        $('#busquedaEmpresa').val("");
        var mensajeElement = $('#mensaje3');

        if (!empresa) {
            mostrarMensaje("Por favor ingrese un nombre de empresa.");
            return;
        }
        $.ajax({
            url: 'filtroEmpresa/',
            method: 'POST',
            data: {
                'busquedaEmpresa': empresa,
            },
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    mostrarMensaje("");
                } else {
                    mostrarMensaje("No se encontró empresa.");
                }
            }
        });
    });
    function mostrarMensaje(mensaje) {
        if (mensaje === "No se encontró empresa.") {
            $('#mensaje3').text(mensaje).addClass('error').show();
        } else {
            $('#mensaje3').text(mensaje).removeClass('error').show();
        }
    }
    function mostrarPagina(data, numeroPagina, filasPorPagina) {
        $('#table-body').empty();
        var inicio = (numeroPagina - 1) * filasPorPagina;
        var fin = inicio + filasPorPagina;
        for (var i = inicio; i < fin && i < data.length; i++) {
            var solicitud = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(solicitud.rut),
                $('<td>').text(solicitud.nombre_solicitante),
                $('<td>').text(solicitud.telefono),
                $('.table-striped').find('thead').find('tr').find('th:contains("Paquete")').length > 0 ? $('<td>').text(solicitud.paquete) : null,
                $('<td>').text(solicitud.empresa),
                $('<td>').text(solicitud.mutualidad),
                $('<td>').text(solicitud.responsable),
                $('<td>').append(
                        $('<button>').text('Ver').addClass('btn btn-primary').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#exampleModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#exampleModal').data('persona-id', personaId);
                            verDetalle(personaId);
                        })
                    ),
                    $('<td>').append(
                        $('<button>').text('Anular').addClass('btn').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#AnulacionModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#AnulacionModal').data('persona-id', personaId);
                            anularRegistro(personaId);
                        })
                        .css('background-color', '#FFA000')
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


///////////////////////////////---------------Filtro fecha------------/////////////////////////////////
$(document).ready(function() {
    $('#filtro').click(function() {
        $('#table-body').empty();
        $('#pagination').empty();
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
                        $('#table-body').empty();
                        if (data.data.length > 4) {
                            var filasPorPagina = 4;
                            var paginaActual = 1;
                            var totalPaginas = Math.ceil(data.data.length / filasPorPagina);

                            mostrarPagina(data.data, paginaActual, filasPorPagina);

                            // Paginación
                            $('#pagination').empty();
                            for (var i = 1; i <= totalPaginas; i++) {
                                var btnPagina = $('<button>').text(i).addClass('btn pagination-btn').attr('type', 'button').click(function() {
                                    var numeroPagina = parseInt($(this).text());
                                    mostrarPagina(data.data, numeroPagina, filasPorPagina);
                                }).mouseenter(function() {
                                    $(this).css('background-color', '#03819A');
                                }).mouseleave(function() {
                                    $(this).css('background-color', '');
                                }).css('border', 'none');
                                if (i === paginaActual) {
                                    btnPagina.addClass('active');
                                }
                                $('#pagination').append(btnPagina);
                            }
                        } else {
                            mostrarPagina(data.data, 1, data.data.length);
                        }
                        mostrarMensaje("");
                    } else {
                        mostrarMensaje("No se encontraron solicitudes para estas fechas.");
                    }
                }
            });
        }
    });

    function mostrarMensaje(mensaje) {
        $('#mensaje4').text(mensaje).addClass('error').show();
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
            var solicitud = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(solicitud.rut),
                $('<td>').text(solicitud.nombre_solicitante),
                $('<td>').text(solicitud.telefono),
                $('.table-striped').find('thead').find('tr').find('th:contains("Paquete")').length > 0 ? $('<td>').text(solicitud.paquete) : null,
                $('<td>').text(solicitud.empresa),
                $('<td>').text(solicitud.mutualidad),
                $('<td>').text(solicitud.responsable),
                $('<td>').append(
                    $('<button>').text('Ver').addClass('btn btn-primary').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#exampleModal').attr('data-persona-id', solicitud.id).click(function() {
                        var personaId = $(this).attr('data-persona-id');
                        $('#exampleModal').data('persona-id', personaId);
                        verDetalle(personaId);
                    })
                ),
                $('<td>').append(
                    $('<button>').text('Anular').addClass('btn').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#AnulacionModal').attr('data-persona-id', solicitud.id).click(function() {
                        var personaId = $(this).attr('data-persona-id');
                        $('#AnulacionModal').data('persona-id', personaId);
                        anularRegistro(personaId);
                    }).css('background-color', '#FFA000')
                )
            );
            $('#table-body').append(fila);
        }
    }
});

///////////////////////////////---------------Filtro urgencia------------/////////////////////////////////
$(document).ready(function() {
    $('#filtrourgencia').click(function() {
        $('#table-body').empty();
        $.ajax({
            url: 'filtroUrgencia/',
            method: 'POST',
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    $('#table').show();
                    mostrarMensajeUrgencia("");
                } else {
                    mostrarMensajeUrgencia('No se encontraron datos en urgencias.');
                    $('#table').hide();
                }
            }
        });
    });

    function mostrarMensajeUrgencia(mensaje) {
        $('#mensajeUrgencia').text(mensaje).show();
    }
    function mostrarPagina(data, numeroPagina, filasPorPagina) {
        $('#table-body').empty();

        var inicio = (numeroPagina - 1) * filasPorPagina;
        var fin = inicio + filasPorPagina;
        for (var i = inicio; i < fin && i < data.length; i++) {
            var solicitud = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(solicitud.rut),
                $('<td>').text(solicitud.nombre_solicitante),
                $('<td>').text(solicitud.telefono),
                $('.table-striped').find('thead').find('tr').find('th:contains("Paquete")').length > 0 ? $('<td>').text(solicitud.paquete) : null,
                $('<td>').text(solicitud.empresa),
                $('<td>').text(solicitud.mutualidad),
                $('<td>').text(solicitud.responsable),
                $('<td>').append(
                        $('<button>').text('Ver').addClass('btn btn-primary').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#exampleModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#exampleModal').data('persona-id', personaId);
                            verDetalle(personaId);
                        })
                    ),
                    $('<td>').append(
                        $('<button>').text('Anular').addClass('btn').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#AnulacionModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#AnulacionModal').data('persona-id', personaId);
                            anularRegistro(personaId);
                        })
                        .css('background-color', '#FFA000')
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
function mostrarMensajeUrgencia(mensaje) {
$('#mensaje5').text(mensaje).addClass('error').show();
}

///////////////////////////////---------------Filtro hospitalario------------/////////////////////////////////
$(document).ready(function() {
    $('#filtrohospitalario').click(function() {
        $('#table-body').empty();
        $.ajax({
            url: 'filtroHospitalario/',
            method: 'POST',
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    $('#mensaje6').empty().hide();
                    $('#table').show();
                    mostrarMensajeHospitalario("");
                } else {
                    mostrarMensajeHospitalario('No se encontraron datos en hospitalario.');
                    $('#table').hide();
                }
            },
        });
    });

    function mostrarMensajeHospitalario(mensaje) {
        if (mensaje === "No se encontraron datos en hospitalario.") {
            $('#mensaje6').text(mensaje).addClass('error').show();
        } else {
            $('#mensaje6').text(mensaje).hide();
        }
    }
    function mostrarPagina(data, numeroPagina, filasPorPagina) {
        $('#table-body').empty();

        var inicio = (numeroPagina - 1) * filasPorPagina;
        var fin = inicio + filasPorPagina;
        for (var i = inicio; i < fin && i < data.length; i++) {
            var solicitud = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(solicitud.rut),
                $('<td>').text(solicitud.nombre_solicitante),
                $('<td>').text(solicitud.telefono),
                $('.table-striped').find('thead').find('tr').find('th:contains("Paquete")').length > 0 ? $('<td>').text(solicitud.paquete) : null,
                $('<td>').text(solicitud.empresa),
                $('<td>').text(solicitud.mutualidad),
                $('<td>').text(solicitud.responsable),
                $('<td>').append(
                        $('<button>').text('Ver').addClass('btn btn-primary').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#exampleModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#exampleModal').data('persona-id', personaId);
                            verDetalle(personaId);
                        })
                    ),
                    $('<td>').append(
                        $('<button>').text('Anular').addClass('btn').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#AnulacionModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#AnulacionModal').data('persona-id', personaId);
                            anularRegistro(personaId);
                        })
                        .css('background-color', '#FFA000')
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

///////////////////////////////---------------Filtro consulta------------/////////////////////////////////
$(document).ready(function() {
    $('#filtroConsulta').click(function() {
        $('#table-body').empty();
        $.ajax({
            url: 'filtroConsultas/',
            method: 'POST',
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    $('#table').show();
                    mostrarMensajeUrgencia("");
                } else {
                    mostrarMensajeUrgencia('No se encontraron datos en la consulta.');
                    $('#table').hide();
                }
            }
        });
    });

    function mostrarMensajeConsulta(mensaje) {
        $('#mensaje8').text(mensaje).show();
    }
    function mostrarPagina(data, numeroPagina, filasPorPagina) {
        $('#table-body').empty();

        var inicio = (numeroPagina - 1) * filasPorPagina;
        var fin = inicio + filasPorPagina;
        for (var i = inicio; i < fin && i < data.length; i++) {
            var solicitud = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(solicitud.rut),
                $('<td>').text(solicitud.nombre_solicitante),
                $('<td>').text(solicitud.telefono),
                $('.table-striped').find('thead').find('tr').find('th:contains("Paquete")').length > 0 ? $('<td>').text(solicitud.paquete) : null,
                $('<td>').text(solicitud.empresa),
                $('<td>').text(solicitud.mutualidad),
                $('<td>').text(solicitud.responsable),
                $('<td>').append(
                        $('<button>').text('Ver').addClass('btn btn-primary').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#exampleModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#exampleModal').data('persona-id', personaId);
                            verDetalle(personaId);
                        })
                    ),
                    $('<td>').append(
                        $('<button>').text('Anular').addClass('btn').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#AnulacionModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#AnulacionModal').data('persona-id', personaId);
                            anularRegistro(personaId);
                        })
                        .css('background-color', '#FFA000')
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
function mostrarMensajeConsulta(mensaje) {
$('#mensaje8').text(mensaje).addClass('error').show();
}

///////////////////////////////---------------Filtro examen------------/////////////////////////////////
$(document).ready(function() {
    $('#filtro').click(function() {
        $('#table-body').empty();
        var examen = $('#busquedaExamen').val().trim();
        var mensajeElement = $('#mensaje8');
        $('#busquedaExamen').val("");
        if (!examen) {
            mostrarMensaje("Por favor ingrese un examen.");
            return;
        }
        $.ajax({
            url: 'filtroExamen/',
            method: 'POST',
            data: {
                'busquedaExamen': examen,
            },
            success: function(data) {
                if (data && data.data && data.data.length > 0) {
                    mostrarPagina(data.data, 1, 4);
                    mostrarMensaje("");
                } else {
                    mostrarMensaje("No se encontró examen.");
                }
            }
        });
    });
    function mostrarMensaje(mensaje) {
        if (mensaje === "No se encontró examen.") {
            $('#mensaje8').text(mensaje).addClass('error').show();
        } else {
            $('#mensaje8').text(mensaje).removeClass('error').hide();
        }
    }
    function mostrarPagina(data, numeroPagina, filasPorPagina) {
        $('#table-body').empty();
        var inicio = (numeroPagina - 1) * filasPorPagina;
        var fin = inicio + filasPorPagina;
        for (var i = inicio; i < fin && i < data.length; i++) {
            var solicitud = data[i];
            var fila = $('<tr>').append(
                $('<td>').text(solicitud.rut),
                $('<td>').text(solicitud.nombre_solicitante),
                $('<td>').text(solicitud.telefono),
                $('.table-striped').find('thead').find('tr').find('th:contains("Paquete")').length > 0 ? $('<td>').text(solicitud.paquete) : null,
                $('<td>').text(solicitud.empresa),
                $('<td>').text(solicitud.mutualidad),
                $('<td>').text(solicitud.responsable),
                $('<td>').append(
                        $('<button>').text('Ver').addClass('btn btn-primary').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#exampleModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#exampleModal').data('persona-id', personaId);
                            verDetalle(personaId);
                        })
                    ),
                    $('<td>').append(
                        $('<button>').text('Anular').addClass('btn').attr('type', 'button').attr('data-bs-toggle', 'modal').attr('data-bs-target', '#AnulacionModal').attr('data-persona-id', solicitud.id).click(function() {
                            var personaId = $(this).attr('data-persona-id');
                            $('#AnulacionModal').data('persona-id', personaId);
                            anularRegistro(personaId);
                        })
                        .css('background-color', '#FFA000')
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


///////////////////////////////---------------Modal ver detalle------------/////////////////////////////////
function verDetalle(personaId) {
    $.ajax({
        url: 'obtener_datos/',
        method: 'POST',
        data: {
            'personaId': personaId,
        },
        success: function(data) {
            if (data.success) {
                var datos = data.data;
                $('input[name="rut"]').val(datos.rut);
                $('input[name="nombre"]').val(datos.nombre_solicitante);
                $('input[name="telefono"]').val(datos.telefono);
                $('input[name="empresa"]').val(datos.empresa);
                $('input[name="paquete"]').val(datos.paquete);
                $('input[name="medico"]').val(datos.nombre_medico);
                $('input[name="ejecutivo"]').val(datos.ejecutivo);
                $('input[name="fecha"]').val(datos.fecha_agendada);
                $('input[name="hora"]').val(datos.hora_agendada);
                $('textarea[name="comentario"]').val(datos.comentario);
                // Establecer el valor del input oculto con el ID de solicitud
                $('#inputIdSolicitud').val(datos.usuario);

                $('#exampleModal').modal('show');
            } else {

                alert(data.error);
            }
        }
    });
}


function anularRegistro(personaId) {
    var isConfirmed = confirm('¿Está seguro que desea anular?');

    if (isConfirmed) {
        var datosJSON = JSON.stringify(personaId);
        document.getElementById('id_persona').value = datosJSON;
        $('#AnulacionModal').modal('show');
    } else {
        $('#AnulacionModal').modal('hide');
    }
}

///////////////////////////////---------------Orden alfabetico de select------------/////////////////////////////////
document.addEventListener("DOMContentLoaded", function(event) {
        var select = document.getElementById("busqueda");
        var options = select.getElementsByTagName("option");
        var arrOptions = Array.from(options).sort((a, b) => a.text.localeCompare(b.text));
        for (var i = 0; i < arrOptions.length; i++) {
            select.appendChild(arrOptions[i]);
        }
    });




