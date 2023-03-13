let spinner;
const peticion = new XMLHttpRequest();
console.log("Empiezo a ejecutar JS");
var form = document.getElementById("mov-form");

function cargarMovimientos() {
  console.log("Has llamado a la función cargarMovimientos()");
  spinner.classList.remove("off"); // quitamos la clase off al spinner para

  peticion.open("GET", "http://127.0.0.1:5000/api/v1/movimientos", true);
  peticion.send();

  console.log("FIN de la función cargarMovimientos()");
}

function borrarMovimiento(event) {
  const target = event.target;
  const id = target.getAttribute("data-id");
  fetch(`http://127.0.0.1:5000/api/v1/movimientos/${id}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (response.status === 204) {
        alert(`El movimiento ha sido eliminado correctamente.`);
        cargarMovimientos();
        // FIXME: Simplemente eliminar la línea del movimiento (sin recargarlos todos)
      } else {
        alert("ERROR: La eliminación del movimiento ha fallado.");
      }
    })
    .catch((error) => alert("ERROR DESCONOCIDO al borrar el movimiento (API)"));
}

function editarMovimiento(id) {
  console.log(`editamos el movimiento con id: ${id}`);
  spinner.classList.add("off");
  obtenerMovimiento(id).then((movimiento) => {
    console.log("Movimiento:", movimiento);
    
    document.querySelector("#id_id").value = movimiento.id;
    document.querySelector("#fecha_id").value = movimiento.fecha.slice(0, 10);
    document.querySelector("#concepto_id").value = movimiento.concepto;
    document.querySelector("#tipo_id").value = movimiento.tipo;
    document.querySelector("#cantidad_id").value = movimiento.cantidad;
  }); 
  
  
}

function actualizarMovimiento(id) {
  console.log("Has llamado a la función actualizarMovimiento()");
  spinner.classList.add("off"); // quitamos la clase off al spinner para

  const datos = {
    fecha: document.querySelector("#fecha_id").value,
    concepto: document.querySelector("#concepto_id").value,
    tipo: document.querySelector("#tipo_id").value,
    cantidad: document.querySelector("#cantidad_id").value,
  };
  
  peticion
    .open(`http://127.0.0.1:5000/api/v1/movimientos/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(datos),
    })
    .then((response) => {
      if (response.ok) {
        window.location.href = "/";
      } else {
        throw new Error("Error al actualizar el movimiento.");
      }
    })
    .catch((error) => {
      console.error(error);
      alert("Error al actualizar el movimiento.");
    })
    .finally(() => {
      spinner.classList.add("off");
    });
}

function obtenerMovimiento(id) {
  return fetch(`http://127.0.0.1:5000/api/v1/movimientos/${id}`) // Hacemos una petición GET al servidor para obtener los datos del movimiento con el id indicado
    .then((response) => response.json())

    .catch((error) => console.error(error));
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
      };
      // TODO: Fecha en formato dd/mm/aaaa
      // TODO: Ajustar los decimales de la cantidad
      const opciones = {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      };
      const formateador = new Intl.NumberFormat("es-ES", opciones);
      const cantidad = formateador.format(mov.cantidad);

      const fecha = new Date(mov.fecha);
      const fechaFormateada = fecha.toLocaleDateString('es-ES')
   
      html =
        html +
        `
        <tr>
          <td class = fecha-format >${fechaFormateada}</td>
          <td class = fecha-format>${mov.concepto}</td>

          <td class = fecha-format>${mov.tipo}</td>
          <td class= "cantidad">${cantidad}</td>
          
          <td class= acciones>
          <a href="http://127.0.0.1:5000/editar/${mov.id}" class="editar-movimiento-enlace" data-id="${mov.id}"><i class="fa-regular fa-pen-to-square" onclick="editarMovimiento(${mov.id})"></i></a> 
          
          <a class="borrar-movimiento">
              <i class="fa-regular fa-trash-can" data-id="${mov.id}"></i>
            </a>
          

          </td>
        </tr>
      `;
    }

    const tabla = document.querySelector("#cuerpo-tabla");
    tabla.innerHTML = html;

     const botonesBorrar = document.querySelectorAll(".borrar-movimiento");
     // for btn in botonesBorrar:
     botonesBorrar.forEach((btn) => {
       btn.addEventListener("click", borrarMovimiento);
     });
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
