from menus.validaciones import ErrorFormulario, explicar_error, preguntar_reintento, leer_texto, leer_fecha, leer_entero
from complementos.complementos import limpiar_pantalla
from dominio.registroTiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from menus.menu_empleado import main_empleado


def menu_dominio_empleado():
    reintento = None
    while True:
        hubo_error = False
        if reintento is None:
            print("\n===== DOMINIO EMPLEADO =====")
            print("1. Mostrar datos de un empleado")
            print("2. Ver salario de un empleado")
            print("3. Registrar horas de trabajo")
            print("4. Ver registros de horas de un empleado")
            print("5. Gestionar empleados (CRUD)")
            print("0. Volver al menu principal")

            opcion = input("Seleccione una opcion: ")

        else:
            opcion = reintento
            reintento = None
            limpiar_pantalla()
        if opcion == "0":
            
            limpiar_pantalla()
            return

        elif opcion == "5":
            limpiar_pantalla()
            main_empleado()

        elif opcion in ("1", "2", "3", "4"):
            try:
                limpiar_pantalla()
                id_empleado = leer_entero("ID del empleado: ")
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)

                if empleado is None:
                    raise ErrorFormulario("Empleado no encontrado.")

                if opcion == "1":
                    print(empleado.mostrar_datos())
                    print("Telefono:", empleado._numero)
                    print("Fecha de contrato:", empleado._fecha_contrato)
                    input("Presione Enter para continuar...")
                    limpiar_pantalla()

                elif opcion == "2":
                    print("Salario:", empleado.ver_salario())
                    input("Presione Enter para continuar...")
                    limpiar_pantalla()

                elif opcion == "3":
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
                    empleado.registrar_horas(registro)

                    guardado = RegistroTiempoDAO.insertar(registro)
                    if guardado:
                        print("Horas registradas correctamente.")
                        print("ID del registro:", registro._id_registro)
                        input("Presione Enter para continuar...")
                        limpiar_pantalla()
                    else:
                        raise ErrorFormulario("No se pudieron guardar las horas. Revisa la asignacion al proyecto.")

                elif opcion == "4":
                    registros = RegistroTiempoDAO.listar()
                    encontrados = False
                    total_horas = 0

                    for registro in registros:
                        if registro._empleado._id == empleado._id:
                            encontrados = True
                            total_horas += registro._horas_trabajadas
                            print(
                                "Registro:", registro._id_registro,
                                "| Fecha:", registro._fecha_trabajada,
                                "| Horas:", registro._horas_trabajadas,
                                "| Proyecto:", registro._proyecto._nombre,
                                "| Tarea:", registro._descripcion_tarea
                            )


                    if encontrados:
                        print("Total de horas registradas:", total_horas)
                        input("Presione Enter para continuar...")
                        limpiar_pantalla()
                    else:
                        print("Este empleado no tiene horas registradas.")
                        input("Presione Enter para continuar...")
                        limpiar_pantalla()

            except ValueError as error:
                explicar_error(error, 'procesar la operacion de empleado')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion
            except Exception as error:
                explicar_error(error, 'procesar la operacion de empleado')
                hubo_error = True
                if preguntar_reintento():
                    reintento = opcion

        else:
            print("Opcion no valida.")
            input("Presione Enter para continuar...")
            limpiar_pantalla()
