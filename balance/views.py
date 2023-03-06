from . import app


@app.route('/')
def inicio():
    return 'vamos a crear una API'