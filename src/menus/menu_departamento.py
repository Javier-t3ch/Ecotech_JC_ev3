from dominio.departamento import Departamento
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from complementos.complementos import limpiar_pantalla

def mostrar_menu_departementos():
    print("\n===== DEPARTAMENTOS - ECOTECH =====")
    print("1. Registrar Departamento")
    print("2. Listar Departamentos")
    print("3. Buscar Departamento")
    print("4. Actualizar Departamento")
    print("5. Eliminar Departamento")
    print("0. Volver al menu principal")


def main_departamento():
    while True:
        limpiar_pantalla()
        mostrar_menu_departementos()
        opcion = input("Seleccione una opcion: ")
        limpiar_pantalla()

        if opcion == "1":
            try:
                nombre = input("Nombre del departamento: ").strip()
                if not nombre:
                    print("El nombre no puede estar vacio.")
                    input("\nPresione Enter para continuar...")
                    continue
                gerente_texto = input("ID del gerente (Enter si no tiene): ").strip()
                id_gerente = int(gerente_texto) if gerente_texto else None
                if id_gerente is not None and EmpleadoDAO.buscar_por_id(id_gerente) is None:
                    print("El empleado indicado como gerente no existe.")
                    input("\nPresione Enter para continuar...")
                    continue
                departamento = Departamento(nombre, id_gerente=id_gerente)
                DepartamentoDAO.insertar(departamento)
                print("Departamento registrado con ID:", departamento._id_departamento)
            except ValueError:
                print("El ID del gerente debe ser numerico.")
            except Exception as error:
                print("Error al registrar el departamento:", error)

        elif opcion == "2":
            try:
                departamentos = DepartamentoDAO.listar()
                if not departamentos:
                    print("No hay departamentos registrados.")
                else:
                    for d in departamentos:
                        print(f"ID: {d._id_departamento} | Nombre: {d._nombre} | Gerente: {d._id_gerente}")
            except Exception as error:
                print("Error al listar departamentos:", error)

        elif opcion == "3":
            try:
                id_departamento = int(input("ID del departamento: "))
                d = DepartamentoDAO.buscar_por_id(id_departamento)
                if d is None:
                    print("Departamento no encontrado.")
                else:
                    print(f"ID: {d._id_departamento} | Nombre: {d._nombre} | Gerente: {d._id_gerente}")
            except ValueError:
                print("Debes ingresar un ID numerico.")
            except Exception as error:
                print("Error al buscar departamento:", error)

        elif opcion == "4":
            try:
                id_departamento = int(input("ID del departamento a actualizar: "))
                d = DepartamentoDAO.buscar_por_id(id_departamento)
                if d is None:
                    print("Departamento no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue
                nombre = input(f"Nombre [{d._nombre}]: ").strip()
                gerente_texto = input(f"ID gerente [{d._id_gerente}] (Enter para mantener): ").strip()
                if not nombre and not gerente_texto:
                    print("No ingresaste cambios.")
                    input("\nPresione Enter para continuar...")
                    continue
                id_gerente = int(gerente_texto) if gerente_texto else d._id_gerente
                if id_gerente is not None and EmpleadoDAO.buscar_por_id(id_gerente) is None:
                    print("El gerente indicado no existe.")
                    input("\nPresione Enter para continuar...")
                    continue
                actualizado = Departamento(
                    nombre=nombre or d._nombre,
                    id_departamento=d._id_departamento,
                    id_gerente=id_gerente
                )
                if DepartamentoDAO.actualizar(actualizado):
                    print("Departamento actualizado.")
                else:
                    print("No se detectaron cambios guardados.")
            except ValueError:
                print("El ID debe ser numerico.")
            except Exception as error:
                print("Error al actualizar departamento:", error)

        elif opcion == "5":
            try:
                id_departamento = int(input("ID del departamento a eliminar: "))
                d = DepartamentoDAO.buscar_por_id(id_departamento)
                if d is None:
                    print("Departamento no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue
                confirmar = input(f"Eliminar {d._nombre}? (s/n): ").strip().lower()
                if confirmar == "s":
                    if DepartamentoDAO.eliminar(id_departamento):
                        print("Departamento eliminado.")
                    else:
                        print("No se pudo eliminar el departamento.")
                else:
                    print("Eliminacion cancelada.")
            except ValueError:
                print("Debes ingresar un ID numerico.")
            except Exception as error:
                print("Error al eliminar departamento:", error)

        elif opcion == "0":
            return
        else:
            print("Opcion no valida.")
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main_departamento()
