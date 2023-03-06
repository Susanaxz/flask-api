from flask import jsonify #convierte un objeto en un json
from . import app
from .models import DBManager

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
    
"""

RUTA = app.config.get('RUTA')

@app.route('/')
def inicio():
    db = DBManager(RUTA)
    sql = 'SELECT * FROM movimientos'
    movimientos = db.consultaSQL(sql)
    return jsonify(movimientos)