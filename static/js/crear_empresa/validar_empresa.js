var formulario_empresa = document.getElementById("formulario");
var selectTipo = document.getElementById('tipo');
formulario_empresa.addEventListener("submit", function(event) {
    event.preventDefault();

     if (selectTipo.value === '01') {
        var cod_empresa = document.getElementById("codigo").value;

        $.get("/crear_empresa/existe_empresa/" + cod_empresa, function (datos) {
            console.log(datos);
            if (datos.length > 0) {
                var alertContainer = document.getElementById("alert-container");
                var alertHTML = `
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Ya existe una empresa con ese codigo
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                `;
                alertContainer.innerHTML = alertHTML;
            } else {

                formulario_empresa.submit();
            }
        });


     } else if (selectTipo.value === '02') {
        var cod_mutual = document.getElementById("codigo").value;

        $.get("/crear_empresa/existe_mutualidad/" + cod_mutual, function (datos) {
        console.log(datos);
        if (datos.length > 0) {
            var alertContainer = document.getElementById("alert-container");
            var alertHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Ya existe una mutual con ese codigo
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            alertContainer.innerHTML = alertHTML;
        } else {

            formulario_empresa.submit();
        }
    });

     }else if (selectTipo.value === '03') {
        var cod_mutual = document.getElementById("codigo").value;

        $.get("/crear_empresa/existe_utms/" + cod_mutual, function (datos) {
        console.log(datos);
        if (datos.length > 0) {
            var alertContainer = document.getElementById("alert-container");
            var alertHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Ya existe una UTMS con ese codigo
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            alertContainer.innerHTML = alertHTML;
        }else {

            formulario_empresa.submit();
        }
    });

     }


});
