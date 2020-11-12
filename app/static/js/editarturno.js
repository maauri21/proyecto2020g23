function traerTurnos(centro_id, fecha) {
  fetch(`/api/v1/centros/${centro_id}/turnos_disponibles?fecha=${fecha}`) // request de la api, devuelve una promesa
  .then((response) => response.json())  // .json xq estoy usando api
  .then((response) => {
      response.turnos.map((turno) => {  // turnos es lo que aparece en la api
        $('#hora').append(`<option value='${turno.hora_inicio}'>${turno.hora_inicio}</option>`)
      })
  })
};

$('#dia').change(function(event){   // toda la funion se ejecuta cada vez que cambie el valor del input dia
    fecha = $(event.target).val();  // event.target tiene el select que levantó el evento (valor de dia)
    centro_id = $('#centro_id').val();
    $('#hora').empty(); // vaciar el select
    traerTurnos(centro_id, fecha);
});

window.onload = () => {         // Cuando cargue el DOM
  fecha = $('#dia').val();
  centro_id = $('#centro_id').val();
  traerTurnos(centro_id, fecha);
};
