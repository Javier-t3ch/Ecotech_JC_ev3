from menus.validaciones import ErrorFormulario, explicar_error, preguntar_reintento, leer_texto, leer_fecha, leer_entero
from complementos.complementos import limpiar_pantalla
from dominio.registroTiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from menus.menu_registroTiempo import main_RegistroTiempo


def menu_dominio_registro_tiempo():
    reintento = None
    while True:
        hubo_error = False
        if reintento is None:
            limpiar_pantalla()
            print("\n===== DOMINIO REGISTRO DE TIEMPO =====")
            print("1. Registrar horas de trabajo")
            print("2. Listar todos los registros")
            print("3. Ver registros de un empleado")
            print("4. Ver registros de un proyecto")
            print("5. Gestionar registros de tiempo (CRUD)")
            print("0. Volver al menu principal")

            opcion = input("Seleccione una opcion: ")
            limpiar_pantalla()

        else:
            opcion = reintento
            reintento = None
            limpiar_pantalla()
        if opcion == "0":
            return
        if opcion == "5":
            main_RegistroTiempo()
            continue

        if opcion == "1":
            try:
                id_empleado = leer_entero("ID del empleado: ")
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    raise ErrorFormulario("Empleado no encontrado.")

                id_proyecto = leer_entero("ID del proyecto: ")
                proyecto = ProyectoDao.buscar_por_id(id_proyecto)
                if proyecto is None:
                    raise ErrorFormulario("Proyecto no encontrado.")

                if not RegistroTiempoDAO.empleado_asignado(empleado._id, proyecto._id_proyecto):
                    raise ErrorFormulario("El empleado no esta asignado a ese proyecto.")

                horas = leer_entero("Horas trabajadas: ")
                if horas <= 0:
                    raise ErrorFormulario("Las horas deben ser mayores que cero.")

                fecha = leer_fecha("Fecha trabajada (AAAA-MM-DD): ")
                descripcion = leer_texto("Descripcion de la tarea: ", campo="La descripcion", maximo=500)
                if descripcion == "":
                    raise ErrorFormulario("La descripcion no puede quedar vacia.")

                registro = RegistroTiempo(
                    horas_trabajadas=horas,
                    fecha_trabajada=fecha,
                    descripcion_tarea=descripcion,
                    empleado=empleado,
                    proyecto=proyecto
                )

                if RegistroTiempoDAO.insertar(registro):
                    print("Registro guardado con ID:", registro._id_registro)
                else:
                    raise ErrorFormulario("No se pudo guardar el registro.")

            except ValueError as error:
                explicar_error(error, 'procesar la operacion de registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'procesar la operacion de registro de tiempo')
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
                        print(
                            "ID:", r._id_registro,
                            "| Empleado:", r._empleado._nombre,
                            "| Proyecto:", r._proyecto._nombre,
                            "| Fecha:", r._fecha_trabajada,
                            "| Horas:", r._horas_trabajadas,
                            "| Tarea:", r._descripcion_tarea
                        )
            except Exception as error:
                explicar_error(error, 'procesar la operacion de registro de tiempo')

        elif opcion == "3":
            try:
                id_empleado = leer_entero("ID del empleado: ")
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    raise ErrorFormulario("Empleado no encontrado.")

                registros = RegistroTiempoDAO.listar()
                encontrados = False
                registros_empleado = []

                for r in registros:
                    if r._empleado._id == empleado._id:
                        encontrados = True
                        registros_empleado.append(r)
                        print(
                            "ID:", r._id_registro,
                            "| Proyecto:", r._proyecto._nombre,
                            "| Fecha:", r._fecha_trabajada,
                            "| Horas:", r._horas_trabajadas,
                            "| Tarea:", r._descripcion_tarea
                        )

                if encontrados:
                    total_horas = registros_empleado[0].calculo_horas(registros)
                    print("Total de horas:", total_horas)
                else:
                    print("Este empleado no tiene registros.")

            except ValueError as error:
                explicar_error(error, 'procesar la operacion de registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'procesar la operacion de registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        elif opcion == "4":
            try:
                id_proyecto = leer_entero("ID del proyecto: ")
                proyecto = ProyectoDao.buscar_por_id(id_proyecto)
                if proyecto is None:
                    raise ErrorFormulario("Proyecto no encontrado.")

                registros = RegistroTiempoDAO.listar()
                encontrados = False
                empleados_contados = []
                total_horas = 0

                for r in registros:
                    if r._proyecto._id_proyecto == proyecto._id_proyecto:
                        encontrados = True
                        if r._empleado._id not in empleados_contados:
                            total_horas += r.calculo_horas_proyecto(registros, proyecto)
                            empleados_contados.append(r._empleado._id)
                        print(
                            "ID:", r._id_registro,
                            "| Empleado:", r._empleado._nombre,
                            "| Fecha:", r._fecha_trabajada,
                            "| Horas:", r._horas_trabajadas,
                            "| Tarea:", r._descripcion_tarea
                        )

                if encontrados:
                    print("Total de horas:", total_horas)
                else:
                    print("Este proyecto no tiene registros.")

            except ValueError as error:
                explicar_error(error, 'procesar la operacion de registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'procesar la operacion de registro de tiempo')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        else:
            print("Opcion no valida.")
        if reintento is not None or hubo_error:
            continue
        input("\nPresione Enter para continuar...")
