from dominio.usuario import Usuario


class GestionPermisos:
    def __init__(self):
        self._permisos_por_usuario = {}

    def listar_permisos(self, id_usuario):
        return tuple(sorted(self._permisos_por_usuario.get(id_usuario, set())))

    def otorgar_permiso(self, encargado, usuario, permiso):
        if not isinstance(encargado, dict) or encargado.get("nombre_usuario") != "admin":
            return False
        if not isinstance(usuario, Usuario) or type(usuario.id) is not int:
            return False
        if not isinstance(permiso, str) or not permiso.strip():
            return False
        nombre = permiso.strip()
        permisos = self._permisos_por_usuario.setdefault(usuario.id, set())
        if nombre in permisos:
            return False
        permisos.add(nombre)
        return True
