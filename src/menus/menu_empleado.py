from datetime import date
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO
from complementos.complementos import limpiar_pantalla


def mostrar_menu_empleado():
    print("\n===== EMPLEADOS - ECOTECH =====")
    print("1. Registrar Empleado")
    print("2. Listar Empleados")
    print("3. Buscar Empleado")
    print("4. Actualizar Empleado")
    print("5. Eliminar Empleado")
    print("0. Volver al menu principal")


def main_empleado():
    while True:
        limpiar_pantalla()
        mostrar_menu_empleado()
        opcion = input("Seleccione una opcion: ")
        limpiar_pantalla()

        if opcion == "1":
            try:
                nombre = input("Nombre: ").strip()
                direccion = input("Direccion: ").strip()
                numero = input("Numero de telefono: ").strip()
                correo = input("Correo: ").strip()
                fecha_contrato = date.fromisoformat(input("Fecha de contrato (AAAA-MM-DD): ").strip())
                salario = float(input("Salario: "))
                cargo = input("Cargo: ").strip()
                empleado = Empleado(nombre, direccion, numero, correo, fecha_contrato, salario, cargo)
                EmpleadoDAO.insertar(empleado)
                print("Empleado registrado con ID:", empleado._id)
            except ValueError as error:
                print("Datos incorrectos:", error)
            except Exception as error:
                print("Error al registrar el empleado:", error)

        elif opcion == "2":
            try:
                empleados = EmpleadoDAO.listar()
                if not empleados:
                    print("No hay empleados registrados.")
                else:
                    for empleado in empleados:
                        print(empleado.mostrar_datos())
            except Exception as error:
                print("Error al listar empleados:", error)

        elif opcion == "3":
            try:
                id_empleado = int(input("ID del empleado: "))
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado.")
                else:
                    print(empleado.mostrar_datos())
                    print("Telefono:", empleado._numero)
                    print("Fecha de contrato:", empleado._fecha_contrato)
                    print("Salario:", empleado.ver_salario())
            except ValueError:
                print("Debes ingresar un ID numerico.")
            except Exception as error:
                print("Error al buscar el empleado:", error)

        elif opcion == "4":
            try:
                id_empleado = int(input("ID del empleado a actualizar: "))
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue
                print("Deja el campo vacio si no quieres modificarlo.")
                nombre = input(f"Nombre [{empleado._nombre}]: ").strip()
                direccion = input(f"Direccion [{empleado._direccion}]: ").strip()
                numero = input(f"Telefono [{empleado._numero}]: ").strip()
                correo = input(f"Correo [{empleado._correo}]: ").strip()
                fecha_texto = input(f"Fecha contrato [{empleado._fecha_contrato}] (AAAA-MM-DD): ").strip()
                salario_texto = input(f"Salario [{empleado._salario}]: ").strip()
                cargo = input(f"Cargo [{empleado._cargo}]: ").strip()
                if not (nombre or direccion or numero or correo or fecha_texto or salario_texto or cargo):
                    print("No ingresaste cambios.")
                    input("\nPresione Enter para continuar...")
                    continue
                fecha = date.fromisoformat(fecha_texto) if fecha_texto else empleado._fecha_contrato
                salario = float(salario_texto) if salario_texto else empleado._salario
                actualizado = Empleado(
                    nombre=nombre or empleado._nombre,
                    direccion=direccion or empleado._direccion,
                    numero=numero or empleado._numero,
                    correo=correo or empleado._correo,
                    fecha_contrato=fecha,
                    salario=salario,
                    cargo=cargo or empleado._cargo,
                    id=empleado._id
                )
                if EmpleadoDAO.actualizar(actualizado):
                    print("Empleado actualizado correctamente.")
                else:
                    print("No se detectaron cambios guardados.")
            except ValueError as error:
                print("Datos incorrectos:", error)
            except Exception as error:
                print("Error al actualizar el empleado:", error)

        elif opcion == "5":
            try:
                id_empleado = int(input("ID del empleado a eliminar: "))
                empleado = EmpleadoDAO.buscar_por_id(id_empleado)
                if empleado is None:
                    print("Empleado no encontrado.")
                    input("\nPresione Enter para continuar...")
                    continue
                print(empleado.mostrar_datos())
                confirmar = input("Confirmar eliminacion (s/n): ").lower().strip()
                if confirmar == "s":
                    if EmpleadoDAO.eliminar(id_empleado):
                        print("Empleado eliminado.")
                    else:
                        print("No se pudo eliminar el empleado.")
                else:
                    print("Eliminacion cancelada.")
            except ValueError:
                print("Debes ingresar un ID numerico.")
            except Exception as error:
                print("Error al eliminar el empleado:", error)

        elif opcion == "0":
            return
        else:
            print("Opcion no valida.")
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main_empleado()
