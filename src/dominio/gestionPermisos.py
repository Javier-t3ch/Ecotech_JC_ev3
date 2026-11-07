from persistencia.usuario_dao import UsuarioDAO
from servicios.autorizacion import exigir_admin


class GestionPermisos:
    def listar_cuentas(self, sesion):
        exigir_admin(sesion)
        return UsuarioDAO.listar()

    def otorgar_admin(self, sesion, id_usuario):
        exigir_admin(sesion)
        cuenta = UsuarioDAO.buscar_por_id(id_usuario)
        if cuenta is None:
            raise ValueError("La cuenta seleccionada no existe.")
        if cuenta.rol == "admin":
            return False
        return UsuarioDAO.asignar_rol(cuenta.id, "admin")
