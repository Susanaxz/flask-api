from flask import jsonify, render_template, request, redirect  # convierte un objeto en un json

from . import app
from .models import DBManager
from .forms import MovimientoForm



"""
Como se trabaja una API REST:
Verbos y formato de endpoints
    GET /movimientos ---------> LISTAR movimientos
    POST /movimientos ---------> CREAR un movimiento nuevo
    
    GET /movimientos/1 ---------> LEER el movimiento con ID=1
    POST /movimientos/1 ---------> ACTUALIZAR el movimiento con ID=1 (sobreescribe todo el objeto)
    PUT /movimientos/1 ---------> ACTUALIZAR el movimiento con ID=1 (sobreescrir los campos que enviemos, sobreescribe parcialmente)
    DELETE /movimientos/1 ---------> ELIMINA el movimiento con ID=1 
    
    !!!IMPORTANTE!!!
    Versionar los endpoints (son un contrato)
    /api/v1/...
    
    devuelve un array de objetos JSON o un objeto JSON
    {
        "id": 1,
        "fecha": 2023-02-23,
        "concepto": camisa,
        "tipo": "G"
    }
"""

RUTA = app.config.get("RUTA")

# TODO: CREAR un ednpoint para ACTUALIZAR un movimiento por ID (PUT)

# llamadas a la web, devuelven HTML
@app.route('/', methods = ['GET'])
def home():
    db = DBManager(RUTA)
    page = int(request.args.get('page', 1))
    items_per_page = 8
    items, total_items = db.get_paginated_movements(page, items_per_page)
    num_pages = (total_items - 1) // items_per_page + 1
    return render_template('index.html', items=items, page=page, num_pages=num_pages, current_page=page)

@app.route('/nuevo')
def form_nuevo():
    formulario = MovimientoForm()
    return render_template('form_movimiento.html', form=formulario, accion='/nuevo')
    
@app.route('/editar/<int:id>')
def editar(id):
    db = DBManager(RUTA)
    movimiento = db.obtener_movimiento(id)

    formulario = MovimientoForm(data=movimiento)
    
    
    return render_template('form_movimiento.html', form=formulario)
   
# llamadas a la API REST, devuelven un JSON


      

