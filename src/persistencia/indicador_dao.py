from dominio.indicador import Indicador
from persistencia.conexion import abrir_conexion, obtener_motor


class IndicadorDAO:
    @staticmethod
    def guardar(indicador):
        if not isinstance(indicador, Indicador):
            raise TypeError("Se esperaba un objeto Indicador.")
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            valores = (
                indicador.fuente, indicador.codigo, indicador.fecha,
                indicador.valor, indicador.unidad, indicador.verificado_en,
            )
            if obtener_motor() == "sqlite":
                cursor.execute("""INSERT INTO indicador_api
                    (fuente, codigo, fecha, valor, unidad, verificado_en)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
                        valor = excluded.valor,
                        unidad = excluded.unidad,
                        verificado_en = excluded.verificado_en""", valores)
            else:
                cursor.execute("""INSERT INTO indicador_api
                    (fuente, codigo, fecha, valor, unidad, verificado_en)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        valor = VALUES(valor),
                        unidad = VALUES(unidad),
                        verificado_en = VALUES(verificado_en)""", valores)
            conexion.commit()
            return True
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def _fila_a_indicador(fila):
        return Indicador(fecha=fila[2], valor=float(fila[3]),
                         fuente=fila[0], verificado_en=fila[5])

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("""SELECT fuente, codigo, fecha, valor, unidad, verificado_en
                FROM indicador_api
                WHERE codigo = 'dolar' AND unidad = 'CLP/USD'
                ORDER BY fecha DESC, verificado_en DESC""")
            filas = cursor.fetchall()
            return [IndicadorDAO._fila_a_indicador(fila) for fila in filas]
        finally:
            conexion.close()

    @staticmethod
    def ultimo():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("""SELECT fuente, codigo, fecha, valor, unidad, verificado_en
                FROM indicador_api
                WHERE codigo = 'dolar' AND unidad = 'CLP/USD'
                ORDER BY fecha DESC, verificado_en DESC LIMIT 1""")
            fila = cursor.fetchone()
            return IndicadorDAO._fila_a_indicador(fila) if fila else None
        finally:
            conexion.close()
