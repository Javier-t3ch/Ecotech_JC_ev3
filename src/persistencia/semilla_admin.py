
from getpass import getpass

from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import registrar_usuario

CORREO_ADMIN = "admin.sistema@ecotech.example"


def preparar_admin(leer_clave=getpass):
    cuenta = UsuarioDAO.buscar_por_nombre("admin")
    if cuenta is not None:
        print("La cuenta admin ya existe. Se conserva su ID y contraseña.")
        return cuenta.id

    empleado = next((e for e in EmpleadoDAO.listar()
                    if e._correo.casefold() == CORREO_ADMIN), None)
    if empleado is None:
        empleado = Empleado(
            "Administrador EcoTech", "Oficina Central", "+56912345678",
            CORREO_ADMIN, "2026-01-01", 0, "Administración del sistema",
        )
        EmpleadoDAO.insertar(empleado)
        print("Empleado administrativo de prueba creado.")
    if UsuarioDAO.buscar_por_empleado(empleado._id) is not None:
        raise ValueError("El empleado administrativo ya tiene otra cuenta.")

    from dominio.usuario import Usuario
    while True:
        clave = leer_clave("Cree una contraseña para admin: ")
        try:
            Usuario.validar_clave(clave)
            from servicios.autenticacion import MAX_BYTES_BCRYPT
            if len(clave.encode("utf-8")) > MAX_BYTES_BCRYPT:
                raise ValueError("Máximo 72 bytes UTF-8.")
        except (TypeError, ValueError) as error:
            print(f"{error} Intente nuevamente.")
            continue
        if leer_clave("Confirme contraseña admin: ") == clave:
            break
        print("Las contraseñas no coinciden. Intente nuevamente.")

    id_cuenta = registrar_usuario(empleado._id, "admin", clave)
    print("Cuenta admin creada. Guarde su contraseña en un lugar seguro.")
    return id_cuenta
