//funcion para obtener los tipo de examen para llenar el select
fetch('http://localhost/recursos/preventivascat/select_examen.php')
  .then(response => response.json())
  .then(dataex => {
    console.log(dataex);
    llenarSelectExamen('tipo_examen', dataex); 
  })
  .catch(error => console.error('Error al obtener las opciones:', error));

function llenarSelectExamen(idSelect, opciones) {
  var select = document.getElementById(idSelect);
  
  select.innerHTML = "";
  
  var optionDefault = document.createElement("option");
  optionDefault.text = "Seleccione tipo";
  optionDefault.value = "";
  select.appendChild(optionDefault);
  
  opciones.forEach(opcion => {
    var option = document.createElement("option");
    option.text = opcion.descripcion;
    option.value = opcion.cod_examen;
    select.appendChild(option);
  });
}

