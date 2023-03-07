const peticion = new XMLHttpRequest(); // Objeto para hacer peticiones HTTP 
console.log("Empiezo a ejecutar JS"); // Se ejecuta al cargar la página

function cargarMovimientos() {
  console.log("Has llamado a la función cargarMovimientos()"); // Se ejecuta al hacer click en el botón

  peticion.open("GET", "http://127.0.0.1:5000/api/v1/movimientos", false); // Se abre la conexión con el servidor (false para sincrona y true para asincrona)
  peticion.send(); // Se envía la petición al servidor petición sincrona
  console.log(peticion.responseText); // Se muestra la respuesta del servidor
  const respuesta = JSON.parse(peticion.responseText); // Se convierte la respuesta a JSON
  const movimientos = respuesta.results; // Se obtienen los movimientos

  let html = ""; // Se crea una variable para almacenar el HTML que se va a mostrar
  for (let i = 0; i < movimientos.length; i = i + 1) {
    // Se recorren los movimientos
    const mov = movimientos[i]; // Se obtiene el movimiento actual
    console.log("Movimiento", mov); // Se muestra el movimiento actual
    html =
      html +
      `
      <tr>
        <td>${mov.fecha}</td>
        <td>${mov.concepto}</td>
        <td>${mov.tipo}</td>
        <td>${mov.cantidad}</td>
      </tr>
    `; // Se añade el movimiento actual al HTML
  }

  const tabla = document.querySelector("#cuerpo-tabla"); // Se obtiene la tabla
  tabla.innerHTML += html; // Se añade el HTML a la tabla
}

window.onload = function () {
  // Se ejecuta al finalizar la carga de la ventana
  console.log("Función anónima al finalizar la carga de la ventana"); // Se ejecuta al finalizar la carga de la ventana
  const boton = document.querySelector("#boton-recarga"); // Se obtiene el botón
  boton.addEventListener("click", cargarMovimientos); // Se añade un evento al botón
  cargarMovimientos(); // Se cargan los movimientos
};
