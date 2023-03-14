from flask import jsonify, request

from . import app
from .config import DEFAULT_PAG, PAG_SIZE
from .forms import MovimientoForm
from .models import DBManager

# Llamadas a la API, devuelven JSON

RUTA = app.config.get('RUTA')


@app.route('/api/v1/movimientos')
def listar_movimientos():
    try:

        # recoger los parámetros de la consulta desde la URL
        # query params
        try:
            pagina = int(request.args.get('p', DEFAULT_PAG))
        except:
            pagina = DEFAULT_PAG

        try:
            tamanyo = int(request.args.get('r', PAG_SIZE))
        except:
            tamanyo = PAG_SIZE

        db = DBManager(RUTA)
        sql = 'SELECT * FROM movimientos'
        movimientos = db.consultaSQL(sql, pagina, tamanyo)
        if len(movimientos) > 0:
            resultado = {
                "status": "success",
                "results": movimientos
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
            "status": "error",
            "message": str(error)
        }
        status_code = 500

    return jsonify(resultado), status_code


@app.route('/api/v1/movimientos/<int:id>')
def get_movimiento(id):
    """
    instanciar DBManager
    preparar la consulta
    ejecutar la consulta
    leer el resultado
    si ok:
      resultado es success / movimiento
    si error:
      resultado es error / mensaje
    devolvemos el resultado
    """

    try:
        db = DBManager(RUTA)
        mov = db.obtenerMovimiento(id)
        if mov:
            resultado = {
                'status': 'success',
                'results': mov
            }
            status_code = 200
        else:
            resultado = {
                'status': 'error',
                'message': f'No he encontrado un movimiento con el ID={id}'
            }
            status_code = 404
    except Exception as error:
        resultado = {
            'status': 'error',
            'message': str(error)
        }
        status_code = 500

    return jsonify(resultado), status_code


@app.route('/api/v1/movimientos/<int:id>', methods=['DELETE'])
def eliminar_movimiento(id):
    """
    Instanciar DBManager
    Comprobar si existe el movimiento con ese ID
    Si existe:
        Preparar sql de la consulta de eliminación
        Ejecutar la consulta de eliminación
        si se ha borrado:
            resultado = ok
        si no:
            resultado = ko
            mensaje = error al borrar
    si no existe:
        resultado = ko
        mensaje = No existe
    """
    try:
        db = DBManager(RUTA)
        mov = db.obtenerMovimiento(id)
        if mov:
            sql = 'DELETE FROM movimientos WHERE id=?'
            esta_borrado = db.consultaConParametros(sql, (id,))
            if esta_borrado:
                # este resultado se ignora si la cabecera
                # envía el estado 204 NO CONTENT
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
                'message': f'No existe un movimiento con ID={id} para eliminar'
            }
            status_code = 404
    except:
        resultado = {
            'status': 'error',
            'message': 'Error desconocido en el servidor'
        }
        status_code = 500

    return jsonify(resultado), status_code


@app.route('/api/v1/movimientos', methods=['POST'])
def insertar_movimiento():
    """
    201 - Creado el movimiento correctamente
    400 - Si los datos recibidos no son válidos
    500 - Si hay un error en el servidor
    """
    try:
        json = request.get_json()
        form = MovimientoForm(data=json)

        if form.validate():
            # si el formulario es válido
            db = DBManager(RUTA)
            # sql = 'INSERT INTO movimientos (fecha, concepto, tipo, cantidad) VALUES (?, ?, ?, ?)'
            # params = (form.fecha.data, form.concepto.data,
            #           form.tipo.data, form.cantidad.data)
            sql = 'INSERT INTO movimientos (fecha, concepto, tipo, cantidad) VALUES (:fecha, :concepto, :tipo, :cantidad)'
            params = request.json
            isSuccess = db.consultaConParametros(sql, params)
            if isSuccess:
                status_code = 201
                resultado = {
                    'status': 'success',
                }
            else:
                status_code = 500
                resultado = {
                    'status': 'error',
                    'message': 'No se pudo insertar el movimiento'
                }
        else:
            # si el formulario tiene errores de validación
            status_code = 400
            resultado = {
                'status': 'error',
                'message': 'Los datos recibidos no son válidos',
                'errors': form.errors
            }

    except:
        status_code = 500
        resultado = {
            'status': 'error',
            'message': 'Error desconocido en el servidor'
        }

    return jsonify(resultado), status_code


@app.route('/api/v1/movimientos/<int:id>', methods=['PUT'])
def modificar_movimiento(id):
    """
    200 - OK. La modificación se ha realizado
    400 - Si los datos recibidos no son válidos
    500 - Si hay error en el servidor
    """

    try:
        json = request.get_json()
        form = MovimientoForm(data=json)

        if form.validate():
            # El formulario es válido
            if id == form.id.data:
                db = DBManager(RUTA)
                sql = 'UPDATE movimientos SET fecha=?, concepto=?, tipo=?, cantidad=? WHERE id=?'
                params = (
                    form.fecha.data,
                    form.concepto.data,
                    form.tipo.data,
                    form.cantidad.data,
                    form.id.data
                )
                modificado = db.consultaConParametros(sql, params)
                if modificado:
                    status_code = 200
                    resultado = {
                        'status': 'success',
                        'results': form.data
                    }
                else:
                    status_code = 500
                    resultado = {
                        'status': 'error',
                        'message': 'No se ha podido insertar el movimiento'
                    }
            else:
                status_code = 400
                resultado = {
                    'status': 'error',
                    'message': 'Los datos enviados son inconsistentes'
                }
        else:
            status_code = 400
            resultado = {
                'status': 'error',
                'message': 'Los datos recibidos no son válidos',
                'errors': form.errors
            }

    except:
        status_code = 500
        resultado = {
            'status': 'error',
            'message': 'Error desconocido en el servidor'
        }
    return jsonify(resultado), status_code