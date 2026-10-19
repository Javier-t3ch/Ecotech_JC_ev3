from datetime import date
from complementos.complementos import limpiar_pantalla
from dominio.registroTiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from menus.menu_empleado import main_empleado


def menu_dominio_empleado():
    while True:
        print("\n===== DOMINIO EMPLEADO =====")
        print("1. Mostrar datos de un empleado")
        print("2. Ver salario de un empleado")
        print("3. Registrar horas de trabajo")
        print("4. Ver registros de horas de un empleado")
        print("5. Gestionar empleados (CRUD)")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ")

        if opcion == "0":
            
            limpiar_pantalla()
            return

        elif opcion == "5":
            limpiar_pantalla()
            main_empleado()

        elif opcion in ("1", "2", "3", "4"):
            try:
                limpiar_pantalla()
                id_empleado = int(input("ID del empleado: "))
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)

                if empleado is None:
                    print("Empleado no encontrado.")
                    input("Presione Enter para continuar...")
                    limpiar_pantalla()
                    continue

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
                    id_proyecto = int(input("ID del proyecto: "))
                    proyecto = ProyectoDao.buscar_por_id(id_proyecto)

                    if proyecto is None:
                        print("Proyecto no encontrado.")
                        input("Presione Enter para continuar...")
                        limpiar_pantalla()
                        continue

                    if not RegistroTiempoDAO.empleado_asignado(empleado._id, proyecto._id_proyecto):
                        print("El empleado no esta asignado a ese proyecto.")
                        input("Presione Enter para continuar...")
                        limpiar_pantalla()
                        continue

                    horas = int(input("Horas trabajadas: "))
                    if horas <= 0:
                        print("Las horas deben ser mayores que cero.")
                        input("Presione Enter para continuar...")
                        limpiar_pantalla()
                        continue

                    fecha = date.fromisoformat(
                        input("Fecha trabajada (AAAA-MM-DD): ").strip()
                    )
                    descripcion = input("Descripcion de la tarea: ").strip()
                    if descripcion == "":
                        print("La descripcion no puede quedar vacia.")
                        input("Presione Enter para continuar...")
                        limpiar_pantalla()
                        continue

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
                        print("No se pudieron guardar las horas.")
                        input("Presione Enter para continuar...")
                        limpiar_pantalla()

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
                print("Datos incorrectos:", error)
                input("Presione Enter para continuar...")
                limpiar_pantalla()
            except Exception as error:
                print("Ocurrio un error:", error)
                input("Presione Enter para continuar...")
                limpiar_pantalla()

        else:
            print("Opcion no valida.")
            input("Presione Enter para continuar...")
            limpiar_pantalla()
