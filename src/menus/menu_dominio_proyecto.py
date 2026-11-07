from validaciones import FormularioCancelado, avisar_cancelacion, aviso_cancelacion, leer_id_existente, leer_entrada, leer_secreto
from validaciones import ErrorFormulario, explicar_error, preguntar_reintento, leer_texto, leer_fecha, leer_entero
from complementos.complementos import limpiar_pantalla, pausar_y_limpiar
from dominio.registroTiempo import RegistroTiempo
from persistencia.proyecto_dao import ProyectoDao
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from menus.menu_proyecto import main_proyecto


def menu_dominio_proyecto(usuario_actual=None):
    from servicios.autorizacion import exigir_admin
    try:
        exigir_admin(usuario_actual)
    except PermissionError as error:
        print(error)
        return
    reintento = None
    while True:
        hubo_error = False
        if reintento is None:
            limpiar_pantalla()
            print("\n===== DOMINIO PROYECTO =====")
            print("1. Asignar empleado al proyecto")
            print("2. Desvincular empleado del proyecto")
            print("3. Registrar horas de un empleado asignado")
            print("4. Generar informe del proyecto")
            print("5. Gestionar proyectos (CRUD)")
            print("0. Volver al menu principal")

            aviso_cancelacion()
            opcion = input("Seleccione una opción: ").strip()
            limpiar_pantalla()
        else:
            opcion = reintento
            reintento = None
            limpiar_pantalla()
        if opcion == "0":
            return
        if opcion == "5":
            main_proyecto(usuario_actual)
            continue
        if opcion not in ("1", "2", "3", "4"):
            print("Opcion no valida.")
            pausar_y_limpiar()
            continue

        try:
            id_proyecto = leer_id_existente("ID del proyecto: ", ProyectoDao.buscar_por_id, etiqueta="El proyecto", listar=ProyectoDao.listar)
            proyecto = ProyectoDao.buscar_por_id(id_proyecto)
            if proyecto is None:
                raise ErrorFormulario("Proyecto no encontrado.")

            if opcion == "4":
                print("\n--- INFORME DEL PROYECTO ---")
                print(proyecto.generar_informe())
                pausar_y_limpiar()
                continue

            id_empleado = leer_id_existente(
                "ID del empleado: ", EmpleadoDAO.buscar_por_id, etiqueta="El empleado",
                condicion=lambda e: (
                    (opcion == "1" and all(a._id != e._id for a in proyecto._empleados))
                    or (opcion in ("2", "3") and any(a._id == e._id for a in proyecto._empleados))
                ),
                mensaje_condicion=("Ya asignado: seleccione otro empleado." if opcion == "1"
                                else "El empleado no está asignado a este proyecto."),
                listar=EmpleadoDAO.listar)
            empleado = EmpleadoDAO.buscar_por_id(id_empleado)
            if empleado is None:
                raise ErrorFormulario("Empleado no encontrado.")

            empleado_asignado = None
            for actual in proyecto._empleados:
                if actual._id == empleado._id:
                    empleado_asignado = actual
                    break

            if opcion == "1":
                if empleado_asignado is not None:
                    raise ErrorFormulario("El empleado ya esta asignado al proyecto.")
                elif proyecto.asignar_empleado(empleado):
                    if ProyectoDao.asignar_empleado(proyecto, empleado):
                        print("Empleado asignado y guardado.")
                    else:
                        raise ErrorFormulario("No se pudo guardar la asignacion.")
                else:
                    raise ErrorFormulario("No se pudo asignar al empleado al proyecto.")

            elif opcion == "2":
                if empleado_asignado is None:
                    raise ErrorFormulario("El empleado no esta asignado a este proyecto.")
                elif proyecto.desvincular_empleado(empleado_asignado):
                    if ProyectoDao.desvincular_empleado(proyecto, empleado_asignado):
                        print("Empleado desvinculado del proyecto.")
                    else:
                        raise ErrorFormulario("No se pudo guardar la desvinculacion.")
                else:
                    raise ErrorFormulario("No se pudo desvincular al empleado del proyecto.")

            elif opcion == "3":
                if empleado_asignado is None:
                    raise ErrorFormulario("Primero debes asignar al empleado al proyecto.")
                horas = leer_entero("Horas trabajadas: ", maximo=24)
                if horas <= 0:
                    raise ErrorFormulario("Las horas deben ser mayores que cero.")
                fecha = leer_fecha("Fecha trabajada (AAAA-MM-DD): ")
                descripcion = leer_texto("Descripcion de la tarea: ", campo="La descripcion", maximo=100)
                if not descripcion:
                    raise ErrorFormulario("La descripcion no puede quedar vacia.")
                registro = RegistroTiempo(
                    horas_trabajadas=horas,
                    fecha_trabajada=fecha,
                    descripcion_tarea=descripcion,
                    empleado=empleado_asignado,
                    proyecto=proyecto
                )
                if proyecto.agregar_registro_tiempo(registro):
                    if RegistroTiempoDAO.insertar(registro):
                        print("Horas guardadas con ID:", registro._id_registro)
                    else:
                        raise ErrorFormulario("No se pudo guardar el registro.")
                else:
                    raise ErrorFormulario("No se pudo registrar tiempo en el proyecto.")

        except FormularioCancelado:
            avisar_cancelacion()
        except ValueError as error:
            explicar_error(error, 'procesar la operacion de proyecto')
            hubo_error = True
            if preguntar_reintento():
                reintento = opcion
        except Exception as error:
            explicar_error(error, 'procesar la operacion de proyecto')
            hubo_error = True
            if preguntar_reintento():
                reintento = opcion
        if reintento is not None:
            continue
        pausar_y_limpiar()
