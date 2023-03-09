console.log("iniciamos ejecucion form.js")

const form = document.getElementById('mov-form');

form.addEventListener('submit', sendForm)

function sendForm(event) {
    console.log("formulario enviado", event);
    event.preventDefault(); // evita que se envie el formulario
    const formData = new FormData(form); // creamos un objeto FormData con los datos del formulario
    console.log('datos del formulario', formData);
    const jsonData = {}; // creamos un objeto vacío
    formData.forEach((value, key) => jsonData[key] = value); // mostramos los datos del formulario en la consola
    console.log('datos del formulario en formato JSON', jsonData);
    
  
    //llamada a la API
    fetch("http://127.0.0.1:5000/api/v1/movimientos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(jsonData), // convertimos el objeto JSON en un string
    })
      .then((response) => {
        console.log("respuesta del servidor", response);
        return response.json();
      })
      .then((data) => {
        console.log("datos del servidor", data);
        if (data.status === "error") {
          // TODO: mostrar mensaje de error en la página
          // TODO: mostrar mensaje de error EN CADA CAMPO
          // TODO: mostrar mensaje de error en el formulario
          // TODO: color rojo 
          alert(`ERROR: \n ${data.message}`);
        } else {
          // TODO: redireccionar a la página de inicio
          // TODO: o mostrar mensaje de éxito y limpiar el formulario
          // TODO: el mensaje debe desaparecer en 5 segundos
          alert("Movimiento creado correctamente");
        }
      })
      .catch((error) => {
        console.log("ERROR!!!!!", error);

    });
}
