from dominio.clima import Clima
from persistencia.conexion import abrir_conexion, obtener_motor


class ClimaDAO:
    @staticmethod
    def guardar(clima):
        if not isinstance(clima, Clima):
            raise TypeError("Se esperaba un objeto Clima.")
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            valores = (clima.fuente, clima.ciudad, clima.fecha_hora,
                    clima.temperatura, clima.humedad, clima.codigo_clima,
                    clima.estado, clima.verificado_en)
            if obtener_motor() == "sqlite":
                cursor.execute("""INSERT INTO clima_api
                    (fuente, ciudad, fecha_hora, temperatura, humedad,
                    codigo_clima, estado, verificado_en)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (fuente, ciudad, fecha_hora) DO UPDATE SET
                        temperatura = excluded.temperatura,
                        humedad = excluded.humedad,
                        codigo_clima = excluded.codigo_clima,
                        estado = excluded.estado,
                        verificado_en = excluded.verificado_en""", valores)
            else:
                cursor.execute("""INSERT INTO clima_api
                    (fuente, ciudad, fecha_hora, temperatura, humedad,
                    codigo_clima, estado, verificado_en)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        temperatura = VALUES(temperatura),
                        humedad = VALUES(humedad),
                        codigo_clima = VALUES(codigo_clima),
                        estado = VALUES(estado),
                        verificado_en = VALUES(verificado_en)""", valores)
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def _fila_a_clima(fila):
        return Clima(ciudad=fila[1], fecha_hora=fila[2], temperatura=float(fila[3]),
                    humedad=float(fila[4]), codigo_clima=int(fila[5]), estado=fila[6],
                    fuente=fila[0], verificado_en=fila[7])

    @staticmethod
    def listar(ciudad):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(f"""SELECT fuente, ciudad, fecha_hora, temperatura,
                humedad, codigo_clima, estado, verificado_en
                FROM clima_api WHERE ciudad = {marcador}
                ORDER BY fecha_hora DESC, verificado_en DESC""", (ciudad,))
            return [ClimaDAO._fila_a_clima(fila) for fila in cursor.fetchall()]
        finally:
            conexion.close()

    @staticmethod
    def ultimo(ciudad):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(f"""SELECT fuente, ciudad, fecha_hora, temperatura,
                humedad, codigo_clima, estado, verificado_en
                FROM clima_api WHERE ciudad = {marcador}
                ORDER BY fecha_hora DESC, verificado_en DESC LIMIT 1""", (ciudad,))
            fila = cursor.fetchone()
            return ClimaDAO._fila_a_clima(fila) if fila else None
        finally:
            conexion.close()
