from dominio.empleado import Empleado
from validaciones import validar_texto
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from persistencia.proyecto_dao import ProyectoDao
from persistencia.departamento_dao import DepartamentoDAO
from servicios.autorizacion import exigir_sesion


def mi_ficha(sesion):
    cuenta = exigir_sesion(sesion)
    return EmpleadoDAO.buscar_por_id(cuenta.empleado_id)


def mis_registros(sesion):
    cuenta = exigir_sesion(sesion)
    return RegistroTiempoDAO.listar_por_empleado(cuenta.empleado_id)


def mis_proyectos(sesion):
    cuenta = exigir_sesion(sesion)
    return ProyectoDao.listar_por_empleado(cuenta.empleado_id)


def mis_departamentos(sesion):
    cuenta = exigir_sesion(sesion)
    return DepartamentoDAO.listar_por_empleado(cuenta.empleado_id)


def actualizar_mis_datos(sesion, nombre, correo):
    cuenta = exigir_sesion(sesion)
    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)
    if EmpleadoDAO.buscar_por_id(cuenta.empleado_id) is None:
        raise ValueError("Empleado no encontrado.")
    if EmpleadoDAO.correo_ocupado(correo, cuenta.empleado_id):
        raise ValueError("El correo ya está registrado para otro empleado.")
    return EmpleadoDAO.actualizar_nombre_correo(cuenta.empleado_id, nombre, correo)



def registrar_mis_horas(sesion, proyecto_id, horas, fecha, descripcion):
    from datetime import date, datetime
    from dominio.registroTiempo import RegistroTiempo
    cuenta = exigir_sesion(sesion)
    if type(proyecto_id) is not int or proyecto_id <= 0:
        raise ValueError("Seleccione un proyecto válido.")
    if type(horas) is not int or not 1 <= horas <= 24:
        raise ValueError("Las horas deben estar entre 1 y 24.")
    if isinstance(fecha, str):
        try:
            fecha = date.fromisoformat(fecha)
        except ValueError as error:
            raise ValueError("La fecha trabajada no es válida.") from error
    if isinstance(fecha, datetime) or not isinstance(fecha, date):
        raise ValueError("La fecha trabajada no es válida.")
    descripcion = validar_texto(descripcion, tipo="descripcion", campo="Descripción", maximo=100)
    if not RegistroTiempoDAO.empleado_asignado(cuenta.empleado_id, proyecto_id):
        raise PermissionError("No estás asignado a ese proyecto.")
    empleado = EmpleadoDAO.buscar_por_id(cuenta.empleado_id)
    proyecto = ProyectoDao.buscar_por_id(proyecto_id, cargar_relaciones=False)
    if empleado is None or proyecto is None:
        raise ValueError("El empleado o el proyecto ya no existe.")
    registro = RegistroTiempo(horas, fecha.isoformat(), descripcion.strip(), empleado, proyecto)
    if not RegistroTiempoDAO.insertar(registro):
        raise ValueError("No se pudo guardar el registro de horas.")
    return registro
