let spinner; //
const peticion = new XMLHttpRequest();
console.log("Empiezo a ejecutar JS");

function cargarMovimientos() {
  console.log("Has llamado a la función cargarMovimientos()");
  spinner.classList.remove("off"); // quitamos la clase off al spinner para 

  peticion.open("GET", "http://127.0.0.1:5000/api/v1/movimientos", true);
  peticion.send();

  console.log("FIN de la función cargarMovimientos()");
}

// crear una función que borre un movimiento pulsando el botón de la papelera del html
function borrarMovimiento() {
  spinner.classList.remove("off"); // quitamos la clase off al spinner para
  if (confirm("¿Estás seguro de que quieres borrar el movimiento?")) {
    peticion.open("DELETE", "http://127.0.0.1:5000/api/v1/movimientos${mov.id}");
  
  }
}
    

function mostrarMovimientos() {
  console.log("Entramos en la función mostrarMovimientos", this);

  if (this.readyState === 4 && this.status === 200) {
    console.log("---- TODO OK ----");
    const respuesta = JSON.parse(peticion.responseText);
    const movimientos = respuesta.results;

    let html = "";
    for (let i = 0; i < movimientos.length; i = i + 1) {
      const mov = movimientos[i];

      if (mov.tipo === "I") {
        mov.tipo = "Ingreso";
      } else if (mov.tipo === "G") {
        mov.tipo = "Gasto";
      } else {
        mov.tipo = "----";
      }
      // TODO: Fecha en formato dd/mm/aaaa
      // TODO: Ajustar los decimales de la cantidad
      // TODO: Incluir los botones de editar y borrar

      html =
        html +
        `
        <tr>
          <td>${mov.fecha}</td>
          <td>${mov.concepto}</td>

          <td>${mov.tipo}</td>
          <td class= "cantidad">${mov.cantidad}</td>
          
          <td>
          <a href="/api/v1/movimientos/" class="editar-movimiento" data-id="${mov.id}"><i class="fa-regular fa-pen-to-square" onclick="editar_movimiento"></i></a> 
        

          <a href="/api/v1/movimientos/" class="borrar-movimiento" data-id="${mov.id}"><i class="fa-solid fa-trash" onclick="borrar_movimiento"></i> </a> 
          </td>
        </tr>
      `;
    }

    const tabla = document.querySelector("#cuerpo-tabla");
    tabla.innerHTML = html;
  } else {
    console.error("---- Algo ha ido mal en la petición ----");
    alert("Error al cargar los movimientos");
  }

  spinner.classList.add("off"); // añadimos la clase off al spinner para que desaparezca cuando se ejecute la función mostrarMovimientos
  console.log("FIN de la función mostrarMovimientos");
}

window.onload = function () {
  console.log("Función anónima al finalizar la carga de la ventana");
  const boton = document.querySelector("#boton-recarga");
  boton.addEventListener("click", cargarMovimientos);
  spinner = document.querySelector("#spinner"); // llamamos al spinner del html para que se ejecute al cargar la página
  
  cargarMovimientos();
  peticion.onload = mostrarMovimientos;
};
