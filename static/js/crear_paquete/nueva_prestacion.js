$(document).ready(function() {
    $('#enviarNuevo').click(function(event) {
        event.preventDefault();

        var nombrePrestacion = $('#nombre_prestacion').val();
        var tipoPrestacion = $('#prestacion').val();
        var cod_interno = $('#codigointerno').val();
        var cod_fonasa = $('#codigofonasa').val();

        if (!nombrePrestacion) {
            alert('Ingrese el nombre de la prestación');
            return;
        }
        if (!tipoPrestacion) {
            alert('Seleccione un tipo de prestación');
            return;
        }
        if (!cod_interno && !cod_fonasa) {
            alert('Debes proporcionar al menos uno de los códigos.');
            return;
        }

        $.ajax({
            url: "/crear_paquete/filtrocod_interno/" + cod_interno,
            method: 'POST',
            data: {
                'cod_interno': cod_interno
            },
            success: function(response) {
                if (response.length > 0) {
                    alert('Ya existe un código interno con el mismo valor.');
                } else {
                    $.ajax({
                        url: "/crear_paquete/filtronombPrestacion/" + nombrePrestacion + "/",
                        method: 'POST',
                        data: {
                            'nombrePrestacion': nombrePrestacion
                        },
                        success: function(response) {
                            if (response.length > 0) {
                                alert('Ya existe un nombre igual.');
                            } else {
                                var data = {
                                    "nombrePrestacion": nombrePrestacion,
                                    "tipoPrestacion": tipoPrestacion,
                                    "cod_interno": cod_interno,
                                    "cod_fonasa": cod_fonasa
                                };
                                $('#datosJson').val(JSON.stringify(data));
                                $('#formulario').submit();
                            }
                        }
                    });
                }
            }
        });
    });
});