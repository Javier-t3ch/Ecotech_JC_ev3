from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.empleado import Empleado


class EmpleadoDAO:

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            id=fila[0],
            nombre=fila[1],
            direccion=fila[2],
            numero=fila[3],
            correo=fila[4],
            fecha_contrato=fila[5],
            salario=fila[6],
            cargo=fila[7]
        )

    def insertar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "INSERT INTO empleado "
                "(nombre, direccion, numero, correo, fecha_contrato, salario, cargo) "
                f"VALUES ({marca}, {marca}, {marca}, {marca}, {marca}, {marca}, {marca})"
            )
            cursor.execute(sql, (
                empleado._nombre,
                empleado._direccion,
                empleado._numero,
                empleado._correo,
                empleado._fecha_contrato,
                empleado._salario,
                empleado._cargo
            ))
            conexion.commit()
            empleado._id = cursor.lastrowid
            return empleado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    def actualizar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "UPDATE empleado SET "
                f"nombre = {marca}, direccion = {marca}, numero = {marca}, "
                f"correo = {marca}, fecha_contrato = {marca}, "
                f"salario = {marca}, cargo = {marca} "
                f"WHERE id = {marca}"
            )
            cursor.execute(sql, (
                empleado._nombre,
                empleado._direccion,
                empleado._numero,
                empleado._correo,
                empleado._fecha_contrato,
                empleado._salario,
                empleado._cargo,
                empleado._id
            ))
            actualizado = cursor.rowcount > 0
            conexion.commit()
            return actualizado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    def eliminar(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = f"DELETE FROM empleado WHERE id = {marca}"
            cursor.execute(sql, (id_empleado,))
            eliminado = cursor.rowcount > 0
            conexion.commit()
            return eliminado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    def buscar_por_id(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "SELECT id, nombre, direccion, numero, correo, "
                "fecha_contrato, salario, cargo "
                f"FROM empleado WHERE id = {marca}"
            )
            cursor.execute(sql, (id_empleado,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return EmpleadoDAO._fila_a_empleado(fila)
        finally:
            if conexion:
                conexion.close()

    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre, direccion, numero, correo, "
                "fecha_contrato, salario, cargo FROM empleado"
            )
            filas = cursor.fetchall()
            empleados = []
            for fila in filas:
                empleados.append(EmpleadoDAO._fila_a_empleado(fila))
            return empleados
        finally:
            if conexion:
                conexion.close()
