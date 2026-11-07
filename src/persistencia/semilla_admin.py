
from complementos.entrada_segura import leer_con_asteriscos

from dominio.empleado import Empleado
from dominio.cargo import CARGO_RECURSOS_HUMANOS
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import crear_hash
from dominio.usuario import Usuario

CORREO_ADMIN = "admin.sistema@ecotech.example"


def preparar_admin(leer_clave=leer_con_asteriscos):
    cuenta = UsuarioDAO.buscar_por_nombre("admin")
    if cuenta is not None:
        empleado_admin = EmpleadoDAO.buscar_por_id(cuenta.empleado_id)
        if empleado_admin is None or empleado_admin._correo.casefold() != CORREO_ADMIN:
            raise ValueError("La cuenta admin no pertenece al empleado inicial esperado.")
        if cuenta.rol != "admin":
            UsuarioDAO.asignar_rol(cuenta.id, "admin")
            print("Rol de la cuenta inicial admin actualizado.")
        if empleado_admin._id_cargo != CARGO_RECURSOS_HUMANOS:
            empleado_admin._id_cargo = CARGO_RECURSOS_HUMANOS
            EmpleadoDAO.actualizar(empleado_admin)
            print("Empleado admin inicial asignado a Recursos Humanos.")
        print("La cuenta admin ya existe. Se conservan su ID y hash.")
        return cuenta.id
    empleado = next((e for e in EmpleadoDAO.listar()
                    if e._correo.casefold() == CORREO_ADMIN), None)
    if empleado is None:
        empleado = Empleado(
            "Administrador EcoTech", "Oficina Central", "+56912345678",
            CORREO_ADMIN, "2026-01-01", 0, CARGO_RECURSOS_HUMANOS,
        )
        EmpleadoDAO.insertar(empleado)
        print("Empleado administrativo de prueba creado.")
    if UsuarioDAO.buscar_por_empleado(empleado._id) is not None:
        raise ValueError("El empleado administrativo ya tiene otra cuenta.")
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
    id_cuenta = UsuarioDAO.insertar(
        Usuario("admin", crear_hash(clave), empleado._id, rol="admin")
    )
    print("Cuenta admin creada. Guarde su contraseña en un lugar seguro.")
    return id_cuenta
