//funcion para obtener los tipo de genero para llenar el select
fetch('http://localhost/preventivascat/select_genero.php')
  .then(response => response.json())
  .then(data => {
    console.log(data);
    llenarSelectGenero('genero', data); 
  })
  .catch(error => console.error('Error al obtener las opciones:', error));

function llenarSelectGenero(idSelect, opciones) {
  var select = document.getElementById(idSelect);
  
  select.innerHTML = "";
  
  var optionDefault = document.createElement("option");
  optionDefault.text = "Seleccione tipo";
  optionDefault.value = "";
  select.appendChild(optionDefault);
  
  opciones.forEach(opcion => {
    var option = document.createElement("option");
    option.text = opcion.descripcion;
    option.value = opcion.cod_genero;
    select.appendChild(option);
  });
}

