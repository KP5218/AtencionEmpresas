//-------variables--------------------
var nombre_paquete = document.getElementById("nombre_paquete");
var nombre_paquete_modal = document.getElementById("nombre_paquete_modal");
var tipo_prestacion = document.getElementById("tipo_prestacion");
var tablaPrestaciones = document.getElementById("tabla_prestaciones").getElementsByTagName('tbody')[0];
var tabla_Seleccionados = document.getElementById("tabla_seleccionados").getElementsByTagName('tbody')[0];
//-------------------------------------------------------------
var modalTableBody = document.querySelector('#modalpaquetes table tbody');

//-------filtro tipo de prestacion---y se agregan a la tabla de prestaciones-------------
function showPrestaciones(cod_tipo_prestacion){
    $.get("/crear_paquete/filtro_tipo_prestacion/" + cod_tipo_prestacion, function(data_prestacion){
        tablaPrestaciones.innerHTML = '';

        data_prestacion.forEach(function(prestacion){
            var row = tablaPrestaciones.insertRow();
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);

            cell1.innerHTML = prestacion.cod_prestacion;
            cell2.innerHTML = prestacion.prestacion;

            var checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = prestacion.cod_prestacion;
            cell3.appendChild(checkbox);


            row.appendChild(EditarButton(prestacion));
            var cancelButton = cancelarButton(prestacion);
            cancelButton.style.marginLeft = '5px';
            row.appendChild(cancelButton);

        });
    });
}


//----------Se agregan las prestaciones a la tabla_seleccionados ------------------
document.querySelector('#agregar_tabla_btn').addEventListener('click', function(){
    var selectedRows = Array.from(tablaPrestaciones.getElementsByTagName('input')).filter(checkbox => checkbox.checked);
    selectedRows.forEach(row => {
        var newRow = tabla_seleccionados.insertRow();
        var tipoPrestacionSeleccionado = tipo_prestacion.options[tipo_prestacion.selectedIndex].text;
        var tipoCell = newRow.insertCell(0);

        tipoCell.innerHTML = tipoPrestacionSeleccionado;

        for(var i = 0; i < row.parentElement.parentElement.cells.length - 1 ; i++){
            var cell = newRow.insertCell();
            cell.innerHTML = row.parentElement.parentElement.cells[i].innerHTML;
        }

        var sacarFilaButtonCell = newRow.insertCell();
        var sacarFilaButton = document.createElement('button');

        sacarFilaButton.textContent = 'Sacar fila';
        sacarFilaButton.classList.add('btn', 'btn-danger');
        sacarFilaButton.addEventListener('click',function(){
            tabla_seleccionados.deleteRow(newRow.rowIndex);
        });
        sacarFilaButtonCell.appendChild(sacarFilaButton);
    });
    selectedRows.forEach(row => {
       row.checked = false;
    });
    tablaPrestaciones.innerHTML = '';
    tipo_prestacion.selectedIndex = 0;
});

//---------------datos de la tabla_seleccionados, se envian a la tabla del modal-----
document.querySelector('#modalpaquetes').addEventListener('show.bs.modal', function(event) {
    nombre_paquete_modal.value = nombre_paquete.value;


    var rows = Array.from(tabla_seleccionados.querySelectorAll('tbody tr'));

    modalTableBody.innerHTML='';

    rows.forEach(row => {
        var newRow = modalTableBody.insertRow();
        var cells = Array.from(row.cells);

        // Iterar hasta la penúltima celda
        for (var i = 0; i < cells.length - 1; i++) {
            var newCell = newRow.insertCell();
            newCell.innerHTML = cells[i].innerHTML;
        }
    });
});

document.querySelector('#enviarDatos').addEventListener('click', function(event){
     var alertContainer = document.getElementById("alert-container");
     var confirmacion = confirm('¿Estás seguro de realizar esta operación?');

     if(confirmacion){
         var nombrePaquete = nombre_paquete_modal.value.trim();

         if(nombrePaquete){
             $.get("/crear_paquete/existe_paquete/" + nombrePaquete, function(existe){
                 if(existe.length > 0){
                     mostrarAlerta('Ya existe un paquete con ese nombre.', 'danger');
                 } else {
                     var datosTabla = [];
                     var modalRows = modalTableBody.querySelectorAll('tbody tr');

                     modalRows.forEach(function(row, index) {
                         if(index > 0) { // Ignorar la primera fila
                             var rowData = {};
                             var cells = Array.from(row.cells);

                             cells.forEach(function(cell, cellIndex) {
                                 if(cellIndex < cells.length - 1) { // Ignorar la última celda
                                     rowData['campo_' + cellIndex] = cell.textContent.trim();
                                 }
                             });

                             datosTabla.push(rowData);
                         }
                     });

                     var csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

                     var datos = {
                         nombrePaquete: nombrePaquete,
                         datosTabla: datosTabla
                     };

                     fetch('/crear_paquete/crear_paquete/', {
                         method: 'POST',
                         headers: {
                             'Content-Type': 'application/json',
                             'X-CSRFToken': csrftoken
                         },
                         body: JSON.stringify(datos)
                     })
                     .then(response => {
                         if (!response.ok) {
                             throw new Error('Hubo un problema al crear el paquete.');
                         }
                         return response.json();
                     })
                     .then(data => {
                         mostrarAlerta(data.mensaje, 'success');
                         limpiarModal();
                         limpiarTablaSeleccionados();
                     })
                     .catch(error => {
                         mostrarAlerta(error.message, 'danger');
                     });
                 }
             });
         } else {
             mostrarAlerta('Debe ingresar un nombre de paquete.', 'danger');
         }
     } else {
         alert("No se guardó el paquete.");
     }

     function mostrarAlerta(mensaje, tipo) {
     console.log(tipo)
         var alertHTML = `
             <div class="alert alert-${tipo} alert-dismissible fade show" role="alert">
                 ${mensaje}
                 <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
             </div>
         `;
         alertContainer.innerHTML = alertHTML;
     }

     function limpiarModal() {
         modalTableBody.innerHTML = '';
         $('#modalpaquetes').modal('hide');
     }

    function limpiarTablaSeleccionados() {
        var tbody_tabla_seleccionados = tabla_seleccionados.querySelector('tbody');
        tbody_tabla_seleccionados.innerHTML = '';
        nombre_paquete.value = "";
    }
 });

