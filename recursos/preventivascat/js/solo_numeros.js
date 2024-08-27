//en esta funcion verifico que solo se escriban numeros
function soloNumeros(event){
    const keyCode = event.keyCode;
    if (keyCode < 48 || keyCode > 57) {
        event.preventDefault();
    }
}

//en esta funcion limito la cantidad de numeros
function maximoNumeros(valor,maxLength) {
    if (valor.value.length > maxLength) {
        valor.value = valor.value.slice(0, maxLength);
    }
}

//aqui actualizo la cantidad de caracteres de un input
let maxCaracteres = 160;
let caracteresRestantesElement = document.getElementById('caracteres_restantes');
function actualizarCaracteresRestantes(textareaMensaje) {
    var cantidadCaracteres = textareaMensaje.value.length;
    var caracteresRestantes = maxCaracteres - cantidadCaracteres;
    caracteresRestantesElement.textContent = caracteresRestantes;
}
