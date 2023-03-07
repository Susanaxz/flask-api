from flask import jsonify, render_template  # convierte un objeto en un json
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
    
    devuelve un array de objetos JSON o un objeto JSON
    {
        "id": 1,
        "fecha": 2023-02-23,
        "concepto": camisa,
        "tipo": "G"
    }
"""

RUTA = app.config.get("RUTA")

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/api/v1/movimientos")
def listar_movimientos():   
    try:
        db = DBManager(RUTA)
        sql = 'SELECT * FROM movimientos'
        movimientos = db.consultaSQL(sql)
        resultado = {
            "status": "success",
            "results": movimientos
        }
    except Exception as error:
        resultado = {
            "status": "error",
            "message": str(error)
        }

    return jsonify(resultado)

@app.route('/api/v1/movimientos/<int:id>')
def get_movimiento(id):
    """
    instanciar DBManager para poder acceder a la BBDD
    preparar la consulta
    ejecutar la consulta
    leer el resultado
    si es ok:
        si es success / movimiento
    si error: 
        resultado es error / mensaje
    devolvemos el resultado
    """
    try:
        db = DBManager(RUTA)
        sql = 'SELECT * FORM movimientos WHERE id=?'
        movimientos = db.obtener_movimiento(id)
        
        if len(movimientos) > 0:
            resultado = {
                'status': 'success',
                'results': movimientos
            }
            status_code = 200
        else:
            resultado = {
            'status': 'error',
            'message': f'No hay movimientos en el sistema'
            }
            status_code = 404
        
    except Exception as error:
        resultado = {
            'status': 'error',
            'message': str(error)
        }
        status_code = 500
        
    return jsonify(resultado), status_code

@app.route('/api/v1/movimientos/<int:id>', methods = ['DELETE'])
def delete_movimiento(id):
    
    try: 
        db = DBManager(RUTA)
        mov = db.obtener_movimiento(id)
        
        if mov: 
            sql = "DELETE FROM movimientos WHERE id=?"
            esta_borrado = db.consultaConParametros(sql, (id,))
            
            if esta_borrado:
                resultado = {
                    'status': 'success'
                }
                status_code = 204
            else:
                resultado = {
                    'status': 'error',
                    'message': f'No se ha eliminado el movimiento con ID={id}'
                }
                status_code = 500
        else:
                resultado = {
                    'status': 'error',
                    'message': f'No existe un movimiento con ID={id}'
                }
                status_code = 404
                
    except: 
        resultado = {
            'status': 'error',
            'message': f'Error desconocido en el servidor'
        }
        status_code = 500
        
    return jsonify(resultado), status_code



# TODO: actualizar movimiento por ID    