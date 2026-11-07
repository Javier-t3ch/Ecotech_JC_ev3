from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.empleado import Empleado
from validaciones import validar_texto, validar_correo, validar_telefono


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
            id_cargo=fila[7]
        )

    @staticmethod
    def _validar_datos(empleado):
        validar_texto(empleado._nombre, tipo="persona", campo="Nombre", maximo=50)
        validar_texto(empleado._direccion, tipo="direccion", campo="Dirección", maximo=150)
        validar_telefono(empleado._numero)
        validar_correo(empleado._correo)

    def insertar(empleado):
        EmpleadoDAO._validar_datos(empleado)
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "INSERT INTO empleado "
                "(nombre, direccion, numero, correo, fecha_contrato, salario, id_cargo) "
                f"VALUES ({marca}, {marca}, {marca}, {marca}, {marca}, {marca}, {marca})"
            )
            cursor.execute(sql, (
                empleado._nombre,
                empleado._direccion,
                empleado._numero,
                empleado._correo,
                empleado._fecha_contrato,
                empleado._salario,
                empleado._id_cargo
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
        EmpleadoDAO._validar_datos(empleado)
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "UPDATE empleado SET "
                f"nombre = {marca}, direccion = {marca}, numero = {marca}, "
                f"correo = {marca}, fecha_contrato = {marca}, "
                f"salario = {marca}, id_cargo = {marca} "
                f"WHERE id = {marca}"
            )
            cursor.execute(sql, (
                empleado._nombre,
                empleado._direccion,
                empleado._numero,
                empleado._correo,
                empleado._fecha_contrato,
                empleado._salario,
                empleado._id_cargo,
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
                "fecha_contrato, salario, id_cargo "
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
                "fecha_contrato, salario, id_cargo FROM empleado"
            )
            filas = cursor.fetchall()
            empleados = []
            for fila in filas:
                empleados.append(EmpleadoDAO._fila_a_empleado(fila))
            return empleados
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def insertar_con_departamento(empleado, departamento_id):
        EmpleadoDAO._validar_datos(empleado)
        if type(departamento_id) is not int or departamento_id <= 0:
            raise ValueError("Seleccione un departamento válido.")
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(f"SELECT 1 FROM departamento WHERE id = {marca}", (departamento_id,))
            if cursor.fetchone() is None:
                raise ValueError("El departamento seleccionado ya no existe.")
            cursor.execute(
                "INSERT INTO empleado (nombre, direccion, numero, correo, "
                "fecha_contrato, salario, id_cargo) "
                f"VALUES ({', '.join([marca] * 7)})",
                (empleado._nombre, empleado._direccion, empleado._numero,
                 empleado._correo, empleado._fecha_contrato, empleado._salario,
                 empleado._id_cargo),
            )
            nuevo_id = cursor.lastrowid
            cursor.execute(
                f"INSERT INTO departamento_empleado (departamento_id, empleado_id) "
                f"VALUES ({marca}, {marca})", (departamento_id, nuevo_id)
            )
            conexion.commit()
            empleado._id = nuevo_id
            return empleado
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def listar_sin_cuenta():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT e.id, e.nombre, e.direccion, e.numero, e.correo, "
                "e.fecha_contrato, e.salario, e.id_cargo "
                "FROM empleado AS e "
                "LEFT JOIN usuario AS u ON u.empleado_id = e.id "
                "WHERE u.id IS NULL "
                "ORDER BY e.id"
            )
            return [EmpleadoDAO._fila_a_empleado(fila) for fila in cursor.fetchall()]
        finally:
            conexion.close()

    @staticmethod
    def correo_ocupado(correo, excluir_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"SELECT 1 FROM empleado WHERE LOWER(correo) = LOWER({marca}) "
                f"AND id <> {marca} LIMIT 1", (correo, excluir_id)
            )
            return cursor.fetchone() is not None
        finally:
            conexion.close()

    @staticmethod
    def actualizar_nombre_correo(empleado_id, nombre, correo):
        validar_texto(nombre, tipo="persona", campo="Nombre", maximo=50)
        validar_correo(correo)
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"UPDATE empleado SET nombre = {marca}, correo = {marca} WHERE id = {marca}",
                (nombre, correo, empleado_id),
            )
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()
