from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.proyecto import Proyecto
from dominio.registroTiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO


class ProyectoDao:

    @staticmethod
    def _fila_a_proyecto(fila, cargar_relaciones=True):
        proyecto = Proyecto(
            id_proyecto=fila[0], nombre=fila[1],
            fecha_inicio=fila[2], descripcion=fila[3]
        )
        if not cargar_relaciones:
            return proyecto

        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"SELECT empleado_id FROM proyecto_empleado WHERE proyecto_id = {marca}",
                (proyecto._id_proyecto,)
            )
            for (id_empleado,) in cursor.fetchall():
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is not None:
                    proyecto._empleados.append(empleado)

            cursor.execute(
                "SELECT id, horas_trabajadas, fecha_trabajada, descripcion_tarea, empleado_id "
                f"FROM registro_tiempo WHERE proyecto_id = {marca}",
                (proyecto._id_proyecto,)
            )
            for fila_registro in cursor.fetchall():
                empleado = None
                for asignado in proyecto._empleados:
                    if asignado._id == fila_registro[4]:
                        empleado = asignado
                        break
                if empleado is None:
                    empleado = EmpleadoDAO.buscar_por_id(fila_registro[4])
                if empleado is not None:
                    proyecto._registros_tiempo.append(RegistroTiempo(
                        id_registro=fila_registro[0],
                        horas_trabajadas=fila_registro[1],
                        fecha_trabajada=fila_registro[2],
                        descripcion_tarea=fila_registro[3],
                        empleado=empleado, proyecto=proyecto
                    ))
        finally:
            conexion.close()
        return proyecto

    @staticmethod
    def insertar(proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"INSERT INTO proyecto (nombre, fecha_inicio, descripcion) VALUES ({marca}, {marca}, {marca})",
                (proyecto._nombre, proyecto._fecha_inicio, proyecto._descripcion)
            )
            conexion.commit()
            proyecto._id_proyecto = cursor.lastrowid
            return proyecto
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def actualizar(proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"UPDATE proyecto SET nombre = {marca}, fecha_inicio = {marca}, descripcion = {marca} WHERE id = {marca}",
                (proyecto._nombre, proyecto._fecha_inicio, proyecto._descripcion, proyecto._id_proyecto)
            )
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

    @staticmethod
    def eliminar(id_proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(f"DELETE FROM proyecto WHERE id = {marca}", (id_proyecto,))
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

    @staticmethod
    def buscar_por_id(id_proyecto, cargar_relaciones=True):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"SELECT id, nombre, fecha_inicio, descripcion FROM proyecto WHERE id = {marca}",
                (id_proyecto,)
            )
            fila = cursor.fetchone()
        finally:
            conexion.close()
        if fila is None:
            return None
        return ProyectoDao._fila_a_proyecto(fila, cargar_relaciones)

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, fecha_inicio, descripcion FROM proyecto")
            filas = cursor.fetchall()
        finally:
            conexion.close()
        return [ProyectoDao._fila_a_proyecto(fila) for fila in filas]

    @staticmethod
    def _cambiar_empleado(proyecto, empleado, agregar):
        if proyecto._id_proyecto is None or empleado._id is None:
            return False
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            if agregar:
                cursor.execute(
                    f"SELECT 1 FROM proyecto_empleado WHERE proyecto_id = {marca} AND empleado_id = {marca}",
                    (proyecto._id_proyecto, empleado._id)
                )
                if cursor.fetchone():
                    return False
                cursor.execute(
                    f"INSERT INTO proyecto_empleado (proyecto_id, empleado_id) VALUES ({marca}, {marca})",
                    (proyecto._id_proyecto, empleado._id)
                )
            else:
                cursor.execute(
                    f"DELETE FROM proyecto_empleado WHERE proyecto_id = {marca} AND empleado_id = {marca}",
                    (proyecto._id_proyecto, empleado._id)
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
    def asignar_empleado(proyecto, empleado):
        return ProyectoDao._cambiar_empleado(proyecto, empleado, True)

    @staticmethod
    def desvincular_empleado(proyecto, empleado):
        return ProyectoDao._cambiar_empleado(proyecto, empleado, False)
