function cargarMovimientos() {
    console.log("Has llamado a la función cargarMovientos()");
}

window.onload = function () {
    console.log("Has llamado a la función anónima al finalizar la carga de la ventana");
    const boton = document.querySelector('#boton-recarga');
    boton.addEventListener('click', cargarMovimientos);

}