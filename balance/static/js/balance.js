const peticion = new XMLHttpRequest();
console.log("Empiezo a ejecutar JS");

function cargarMovimientos() {
  console.log("Has llamado a la función cargarMovimientos()");

  peticion.open(
    "GET",
    "http://127.0.0.1:5000/api/v1/movimientos",
    false
  );
  peticion.send();
  console.log(peticion.responseText);
  const respuesta = JSON.parse(peticion.responseText);
  const movimientos = respuesta.results;

  let html = "";
  for (let i = 0; i < movimientos.length; i = i + 1) {
    const mov = movimientos[i];
    console.log("Movimiento", mov);
    html =
      html +
      `
      <tr>
        <td>${mov.fecha}</td>
        <td>${mov.concepto}</td>
        <td>${mov.tipo}</td>
        <td>${mov.cantidad}</td>
      </tr>
    `;
  }

  const tabla = document.querySelector("#cuerpo-tabla");
  tabla.innerHTML += html;
}

window.onload = function () {
  console.log("Función anónima al finalizar la carga de la ventana");
  const boton = document.querySelector("#boton-recarga");
  boton.addEventListener("click", cargarMovimientos);
  cargarMovimientos();
};