//-----------------------------------------Boton Editar antiguos------------------------------------------///
function EditarButton(prestacion) {
    var editarButton = document.createElement('button');
    editarButton.textContent = 'Editar';

    editarButton.className = 'btn btn-primary btn-sm mr-1';
    editarButton.style.backgroundColor = '#007bff';
    editarButton.style.borderColor = '#007bff';
    editarButton.style.color = '#fff';

    editarButton.onclick = function() {
        openModal('modaleditar');

        document.getElementById('nombre').value = prestacion.prestacion;
        document.getElementById('codigoInterno').value = prestacion.codigo_interno;
        document.getElementById('codigoFonasa').value = prestacion.cod_fonasa;
        document.getElementById('id').value = prestacion.id;

         $('#nombre').attr('data-nombre', prestacion.prestacion);
         $('#codigoInterno').attr('data-codigoInterno', prestacion.codigo_interno);
         $('#codigoFonasa').attr('data-codigoFonasa', prestacion.cod_fonasa);


        var datosAntes = JSON.stringify({
            nombre: prestacion.prestacion,
            cod_interno: prestacion.codigo_interno,
            cod_fonasa: prestacion.cod_fonasa,
            id: prestacion.id
        });

        document.getElementById('datosAntes').value = datosAntes;
    };
    return editarButton;
}



//-----------------------------------------Boton Anular------------------------------------------///
function cancelarButton(prestacion) {
    var cancelar = document.createElement('button');
    cancelar.textContent = 'Anular';
    cancelar.className = 'btn btn-danger btn-sm';
    cancelar.style.backgroundColor = '#ffc107';
    cancelar.style.borderColor = '#ffc107';
    cancelar.style.color = '#000';
    cancelar.style.boxShadow = 'none';

    cancelar.onclick = function()
    {
    openModal('AnulacionModal');

    document.getElementById('nombre').value = prestacion.prestacion;

        var datosPrestacion = {
            nombre_prestacion: document.getElementById('nombre').value,
            codigo_prestacion: prestacion.cod_prestacion
        };
        var datosPrestacionJSON = JSON.stringify(datosPrestacion);
        document.getElementById('anular').value = datosPrestacionJSON;
    };
    return cancelar;
}



//-----------------------------------------Abrir modales------------------------------------------///
function openModal(modalId)
{
$('#' + modalId).modal('show');
}

//-----------------------------------------Boton editar datos actuales------------------------------------------///
$(document).ready(function() {
    $('#nombre').val("");
    $('#enviarEditar').click(function () {
        var nombrePrestacion = $('#nombre').val();
        var codigo_interno = $('#codigoInterno').val();
        var codigo_fonasa = $('#codigoFonasa').val();
        var id = $('#id').val();

        var nombreOriginal = $('#nombre').attr('data-nombre');
        var codinternoOriginal = $('#codigoInterno').attr('data-codigoInterno');
        var codfonasaOriginal = $('#codigoFonasa').attr('data-codigoFonasa');

        if (nombrePrestacion !== nombreOriginal) {
            $.ajax({
                url: "/crear_paquete/filtronombPrestacion/" + nombrePrestacion + "/",
                method: 'POST',
                data: {
                    'nombrePrestacion': nombrePrestacion
                },
                success: function(response) {
                    if (response.length > 0) {
                        alert('Ya existe un nombre con el mismo valor.');
                    } else {
                        Enviar();
                    }
                }
            });
        } else if (codigo_interno !== codinternoOriginal) {
            $.ajax({
                url: "/crear_paquete/filtrocod_interno/" + codigo_interno,
                method: 'POST',
                data: {
                    'codigo_interno': codigo_interno
                },
                success: function(response) {
                    if (response.length > 0) {
                        alert('Ya existe un código con el mismo valor.');
                    } else {
                        Enviar();
                    }
                }
            });
        } else if (codigo_fonasa !== codfonasaOriginal) {
            Enviar();
        } else {
            Enviar();
        }
        function Enviar() {
            var data = {
                "nombrePrestacion": nombrePrestacion,
                "cod_interno": codigo_interno,
                "codigo_fonasa": codigo_fonasa,
                "id": id
            };
            $('#datosEditar').val(JSON.stringify(data));
            $('#Form2').submit();
        }
    });
});



