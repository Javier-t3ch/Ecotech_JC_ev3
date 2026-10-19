from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDao
from menus.menu_departamento import main_departamento
from complementos.complementos import limpiar_pantalla


def menu_dominio_departamento():
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO DEPARTAMENTO =====")
        print("1. Contratar empleado (autorizado por RRHH)")
        print("2. Agregar empleado al departamento")
        print("3. Quitar empleado del departamento")
        print("4. Vincular proyecto existente al departamento")
        print("5. Editar nombre de un proyecto del departamento")
        print("6. Desvincular proyecto del departamento")
        print("7. Gestionar departamentos (CRUD)")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ")
        limpiar_pantalla()
        if opcion == "0":
            return
        if opcion == "7":
            main_departamento()
            continue
        if opcion not in ("1", "2", "3", "4", "5", "6"):
            print("Opcion no valida.")
            input("\nPresione Enter para continuar...")
            continue

        try:
            id_departamento = int(input("ID del departamento: "))
            departamento = DepartamentoDAO.buscar_por_id(id_departamento)
            if departamento is None:
                print("Departamento no encontrado.")
                input("\nPresione Enter para continuar...")
                continue

            if opcion in ("1", "2", "3"):
                id_empleado = int(input("ID del empleado: "))
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue


                empleado_asociado = None
                for actual in departamento._empleados:
                    if actual._id == empleado._id:
                        empleado_asociado = actual
                        break

                if opcion == "1":
                    if empleado_asociado is not None:
                        print("El empleado ya pertenece al departamento.")
                        input("\nPresione Enter para continuar...")
                        continue
                    id_encargado = int(input("ID del encargado de RRHH: "))
                    encargado = EmpleadoDAO.buscar_por_id(id_encargado)
                    if encargado is None:
                        print("Encargado no encontrado.")
                        input("\nPresione Enter para continuar...")
                        continue
                    if departamento.contratar_empleado(empleado, encargado):
                        if DepartamentoDAO.agregar_empleado(departamento, empleado):
                            print("Empleado contratado y guardado en la base de datos.")
                        else:
                            print("No se pudo guardar la contratacion.")
                    else:
                        print("No autorizado: el encargado debe tener cargo Recursos Humanos.")

                elif opcion == "2":
                    if empleado_asociado is not None:
                        print("El empleado ya pertenece al departamento.")
                    elif departamento.agregar_empleado(empleado):
                        if DepartamentoDAO.agregar_empleado(departamento, empleado):
                            print("Empleado agregado y guardado.")
                        else:
                            print("No se pudo guardar la asociacion.")
                    else:
                        print("No se pudo agregar al empleado.")

                elif opcion == "3":
                    if empleado_asociado is None:
                        print("El empleado no pertenece al departamento.")
                    else:
                        departamento.eliminar_empleado(empleado_asociado)
                        if DepartamentoDAO.quitar_empleado(departamento, empleado):
                            print("Empleado desvinculado del departamento.")
                        else:
                            print("No se pudo quitar la asociacion de la base de datos.")

            elif opcion in ("4", "5", "6"):
                id_proyecto = int(input("ID del proyecto: "))
                proyecto = ProyectoDao.buscar_por_id(id_proyecto)
                if proyecto is None:
                    print("Proyecto no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue

                proyecto_asociado = None
                for actual in departamento._proyectos:
                    if actual._id_proyecto == proyecto._id_proyecto:
                        proyecto_asociado = actual
                        break

                if opcion == "4":
                    if proyecto_asociado is not None:
                        print("El proyecto ya pertenece al departamento.")
                    elif departamento.crear_proyecto(proyecto):
                        if DepartamentoDAO.agregar_proyecto(departamento, proyecto):
                            print("Proyecto vinculado y guardado.")
                        else:
                            print("No se pudo guardar la asociacion.")
                    else:
                        print("No se pudo vincular el proyecto.")

                elif opcion == "5":
                    if proyecto_asociado is None:
                        print("El proyecto no pertenece al departamento.")
                        input("\nPresione Enter para continuar...")
                        continue
                    nuevo_nombre = input("Nuevo nombre del proyecto: ").strip()
                    if departamento.editar_proyecto(proyecto_asociado, nuevo_nombre):
                        if ProyectoDao.actualizar(proyecto_asociado):
                            print("Nombre del proyecto actualizado en la base de datos.")
                        else:
                            print("No se pudo actualizar el proyecto.")
                    else:
                        print("No se pudo editar: ingrese un nombre valido.")

                elif opcion == "6":
                    if proyecto_asociado is None:
                        print("El proyecto no pertenece al departamento.")
                    elif departamento.eliminar_proyecto(proyecto_asociado):
                        if DepartamentoDAO.quitar_proyecto(departamento, proyecto_asociado):
                            print("Proyecto desvinculado del departamento.")
                        else:
                            print("No se pudo quitar la asociacion de la base de datos.")
                    else:
                        print("No se pudo desvincular el proyecto.")

        except ValueError as error:
            print("Datos incorrectos:", error)
        except Exception as error:
            print("Ocurrio un error:", error)
        input("\nPresione Enter para continuar...")
