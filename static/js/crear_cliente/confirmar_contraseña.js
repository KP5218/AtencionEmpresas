var formulario_cliente = document.getElementById("formulario_cliente");

//validar  que los campos de contraseña no admita campos en blanco
document.getElementById("contraseña_cliente").addEventListener("keydown", function(event) {
    if (event.keyCode === 32) {
        event.preventDefault();
    }
});
document.getElementById("confirmar_contraseña").addEventListener("keydown", function(event) {
    if (event.keyCode === 32) {
        event.preventDefault();
    }
});


//aqui valido las contraseñas y los campos.. tambien que el usuario no sea uno existente
formulario_cliente.addEventListener("submit", function(event) {
    event.preventDefault();
    if (validar_pass()) {
        validar();
    }
});

function validar() {
    if (!formulario_cliente.checkValidity()) {
        event.preventDefault();
    } else {
        existe_usuario();
    }
}

function validar_pass() {
    var contraseña = document.getElementById("contraseña_cliente").value;
    var confirmarContraseña = document.getElementById("confirmar_contraseña").value;
    var regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&-])([A-Za-z\d$@$!%*?&-]|[^ ]){8,}$/;

    document.getElementById("error_confirmar_contraseña").style.display = "none";
    document.getElementById("error_contraseña").style.display = "none";
    if (contraseña !== confirmarContraseña) {
        document.getElementById("error_confirmar_contraseña").style.display = "inline";
        return false;
    }

    if (!regex.test(contraseña)) {
        document.getElementById("error_contraseña").style.display = "inline";
        return false;
    }

    return true;
}

function existe_usuario() {
    var usuario = document.getElementById("usuario_cliente").value;

    $.get("/crear_cliente/existe_usuario/" + usuario, function (datos) {
        console.log(datos);
        if (datos.length > 0) {
           var alertContainer = document.getElementById("alert-container");
            var alertHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Ya existe un usuario con ese nombre
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            alertContainer.innerHTML = alertHTML;
        } else {
            formulario_cliente.submit();
        }
    });
}
