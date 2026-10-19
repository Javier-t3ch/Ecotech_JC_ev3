from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.registroTiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao


class RegistroTiempoDAO:

    @staticmethod
    def _asignacion_valida(cursor, marca, id_empleado, id_proyecto):
        cursor.execute(
            f"SELECT 1 FROM proyecto_empleado WHERE empleado_id = {marca} AND proyecto_id = {marca}",
            (id_empleado, id_proyecto)
        )
        return cursor.fetchone() is not None

    @staticmethod
    def empleado_asignado(id_empleado, id_proyecto):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            return RegistroTiempoDAO._asignacion_valida(
                cursor, marca, id_empleado, id_proyecto
            )
        finally:
            conexion.close()

    @staticmethod
    def _fila_de_registroTiempo(fila):
        empleado = EmpleadoDAO.buscar_por_id(fila[4])
        proyecto = ProyectoDao.buscar_por_id(fila[5], cargar_relaciones=False)
        if empleado is None or proyecto is None:
            raise ValueError("El registro tiene un empleado o proyecto inexistente")
        return RegistroTiempo(
            id_registro=fila[0],
            horas_trabajadas=fila[1],
            fecha_trabajada=fila[2],
            descripcion_tarea=fila[3],
            empleado=empleado,
            proyecto=proyecto
        )

    def insertar(registroTiempo):
        if registroTiempo._empleado is None or registroTiempo._proyecto is None:
            return False
        if registroTiempo._empleado._id is None or registroTiempo._proyecto._id_proyecto is None:
            return False
        if registroTiempo._horas_trabajadas <= 0:
            return False
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            if not RegistroTiempoDAO._asignacion_valida(
                cursor, marca, registroTiempo._empleado._id,
                registroTiempo._proyecto._id_proyecto
            ):
                return False
            sql = (
                "INSERT INTO registro_tiempo "
                "(horas_trabajadas, fecha_trabajada, descripcion_tarea, empleado_id, proyecto_id) "
                f"VALUES ({marca}, {marca}, {marca}, {marca}, {marca})"
            )
            cursor.execute(sql, (
                registroTiempo._horas_trabajadas,
                registroTiempo._fecha_trabajada,
                registroTiempo._descripcion_tarea,
                registroTiempo._empleado._id,
                registroTiempo._proyecto._id_proyecto
            ))
            conexion.commit()
            registroTiempo._id_registro = cursor.lastrowid
            return registroTiempo
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    def actualizar(registroTiempo):
        if registroTiempo._empleado is None or registroTiempo._proyecto is None:
            return False
        if registroTiempo._empleado._id is None or registroTiempo._proyecto._id_proyecto is None:
            return False
        if registroTiempo._horas_trabajadas <= 0:
            return False
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            if not RegistroTiempoDAO._asignacion_valida(
                cursor, marca, registroTiempo._empleado._id,
                registroTiempo._proyecto._id_proyecto
            ):
                return False
            sql = (
                "UPDATE registro_tiempo SET "
                f"horas_trabajadas = {marca}, fecha_trabajada = {marca}, "
                f"descripcion_tarea = {marca}, empleado_id = {marca}, "
                f"proyecto_id = {marca} WHERE id = {marca}"
            )
            cursor.execute(sql, (
                registroTiempo._horas_trabajadas,
                registroTiempo._fecha_trabajada,
                registroTiempo._descripcion_tarea,
                registroTiempo._empleado._id,
                registroTiempo._proyecto._id_proyecto,
                registroTiempo._id_registro
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

    def eliminar(id_registro):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = f"DELETE FROM registro_tiempo WHERE id = {marca}"
            cursor.execute(sql, (id_registro,))
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

    def buscar_por_id(id_registro):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            sql = (
                "SELECT id, horas_trabajadas, fecha_trabajada, descripcion_tarea, "
                f"empleado_id, proyecto_id FROM registro_tiempo WHERE id = {marca}"
            )
            cursor.execute(sql, (id_registro,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return RegistroTiempoDAO._fila_de_registroTiempo(fila)
        finally:
            if conexion:
                conexion.close()

    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, horas_trabajadas, fecha_trabajada, descripcion_tarea, "
                "empleado_id, proyecto_id FROM registro_tiempo"
            )
            filas = cursor.fetchall()
            registros = []
            for fila in filas:
                registros.append(RegistroTiempoDAO._fila_de_registroTiempo(fila))
            return registros
        finally:
            if conexion:
                conexion.close()
