from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from servicios.autorizacion import exigir_admin, puede_contratar, exigir_recursos_humanos


def listar_todos(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar()


def buscar_empleado(empleado_id, sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_id(empleado_id)


def registrar_empleado(empleado, sesion, departamento_id):
    exigir_recursos_humanos(sesion)
    return EmpleadoDAO.insertar_con_departamento(empleado, departamento_id)


def asignar_empleado_a_departamento(empleado_id, departamento_id, sesion):
    exigir_recursos_humanos(sesion)
    empleado = EmpleadoDAO.buscar_por_id(empleado_id)
    departamento = DepartamentoDAO.buscar_por_id(departamento_id)
    if empleado is None or departamento is None:
        raise ValueError("El empleado o departamento seleccionado no existe.")
    if any(e._id == empleado_id for e in departamento._empleados):
        raise ValueError("El empleado ya pertenece a ese departamento.")
    return DepartamentoDAO.agregar_empleado(departamento, empleado)


def actualizar_empleado(empleado, sesion):
    exigir_admin(sesion)
    actual = EmpleadoDAO.buscar_por_id(empleado._id)
    if actual is None:
        raise ValueError("Empleado no encontrado.")
    if empleado._id_cargo != actual._id_cargo and not puede_contratar(sesion):
        raise PermissionError("Solo Recursos Humanos puede cambiar el cargo.")
    return EmpleadoDAO.actualizar(empleado)


def eliminar_empleado(empleado_id, sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.eliminar(empleado_id)
