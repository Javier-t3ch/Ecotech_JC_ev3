import bcrypt

from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO

MAX_BYTES_BCRYPT = 72


def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("La contraseña supera los 72 bytes permitidos.")
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")


def registrar_usuario(empleado_id, nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if type(empleado_id) is not int or empleado_id <= 0:
        raise ValueError("El ID del empleado debe ser positivo.")
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("El empleado no existe.")
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError("Ese nombre de usuario ya está ocupado.")
    if UsuarioDAO.buscar_por_empleado(empleado_id) is not None:
        raise ValueError("Este empleado ya tiene una cuenta.")

    cuenta = Usuario(nombre, crear_hash(clave), empleado_id)
    return UsuarioDAO.insertar(cuenta)


def autenticar(nombre, clave):
    try:
        nombre = Usuario.normalizar_usuario(nombre)
    except (TypeError, ValueError):
        return None
    if not isinstance(clave, str):
        return None
    datos = clave.encode("utf-8")
    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
        return None
    cuenta = UsuarioDAO.buscar_por_nombre(nombre)
    if cuenta is None:
        return None
    try:
        es_valida = bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8"))
    except ValueError:
        return None
    if not es_valida:
        return None
    return {
        "id": cuenta.id,
        "empleado_id": cuenta.empleado_id,
        "nombre_usuario": cuenta.nombre_usuario,
    }


def cambiar_contrasena(nombre, clave_actual, clave_nueva):
    sesion = autenticar(nombre, clave_actual)
    if sesion is None or clave_nueva == clave_actual:
        return False
    nuevo_hash = crear_hash(clave_nueva)
    return UsuarioDAO.actualizar_password_hash(sesion["id"], nuevo_hash)

