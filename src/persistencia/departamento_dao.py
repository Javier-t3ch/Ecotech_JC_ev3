from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.departamento import Departamento
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao


class DepartamentoDAO:

    @staticmethod
    def _fila_de_departamento(fila):
        departamento = Departamento(
            id_departamento=fila[0],
            nombre=fila[1],
            id_gerente=fila[2]
        )
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"SELECT empleado_id FROM departamento_empleado WHERE departamento_id = {marca}",
                (departamento._id_departamento,)
            )
            for (id_empleado,) in cursor.fetchall():
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is not None:
                    departamento._empleados.append(empleado)

            cursor.execute(
                f"SELECT proyecto_id FROM departamento_proyecto WHERE departamento_id = {marca}",
                (departamento._id_departamento,)
            )
            for (id_proyecto,) in cursor.fetchall():
                proyecto = ProyectoDao.buscar_por_id(id_proyecto)
                if proyecto is not None:
                    departamento._proyectos.append(proyecto)
        finally:
            conexion.close()
        return departamento

    @staticmethod
    def insertar(departamento):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"INSERT INTO departamento (nombre, id_gerente) VALUES ({marca}, {marca})",
                (departamento._nombre, departamento._id_gerente)
            )
            conexion.commit()
            departamento._id_departamento = cursor.lastrowid
            return departamento
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def actualizar(departamento):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"UPDATE departamento SET nombre = {marca}, id_gerente = {marca} WHERE id = {marca}",
                (departamento._nombre, departamento._id_gerente, departamento._id_departamento)
            )
            resultado = cursor.rowcount > 0
            conexion.commit()
            return resultado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(id_departamento):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(f"DELETE FROM departamento WHERE id = {marca}", (id_departamento,))
            resultado = cursor.rowcount > 0
            conexion.commit()
            return resultado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_id(id_departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"SELECT id, nombre, id_gerente FROM departamento WHERE id = {marca}",
                (id_departamento,)
            )
            fila = cursor.fetchone()
        finally:
            conexion.close()
        if fila is None:
            return None
        return DepartamentoDAO._fila_de_departamento(fila)

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, id_gerente FROM departamento")
            filas = cursor.fetchall()
        finally:
            conexion.close()
        return [DepartamentoDAO._fila_de_departamento(fila) for fila in filas]

    @staticmethod
    def _cambiar_relacion(tabla, id_departamento, columna, id_objeto, agregar):
        if id_departamento is None or id_objeto is None:
            return False
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            if agregar:
                cursor.execute(
                    f"SELECT 1 FROM {tabla} WHERE departamento_id = {marca} AND {columna} = {marca}",
                    (id_departamento, id_objeto)
                )
                if cursor.fetchone():
                    return False
                cursor.execute(
                    f"INSERT INTO {tabla} (departamento_id, {columna}) VALUES ({marca}, {marca})",
                    (id_departamento, id_objeto)
                )
            else:
                cursor.execute(
                    f"DELETE FROM {tabla} WHERE departamento_id = {marca} AND {columna} = {marca}",
                    (id_departamento, id_objeto)
                )
            resultado = cursor.rowcount > 0
            conexion.commit()
            return resultado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def agregar_empleado(departamento, empleado):
        return DepartamentoDAO._cambiar_relacion(
            "departamento_empleado", departamento._id_departamento,
            "empleado_id", empleado._id, True
        )

    @staticmethod
    def quitar_empleado(departamento, empleado):
        return DepartamentoDAO._cambiar_relacion(
            "departamento_empleado", departamento._id_departamento,
            "empleado_id", empleado._id, False
        )

    @staticmethod
    def agregar_proyecto(departamento, proyecto):
        return DepartamentoDAO._cambiar_relacion(
            "departamento_proyecto", departamento._id_departamento,
            "proyecto_id", proyecto._id_proyecto, True
        )

    @staticmethod
    def quitar_proyecto(departamento, proyecto):
        return DepartamentoDAO._cambiar_relacion(
            "departamento_proyecto", departamento._id_departamento,
            "proyecto_id", proyecto._id_proyecto, False
        )
