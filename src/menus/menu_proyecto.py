from complementos.complementos import limpiar_pantalla
from datetime import date
from dominio.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDao


def mostrar_menu_proyecto():
    print("\n===== PROYECTOS - ECOTECH =====")
    print("1. Registrar Proyecto")
    print("2. Listar Proyectos")
    print("3. Buscar Proyecto")
    print("4. Actualizar Proyecto")
    print("5. Eliminar Proyecto")
    print("0. Volver al menu principal")


def main_proyecto():
    while True:
        limpiar_pantalla()
        mostrar_menu_proyecto()
        opcion = input("Seleccione una opcion: ")
        limpiar_pantalla()

        if opcion == "1":
            try:
                nombre = input("Nombre: ").strip()
                fecha_inicio = date.fromisoformat(input("Fecha de inicio (AAAA-MM-DD): ").strip())
                descripcion = input("Descripcion: ").strip()
                if not nombre or not descripcion:
                    print("Nombre y descripcion son obligatorios.")
                    input("\nPresione Enter para continuar...")
                    continue
                proyecto = Proyecto(nombre, fecha_inicio, descripcion)
                ProyectoDao.insertar(proyecto)
                print("Proyecto registrado con ID:", proyecto._id_proyecto)
            except ValueError:
                print("Fecha incorrecta. Usa AAAA-MM-DD.")
            except Exception as error:
                print("Error al registrar proyecto:", error)

        elif opcion == "2":
            try:
                proyectos = ProyectoDao.listar()
                if not proyectos:
                    print("No hay proyectos registrados.")
                else:
                    for p in proyectos:
                        print(f"ID: {p._id_proyecto} | {p._nombre} | Inicio: {p._fecha_inicio} | {p._descripcion}")
            except Exception as error:
                print("Error al listar proyectos:", error)

        elif opcion == "3":
            try:
                id_proyecto = int(input("ID del proyecto: "))
                p = ProyectoDao.buscar_por_id(id_proyecto)
                if p is None:
                    print("Proyecto no encontrado.")
                else:
                    print(f"ID: {p._id_proyecto} | {p._nombre} | Inicio: {p._fecha_inicio} | {p._descripcion}")
            except ValueError:
                print("Debes ingresar un ID numerico.")
            except Exception as error:
                print("Error al buscar proyecto:", error)

        elif opcion == "4":
            try:
                id_proyecto = int(input("ID del proyecto a actualizar: "))
                p = ProyectoDao.buscar_por_id(id_proyecto)
                if p is None:
                    print("Proyecto no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue
                nombre = input(f"Nombre [{p._nombre}]: ").strip()
                fecha_texto = input(f"Fecha de inicio [{p._fecha_inicio}] (AAAA-MM-DD): ").strip()
                descripcion = input(f"Descripcion [{p._descripcion}]: ").strip()
                if not (nombre or fecha_texto or descripcion):
                    print("No ingresaste cambios.")
                    input("\nPresione Enter para continuar...")
                    continue
                fecha = date.fromisoformat(fecha_texto) if fecha_texto else p._fecha_inicio
                actualizado = Proyecto(
                    nombre=nombre or p._nombre,
                    fecha_inicio=fecha,
                    descripcion=descripcion or p._descripcion,
                    id_proyecto=p._id_proyecto
                )
                if ProyectoDao.actualizar(actualizado):
                    print("Proyecto actualizado.")
                else:
                    print("No se detectaron cambios guardados.")
            except ValueError:
                print("ID o fecha incorrectos.")
            except Exception as error:
                print("Error al actualizar proyecto:", error)

        elif opcion == "5":
            try:
                id_proyecto = int(input("ID del proyecto a eliminar: "))
                p = ProyectoDao.buscar_por_id(id_proyecto)
                if p is None:
                    print("Proyecto no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue
                confirmar = input(f"Eliminar {p._nombre}? (s/n): ").strip().lower()
                if confirmar == "s":
                    if ProyectoDao.eliminar(id_proyecto):
                        print("Proyecto eliminado.")
                    else:
                        print("No se pudo eliminar el proyecto.")
                else:
                    print("Eliminacion cancelada.")
            except ValueError:
                print("Debes ingresar un ID numerico.")
            except Exception as error:
                print("Error al eliminar proyecto:", error)

        elif opcion == "0":
            return
        else:
            print("Opcion no valida.")
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main_proyecto()
