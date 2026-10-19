from complementos.complementos import limpiar_pantalla
from datetime import date
from dominio.registroTiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from menus.menu_registroTiempo import main_RegistroTiempo


def menu_dominio_registro_tiempo():
    while True:
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

        if opcion == "0":
            return
        if opcion == "5":
            main_RegistroTiempo()
            continue

        if opcion == "1":
            try:
                id_empleado = int(input("ID del empleado: "))
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                id_proyecto = int(input("ID del proyecto: "))
                proyecto = ProyectoDao.buscar_por_id(id_proyecto)
                if proyecto is None:
                    print("Proyecto no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                if not RegistroTiempoDAO.empleado_asignado(empleado._id, proyecto._id_proyecto):
                    print("El empleado no esta asignado a ese proyecto.")
                    input("\nPresione Enter para continuar...")
                    continue

                horas = int(input("Horas trabajadas: "))
                if horas <= 0:
                    print("Las horas deben ser mayores que cero.")
                    input("\nPresione Enter para continuar...")
                    continue

                fecha = date.fromisoformat(
                    input("Fecha trabajada (AAAA-MM-DD): ").strip()
                )
                descripcion = input("Descripcion de la tarea: ").strip()
                if descripcion == "":
                    print("La descripcion no puede quedar vacia.")
                    input("\nPresione Enter para continuar...")
                    continue

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
                    print("No se pudo guardar el registro.")

            except ValueError as error:
                print("Datos incorrectos:", error)
            except Exception as error:
                print("Ocurrio un error:", error)

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
                print("Error al listar registros:", error)

        elif opcion == "3":
            try:
                id_empleado = int(input("ID del empleado: "))
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

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
                print("Datos incorrectos:", error)
            except Exception as error:
                print("Ocurrio un error:", error)

        elif opcion == "4":
            try:
                id_proyecto = int(input("ID del proyecto: "))
                proyecto = ProyectoDao.buscar_por_id(id_proyecto)
                if proyecto is None:
                    print("Proyecto no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

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
                print("Datos incorrectos:", error)
            except Exception as error:
                print("Ocurrio un error:", error)

        else:
            print("Opcion no valida.")
        input("\nPresione Enter para continuar...")
