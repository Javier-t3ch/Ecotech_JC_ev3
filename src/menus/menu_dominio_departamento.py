from validaciones import FormularioCancelado, avisar_cancelacion, aviso_cancelacion, leer_id_existente, leer_entrada, leer_secreto
from validaciones import ErrorFormulario, explicar_error, preguntar_reintento, leer_texto, leer_entero
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao
from menus.menu_departamento import main_departamento
from menus.menu_empleado import contratar_y_asignar_empleado, asignar_empleado_existente
from complementos.complementos import limpiar_pantalla, pausar_y_limpiar


def menu_dominio_departamento(usuario_actual=None):
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
            print("\n===== DOMINIO DEPARTAMENTO =====")
            print("1. Contratar nuevo empleado y asignarlo (RRHH)")
            print("2. Agregar empleado al departamento")
            print("3. Quitar empleado del departamento")
            print("4. Vincular proyecto existente al departamento")
            print("5. Editar nombre de un proyecto del departamento")
            print("6. Desvincular proyecto del departamento")
            print("7. Gestionar departamentos (CRUD)")
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
        if opcion == "7":
            main_departamento(usuario_actual)
            continue
        if opcion == "1":
            contratar_y_asignar_empleado(usuario_actual)
            pausar_y_limpiar()
            continue
        if opcion == "2":
            asignar_empleado_existente(usuario_actual)
            pausar_y_limpiar()
            continue
        if opcion not in ("3", "4", "5", "6"):
            print("Opcion no valida.")
            pausar_y_limpiar()
            continue

        try:
            id_departamento = leer_id_existente(
                "ID del departamento: ", DepartamentoDAO.buscar_por_id,
                etiqueta="El departamento", listar=DepartamentoDAO.listar)
            departamento = DepartamentoDAO.buscar_por_id(id_departamento)
            if departamento is None:
                raise ErrorFormulario("Departamento no encontrado.")

            if opcion == "3":
                id_empleado = leer_id_existente(
                    "ID del empleado: ", EmpleadoDAO.buscar_por_id,
                    etiqueta="El empleado",
                    condicion=lambda e: any(a._id == e._id for a in departamento._empleados),
                    mensaje_condicion="El empleado no pertenece al departamento.",
                    listar=EmpleadoDAO.listar)
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if DepartamentoDAO.quitar_empleado(departamento, empleado):
                    print("Empleado desvinculado del departamento.")
                else:
                    raise ErrorFormulario("No se pudo desvincular al empleado.")

            elif opcion in ("4", "5", "6"):
                id_proyecto = leer_id_existente(
                    "ID del proyecto: ", ProyectoDao.buscar_por_id, etiqueta="El proyecto",
                    condicion=lambda p: (
                        all(a._id_proyecto != p._id_proyecto for a in departamento._proyectos) if opcion == "4"
                        else any(a._id_proyecto == p._id_proyecto for a in departamento._proyectos)
                    ),
                    mensaje_condicion=("El proyecto ya pertenece al departamento." if opcion == "4"
                                       else "El proyecto no pertenece al departamento."),
                    listar=ProyectoDao.listar)
                proyecto = ProyectoDao.buscar_por_id(id_proyecto)
                if proyecto is None:
                    raise ErrorFormulario("Proyecto no encontrado.")

                proyecto_asociado = None
                for actual in departamento._proyectos:
                    if actual._id_proyecto == proyecto._id_proyecto:
                        proyecto_asociado = actual
                        break

                if opcion == "4":
                    if proyecto_asociado is not None:
                        raise ErrorFormulario("El proyecto ya pertenece al departamento.")
                    elif departamento.crear_proyecto(proyecto):
                        if DepartamentoDAO.agregar_proyecto(departamento, proyecto):
                            print("Proyecto vinculado y guardado.")
                        else:
                            raise ErrorFormulario("No se pudo guardar la asociacion.")
                    else:
                        raise ErrorFormulario("No se pudo vincular el proyecto.")

                elif opcion == "5":
                    if proyecto_asociado is None:
                        raise ErrorFormulario("El proyecto no pertenece al departamento.")
                    nuevo_nombre = leer_texto("Nuevo nombre del proyecto: ", campo="Nombre", maximo=50, tipo="proyecto")
                    if departamento.editar_proyecto(proyecto_asociado, nuevo_nombre):
                        if ProyectoDao.actualizar(proyecto_asociado):
                            print("Nombre del proyecto actualizado en la base de datos.")
                        else:
                            raise ErrorFormulario("No se pudo actualizar el proyecto.")
                    else:
                        raise ErrorFormulario("No se pudo editar: ingrese un nombre valido.")

                elif opcion == "6":
                    if proyecto_asociado is None:
                        raise ErrorFormulario("El proyecto no pertenece al departamento.")
                    elif departamento.eliminar_proyecto(proyecto_asociado):
                        if DepartamentoDAO.quitar_proyecto(departamento, proyecto_asociado):
                            print("Proyecto desvinculado del departamento.")
                        else:
                            raise ErrorFormulario("No se pudo quitar la asociacion de la base de datos.")
                    else:
                        raise ErrorFormulario("No se pudo desvincular el proyecto.")

        except FormularioCancelado:
            avisar_cancelacion()
        except ValueError as error:
            explicar_error(error, 'procesar la operacion de departamento')
            hubo_error = True
            if preguntar_reintento():
                reintento = opcion
        except Exception as error:
            explicar_error(error, 'procesar la operacion de departamento')
            hubo_error = True
            if preguntar_reintento():
                reintento = opcion
        if reintento is not None:
            continue
        pausar_y_limpiar()