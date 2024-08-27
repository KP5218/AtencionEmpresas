
//fucion para los check de tipos de formularios
function checkFormulario(checkbox) {
    if (checkbox.id === "diep_check" && checkbox.checked) {
        document.getElementById("diat_check").checked = false;
    } else if (checkbox.id === "diat_check" && checkbox.checked) {
        document.getElementById("diep_check").checked = false;
    }
}