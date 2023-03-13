console.log("--- Iniciamos ejecución de form.js ---");

// const form = document.querySelector('#mov-form');
const form = document.getElementById("mov-form");
form.addEventListener("submit", sendForm);

function sendForm(event) {
  console.log("Formulario enviado", event);
  event.preventDefault();

  // recoger los datos del formulario
  const formData = new FormData(form);
  console.log("formData", formData);
  // for value,key in formData:
  //   print(key, value)
  const jsonData = {};
  formData.forEach((value, key) => (jsonData[key] = value));
  console.log("1. JSON", jsonData);

  // function(param1, param2) {
  //   console.log("Hola mundo")
  // }
  // (param1, param2) => {
  //   console.log("Hola mundo")
  // }

  // function() { console.log("Hola"); }
  // () => console.log("Hola");

  // ¿Cómo sé si es POST (crear) o PUT (actualizar)?
  // opción 1: la url no es la misma
  // opción 2: si el ID ya existe la BBDD  ---- La BBDD está en el servidor :(
  // opción 3: la URL tiene el ID
  // opción 4: el formulario tiene in valor en ID

  const campoId = document.getElementById("id");
  let operacion;
  let url;
  if (campoId.value > 0) {
    operacion = "PUT";
    url = `http://127.0.0.1:5000/api/v1/movimientos/${campoId.value}`;
    window.location.href = "/";
  } else {
    operacion = "POST";
    url = "http://127.0.0.1:5000/api/v1/movimientos";
    window.location.href = "/";
  }

  // enviar la petición con los datos a la API
  fetch(url, {
    method: operacion,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(jsonData),
    // JavaScript Object Notation
  })
    .then((response) => {
      console.log("2.", response);
      return response.json();
    })
    .then((data) => {
      console.log("3.", data);
      if (data.status === "error") {
        // TODO: mostrar los errores en la página
        // 1. mensaje global encima del formulario ---
        // 2: mensaje en cada campo con error --------
        // 2.1: el mensaje debe desaparecer tras unos segundos (5)
        // 3. color rojo en los campos con error -----
        alert(`ERROR:\n${data.message}`);
      } else {
        // A ELEGIR
        // TODO: redireccionar a la página de inicio
        // TODO: mostrar mensaje de OK y vaciar el formulario (para poder insertar otro movimiento)
        // TODO: el mensaje debe desaparecer tras unos segundos (5)
        if (operacion === "PUT") {
          alert("Se ha modificado el movimiento");
        } else {
          alert("Se ha insertado el movimiento");
        }
      }
    })
    .catch((error) =>
      console.error("4. ERROR!", "No se ha podido acceder a la API")
    );
  console.log("5. He hecho la petición");
  // esperar el resultado
}
