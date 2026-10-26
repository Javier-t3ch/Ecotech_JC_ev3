import bcrypt
from dominio.usuario import Usuario

MAX_BYTES_BCRYPT = 72

def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")

    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(
        clave_bytes, bcrypt.gensalt()
).decode("utf-8")

def registrar_usuario(empleado_id, nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta.")

    hash_guardado = crear_hash(clave)
    usuario = Usuario(nombre, hash_guardado, empleado_id)

    return UsuarioDAO.insertar(usuario)