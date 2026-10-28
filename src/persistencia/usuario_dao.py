from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion, marcador_sql


class UsuarioDAO:

    @staticmethod
    def _desde_fila(fila):
        return None if fila is None else Usuario(
            nombre_usuario=fila[1], password_hash=fila[2],
            empleado_id=int(fila[3]), id=int(fila[0])
        )

    @staticmethod
    def insertar(usuario):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"INSERT INTO usuario (nombre_usuario, password_hash, empleado_id) "
                f"VALUES ({marca}, {marca}, {marca})",
                (usuario.nombre_usuario, usuario.password_hash, usuario.empleado_id),
            )
            conexion.commit()
            usuario.id = cursor.lastrowid
            return usuario.id
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_nombre(nombre):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT id, nombre_usuario, password_hash, empleado_id "
                f"FROM usuario WHERE nombre_usuario = {marcador_sql()}", (nombre,)
            )
            return UsuarioDAO._desde_fila(cursor.fetchone())
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_empleado(empleado_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT id, nombre_usuario, password_hash, empleado_id "
                f"FROM usuario WHERE empleado_id = {marcador_sql()}", (empleado_id,)
            )
            return UsuarioDAO._desde_fila(cursor.fetchone())
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_id(usuario_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT id, nombre_usuario, password_hash, empleado_id "
                f"FROM usuario WHERE id = {marcador_sql()}", (usuario_id,)
            )
            return UsuarioDAO._desde_fila(cursor.fetchone())
        finally:
            conexion.close()

    @staticmethod
    def listar():
        """No entrega hashes al menú que lista cuentas."""
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre_usuario, empleado_id FROM usuario ORDER BY id")
            return [
                {"id": int(id_usuario), "nombre_usuario": nombre, "empleado_id": int(empleado_id)}
                for id_usuario, nombre, empleado_id in cursor.fetchall()
            ]
        finally:
            conexion.close()

    @staticmethod
    def actualizar_password_hash(usuario_id, password_hash):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                f"UPDATE usuario SET password_hash = {marcador_sql()} "
                f"WHERE id = {marcador_sql()}", (password_hash, usuario_id)
            )
            actualizado = cursor.rowcount > 0
            conexion.commit()
            return actualizado
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()
