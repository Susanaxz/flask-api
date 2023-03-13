from flask import jsonify, request  # convierte un objeto en un json
from . import app
from .models import DBManager
from .forms import MovimientoForm


RUTA = app.config.get("RUTA")


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

@app.route('/api/v1/movimientos', methods = ['POST'])
def insertar_movimiento ():
    """
    201 si se ha creado
    400 si hay un error de validacion
    500 si hay un error en el servidor
    """
    try:
       
        json = request.get_json()
        form = MovimientoForm(data=json)
        
        if form.validate():
            
            db = DBManager(RUTA) # instanciamos la clase DBManager
            sql = 'INSERT INTO movimientos (fecha, concepto, tipo, cantidad) VALUES (:fecha, :concepto, :tipo, :cantidad)'
            params = request.json
            es_correcto = db.consultaConParametros(sql, params)
            if es_correcto:
                status_code = 201
                resultado = {
                    'status': 'success',
                    'message': 'Movimiento creado correctamente'
                }
            else:
                status_code = 500
                resultado = {
                    'status': 'error',
                    'message': 'No se ha podido crear el movimiento'
                    
                }
            
        else:
            status_code = 400
            resultado = {
                'status': 'error',
                'message': 'Los datos recibidos no son correctos',
                'errors': form.errors
            }
        
        return jsonify({'status': 'success'})
    
    except Exception as error:
        status_code = 500
        resultado = {
            'status': 'error',
            'message': ('Error desconocido en el servidor')
        }
        
    return jsonify(resultado), status_code
      
@app.route('/api/v1/movimientos/<int:id>', methods=['PUT'])
def editar_movimiento(id):
    try:
        headers = request.headers
        if headers.get('Content-Type') != 'application/json':
            return jsonify({'status': 'error', 'message': 'Content-Type debe ser application/json'}), 400
        
        db = DBManager(RUTA)
        movimiento = db.obtener_movimiento(id)
        if not movimiento:
            return jsonify({'status': 'error', 'message': f'No existe un movimiento con ID={id}'}), 404

        # Validar los datos recibidos en el body de la petición (request.json)
        data = request.json
        if not all(key in data for key in ["fecha", "concepto", "tipo", "cantidad"]):
            return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400
        
        fecha = data['fecha']
        concepto = data['concepto']
        tipo = data['tipo']
        cantidad = data['cantidad']

        sql = "UPDATE movimientos SET fecha=?, concepto=?, tipo=?, cantidad=? WHERE id=?"
        es_correcto = db.consultaConParametros(sql, (fecha, concepto, tipo, cantidad, id))

        if es_correcto:
            status_code = 200
            resultado = {
                'status': 'success',
                'message': 'Movimiento actualizado correctamente'
            }
        else:
            status_code = 500
            resultado = {
                'status': 'error',
                'message': 'No se ha podido actualizar el movimiento'
            }
    except Exception as error:
        status_code = 500
        resultado = {
            'status': 'error',
            'message': f'Error desconocido en el servidor: {str(error)}'
        }
        
    return jsonify(resultado), status_code
        
    
        
@app.route('/api/v1/movimientos/<int:id>', methods=['GET'])
def obtener_movimiento_id(id):
    try:
        db = DBManager(RUTA)
        movimiento = db.obtener_movimiento(id)

        if movimiento:
            resultado = {
                'status': 'success',
                'results': movimiento
            }
            status_code = 200
        else:
            resultado = {
                'status': 'error',
                'message': f'No existe un movimiento con ID={id}'
            }
            status_code = 404
    except Exception as error:
        resultado = {
            'status': 'error',
            'message': str(error)
        }
        status_code = 500

    return jsonify(resultado), status_code