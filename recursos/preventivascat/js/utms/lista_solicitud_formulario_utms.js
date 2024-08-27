//funciones para mostrar la lista de registros que ha realizado el usuario logeado

document.addEventListener('DOMContentLoaded', function() {
    cargarDatos();

    const fechaInicioInput = document.getElementById('fechaInicio');
    const fechaFinInput = document.getElementById('fechaFin');
    const buscarBtn = document.getElementById('buscarBtn');
    let currentPage = 1;
    const recordsPerPage = 10; 

    //funcion para habilitar el boton para filtrar por fechas
    function checkInputs() {
        const fechaInicio = fechaInicioInput.value.trim();
        const fechaFin = fechaFinInput.value.trim();

        if (fechaInicio !== '' && fechaFin !== '') {
            buscarBtn.disabled = false;
        } else {
            buscarBtn.disabled = true;
        }
    }

    fechaInicioInput.addEventListener('change', checkInputs);
    fechaFinInput.addEventListener('change', checkInputs);

    //pagina actual
    document.getElementById('buscarBtn').addEventListener('click', function() {
        currentPage = 1; 
        cargarRegistrosPaginados();
    });

    //pagina anterior
    document.getElementById('prevPageBtn').addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            cargarRegistrosPaginados();
        }
    });

    //pagina siguiente
    document.getElementById('nextPageBtn').addEventListener('click', function() {
        const totalRecords = document.getElementById('totalRecords').textContent;
        if (currentPage < Math.ceil(totalRecords / recordsPerPage)) {
            currentPage++;
            cargarRegistrosPaginados();
        }
    });

    function cargarRegistrosPaginados() {
        const fechaInicio = fechaInicioInput.value.trim();
        const fechaFin = fechaFinInput.value.trim();
        const startIndex = (currentPage - 1) * recordsPerPage;
        const endIndex = startIndex + recordsPerPage;

        if (fechaInicio !== '' && fechaFin !== '') {
            buscarRegistrosPorFechas(fechaInicio, fechaFin, startIndex, endIndex,currentPage);
        } else {
            cargarDatos(startIndex, endIndex,currentPage);
        }
    }

//funcion para traer todos los datos
function cargarDatos(startIndex = 0, endIndex =10,currentPage) {
    fetch('http://localhost/preventivascat/lista_solicitud_formulario_utms.php')
    .then(response => response.json())
    .then(data => {

        mostrarRegistros(data, startIndex, endIndex,currentPage);
    })
    .catch(error => {
        console.error('Error al obtener los datos:', error);
    });
}

//si estoy haciendo un filtro por fechas
function buscarRegistrosPorFechas(fechaInicio, fechaFin, startIndex = 0, endIndex = 10,currentPage) {
    const url = `http://localhost/preventivascat/lista_solicitud_formulario_utms.php?fechaInicio=${fechaInicio}&fechaFin=${fechaFin}`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
        mostrarRegistros(data, startIndex, endIndex,currentPage);
    })
    .catch(error => {
        console.error('Error al obtener los datos:', error);
    });
}

//tomo los datos y los muestro en la tabla junto con el paginador
function mostrarRegistros(data, startIndex, endIndex, currentPage) {
    const totalRecords = data.length;
    const totalPages = Math.ceil(totalRecords / recordsPerPage);
    const paginatedData = data.slice(startIndex, endIndex);
    let fecha_recepcion = "";
    if (currentPage == undefined){
        currentPage = 1;
    }

    let tablaHTML = '<div class="table-responsive">' + 
                        '<table class="table table-striped" style="margin-top:0.5%;">' +
                            '<thead>' + 
                                '<tr>' +
                                    '<th>RUT</th>' +
                                    '<th>Nombre Paciente</th>' +
                                    '<th>Teléfono</th>' +
                                    '<th>Estado</th>' +
                                    '<th>Fecha Ingreso</th>' +
                                    '<th>Fecha Recepción</th>' +
                                '</tr>' +
                            '</thead>' +
                            '<tbody>';

    paginatedData.forEach(solicitud => {
        
        if (solicitud.fecha_recepcion != null){
            fecha_recepcion = formatearFecha(solicitud.fecha_ingreso);
        }else{
            fecha_recepcion = "";
        }
        tablaHTML += '<tr>' +
                        '<td>' + solicitud.rut + '</td>' +
                        '<td>' + solicitud.nombre_paciente + '</td>' +
                        '<td>' + solicitud.telefono + '</td>' +
                        '<td>' + solicitud.estado + '</td>' +
                        '<td>' + solicitud.fecha_ingreso + '</td>' +
                        '<td>' + fecha_recepcion + '</td>' +
                        
                    '</tr>';
    });

    tablaHTML += '<tr>' +
                    '<td><strong style="font-size: 18px;">Total :</strong></td>' +
                    '<td colspan="5"><strong id="totalRecords" style="font-size: 18px;">' + totalRecords + '</strong></td>' +
                    
                '</tr>'+
                '</tbody>' +
                '</table>' +
                '</div>'; 

    document.getElementById('tabla-container').innerHTML = tablaHTML;
    document.getElementById('currentPage').textContent = `Página: ${currentPage} de ${totalPages}`;
    document.getElementById('totalRecords').textContent = totalRecords;
}

//funcion para formatear la fecha 
function formatearFecha(fechaString) {
    const partesFecha = fechaString.split('-');
    const dia = partesFecha[2];
    const mes = partesFecha[1];
    const año = partesFecha[0];
    return `${dia}-${mes}-${año}`;
}


});