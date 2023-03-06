from . import app


@app.route('/')
def inicio():
    return (f'la ruta del archivo de datos es: {app.config["RUTA"]}<br>'
            f' Secret key: {app.config["SECRET_KEY"]}')
    