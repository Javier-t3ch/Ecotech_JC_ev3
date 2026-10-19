from complementos.complementos import limpiar_pantalla
from datetime import date
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
    while True:
        limpiar_pantalla()
        mostrar_menu_RegistroTiempo()
        opcion = input("Seleccione una opcion: ")
        limpiar_pantalla()

        if opcion == "1":
            try:
                empleado_id = int(input("ID del empleado: "))
                proyecto_id = int(input("ID del proyecto: "))
                empleado = EmpleadoDAO.buscar_por_id(empleado_id)
                proyecto = ProyectoDao.buscar_por_id(proyecto_id)
                if empleado is None or proyecto is None:
                    print("Empleado o proyecto no encontrado.")
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
                fecha = date.fromisoformat(input("Fecha trabajada (AAAA-MM-DD): ").strip())
                descripcion = input("Descripcion de la tarea: ").strip()
                if not descripcion:
                    print("La descripcion no puede quedar vacia.")
                    input("\nPresione Enter para continuar...")
                    continue
                registro = RegistroTiempo(horas, fecha, descripcion, empleado, proyecto)
                if RegistroTiempoDAO.insertar(registro):
                    print("Registro creado con ID:", registro._id_registro)
                else:
                    print("No se pudo guardar el registro.")
            except ValueError:
                print("ID, horas o fecha incorrectos.")
            except Exception as error:
                print("Error al registrar tiempo:", error)

        elif opcion == "2":
            try:
                registros = RegistroTiempoDAO.listar()
                if not registros:
                    print("No hay registros de tiempo.")
                else:
                    for r in registros:
                        print(f"ID: {r._id_registro} | Empleado: {r._empleado._id} | Proyecto: {r._proyecto._id_proyecto} | Horas: {r._horas_trabajadas} | Fecha: {r._fecha_trabajada} | {r._descripcion_tarea}")
            except Exception as error:
                print("Error al listar registros:", error)

        elif opcion == "3":
            try:
                id_registro = int(input("ID del registro: "))
                r = RegistroTiempoDAO.buscar_por_id(id_registro)
                if r is None:
                    print("Registro no encontrado.")
                else:
                    print(f"ID: {r._id_registro} | Empleado: {r._empleado._id} | Proyecto: {r._proyecto._id_proyecto} | Horas: {r._horas_trabajadas} | Fecha: {r._fecha_trabajada} | {r._descripcion_tarea}")
            except ValueError:
                print("Debes ingresar un ID numerico.")
            except Exception as error:
                print("Error al buscar registro:", error)

        elif opcion == "4":
            try:
                id_registro = int(input("ID del registro a actualizar: "))
                r = RegistroTiempoDAO.buscar_por_id(id_registro)
                if r is None:
                    print("Registro no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue
                print("Deja el campo vacio si no deseas cambiarlo.")
                horas_texto = input(f"Horas [{r._horas_trabajadas}]: ").strip()
                fecha_texto = input(f"Fecha [{r._fecha_trabajada}] (AAAA-MM-DD): ").strip()
                descripcion = input(f"Descripcion [{r._descripcion_tarea}]: ").strip()
                empleado_texto = input(f"ID empleado [{r._empleado._id}]: ").strip()
                proyecto_texto = input(f"ID proyecto [{r._proyecto._id_proyecto}]: ").strip()

                if not (horas_texto or fecha_texto or descripcion or empleado_texto or proyecto_texto):
                    print("No ingresaste cambios.")
                    input("\nPresione Enter para continuar...")
                    continue
                horas = int(horas_texto) if horas_texto else r._horas_trabajadas
                if horas <= 0:
                    print("Las horas deben ser mayores que cero.")
                    input("\nPresione Enter para continuar...")
                    continue
                fecha = date.fromisoformat(fecha_texto) if fecha_texto else r._fecha_trabajada
                id_empleado = int(empleado_texto) if empleado_texto else r._empleado._id
                id_proyecto = int(proyecto_texto) if proyecto_texto else r._proyecto._id_proyecto
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                proyecto = ProyectoDao.buscar_por_id(id_proyecto)
                if empleado is None or proyecto is None:
                    print("El empleado o proyecto seleccionado no existe.")
                    input("\nPresione Enter para continuar...")
                    continue
                if not RegistroTiempoDAO.empleado_asignado(empleado._id, proyecto._id_proyecto):
                    print("El empleado no esta asignado a ese proyecto.")
                    input("\nPresione Enter para continuar...")
                    continue
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
                    print("No se detectaron cambios guardados.")
            except ValueError:
                print("ID, horas o fecha incorrectos.")
            except Exception as error:
                print("Error al actualizar registro:", error)

        elif opcion == "5":
            try:
                id_registro = int(input("ID del registro a eliminar: "))
                r = RegistroTiempoDAO.buscar_por_id(id_registro)
                if r is None:
                    print("Registro no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue
                confirmar = input(f"Eliminar registro {r._id_registro}? (s/n): ").strip().lower()
                if confirmar == "s":
                    if RegistroTiempoDAO.eliminar(id_registro):
                        print("Registro eliminado.")
                    else:
                        print("No se pudo eliminar el registro.")
                else:
                    print("Eliminacion cancelada.")
            except ValueError:
                print("Debes ingresar un ID numerico.")
            except Exception as error:
                print("Error al eliminar registro:", error)

        elif opcion == "0":
            return
        else:
            print("Opcion no valida.")
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main_RegistroTiempo()
