//aqui obtengo desde bd los tipos de formulario para llenar el select
fetch('http://localhost/preventivascat/select_form.php')
  .then(response => response.json())
  .then(data => {
    llenarSelect('tipo_formulario', data); 
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
    option.text = opcion.descripcion;
    option.value = opcion.cod_formulario;
    select.appendChild(option);
  });
}

