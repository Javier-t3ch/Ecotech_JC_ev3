from dominio.cargo import CARGO_RECURSOS_HUMANOS
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO


def exigir_sesion(sesion):
    if not isinstance(sesion, dict):
        raise PermissionError("Debe iniciar sesión.")
    usuario_id = sesion.get("id")
    empleado_id = sesion.get("empleado_id")
    if (type(usuario_id) is not int or usuario_id <= 0
            or type(empleado_id) is not int or empleado_id <= 0
            or sesion.get("rol") not in ("admin", "empleado")):
        raise PermissionError("Sesión inválida.")
    cuenta = UsuarioDAO.buscar_por_id(usuario_id)
    if (cuenta is None or cuenta.empleado_id != empleado_id
            or cuenta.rol != sesion["rol"]
            or cuenta.nombre_usuario != sesion.get("nombre_usuario")):
        raise PermissionError("La cuenta ya no tiene acceso con esta sesión.")
    return cuenta


def exigir_admin(sesion):
    cuenta = exigir_sesion(sesion)
    if cuenta.rol != "admin":
        raise PermissionError("Acción exclusiva del administrador.")
    return cuenta


def empleado_de_sesion(sesion):
    try:
        cuenta = exigir_sesion(sesion)
    except PermissionError:
        return None
    return EmpleadoDAO.buscar_por_id(cuenta.empleado_id)


def exigir_recursos_humanos(sesion):
    cuenta = exigir_sesion(sesion)
    empleado = EmpleadoDAO.buscar_por_id(cuenta.empleado_id)
    if empleado is None or empleado._id_cargo != CARGO_RECURSOS_HUMANOS:
        raise PermissionError("Solo Recursos Humanos puede contratar empleados.")
    return empleado


def puede_contratar(sesion):
    try:
        exigir_recursos_humanos(sesion)
        return True
    except PermissionError:
        return False
