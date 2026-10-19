from complementos.complementos import limpiar_pantalla
from datetime import date
from dominio.registroTiempo import RegistroTiempo
from persistencia.proyecto_dao import ProyectoDao
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from menus.menu_proyecto import main_proyecto


def menu_dominio_proyecto():
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO PROYECTO =====")
        print("1. Asignar empleado al proyecto")
        print("2. Desvincular empleado del proyecto")
        print("3. Registrar horas de un empleado asignado")
        print("4. Generar informe del proyecto")
        print("5. Gestionar proyectos (CRUD)")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ")
        limpiar_pantalla()
        if opcion == "0":
            return
        if opcion == "5":
            main_proyecto()
            continue
        if opcion not in ("1", "2", "3", "4"):
            print("Opcion no valida.")
            input("\nPresione Enter para continuar...")
            continue

        try:
            id_proyecto = int(input("ID del proyecto: "))
            proyecto = ProyectoDao.buscar_por_id(id_proyecto)
            if proyecto is None:
                print("Proyecto no encontrado.")
                input("\nPresione Enter para continuar...")
                continue

            if opcion == "4":
                print("\n--- INFORME DEL PROYECTO ---")
                print(proyecto.generar_informe())
                input("\nPresione Enter para continuar...")
                continue

            id_empleado = int(input("ID del empleado: "))
            empleado = EmpleadoDAO.buscar_por_id(id_empleado)
            if empleado is None:
                print("Empleado no encontrado.")
                input("\nPresione Enter para continuar...")
                continue

            empleado_asignado = None
            for actual in proyecto._empleados:
                if actual._id == empleado._id:
                    empleado_asignado = actual
                    break

            if opcion == "1":
                if empleado_asignado is not None:
                    print("El empleado ya esta asignado al proyecto.")
                elif proyecto.asignar_empleado(empleado):
                    if ProyectoDao.asignar_empleado(proyecto, empleado):
                        print("Empleado asignado y guardado.")
                    else:
                        print("No se pudo guardar la asignacion.")

            elif opcion == "2":
                if empleado_asignado is None:
                    print("El empleado no esta asignado a este proyecto.")
                elif proyecto.desvincular_empleado(empleado_asignado):
                    if ProyectoDao.desvincular_empleado(proyecto, empleado_asignado):
                        print("Empleado desvinculado del proyecto.")
                    else:
                        print("No se pudo guardar la desvinculacion.")

            elif opcion == "3":
                if empleado_asignado is None:
                    print("Primero debes asignar al empleado al proyecto.")
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
                if not descripcion:
                    print("La descripcion no puede quedar vacia.")
                    input("\nPresione Enter para continuar...")
                    continue
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
                        print("No se pudo guardar el registro.")
                else:
                    print("No se pudo registrar tiempo en el proyecto.")

        except ValueError as error:
            print("Datos incorrectos:", error)
        except Exception as error:
            print("Ocurrio un error:", error)
        input("\nPresione Enter para continuar...")
