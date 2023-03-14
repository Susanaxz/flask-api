from datetime import date
import sqlite3
from . config import DEFAULT_PAG, PAG_SIZE

"""
SELECT id, fecha, concepto, tipo, cantidad FROM movimientos
"""


class DBManager:
    """
    Clase para interactuar con la base de datos SQLite
    """

    def __init__(self, ruta):
        self.ruta = ruta

    def consultaSQL(self, consulta, pag=DEFAULT_PAG, nreg=PAG_SIZE):
        """
        Paginación:
            - número de página
            - cantidad de registros en cada página
        r = 5
        p = 1
        p1           p2            p3                p4
        1 2 3 4 5    6 7 8 9 10    11 12 13 14 15    16 17 18 19
        p1
        offset = 0  --> (p-1)*r = 0*5: 0
        r = 5
        p2
        offset = 5  --> (p-1)*r = 1*5: 5
        r = 5
        p3
        offset = 10  --> (p-1)*r = 2*5: 10
        r = 5
        p4
        offset = 15  --> (p-1)*r = 3*5: 15
        r = 5
        """
        # 1. Conectar a la base de datos
        conexion = sqlite3.connect(self.ruta)
        offset = nreg*(pag - 1)
        consulta = f'{consulta} LIMIT {nreg} OFFSET {offset}'

        # 2. Abrir un cursor
        cursor = conexion.cursor()

        # 3. Ejecutar la consulta SQL sobre ese cursor
        cursor.execute(consulta)

        # 4. Tratar los datos
        # 4.1 obtener los datos
        datos = cursor.fetchall()

        self.movimientos = []
        nombres_columna = []
        for columna in cursor.description:
            nombres_columna.append(columna[0])

        for dato in datos:
            indice = 0
            movimiento = {}
            for nombre in nombres_columna:
                movimiento[nombre] = dato[indice]
                indice += 1

            self.movimientos.append(movimiento)

        # 5. Cerrar la conexión
        conexion.close()

        # 6. Devolver la colección de resultados
        return self.movimientos

    def conectar(self):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        return conexion, cursor

    def desconectar(self, conexion):
        conexion.close()

    def consultaConParametros(self, consulta, params):
        conexion, cursor = self.conectar()

        resultado = False
        try:
            cursor.execute(consulta, params)
            conexion.commit()
            resultado = True
        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)
        return resultado

    def borrar(self, id):
        consulta = 'DELETE FROM movimientos WHERE id=?'
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        resultado = False
        try:
            cursor.execute(consulta, (id,))
            conexion.commit()
            resultado = True
        except:
            conexion.rollback()

        conexion.close()
        return resultado

    def obtenerMovimiento(self, id):
        """
        Obtiene un movimiento a partir de su ID de la base de datos
        """
        consulta = 'SELECT id, fecha, concepto, tipo, cantidad FROM movimientos WHERE id=?'
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta, (id,))

        datos = cursor.fetchone()
        resultado = None

        if datos:
            nombres_columna = []
            for column in cursor.description:
                nombres_columna.append(column[0])

            # nombres_columna = ['id', 'fecha', 'concepto', 'tipo', 'cantidad']
            # datos           = ( 3,  2023-02-28, 'Camiseta', 'G',   15.00)
            movimiento = {}
            indice = 0
            for nombre in nombres_columna:
                movimiento[nombre] = datos[indice]
                indice += 1

            print(f'Fecha ANTES: {movimiento["fecha"]}')
            movimiento['fecha'] = date.fromisoformat(movimiento['fecha'])
            print(f'DESPUÉS:     {movimiento["fecha"]}')

            resultado = movimiento

        conexion.close()
        return resultado