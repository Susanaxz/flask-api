from flask import jsonify, render_template, request  # convierte un objeto en un json
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

# TODO: CREAR un endpoint para CREAR un movimiento nuevo
# TODO: CREAR un ednpoint para ACTUALIZAR un movimiento por ID (PUT)

# llamadas a la web, devuelven HTML
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nuevo')
def form_nuevo():
    formulario = MovimientoForm()
    return render_template('form_movimiento.html', form=formulario, accion='/nuevo')
    
    
   
# llamadas a la API REST, devuelven un JSON

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
      
      
      
# TODO: actualizar movimiento por ID    
