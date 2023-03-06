const peticion = new XMLHttpRequest() // esto hace una llamada




function cargarMovimientos() {
    console.log("Has llamado a la función cargarMovientos()");

    peticion.open('GET', 'http://127.0.0.1:5000//api/v1/movimientos', false); //abre una conexion donde se le diga
    peticion.send();
    console.log(peticion.responseText);
}

window.onload = function () {
    console.log("Has llamado a la función anónima al finalizar la carga de la ventana");
    const boton = document.querySelector('#boton-recarga');
    boton.addEventListener('click', cargarMovimientos);
}