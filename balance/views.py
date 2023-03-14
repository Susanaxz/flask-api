from flask import render_template

from . import app
from .forms import MovimientoForm
from .models import DBManager


"""
    Verbos y formato de endpoints
    GET /movimientos ----------> LISTAR movimientos
    POST /movimientos ---------> CREAR un movimiento nuevo
    GET /movimientos/1 --------> LEER el movimiento con ID=1
    POST /movimientos/1 -------> ACTUALIZAR el movimiento con ID=1 (sobreescribe todo el objeto)
    PUT /movimientos/1 --------> ACTUALIZAR el movimiento con ID=1 (sobreescribe parcialmente)
    DELETE /movimientos/1 -----> ELIMINAR el movimiento con ID=1
    IMPORTANTE!!!
    Versionar los endpoint (son un contrato)
    /api/v1/...
    /api/v1/facturas
    /api/v2/movimientos
    /api/v1/contatos
    /api/v1/usuarios
    /api/v1/donaciones
    /api/v1/compras
    Devuelve un array de objetos JSON o un objeto JSON.
    Por ejemplo, un movimiento:
    {
    "id": 1,
    "fecha": "2023-02-27",
    "concepto": "Camiseta",
    "tipo": "G",
    "cantidad": 12.35
    }
"""


# Devuelve HTML, son vistas estándar (clásicas)

RUTA = app.config.get('RUTA')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/nuevo')
def form_nuevo():
    formulario = MovimientoForm()
    return render_template('form_movimiento.html', form=formulario)


@app.route('/modificar/<int:id>')
def form_modificar(id):
    db = DBManager(RUTA)
    mov = db.obtenerMovimiento(id)
    formulario = MovimientoForm(data=mov)
    return render_template('form_movimiento.html', form=formulario)