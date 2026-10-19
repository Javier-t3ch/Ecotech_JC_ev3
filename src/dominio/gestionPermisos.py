from dominio import usuario

class GestionPermisos:

    def otorgar_permiso(self, encargado, usuario, permiso):
        if encargado is None or usuario is None:
            return False
        return usuario.agregar_permiso(permiso, encargado)

