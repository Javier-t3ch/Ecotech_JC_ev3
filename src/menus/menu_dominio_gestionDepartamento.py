from complementos.complementos import limpiar_pantalla


def menu_dominio_gestionDepartamento(gestion_departamentos):
    while True:
        limpiar_pantalla()
        print("\n===== DOMINIO GESTION DEPARTAMENTO (DEMOSTRACION) =====")
        print("1. Crear departamento")
        print("2. Buscar departamento")
        print("3. Editar departamento")
        print("4. Eliminar departamento")
        print("5. Listar departamentos de la demostracion")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return

        elif opcion == "1":
            nombre = input("Nombre del departamento: ").strip()
            departamento = gestion_departamentos.crear_departamento(nombre)
            if departamento is False:
                print("No se pudo crear: nombre vacio o ya existente.")
            else:
                print("Departamento creado:", departamento._nombre)
                print("Nota: este ejemplo no guarda datos en la base de datos.")

        elif opcion == "2":
            nombre = input("Nombre a buscar: ").strip()
            departamento = gestion_departamentos.buscar_departamento(nombre)
            if departamento is False:
                print("Departamento no encontrado.")
            else:
                print("Departamento encontrado:", departamento._nombre)

        elif opcion == "3":
            nombre = input("Nombre actual del departamento: ").strip()
            departamento = gestion_departamentos.buscar_departamento(nombre)
            if departamento is False:
                print("Departamento no encontrado.")
                input("\nPresione Enter para continuar...")
                continue

            nuevo_nombre = input("Nuevo nombre: ").strip()
            if gestion_departamentos.editar_departamento(departamento, nuevo_nombre):
                print("Departamento actualizado:", departamento._nombre)
            else:
                print("No se pudo actualizar: nombre invalido o repetido.")

        elif opcion == "4":
            nombre = input("Nombre del departamento a eliminar: ").strip()
            departamento = gestion_departamentos.buscar_departamento(nombre)
            if departamento is False:
                print("Departamento no encontrado.")
                input("\nPresione Enter para continuar...")
                continue

            confirmar = input("Confirmar eliminacion (s/n): ").strip().lower()
            if confirmar != "s":
                print("Eliminacion cancelada.")
                input("\nPresione Enter para continuar...")
                continue

            if gestion_departamentos.eliminar_departamento(departamento):
                print("Departamento eliminado.")
            else:
                print("No se puede eliminar un departamento con empleados o proyectos.")

        elif opcion == "5":
            if not gestion_departamentos._departamentos:
                print("No hay departamentos creados en la demostracion.")
            else:
                for departamento in gestion_departamentos._departamentos:
                    print("-", departamento._nombre)

        else:
            print("Opcion no valida.")
        input("\nPresione Enter para continuar...")
