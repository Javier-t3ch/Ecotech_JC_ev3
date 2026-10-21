from menus.validaciones import (
    ErrorFormulario, explicar_error, preguntar_reintento,
    leer_texto, leer_fecha, leer_entero,
    leer_confirmacion
)
from complementos.complementos import limpiar_pantalla
from dominio.registroTiempo import RegistroTiempo
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao


def mostrar_menu_RegistroTiempo():
    print("\n===== REGISTROS DE TIEMPO - ECOTECH =====")
    print("1. Registrar Registro de Tiempo")
    print("2. Listar Registros de Tiempo")
    print("3. Buscar Registro de Tiempo")
    print("4. Actualizar Registro de Tiempo")
    print("5. Eliminar Registro de Tiempo")
    print("0. Volver al menu principal")


def main_RegistroTiempo():
    reintento = None
    while True:
        hubo_error = False
        if reintento is None:
            limpiar_pantalla()
            mostrar_menu_RegistroTiempo()
            opcion = input("Seleccione una opcion: ")
            limpiar_pantalla()

        else:
            opcion = reintento
            reintento = None
            limpiar_pantalla()
        if opcion == "1":
            try:
                empleado_id = leer_entero("ID del empleado: ")
                proyecto_id = leer_entero("ID del proyecto: ")
                empleado = EmpleadoDAO.buscar_por_id(empleado_id)
                proyecto = ProyectoDao.buscar_por_id(proyecto_id)
                if empleado is None or proyecto is None:
                    raise ErrorFormulario("Empleado o proyecto no encontrado.")
                if not RegistroTiempoDAO.empleado_asignado(empleado._id, proyecto._id_proyecto):
                    raise ErrorFormulario("El empleado no esta asignado a ese proyecto.")
                horas = leer_entero("Horas trabajadas: ")
                if horas <= 0:
                    raise ErrorFormulario("Las horas deben ser mayores que cero.")
                fecha = leer_fecha("Fecha trabajada (AAAA-MM-DD): ")
                descripcion = leer_texto("Descripcion de la tarea: ", campo="La descripcion", maximo=500)
                if not descripcion:
                    raise ErrorFormulario("La descripcion no puede quedar vacia.")
                registro = RegistroTiempo(horas, fecha, descripcion, empleado, proyecto)
                if RegistroTiempoDAO.insertar(registro):
                    print("Registro creado con ID:", registro._id_registro)
                else:
                    raise ErrorFormulario("No se pudo guardar el registro.")
            except ValueError as error:
                explicar_error(error, 'registrar registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'registrar registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "2":
            try:
                registros = RegistroTiempoDAO.listar()
                if not registros:
                    print("No hay registros de tiempo.")
                else:
                    for r in registros:
                        print(f"ID: {r._id_registro} | Empleado: {r._empleado._id} | Proyecto: {r._proyecto._id_proyecto} | Horas: {r._horas_trabajadas} | Fecha: {r._fecha_trabajada} | {r._descripcion_tarea}")
            except Exception as error:
                explicar_error(error, 'consultar registro de tiempo')

        elif opcion == "3":
            try:
                id_registro = leer_entero("ID del registro: ")
                r = RegistroTiempoDAO.buscar_por_id(id_registro)
                if r is None:
                    raise ErrorFormulario("Registro no encontrado.")
                else:
                    print(f"ID: {r._id_registro} | Empleado: {r._empleado._id} | Proyecto: {r._proyecto._id_proyecto} | Horas: {r._horas_trabajadas} | Fecha: {r._fecha_trabajada} | {r._descripcion_tarea}")
            except ValueError as error:
                explicar_error(error, 'buscar registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'buscar registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "4":
            try:
                id_registro = leer_entero("ID del registro a actualizar: ")
                r = RegistroTiempoDAO.buscar_por_id(id_registro)
                if r is None:
                    raise ErrorFormulario("Registro no encontrado.")
                print("Deja el campo vacio si no deseas cambiarlo.")
                horas_texto = leer_entero(f"Horas [{r._horas_trabajadas}]: ", obligatorio=False)
                fecha_texto = leer_fecha(f"Fecha [{r._fecha_trabajada}] (AAAA-MM-DD): ", obligatorio=False)
                descripcion = leer_texto(f"Descripcion [{r._descripcion_tarea}]: ", obligatorio=False, campo="La descripcion", maximo=500)
                empleado_texto = leer_entero(f"ID empleado [{r._empleado._id}]: ", obligatorio=False)
                proyecto_texto = leer_entero(f"ID proyecto [{r._proyecto._id_proyecto}]: ", obligatorio=False)

                if not (horas_texto or fecha_texto or descripcion or empleado_texto or proyecto_texto):
                    raise ErrorFormulario("No ingresaste cambios.")
                horas = horas_texto if horas_texto is not None else r._horas_trabajadas
                if horas <= 0:
                    raise ErrorFormulario("Las horas deben ser mayores que cero.")
                fecha = fecha_texto if fecha_texto is not None else r._fecha_trabajada
                id_empleado = empleado_texto if empleado_texto is not None else r._empleado._id
                id_proyecto = proyecto_texto if proyecto_texto is not None else r._proyecto._id_proyecto
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                proyecto = ProyectoDao.buscar_por_id(id_proyecto)
                if empleado is None or proyecto is None:
                    raise ErrorFormulario("El empleado o proyecto seleccionado no existe.")
                if not RegistroTiempoDAO.empleado_asignado(empleado._id, proyecto._id_proyecto):
                    raise ErrorFormulario("El empleado no esta asignado a ese proyecto.")
                actualizado = RegistroTiempo(
                    horas_trabajadas=horas,
                    fecha_trabajada=fecha,
                    descripcion_tarea=descripcion or r._descripcion_tarea,
                    empleado=empleado,
                    proyecto=proyecto,
                    id_registro=r._id_registro
                )
                if RegistroTiempoDAO.actualizar(actualizado):
                    print("Registro actualizado.")
                else:
                    raise ErrorFormulario("No se detectaron cambios guardados.")
            except ValueError as error:
                explicar_error(error, 'actualizar registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'actualizar registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "5":
            try:
                id_registro = leer_entero("ID del registro a eliminar: ")
                r = RegistroTiempoDAO.buscar_por_id(id_registro)
                if r is None:
                    raise ErrorFormulario("Registro no encontrado.")
                confirmar = leer_confirmacion(f"Eliminar registro {r._id_registro}? (s/n): ")
                if confirmar == "s":
                    if RegistroTiempoDAO.eliminar(id_registro):
                        print("Registro eliminado.")
                    else:
                        raise ErrorFormulario("No se pudo eliminar el registro.")
                else:
                    print("Eliminacion cancelada.")
            except ValueError as error:
                explicar_error(error, 'eliminar registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'eliminar registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "0":
            return
        else:
            print("Opcion no valida.")
        if reintento is not None or hubo_error:
            continue
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main_RegistroTiempo()
