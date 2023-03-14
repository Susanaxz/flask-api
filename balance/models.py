import sqlite3
from datetime import date, datetime, timedelta
import random


"""
SELECT id,fecha,concepto,tipo,cantidad FROM movimientos
"""


class DBManager:
    """
    clase para interactuar con la bbdd SQLite

    """

    def __init__(self, ruta):
        self.ruta = ruta

    # consulta = f'DELETE FROM movimientos WHERE id={id}'

    def consultaSQL(self, consulta, params=None):
        """
        1. Conectar a la BBDD
        2. Generar un cursor que nos permita escribir o leer líneas
        3. Ejecutar la consulta SQL sobre ese cursor
        4. Tratar los datos de forma que python los pueda interpretar
        5. Cerrar la conexión
        6. Devolver la colección de resultados
        """
        conexion = sqlite3.connect(self.ruta)  # 1. conecta a la bbdd
        cursor = conexion.cursor()  # 2.crea un cursor
        if params is None:
            cursor.execute(consulta)
        else:
            cursor.execute(consulta, params)

        # 4. Tratar los datos de forma que python los pueda interpretar
        # 4.1 obtener los datos
        datos = cursor.fetchall()

        self.movimientos = []

        # nombres_columna = ['id', 'fecha', 'concepto', 'tipo', 'cantidad']

        nombres_columna = []
        for (
            columna
        ) in (
            cursor.description
        ):  # recorres los nombres de la bbdd y los añade a la lista
            nombres_columna.append(columna[0])  # en la posición 0

        for dato in datos:
            indice = 0
            movimiento = {}
            for nombre in nombres_columna:
                movimiento[nombre] = dato[indice]
                indice += 1
            self.movimientos.append(movimiento)  # tendríamos una lista de diccionarios

            #### es lo mismo que el código de arriba ####
            # movimiento = {
            #     'id': dato[0],
            #     'fecha': dato[1],
            #     'concepto': dato[2],
            #     'tipo': dato[3],
            #     'cantidad': dato[4]
            # }
            # """ CERRAR LA CONEXION"""
        conexion.close()

        # devolver la colección de resultados
        return self.movimientos

    def consultaConParametros(self, consulta, params):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        resultado = False

        try:
            cursor.execute(consulta, params)
            conexion.commit()
            resultado = True

        except Exception as ex:
            print(ex)
            conexion.rollback()

        conexion.close()
        return resultado

    def borrar(self, id):
        consulta = "DELETE FROM movimientos WHERE id=?"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        resultado = False
        try:
            cursor.execute(consulta, (id,))
            conexion.commit()  # guarda los cambios de la bbdd
            resultado = True

        except:
            conexion.rollback()

        conexion.close()
        return resultado

    def obtener_movimiento(self, id):
        """
        obtiene un movimiento a partir de su id de la base de datos

        """
        consulta = (
            "SELECT id, fecha, concepto, tipo, cantidad FROM movimientos WHERE id=?"
        )
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta, (id,))
        datos = cursor.fetchone()
        resultado = None

        if datos:
            nombres_col = []
            for columna in cursor.description:
                nombres_col.append(columna[0])
            movimiento = {}
            indice = 0
            for nombre in nombres_col:
                movimiento[nombre] = datos[indice]
                indice += 1

            movimiento["fecha"] = date.fromisoformat(movimiento["fecha"])

            resultado = movimiento

        conexion.close()
        return resultado

    def añadir(self, movimiento):
        consulta = "INSERT INTO movimientos(fecha, concepto, tipo, cantidad) VALUES(?,?,?,?)"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        resultado = False
        try:
            cursor.execute(
                consulta,
                (
                    movimiento["fecha"],
                    # movimiento["fecha"].isoformat(),
                    movimiento["concepto"],
                    movimiento["tipo"],
                    movimiento["cantidad"],
                ),
            )
            conexion.commit() # guarda los cambios de la bbdd
            resultado = True

        except:
            conexion.rollback()

        conexion.close()
        return resultado
    
    def obtener_movimientos_por_tipo(self, tipo):
        consulta = "SELECT id, fecha, concepto, tipo, cantidad FROM movimientos WHERE tipo = ?"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta, (tipo,))
        datos = cursor.fetchall()
        conexion.close()
        return datos
    
    def obtener_mov_por_pagina(self, pagina):
        consulta = "SELECT id, fecha, concepto, tipo, cantidad FROM movimientos LIMIT 10 OFFSET ?"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta, (pagina,))
        movimientos_por_pagina = 20
        datos = cursor.fetchall()
        conexion.close()
        return datos
    
    def get_paginated_movements(self, page, items_per_page):
        offset = (page - 1) * items_per_page
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute('SELECT COUNT(*) FROM movimientos')
        total_items = cursor.fetchone()[0]
        cursor.execute('SELECT * FROM movimientos LIMIT ? OFFSET ?', (items_per_page, offset))
        items = cursor.fetchall()
        cursor.close()
        return items, total_items