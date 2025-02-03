//funcion para obtener los tipo de solicitud para llenar el select
fetch('http://localhost/recursos/preventivascat/opciones_select_tipo.php')
  .then(response => response.json())
  .then(data => {
    llenarSelect('tipo', data); 
  })
  .catch(error => console.error('Error al obtener las opciones:', error));

function llenarSelect(idSelect, opciones) {
  var select = document.getElementById(idSelect);
  
  select.innerHTML = "";
  
  var optionDefault = document.createElement("option");
  optionDefault.text = "Seleccione tipo";
  optionDefault.value = "";
  select.appendChild(optionDefault);
  
  opciones.forEach(opcion => {
    var option = document.createElement("option");
    option.text = opcion.tipo_solicitud;
    option.value = opcion.cod_tipo_solicitud;
    select.appendChild(option);
  });
}
